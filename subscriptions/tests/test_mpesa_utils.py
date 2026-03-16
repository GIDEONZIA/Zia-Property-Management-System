import pytest
from django.contrib.auth import get_user_model
from subscriptions.models import PremiumSubscription
from utils import mpesa_callback

User = get_user_model()

@pytest.mark.django_db
class TestMpesaCallback:

    def test_process_mpesa_callback_valid(self):
        # 1. Create User to fix IntegrityError (NotNullViolation)
        user = User.objects.create_user(username='tester', password='password')

        # 2. Setup: Use a specific CheckoutRequestID for matching
        PremiumSubscription.objects.create(
            user=user,
            phone='254712345678',
            plan='monthly',
            amount=29,
            paid=False,
            checkout_request_id="CH_12345" 
        )

        payload = {
            "Body": {
                "stkCallback": {
                    "CheckoutRequestID": "CH_12345",
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

        # 3. Action: Process the simulated callback
        response = mpesa_callback.process_mpesa_callback(payload)
        
        # 4. Assertions: Verify everything updated
        sub = PremiumSubscription.objects.get(user=user)
        assert response["ResultCode"] == 0
        assert sub.paid is True
        assert sub.mpesa_receipt == "ABC123XYZ"
        assert sub.expiry_date is not None  # Verifies Fair Renewal Logic worked
