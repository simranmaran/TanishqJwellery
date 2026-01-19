from django.urls import path
from .views import admin_dashboard, add_product,edit_product, delete_product

urlpatterns = [
    path('', admin_dashboard, name='dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('edit/<int:id>/', edit_product, name='edit_product'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
]

