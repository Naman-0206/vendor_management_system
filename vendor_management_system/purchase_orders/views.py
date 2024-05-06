from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.http import Http404


class PurchaseOrderListCreate(APIView):
    def get(self, request):
        vendor_code = request.query_params.get('vendor_code', None)
        if vendor_code:
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_code)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetail(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404("Purchase Order does not exist")

    def get(self, request, po_number):
        purchase_order = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, po_number):
        purchase_order = self.get_object(po_number)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_number):
        purchase_order = self.get_object(po_number)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
