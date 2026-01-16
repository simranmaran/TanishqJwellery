from django.shortcuts import render, redirect
import random
from django.core.mail import send_mail
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'msg':'User already exists'})

        User.objects.create(
            username=name,
            email=email,
            password=password,
            first_name=name
        )
        return redirect('login')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'accounts/login.html', {'msg':'Invalid credentials'})

    return render(request, 'accounts/login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'accounts/forgot_password.html', {
                'msg': 'Email not registered'
            })
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_verified = False
        user.save()

        send_mail(
            'Password Reset OTP',
            f'Your OTP is {otp}',
            'simranmaran10gmail@gmail.com',
            [email],
            fail_silently=False,
        )

        request.session['reset_email'] = email
        return redirect('verify_otp')

    return render(request, 'accounts/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, 'accounts/verify_otp.html', {
                'msg': 'Email not registered',
                'email': email
            })

        if user.otp == otp:
            user.otp_verified = True
            user.save()

            # next step ke liye email session me store
            request.session['reset_email'] = email
            return redirect('reset_password')

        return render(request, 'accounts/verify_otp.html', {
            'msg': 'Invalid OTP',
            'email': email
        })

    # GET request (page load)
    email = request.session.get('reset_email')
    return render(request, 'accounts/verify_otp.html', {
        'email': email,
        'msg': 'Enter OTP sent to your email'
    })




def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')

    user = User.objects.get(email=email)

    if not user.otp_verified:
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'accounts/reset_password.html', {
                'msg': 'Passwords do not match'
            })

        user.set_password(password)
        user.otp = None
        user.otp_verified = False
        user.save()

        request.session.flush()
        return redirect('login')

    return render(request, 'accounts/reset_password.html')
  