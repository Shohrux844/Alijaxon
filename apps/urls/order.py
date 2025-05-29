from django.urls import path

from apps.views import OrderFormView, OrderListView, OrderUpdateView

urlpatterns = [
    path('order/form', OrderFormView.as_view(), name='order'),
    path('order/list', OrderListView.as_view(), name='order-list'),
    path('order/update/<int:pk>', OrderUpdateView.as_view(), name='order-update'),
]
