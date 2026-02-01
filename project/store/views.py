from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category, Product, Order, OrderItem, Wishlist

# django api
from google import genai
from django.conf import settings
from django.http import HttpResponse
# django api

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:8]
    context = {'categories': categories, 'products': products}
    return render(request, 'store/home.html', context)


def product_list(request):
    products = Product.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    context = {'page_obj': page_obj, 'categories': categories}
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    context = {'items': items, 'total': total}
    return render(request, 'store/cart.html', context)


@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def update_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(pk)] = quantity
        else:
            cart.pop(str(pk), None)
        request.session['cart'] = cart
    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_amount=total)
        for item in items:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['product'].price)
        request.session['cart'] = {}
        return redirect('orders')
    context = {'items': items, 'total': total}
    return render(request, 'store/checkout.html', context)


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, pk):
    Wishlist.objects.filter(user=request.user, product_id=pk).delete()
    return redirect('wishlist')

def wedding_collection(request):
    wedding_products = Product.objects.filter(category__name__iexact='wedding')

    return render(request, 'store/wedding.html', {
        'products': wedding_products
    })
    
def community_view(request, name):
    products = Product.objects.filter(community=name)
    return render(request, 'community.html', {
        'products': products,
        'community_name': name.capitalize()
    })

def search(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'search.html', {
        'products': products,
        'query': query
    })

def dailywear_collection(request):
    products = Product.objects.filter(category__name__iexact='dailywear')
    return render(request, 'store/dailywear.html', {
        'products': products
    })


def dailywear_collection(request):
    products = Product.objects.filter(category__name="Dailywear")
    categories = Category.objects.all()

    # Filters
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    if category:
        products = products.filter(category_id=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'store/dailywear.html', {
        'products': products,
        'categories': categories
    })


def test_gemini(request):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Write a luxury jewellery product description in 2 lines"
    )

    return HttpResponse(response.text)

def gold_products(request):
    products = Product.objects.filter(metal__icontains='Gold')
    return render(request, 'store/gold.html', {'products': products})


def diamond_products(request):
    products = Product.objects.all()
    return render(request, 'store/diamond.html', {'products': products})
