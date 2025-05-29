from django.urls import path

from apps.views import OperatorTemplateView, OperatorOrderChangeDetailView

urlpatterns = [
    path('operator', OperatorTemplateView.as_view(), name='operator'),
    path('operator/order-change/<int:pk>', OperatorOrderChangeDetailView.as_view(), name='order-change'),

]
