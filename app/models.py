from django.db import models

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    

    # optional (future use)
    contact = models.CharField(max_length=15, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.email
