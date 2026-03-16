import os
import django

# Force Django settings to load
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'property_mgmt.settings')
django.setup()

import unittest
from unittest.mock import patch
from utils import mpesa, mpesa_callback

class MpesaUtilsTest(unittest.TestCase):

    @patch('utils.mpesa.requests.get')
    def test_get_access_token_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'access_token': 'dummy_token'}
        token = mpesa.get_access_token()
        self.assertEqual(token, 'dummy_token')

    @patch('utils.mpesa.requests.post')
    @patch('utils.mpesa.get_access_token')
    def test_initiate_stk_push_success(self, mock_token, mock_post):
        mock_token.return_value = 'dummy_token'
        mock_post.return_value.json.return_value = {'ResponseCode': '0'}
        result = mpesa.initiate_stk_push('254712345678', 29)
        self.assertEqual(result['ResponseCode'], '0')

    def test_process_mpesa_callback_valid(self):
        from subscriptions.models import PremiumSubscription
        PremiumSubscription.objects.create(phone='254712345678', plan='monthly', amount=29, paid=False)

        payload = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "12345",
                    "CheckoutRequestID": "67890",
                    "ResultCode": 0,
                    "ResultDesc": "Success",
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

        response = mpesa_callback.process_mpesa_callback(payload)
        self.assertEqual(response["ResultCode"], 0)

        sub = PremiumSubscription.objects.last()
        self.assertTrue(sub.paid)
        self.assertEqual(sub.mpesa_receipt, "ABC123XYZ")
