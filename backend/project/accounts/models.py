# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     is_admin = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email 

#     # OTP fields
# class User(AbstractBaseUser):
#     otp = models.CharField(max_length=6, blank=True, null=True)
#     otp_verified = models.BooleanField(default=False)
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # ✅ Extends AbstractUser
    is_admin = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = ['first_name']
    
    def __str__(self):
        return self.email
