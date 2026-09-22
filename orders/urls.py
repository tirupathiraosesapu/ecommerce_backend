from django.urls import path
from .views import CreateOrderView, MyOrdersListView, OrderDetailView

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create_order'),
    path('my-orders/', MyOrdersListView.as_view(), name='my_orders'),
    path('<int:id>/', OrderDetailView.as_view(), name='order_detail'),
]
