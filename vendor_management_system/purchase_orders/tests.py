from django.test import TestCase, Client
from rest_framework import status
from .models import PurchaseOrder
from vendors.models import Vendor
from .serializers import PurchaseOrderSerializer
from django.utils import timezone
from datetime import timedelta
import json


class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor1 = Vendor.objects.create(
            name="Test Vendor 1", vendor_code="TestVendor1")
        self.vendor2 = Vendor.objects.create(
            name="Test Vendor 2", vendor_code="TestVendor2")
        self.po_details = {
            'po_number': 'PO-001',
            'vendor': self.vendor1,
            'items': ['item1', 'item2'],
            'quantity': 10,
            'issue_date': timezone.now(),
            'expected_delivery_date': timezone.now(),
            'status': 'pending'
        }

    def test_get_purchase_orders(self):
        po2_details = self.po_details.copy()
        po2_details['po_number'] = 'PO-002'

        PurchaseOrder.objects.create(**self.po_details)
        PurchaseOrder.objects.create(**po2_details)

        response = self.client.get('/api/purchase_orders/')
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_purchase_orders_by_vendor(self):
        po2_details = self.po_details.copy()
        po2_details['po_number'] = 'PO-002'
        po3_details = self.po_details.copy()
        po3_details['po_number'] = 'PO-003'
        po3_details['vendor'] = self.vendor2

        PurchaseOrder.objects.create(**self.po_details)
        PurchaseOrder.objects.create(**po2_details)
        PurchaseOrder.objects.create(**po3_details)

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
            'issue_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'expected_delivery_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'quantity': '10',
            'status': 'pending'
        }

        response = self.client.post(
            '/api/purchase_orders/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO-001')

    def test_retrive_purchase_orders(self):
        purchase_order = PurchaseOrder.objects.create(**self.po_details)

        response = self.client.get(f'/api/purchase_orders/{purchase_order}/')
        serializer = PurchaseOrderSerializer(purchase_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(**self.po_details)
        updated_data = {
            'po_number': 'PO-001',
            'vendor': self.vendor2.pk,
            'items': '["updated_item1", "updated_item2"]',
            'issue_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'expected_delivery_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'quantity': 20,
            'status': 'pending'
        }

        response = self.client.put(
            f'/api/purchase_orders/{purchase_order}/', updated_data, content_type='application/json')
        purchase_order.refresh_from_db()
        serializer = PurchaseOrderSerializer(purchase_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_purchase_order_completed(self):
        purchase_order = PurchaseOrder.objects.create(**self.po_details)
        updated_data = {
            'po_number': 'PO-001',
            'vendor': self.vendor2.pk,
            'items': '["updated_item1", "updated_item2"]',
            'issue_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'expected_delivery_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'quantity': 20,
            'status': 'completed'
        }

        response = self.client.put(
            f'/api/purchase_orders/{purchase_order}/', updated_data, content_type='application/json')
        purchase_order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_data = {
            'po_number': 'PO-001',
            'vendor': self.vendor2.pk,
            'items': '["updated_item1", "updated_item2"]',
            'issue_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'expected_delivery_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'quantity': 20,
            'status': 'completed',
            'delivery_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S')
        }

        response = self.client.put(
            f'/api/purchase_orders/{purchase_order}/', updated_data, content_type='application/json')
        purchase_order.refresh_from_db()
        serializer = PurchaseOrderSerializer(purchase_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(**self.po_details)
        response = self.client.delete(
            f'/api/purchase_orders/{purchase_order.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):

        purchase_order = PurchaseOrder.objects.create(**self.po_details)

        self.assertEqual(purchase_order.acknowledgment_date, None)

        response = self.client.post(
            f'/api/purchase_orders/{purchase_order}/acknowledge/')

        purchase_order.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(purchase_order.acknowledgment_date, None)
        self.assertEqual(
            purchase_order.acknowledgment_date.strftime("%Y-%m-%d %H:%M:%S"), timezone.now().strftime("%Y-%m-%d %H:%M:%S"))


class VendorPreformanceUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = Vendor.objects.create(
            name="Test Vendor 1", vendor_code="TestVendor1")
        self.po_details = {
            'po_number': 'PO-001',
            'vendor': self.vendor,
            'items': ['item1', 'item2'],
            'quantity': 10,
            'issue_date': timezone.now(),
            'expected_delivery_date': timezone.now(),
            'status': 'pending'
        }

    def test_update_vendor_performance(self):
        response = self.client.get(
            f'/api/vendors/{self.vendor.pk}/performance/')
        expected_data = {
            "vendor_code": self.vendor.pk,
            "on_time_delivery_rate": 0,
            "quality_rating_avg": 0,
            "average_response_time": 0,
            "fulfilment_rate": 0
        }
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, expected_data)

        purchase_order = PurchaseOrder.objects.create(**self.po_details)
        updated_data = self.po_details.copy()
        updated_data['vendor'] = self.vendor.pk
        updated_data['status'] = 'completed'
        updated_data['quality_rating'] = 4
        updated_data['delivery_date'] = self.po_details['issue_date'] - \
            timedelta(days=1)

        expected_data = {
            "vendor_code": self.vendor.pk,
            "on_time_delivery_rate": 100.0,
            "quality_rating_avg": 4.0,
            "average_response_time": 0.0,
            "fulfilment_rate": 100.0
        }

        response = self.client.put(
            f'/api/purchase_orders/{purchase_order}/', updated_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f'/api/vendors/{self.vendor.pk}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
