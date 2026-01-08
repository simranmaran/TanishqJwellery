from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def product_list(request):
    return render(request, 'products.html')

def product_detail(request):
    return render(request, 'product-detail.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def my_account(request):
    return render(request, 'my-account.html')
def my_account(request):
    return render(request, 'my-account.html')
def wishlist(request):
    return render(request, 'wishlist.html')
def cart(request):
    return render(request, 'cart.html')
