from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product_detail, name='product-detail'),
    path('product-buy/<int:id>/', views.product_buy, name='product-buy'),
    path('logout/', views.logout_view, name='logout'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('my-account/', views.my_account, name='my-account'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-cart/<int:id>/', views.remove_from_cart, name='remove-cart'),
    path('place-order/', views.place_order, name='place-order'),
    path('order-success/<int:id>/', views.order_success, name='order-success'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-wishlist/<int:id>/', views.add_to_wishlist, name='add-wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove-wishlist'),
    path('wishlist-to-cart/<int:id>/', views.wishlist_to_cart, name='wishlist-to-cart'),
    # ADMIN PANEL
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-products/', views.admin_products, name='admin-products'),
    path('admin-orders/', views.admin_orders, name='admin-orders'),
    path('admin-product-edit/<int:id>/', views.admin_product_edit, name='admin-product-edit'),
    path('admin-product-delete/<int:id>/', views.admin_product_delete, name='admin-product-delete'),
    path('admin-order-status/<int:id>/', views.admin_update_order_status, name='admin-order-status'),
    




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)