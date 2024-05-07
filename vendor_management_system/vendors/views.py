from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorDetailsSerializer, VendorPerformanceSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailsSerializer
    lookup_field = 'vendor_code'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class VendorPerformance(APIView):
    """
    API endpoint for retrieving performance metrics of a vendor.

    GET request:
    - Retrieves the performance metrics of a vendor based on the provided vendor code.
    - Returns the performance metrics in the response along with a status code.

    Response format:
    {
        "vendor_code": "<vendor_code>",
        "on_time_delivery_rate": <value>,
        "quality_rating_avg": <value>,
        "average_response_time": <value>,
        "fulfilment_rate": <value>
    }

    If the vendor with the provided code is not found, returns a 404 error.

    Error response format:
    {
        "error": "Vendor not found"
    }
    """
    serializer_class = VendorPerformanceSerializer

    def get(self, request, vendor_code):
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
