from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_management, name='product_management'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('categories/', views.category_management, name='category_management'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('orders/', views.order_management, name='order_management'),
    path('orders/update/<int:pk>/', views.update_order_status, name='update_order_status'),
    path('users/', views.user_management, name='user_management'),
    path('users/block/<int:pk>/', views.block_user, name='block_user'),
    path('users/unblock/<int:pk>/', views.unblock_user, name='unblock_user'),
]