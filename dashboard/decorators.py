from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_admin'):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
