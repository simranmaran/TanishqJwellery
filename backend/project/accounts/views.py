# # from django.shortcuts import render, redirect
# # import random
# # from django.core.mail import send_mail
# # # from django.contrib.auth.models import User
# # from .models import User
# # from django.contrib.auth import authenticate,login,logout
# # from django.conf import settings
# # from django.contrib import messages

# # def register(request):
# #     if request.method == 'POST':
# #         name = request.POST['name']
# #         email = request.POST['email']
# #         password = request.POST['password']

# #         if User.objects.filter(email=email).exists():
# #             return render(request, 'accounts/register.html', {'msg':'User already exists'})

# #         User.objects.create(
# #             username=name,
# #             email=email,
# #             password=password,
# #             first_name=name
# #         )
# #         return redirect('login')

# #     return render(request, 'accounts/register.html')


# # def user_login(request):
# #     if request.method == 'POST':
# #         email = request.POST['email']
# #         password = request.POST['password']

# #         user = authenticate(request, username=email, password=password)

# #         if user:
# #             login(request, user)
# #             return redirect('home')

# #         return render(request, 'accounts/login.html', {'msg':'Invalid credentials'})

# #     return render(request, 'accounts/login.html')


# # def logout(request):
# #     request.session.flush()
# #     return redirect('login')


# # def forgot_password(request):
# #     if request.method == 'POST':
# #         email = request.POST.get('email')
# #         user = User.objects.filter(email=email).first()
# #         if not user:
# #             return render(request, 'accounts/forgot_password.html', {
# #                 'msg': 'Email not registered'
# #             })
# #         otp = str(random.randint(100000, 999999))
# #         user.otp = otp
# #         user.otp_verified = False
# #         user.save()

# #         send_mail(
# #             'Password Reset OTP',
# #             f'Your OTP is {otp}',
# #             'simranmaran10gmail@gmail.com',
# #             [email],
# #             fail_silently=False,
# #         )

# #         request.session['reset_email'] = email
# #         return redirect('verify_otp')

# #     return render(request, 'accounts/forgot_password.html')

# # def verify_otp(request):
# #     if request.method == 'POST':
# #         email = request.POST.get('email')
# #         otp = request.POST.get('otp')

# #         user = User.objects.filter(email=email).first()

# #         if not user:
# #             return render(request, 'accounts/verify_otp.html', {
# #                 'msg': 'Email not registered',
# #                 'email': email
# #             })

# #         if user.otp == otp:
# #             user.otp_verified = True
# #             user.save()

# #             # next step ke liye email session me store
# #             request.session['reset_email'] = email
# #             return redirect('reset_password')

# #         return render(request, 'accounts/verify_otp.html', {
# #             'msg': 'Invalid OTP',
# #             'email': email
# #         })

# #     # GET request (page load)
# #     email = request.session.get('reset_email')
# #     return render(request, 'accounts/verify_otp.html', {
# #         'email': email,
# #         'msg': 'Enter OTP sent to your email'
# #     })




# # def reset_password(request):
# #     email = request.session.get('reset_email')
# #     if not email:
# #         return redirect('forgot_password')

# #     user = User.objects.get(email=email)

# #     if not user.otp_verified:
# #         return redirect('forgot_password')

# #     if request.method == 'POST':
# #         password = request.POST.get('password')
# #         confirm = request.POST.get('confirm')

# #         if password != confirm:
# #             return render(request, 'accounts/reset_password.html', {
# #                 'msg': 'Passwords do not match'
# #             })

# #         user.set_password(password)
# #         user.otp = None
# #         user.otp_verified = False
# #         user.save()

# #         request.session.flush()
# #         return redirect('login')

# #     return render(request, 'accounts/reset_password.html')

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.contrib import messages
# from django.views import View
# from .models import Category, Product, Address, Cart, Order
  
# def home(request):
#     categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
#     products = Product.objects.filter(is_active=True, is_featured=True)[:8]
#     return render(request, 'store/index.html', {
#         'categories': categories,
#         'products': products,
#     })
# @login_required
# def profile(request):
#     addresses = Address.objects.filter(user=request.user)
#     orders = Order.objects.filter(user=request.user)
#     return render(request, 'account/profile.html', {
#         'addresses': addresses,
#         'orders': orders
#     })
# @method_decorator(login_required, name='dispatch')
# class AddressView(View):
#     def get(self, request):
#         form = AddressForm()
#         return render(request, 'account/add_address.html', {'form': form})

