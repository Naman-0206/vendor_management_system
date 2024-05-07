from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer, AcknowledgePurchaseOrderSerializer
from django.http import Http404
from django.utils import timezone
from .signals import recalculate_avg_response_time_signal
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PurchaseOrderListCreate(APIView):
    """
    API endpoint for listing and creating purchase orders.

    - GET: Retrieve a list of purchase orders. You can filter by vendor code using the query parameter 'vendor_code'.
    - POST: Create a new purchase order.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def get(self, request):
        """
        Retrieve a list of purchase orders.

        You can filter by vendor code using the query parameter 'vendor_code'.
        """
        vendor_code = request.query_params.get('vendor_code', None)
        if vendor_code:
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_code)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new purchase order.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetail(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific purchase order.

    - GET: Retrieve a specific purchase order by its PO number.
    - PUT: Update a specific purchase order by its PO number.
    - DELETE: Delete a specific purchase order by its PO number.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404("Purchase Order does not exist")

    def get(self, request, po_number):
        """
        Retrieve a specific purchase order by its PO number.
        """
        purchase_order = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, po_number):
        """
        Update a specific purchase order by its PO number.
        """
        purchase_order = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_number):
        """
        Delete a specific purchase order by its PO number.
        """
        purchase_order = self.get_object(po_number)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcknowledgePurchaseOrder(APIView):
    """
    API endpoint for acknowledging a purchase order.

    - POST: Acknowledge a purchase order by updating its acknowledgment date.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AcknowledgePurchaseOrderSerializer

    def post(self, request, po_number):
        """
        Acknowledge a purchase order by updating its acknowledgment date.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_number)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            recalculate_avg_response_time_signal.send(
                sender=None, vendor=purchase_order.vendor)

            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
