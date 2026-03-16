import pytest
from django.contrib.auth import get_user_model
from subscriptions.models import PremiumSubscription
from utils import mpesa_callback

User = get_user_model()

@pytest.mark.django_db
class TestMpesaCallback:

    def test_process_mpesa_callback_valid(self):
        """
        Tests that a valid M-Pesa callback correctly updates a 
        pending subscription to paid and sets an expiry date.
        """
        # 1. Create a user to satisfy the NOT NULL (user_id) constraint
        user = User.objects.create_user(
            username='testworker', 
            password='password123'
        )
        
        # 2. Create a pending subscription linked to the user
        # 'checkout_request_id' must match the payload ID below
        PremiumSubscription.objects.create(
            user=user, 
            phone='254712345678', 
            plan='monthly', 
            amount=29, 
            paid=False,
            checkout_request_id="67890" 
        )

        # 3. Simulate the JSON payload sent by Safaricom
        payload = {
            "Body": {
                "stkCallback": {
                    "CheckoutRequestID": "67890",
                    "ResultCode": 0,
                    "CallbackMetadata": {
                        "Item": [
                            {"Name": "Amount", "Value": 29},
                            {"Name": "MpesaReceiptNumber", "Value": "ABC123XYZ"},
                            {"Name": "PhoneNumber", "Value": 254712345678}
                        ]
                    }
                }
            }
        }

        # 4. Run the callback processor logic
        response = mpesa_callback.process_mpesa_callback(payload)
        
        # 5. Assertions
        assert response["ResultCode"] == 0
        
        # Refresh from database and verify updates
        sub = PremiumSubscription.objects.get(user=user)
        assert sub.paid is True
        assert sub.mpesa_receipt == "ABC123XYZ"
        assert sub.expiry_date is not None  # Verifies activate() logic worked
