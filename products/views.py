from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Category
from datetime import datetime
from django.contrib.auth.models import User  # ✅ ADD THIS IMPORT


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category = request.GET.get('category')
    gold = request.GET.get('gold')
    diamond = request.GET.get('diamond')

    if category:
        products = products.filter(category_id=category)
    if gold:
        products = products.filter(is_gold=True)
    if diamond:
        products = products.filter(is_diamond=True)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)]['qty'] += 1
    else:
        cart[str(id)] = {
            'name': product.name,
            'price': float(product.price),
            'qty': 1,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())

    return render(request, 'products/cart.html', {
        'cart': cart,
        'total': total
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    cart.pop(str(id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

def order_summary(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    total = sum(item['price'] * item['qty'] for item in cart.values())

    return render(request, 'products/order_summary.html', {
        'cart': cart,
        'total': total
    })
    
def profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    orders = request.session.get('orders', [])
    
    return render(request, 'accounts/profile.html', {
        'user': user,
        'orders': orders
    })

    

def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')

    total = sum(item['price'] * item['qty'] for item in cart.values())

    order = {
        'items': list(cart.values()),
        'total': total,
        'date': datetime.now().strftime('%d %b %Y')
    }

    orders = request.session.get('orders', [])
    orders.append(order)

    request.session['orders'] = orders
    request.session['cart'] = {}   # clear cart

    return redirect('profile')