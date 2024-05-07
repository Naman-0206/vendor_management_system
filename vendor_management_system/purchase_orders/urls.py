from django.urls import path
from .views import PurchaseOrderListCreate, PurchaseOrderDetail, AcknowledgePurchaseOrder

urlpatterns = [
    path('api/purchase_orders/', PurchaseOrderListCreate.as_view(),
         name='api_purchase_orders_list'),
    path('api/purchase_orders/<str:po_number>/',
         PurchaseOrderDetail.as_view(), name='api_purchase_order_detail'),
    path('api/purchase_orders/<str:po_number>/acknowledge/',
         AcknowledgePurchaseOrder.as_view(), name='api_acknowledge_purchase_order'),
]
