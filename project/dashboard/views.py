from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from store.models import Category, Product, Order
from store.forms import ProductForm, CategoryForm


@login_required
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)
        if user and user.is_staff and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'dashboard/admin_login.html')


@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    revenue = Order.objects.filter(status='Delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:5]
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'revenue': revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def product_management(request):
    if not request.user.is_staff:
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'dashboard/product_management.html', {'products': products})


@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/edit_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management')
    return render(request, 'dashboard/delete_product.html', {'product': product})


@login_required
def category_management(request):
    if not request.user.is_staff:
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'dashboard/category_management.html', {'categories': categories})


@login_required
def add_category(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_management')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})


@login_required
def edit_category(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_management')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {'form': form})


@login_required
def delete_category(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_management')
    return render(request, 'dashboard/delete_category.html', {'category': category})


@login_required
def order_management(request):
    if not request.user.is_staff:
        return redirect('home')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_management.html', {'orders': orders})


@login_required
def update_order_status(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('order_management')
    return render(request, 'dashboard/update_order_status.html', {'order': order})


@login_required
def user_management(request):
    if not request.user.is_staff:
        return redirect('home')
    users = User.objects.all()
    return render(request, 'dashboard/user_management.html', {'users': users})


@login_required
def block_user(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect('user_management')


@login_required
def unblock_user(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect('user_management')