from django.test import TestCase
from django.contrib.auth import get_user_model
from subscriptions.models import PremiumSubscription
from utils import mpesa_callback


User = get_user_model()

class TestMpesaUtils (TestCase):

    def test_process_mpesa_callback_valid(self):

        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        PremiumSubscription.objects.create(
            user=user,
            phone="254712345678",
            plan="monthly",
            amount=29,
            paid=False,
            checkout_request_id="67890"  # match the payload
        )
        

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

        # 3. Process the callback
        response = mpesa_callback.process_mpesa_callback(payload)
        
        # 4. Verify results
        assert response["ResultCode"] == 0
        sub = PremiumSubscription.objects.get(user=user)
        assert sub.paid is True
        assert sub.mpesa_receipt == "ABC123XYZ"
