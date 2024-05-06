from django.test import TestCase, Client
from rest_framework import status
from .models import PurchaseOrder
from vendors.models import Vendor
from .serializers import PurchaseOrderSerializer
from django.utils import timezone


class PurchaseOrderListAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor1 = Vendor.objects.create(
            name="Test Vendor 1", vendor_code="TestVendor1")
        self.vendor2 = Vendor.objects.create(
            name="Test Vendor 2", vendor_code="TestVendor2")

    def test_get_purchase_orders(self):
        PurchaseOrder.objects.create(
            po_number='PO-001', vendor=self.vendor1, items="[{'name': 'Product X', 'quantity': 10}]", quantity=10, status='pending')
        PurchaseOrder.objects.create(
            po_number='PO-002', vendor=self.vendor2, items="[{'name': 'Product X', 'quantity': 10}]", quantity=10, status='pending')

        response = self.client.get('/api/purchase_orders/')
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_purchase_orders_by_vendor(self):
        PurchaseOrder.objects.create(
            po_number='PO-001', vendor=self.vendor1, items="[{'name': 'Product X', 'quantity': 10}]", quantity=10, status='pending')
        PurchaseOrder.objects.create(
            po_number='PO-002', vendor=self.vendor1, items="[{'name': 'Product A', 'quantity': 5}]", quantity=5, status='pending')
        PurchaseOrder.objects.create(
            po_number='PO-003', vendor=self.vendor2, items="[{'name': 'Product B', 'quantity': 5}]", quantity=5, status='pending')

        response = self.client.get(
            '/api/purchase_orders/?vendor_code='+self.vendor1.pk)
        purchase_orders = PurchaseOrder.objects.filter(vendor=self.vendor1)
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_purchase_order(self):
        data = {
            'po_number': 'PO-001',
            'vendor': self.vendor1.pk,
            'items': "[{'name': 'Product X', 'quantity': 10}]",
            'quantity': '10',
            'status': 'pending'
        }

        response = self.client.post(
            '/api/purchase_orders/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO-001')

    def test_retrive_purchase_orders(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001', vendor=self.vendor1, items="[{'name': 'Product X', 'quantity': 10}]", quantity=10, status='pending')

        response = self.client.get(f'/api/purchase_orders/{purchase_order}/')
        serializer = PurchaseOrderSerializer(purchase_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor1,
            items=['item1', 'item2'],
            quantity=10,
            status='pending'
        )
        updated_data = {
            'po_number': 'PO-001',
            'vendor': self.vendor2.pk,
            'items': '["updated_item1", "updated_item2"]',
            'quantity': 20,
            'status': 'completed'
        }

        response = self.client.put(
            f'/api/purchase_orders/{purchase_order}/', updated_data, content_type='application/json')
        purchase_order.refresh_from_db()
        serializer = PurchaseOrderSerializer(purchase_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor1,
            items=['item1', 'item2'],
            quantity=10,
            status='pending'
        )
        response = self.client.delete(
            f'/api/purchase_orders/{purchase_order.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):

        purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor1,
            items=['item1', 'item2'],
            quantity=10,
            status='pending'
        )

        self.assertEqual(purchase_order.acknowledgment_date, None)

        response = self.client.post(
            f'/api/purchase_orders/{purchase_order}/acknowledge/')

        purchase_order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(purchase_order.acknowledgment_date, None)
        self.assertAlmostEqual(
            purchase_order.acknowledgment_date, timezone.now())
