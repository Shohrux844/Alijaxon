from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.forms import PaymentModelForm


class PaymentFormView(FormView):
    form_class = PaymentModelForm
    success_url = reverse_lazy('payment')
    template_name = 'apps/payment/payment.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['payments'] = self.request.user.payments.all()
        return data

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        if amount > self.request.user.balance:
            form.add_error('amount', "Mablag yetarli emas")
            return self.form_invalid(form)
        user = self.request.user
        user.balance -= amount
        user.save()
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)
