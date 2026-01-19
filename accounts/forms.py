from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    UsernameField, PasswordChangeForm as DjangoPasswordChangeForm,
    PasswordResetForm as DjangoPasswordResetForm,
    SetPasswordForm as DjangoSetPasswordForm
)

from .models import Address


# ================= REGISTER =================
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
        }


# ================= LOGIN =================
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'}))


# ================= ADDRESS =================
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        widgets = {
            'locality': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
        }


# ================= PASSWORD CHANGE =================
class PasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                     help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


# ================= PASSWORD RESET =================
class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


# ================= SET NEW PASSWORD =================
class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                     help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
