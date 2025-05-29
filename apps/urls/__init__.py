from apps.urls.home import urlpatterns as home_urls
from apps.urls.order import urlpatterns as order_urls
from apps.urls.auth import urlpatterns as auth_urls
from apps.urls.thread import urlpatterns as thread_urls
from apps.urls.operator import urlpatterns as operator_urls
from apps.urls.payments import urlpatterns as payments_urls

urlpatterns = [
    *home_urls,
    *order_urls,
    *auth_urls,
    *thread_urls,
    *operator_urls,
    *payments_urls,
]