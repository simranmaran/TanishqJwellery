from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('product/', views.product_detail, name='product-detail'),

    # Auth pages
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    # Account
    path('my-account/', views.my_account, name='my-account'),

    # Other app (ONLY if really needed)
    # path('store/', include('store.urls')),
    path('my-account/', views.my_account, name='my-account'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),


]

