
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('shop/', views.shop_page, name='shop'),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path('cart/', views.cart_page, name='cart'),

    
path(
    "collection/",
    views.collection_page,
    name="collection"
),

path(
    "collection/<slug:slug>/",
    views.collection_detail,
    name="collection_detail"
),


    path('about/', views.about_page, name='about'),

    path('contact/', views.contact_page, name='contact'),
         
path(
    "cart/update/",
    views.update_cart,
    name="update_cart"
),

path(
    "cart/remove/",
    views.remove_from_cart,
    name="remove_from_cart"
),
path("cart/update/", views.update_cart, name="update_cart"),
path("cart/remove/", views.remove_from_cart, name="remove_from_cart"),

path(
    "checkout/",
    views.checkout_page,
    name="checkout"
),

path(
    "order-success/<int:order_id>/",
    views.order_success,
    name="order_success"
),
path(
    'checkout/',
    views.checkout_page,
    name='checkout'
),

path(
    'order-success/<int:order_id>/',
    views.order_success,
    name='order_success'
),
]




