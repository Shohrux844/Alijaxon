from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.models import User, Category, Product, Wishlist, AdminSetting, Order


class HomeListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/home.html'
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",
                                                                                                       flat=True)
        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/menus/product-list.html'
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=slug).first()
        data = super().get_context_data(object_list=object_list, **kwargs)
        products = Product.objects.all()
        if slug != 'all':
            products = products.filter(category=category)
        # -------------- search --------------
        query = self.request.GET.get('query')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data['products'] = products
        # -------------- search --------------

        data['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",
                                                                                                       flat=True)
        data['session_category'] = category
        return data


class WishlistView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    def get(self, request, pk):
        liked = True
        like = Wishlist.objects.filter(product_id=pk, user=self.request.user)
        if like.exists():
            like.delete()
            liked = False
        else:
            Wishlist.objects.create(product_id=pk, user=self.request.user)

        return JsonResponse({"liked": liked})


class ProductSellListView(ListView):
    queryset = Product.objects.all()
    template_name = "apps/thread/market-list.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        products = data['products']
        slug = self.request.GET.get('category')
        if slug == 'top':
            products = Product.objects.annotate(order_count=Count(F('orders'))).order_by('order_count')[:10]
        elif slug != 'all':
            products = Product.objects.filter(category__slug=slug)
        data['products'] = products
        data['categories'] = Category.objects.all()
        return data


class LikeListView(ListView):
    queryset = Wishlist.objects.all()
    template_name = 'apps/menus/wish-list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['products'] = Product.objects.filter(wishlist__user=self.request.user)
        data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user.id).values_list("product_id",
                                                                                                      flat=True)
        return data


class CompetitionListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/menus/competition.html'
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['site'] = AdminSetting.objects.first()
        return data

    def get_queryset(self):
        query = super().get_queryset()
        query = query.annotate(
            order_count=Count('thread__orders', filter=Q(thread__orders__status=Order.StatusType.COMPLETED))).order_by(
            "-order_count").only('first_name')
        return query


class ArchivedTemplateView(TemplateView):
    template_name = 'apps/archived.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['orders'] = Order.objects.filter(thread__user=self.request.user)
        return data


class DiagramTemplateView(TemplateView):
    template_name = 'apps/diagram.html'
