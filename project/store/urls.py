from django.urls import path
from . import views
from .views import test_gemini

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('collections/wedding/', views.wedding_collection, name='wedding_collection'),
    path('community/<str:name>/', views.community_view, name='community'),
    path('search/', views.search, name='search'),
    path('dailywear/', views.dailywear_collection, name='dailywear'),
    path("test-gemini/", test_gemini, name="test_gemini"),
    path('gold/', views.gold_products, name='gold_products'),
    path('diamond/', views.diamond_products, name='diamond_products'),
    path('payment/', views.payment, name='payment'),
    path('payment-status/', views.payment_status, name='payment_status')
    ]