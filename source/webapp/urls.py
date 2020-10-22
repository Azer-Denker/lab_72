from django.urls import path, include

from accounts.views import json_echo_view, get_token_view
from webapp.views import IndexView, ProductView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, CartView, CartAddView, \
    CartDeleteView, CartDeleteOneView, OrderCreateView, WatchOrdersView


app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('echo/', json_echo_view),
    path('get_token/', get_token_view),

    path('product/', include([
        path('add/', ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>/', include([
            path('', ProductView.as_view(), name='product_view'),
            path('update/', ProductUpdateView.as_view(), name='product_update'),
            path('delete/', ProductDeleteView.as_view(), name='product_delete'),
            path('add-to-cart/', CartAddView.as_view(), name='product_add_to_cart'),
        ])),
    ])),

    path('cart/', include([
        path('', CartView.as_view(), name='cart_view'),
        path('<int:pk>/', include([
            path('delete/', CartDeleteView.as_view(), name='cart_delete'),
            path('delete-one/', CartDeleteOneView.as_view(), name='cart_delete_one'),
        ])),
    ])),

    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/wath/', WatchOrdersView.as_view(), name='watch_orders')
]
