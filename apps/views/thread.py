import datetime

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, TemplateView

from apps.forms import ThreadForm
from apps.models import Thread, Product, Category, Order


class ThreadFormView(FormView):
    form_class = ThreadForm
    template_name = 'apps/thread/market-list.html'
    success_url = reverse_lazy('thread-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['categories'] = Category.objects.all()
        return data

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.user = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class ThreadListView(ListView):
    queryset = Thread.objects.all()
    template_name = 'apps/thread/thread-list.html'
    context_object_name = 'threads'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['threads'] = data.get('threads').filter(user=self.request.user).order_by('-created_at')
        return data


class ThreadProductDetailView(DetailView):
    queryset = Thread.objects.all()
    template_name = 'apps/order/product-detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        thread = data.get('thread')
        data['product'] = thread.product
        thread.visit_count += 1
        thread.save()
        return data


class ThreadStatisticTemplateView(TemplateView):
    template_name = 'apps/thread/thread-statistic.html'

    def get_context_data(self, **kwargs):
        map_range_date = {
            "last_day": (datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()),
            "wekly": (datetime.datetime.now() - datetime.timedelta(days=7), datetime.datetime.now()),
            "last_month": (datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()),
            "today": (
                datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), datetime.datetime.now()),
            "yesterday": (
                datetime.datetime.now() - datetime.timedelta(days=1),
                datetime.datetime.now() - datetime.timedelta(days=1 , hours=23 , minutes=59 , seconds=59 , microseconds=9999999)),
        }
        period = self.request.GET.get('period')
        date = map_range_date.get(period)
        data = super().get_context_data(**kwargs)
        statistics = Thread.objects.filter(user=self.request.user)
        if date:
            statistics = statistics.filter(orders__ordered_at__range=date)
        statistics = statistics.annotate(
            new_count=Count('orders', filter=Q(orders__status=Order.StatusType.NEW)),
            ready_to_order_count=Count('orders', filter=Q(orders__status=Order.StatusType.READY_TO_ORDER)),
            delivering_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERING)),
            delivered_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)),
            not_pick_up_count=Count('orders', filter=Q(orders__status=Order.StatusType.NOT_PICK_UP)),
            canceled_count=Count('orders', filter=Q(orders__status=Order.StatusType.CANCELED)),
            archived_count=Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVED)),
        ).only('name', 'product__name', "visit_count")
        tmp = statistics.aggregate(
            all_visit_count=Sum('visit_count'),
            all_new_count=Sum('new_count'),
            all_ready_to_order_count=Sum('ready_to_order_count'),
            all_delivering_count=Sum('delivering_count'),
            all_delivered_count=Sum('delivered_count'),
            all_not_pick_up_count=Sum('not_pick_up_count'),
            all_canceled_count=Sum('canceled_count'),
            all_archived_count=Sum('archived_count'),

        )
        data['statistics'] = statistics
        data['thread_count'] = statistics.count()
        data.update(tmp)
        return data


class MarketListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/thread/market-list.html'
    context_object_name = "categories"

    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.request.GET.get('category')
        data = super().get_context_data(**kwargs)
        products = Product.objects.all()
        if slug != "all":
            products = products.filter(category__slug=slug)
        data['products'] = products
        data['slug'] = slug
        return data
