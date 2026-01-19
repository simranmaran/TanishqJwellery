from django.urls import path
from .views import home, product_detail,add_to_cart, view_cart, remove_from_cart, order_summary,profile,place_order

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove/<int:id>/', remove_from_cart, name='remove_cart'),
    path('order-summary/', order_summary, name='order_summary'),
    path('profile/', profile, name='profile'),
    path('place-order/', place_order, name='place_order'),
    
]

