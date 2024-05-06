from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorDetailsSerializer, VendorPerformanceSerializer


class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailsSerializer


class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailsSerializer
    lookup_field = 'vendor_code'


class VendorPerformance(APIView):
    def get(self, request, vendor_code):
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
