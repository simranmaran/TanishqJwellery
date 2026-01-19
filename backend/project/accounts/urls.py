from django.urls import path
# from .views import register, user_login, logout,forgot_password,verify_otp,reset_password
from django.contrib.auth import views as auth_views
from .forms import LoginForm, RegistrationForm, AddressForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from accounts import views
app_name = "accounts"   


urlpatterns = [
    # Registration & Login
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    
    # Profile & Addresses
    path('profile/', views.profile, name="profile"),
    path('add-address/', views.AddressView.as_view(), name="add-address"),
    path('remove-address/<int:id>/', views.remove_address, name="remove-address"),
    
    # Password Management
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html', 
        form_class=PasswordChangeForm, 
        success_url='password-change-done'
    ), name="password-change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name="password-change-done"),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html', 
        form_class=PasswordResetForm,
        email_template_name='accounts/password_reset_email.html',
        success_url='password-reset-done'
    ), name="password-reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html', 
        form_class=SetPasswordForm,
        success_url='password-reset-complete'
    ), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name="password_reset_complete"),
]
