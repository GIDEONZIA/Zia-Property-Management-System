from rest_framework import serializers
from .models import Property, Tenant, Lease, RentPayment  # Add RentPayment here

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = '__all__'

class RentPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentPayment # type: ignore
        fields = '__all__'

