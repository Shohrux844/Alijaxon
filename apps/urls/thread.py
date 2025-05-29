from django.urls import path

from apps.views import ThreadFormView, ThreadListView, ThreadProductDetailView, ThreadStatisticTemplateView, \
    MarketListView

urlpatterns = [
    path('thread/form', ThreadFormView.as_view(), name='thread-form'),
    path('thread/list', ThreadListView.as_view(), name='thread-list'),
    path('thread/<int:pk>', ThreadProductDetailView.as_view(), name='thread-list'),
    path('thread/statistic', ThreadStatisticTemplateView.as_view(), name='thread-statistic'),
    path('market', MarketListView.as_view(), name='market'),
]
