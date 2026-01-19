from django.shortcuts import render, redirect,get_object_or_404
from products.models import Product, Category
from .decorators import admin_required

def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard/dashboard.html', {
        'products': products
    })


def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category'),
            image=request.FILES.get('image'),
            is_gold=request.POST.get('is_gold') == 'on',
            is_diamond=request.POST.get('is_diamond') == 'on'
        )
        return redirect('dashboard')

    return render(request, 'dashboard/add_product.html', {
        'categories': categories
    })

# @admin_required
# def admin_dashboard(request):
#     ...


# dashboard/views.py - CORRECTED
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Use this instead
from products.models import Product, Category

@login_required  # Only logged-in users can access
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard/dashboard.html', {
        'products': products
    })

@login_required  # Only logged-in users can add products
def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category'),
            image=request.FILES.get('image'),
            is_gold=request.POST.get('is_gold') == 'on',
            is_diamond=request.POST.get('is_diamond') == 'on'
        )
        return redirect('dashboard')

    return render(request, 'dashboard/add_product.html', {
        'categories': categories
    })

@admin_required
def admin_dashboard(request):
    products = Product.objects.all()
    orders = request.session.get('orders', [])
    return render(request, 'dashboard/dashboard.html', {
        'products': products,
        'orders': orders
    })
@admin_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('dashboard')

    return render(request, 'dashboard/edit_product.html', {
        'product': product
    })
@admin_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('dashboard')
