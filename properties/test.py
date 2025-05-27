from django.test import TestCase
from .models import Property

class PropertyModelTest(TestCase):

    def setUp(self):
        self.property = Property.objects.create(
            title='Test Property',
            description='This is a test',
            price=100000,
            location='Nairobi',
            property_type='apartment'
        )

    def test_property_str(self):
        self.assertEqual(str(self.property), 'Test Property')

    def test_price_is_integer(self):
        self.assertIsInstance(self.property.price, int)
