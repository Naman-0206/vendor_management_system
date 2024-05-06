from rest_framework import serializers
from .models import Vendor


class VendorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'on_time_delivery_rate',
                  'quality_rating_avg', 'average_response_time', 'fulfilment_rate']