#     def post(self, request):
#         form = AddressForm(request.POST)
#         if form.is_valid():
#             Address.objects.create(user=request.user, **form.cleaned_data)
#             messages.success(request, "Address Added Successfully")
#         return redirect('store:profile')
# @login_required
# def remove_address(request, id):
#     address = get_object_or_404(Address, id=id, user=request.user)
#     address.delete()
#     messages.success(request, "Address removed")
#     return redirect('store:profile')

# @login_required
# def add_to_cart(request):
#     product_id = request.GET.get('prod_id')
#     product = get_object_or_404(Product, id=product_id)

#     cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('store:cart')
# @login_required
# def cart(request):
#     cart_products = Cart.objects.filter(user=request.user)

#     amount = sum(item.quantity * item.product.price for item in cart_products)
#     shipping_amount = 10

#     return render(request, 'store/cart.html', {
#         'cart_products': cart_products,
#         'amount': amount,
#         'shipping_amount': shipping_amount,
#         'total_amount': amount + shipping_amount,
#         'addresses': Address.objects.filter(user=request.user)
#     })
# @login_required
# def remove_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, id=cart_id)
#     cart_item.delete()
#     messages.success(request, "Item removed")
#     return redirect('store:cart')
# @login_required
# def plus_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, id=cart_id)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('store:cart')
# @login_required
# def minus_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, id=cart_id)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('store:cart')
# @login_required
# def checkout(request):
#     address_id = request.GET.get('address')
#     address = get_object_or_404(Address, id=address_id)

#     cart_items = Cart.objects.filter(user=request.user)

#     for item in cart_items:
#         Order.objects.create(user=request.user, product=item.product, quantity=item.quantity, address=address)
#         item.delete()

#     return redirect('store:orders')
# @login_required
# def orders(request):
#     return render(request, 'store/orders.html', {
#         'orders': Order.objects.filter(user=request.user).order_by('-ordered_date')
#     })
# @login_required
# def orders(request):
#     return render(request, 'store/orders.html', {
#         'orders': Order.objects.filter(user=request.user).order_by('-ordered_date')
#     })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .forms import RegistrationForm, AddressForm
from .models import Address, Cart, Product, Order, Category
import decimal
from django.contrib.auth import get_user_model
User = get_user_model()



# ================= REGISTER =================
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful!")
            return redirect("accounts:login")
        return render(request, "accounts/register.html", {"form": form})


# ================= PROFILE =================
@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, "account/profile.html", {
        "addresses": addresses,
        "orders": orders
    })


# ================= ADD ADDRESS =================
@method_decorator(login_required, name="dispatch")
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, "account/add_address.html", {"form": form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            Address.objects.create(user=request.user, **form.cleaned_data)
            messages.success(request, "New Address Added Successfully.")
            return redirect("profile")
        return render(request, "account/add_address.html", {"form": form})


# ================= REMOVE ADDRESS =================
@login_required
def remove_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    messages.success(request, "Address removed.")
    return redirect("profile")


# ================= ADD TO CART =================
@login_required
def add_to_cart(request):
    product_id = request.GET.get("prod_id")
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# ================= CART VIEW =================
@login_required
def cart(request):
    cart_products = Cart.objects.filter(user=request.user)

    amount = sum(item.quantity * item.product.price for item in cart_products)
    shipping_amount = 10

    return render(request, "store/cart.html", {
        "cart_products": cart_products,
        "amount": amount,
        "shipping_amount": shipping_amount,
        "total_amount": amount + shipping_amount,
        "addresses": Address.objects.filter(user=request.user)
    })


# ================= REMOVE CART =================
@login_required
def remove_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Product removed from Cart.")
    return redirect("cart")


# ================= PLUS CART =================
@login_required
def plus_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")


# ================= MINUS CART =================
@login_required
def minus_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


# ================= CHECKOUT =================
@login_required
def checkout(request):
    address_id = request.GET.get("address")
    address = get_object_or_404(Address, id=address_id, user=request.user)

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            address=address
        )
        item.delete()

    messages.success(request, "Order placed successfully.")
    return redirect("orders")


# ================= ORDERS =================
@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by("-ordered_date")
    return render(request, "store/orders.html", {"orders": all_orders})
