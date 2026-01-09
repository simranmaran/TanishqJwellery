from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, Order, OrderItem,Wishlist
from django.contrib.auth.decorators import user_passes_test



# ===== HOME =====
def index(request):
    return render(request, 'index.html')


# ===== PRODUCTS =====
def products(request):
    # create sample products if none exist (developer-friendly)
    if not Product.objects.exists():
        Product.objects.create(
            name='The Aura Gold Ring',
            sku='G-22K-R04',
            price=85999,
            discount_price=95000,
            metal='Gold',
            purity='22K',
            weight='5.8g',
            description='A classic gold ring perfect for every occasion.'
        )
        Product.objects.create(
            name='Royal Charm Bangle',
            sku='G-22K-B15',
            price=150000,
            metal='Gold',
            purity='22K',
            weight='20g',
            description='A beautiful bangle for special moments.'
        )

    all_products = Product.objects.all()
    return render(request, 'products.html', {'products': all_products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product-detail.html', {'product': product})


# ===== AUTH =====
def signup_view(request):
    """Handle user signup. Simple form that creates a Django user.

    Note: this is kept intentionally simple for beginners. In production add
    stronger validation and email verification.
    """
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect('signup')

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('my-account')

        messages.error(request, "Invalid credentials")
        return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ===== CART =====
@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required(login_url='login')
def product_buy(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity = 1
    cart_item.save()
    return redirect('place-order')


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required(login_url='login')
def remove_from_cart(request, id):
    Cart.objects.filter(id=id, user=request.user).delete()
    return redirect('cart')


# ===== ORDER =====
@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.total_price for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    return redirect('order-success', order.id)


@login_required(login_url='login')
def order_success(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'order-success.html', {
        'order': order,
        'items': items
    })


@login_required(login_url='login')
def my_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'my-account.html', {'orders': orders})


def wishlist(request):
    """Show wishlist items stored in the session.

    This uses a simple session-based wishlist (list of product IDs). It's
    beginner-friendly and avoids creating a DB model.
    """
    wishlist_ids = request.session.get('wishlist', [])
    products = Product.objects.filter(id__in=wishlist_ids) if wishlist_ids else []
    return render(request, 'wishlist.html', {'products': products})


def add_to_wishlist(request, id):
    """Add a product to session wishlist (no login required)."""
    product = get_object_or_404(Product, id=id)
    wishlist = request.session.get('wishlist', [])
    if id not in wishlist:
        wishlist.append(id)
        request.session['wishlist'] = wishlist
        messages.success(request, f'Added "{product.name}" to wishlist.')
    else:
        messages.info(request, f'"{product.name}" is already in your wishlist.')
    return redirect('product-detail', id=id)


def remove_wishlist(request, id):
    """Remove a product from the session wishlist."""
    wishlist = request.session.get('wishlist', [])
    if id in wishlist:
        wishlist.remove(id)
        request.session['wishlist'] = wishlist
        messages.success(request, 'Removed item from wishlist.')
    else:
        messages.info(request, 'Item not found in wishlist.')
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist_to_cart(request, id):
    """Move an item from wishlist to the user's cart."""
    product = get_object_or_404(Product, id=id)
    # remove from wishlist session
    wishlist = request.session.get('wishlist', [])
    if id in wishlist:
        wishlist.remove(id)
        request.session['wishlist'] = wishlist

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f'Moved "{product.name}" to cart.')
    return redirect('cart')


# --- Admin placeholder views (simple stubs) ---

def admin_login(request):
    return render(request, 'admin/login.html')


def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')





def admin_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'admin/orders.html', {'orders': orders})


@login_required(login_url='login')
def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')
@login_required(login_url='login')
def wishlist_to_cart(request, id):
    wishlist_item = Wishlist.objects.get(id=id, user=request.user)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=wishlist_item.product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    wishlist_item.delete()

    return redirect('cart')
  
def admin_required(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('admin-dashboard')

    return render(request, 'admin/login.html')

@user_passes_test(admin_required, login_url='admin-login')
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_staff=False).count()

    return render(request, 'admin/dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users
    })
@user_passes_test(admin_required, login_url='admin-login')
def admin_products(request):
    products = Product.objects.all()

    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            price=int(request.POST.get('price') or 0),
            metal=request.POST.get('metal'),
            purity=request.POST.get('purity'),
            weight=request.POST.get('weight'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            image_url=request.POST.get('image_url') or None
        )
        return redirect('admin-products')

    return render(request, 'admin/products.html', {'products': products})
@user_passes_test(admin_required, login_url='admin-login')
def admin_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'admin/orders.html', {'orders': orders})
  
@user_passes_test(admin_required, login_url='admin-login')
def admin_product_edit(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = int(request.POST.get('price') or 0)
        product.metal = request.POST.get('metal')
        product.purity = request.POST.get('purity')
        product.weight = request.POST.get('weight')
        product.description = request.POST.get('description')
        product.image_url = request.POST.get('image_url') or None

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('admin-products')

    return render(request, 'admin/product-edit.html', {'product': product})
@user_passes_test(admin_required, login_url='admin-login')
def admin_update_order_status(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        return redirect('admin-orders')

    return render(request, 'admin/order-status.html', {'order': order})
  
@user_passes_test(admin_required, login_url='admin-login')
def admin_product_delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin-products')

