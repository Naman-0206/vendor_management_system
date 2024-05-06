from django.urls import path
from .views import PurchaseOrderListCreate, PurchaseOrderDetail

urlpatterns = [
    path('api/purchase_orders/', PurchaseOrderListCreate.as_view()),
    path('api/purchase_orders/<str:po_number>/',
         PurchaseOrderDetail.as_view()),
]