from django.urls import path

from apps.views import PaymentFormView

urlpatterns = [
    path('payment', PaymentFormView.as_view(), name='payment'),

]
