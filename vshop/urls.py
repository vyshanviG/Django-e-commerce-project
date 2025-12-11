from django.urls import path
from .views import home, add_to_cart, cart_detail
from .views import checkout, success
from vshop import views
from .views import order_history, update_cart, product_list, category_products


urlpatterns = [
    path('home/', views.home, name='home'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.proceed_to_checkout, name='proceed_to_checkout'),
    path('success/', views.success, name='success'),
    path('orders/', views.order_history, name='order_history'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]

