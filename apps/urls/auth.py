from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.views import HomeListView, ProductListView, WishlistView, LikeListView, ProductSellListView, \
    CompetitionListView, AuthFormView, district_list_view, ProfileFormView, CustomLogoutView, ChangePasswordFormView, \
    ProductDetailView, OrderFormView

urlpatterns = [
    path('auth', AuthFormView.as_view(), name='auth'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('profile', ProfileFormView.as_view(), name='profile'),
    path('district-list', district_list_view, name='district-list'),
    path('change-password', ChangePasswordFormView.as_view(), name='change-password'),
]
