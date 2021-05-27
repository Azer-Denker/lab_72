from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api_v1.views import ProductView, OrderApiView

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductView)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderApiView.as_view(), name='order_api'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
