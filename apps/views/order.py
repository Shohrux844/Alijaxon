from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView, UpdateView
from apps.forms import OrderForm, OrderModelForm
from apps.models import Product, AdminSetting, Order, Category


class OrderFormView(FormView):
    form_class = OrderForm
    template_name = 'apps/order/order-success.html'
    success_url = reverse_lazy('order')

    def form_valid(self, form):
        order = form.save(self.request.user)
        deliver_price = AdminSetting.objects.first().deliver_price
        return render(self.request, 'apps/order/order-success.html',
                      context={'order': order, 'deliver_price': deliver_price})


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/order/product-detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'


class OrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('auth')
    queryset = Order.objects.all()
    template_name = 'apps/order/order-list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['orders'] = data.get('orders').filter(owner=self.request.user)
        return data


class OrderUpdateView(UpdateView):
    queryset = Order.objects.all()
    form_class = OrderModelForm
    template_name = 'apps/operator/order-change.html'
    success_url = reverse_lazy('operator')
    pk_url_kwarg = 'pk'


    def form_valid(self, form):
        obj = self.get_object(self.get_queryset())
        status = form.cleaned_data.get('status')
        if obj.status != status and status == 'completed':
            if obj.thread:
                user = obj.thread.user
                user.balance += obj.thread.product.sell_price - obj.thread.discount_sum
                user.save()
        return super().form_valid(form)



