from django.urls import path

from apps.views import HomeListView, ProductListView, WishlistView, LikeListView, ProductSellListView, \
    CompetitionListView, ProductDetailView, ArchivedTemplateView, DiagramTemplateView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('products/<str:slug>', ProductListView.as_view(), name='product-list'),
    path('wishlist/<int:pk>', WishlistView.as_view(), name='wishlist'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('like', LikeListView.as_view(), name='like'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('product/sell', ProductSellListView.as_view(), name='product-sell'),
    path('competition', CompetitionListView.as_view(), name='competition'),
    path('archived', ArchivedTemplateView.as_view(), name='archived'),
    path('diagram', DiagramTemplateView.as_view(), name='diagram'),
]
