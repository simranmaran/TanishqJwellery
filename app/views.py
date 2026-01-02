from django.shortcuts import render, redirect
from .models import Registration

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def registerdata(request):
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['cpassword']

        if Registration.objects.filter(email=e).exists():
            return render(request, 'register.html', {'msg': 'User already exists'})

        if p != cp:
            return render(request, 'register.html', {'msg': 'Passwords do not match'})

        Registration.objects.create(email=e, password=p)
        return render(request, 'login.html', {'y': 'Registration successful. Please login'})

def login(request):
    return render(request, 'login.html')

def logindata(request):
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['password']

        user = Registration.objects.filter(email=e).first()

        if not user:
            return redirect('register')

        if user.password != p:
            return render(request, 'login.html', {'msg': 'Incorrect password'})

        request.session['user_id'] = user.id
        return redirect('dashboard')

def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'dashboard.html')
