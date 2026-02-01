from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    metal = models.CharField(max_length=50)
    purity = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True, null=True) 
    
    description = models.TextField()

    # ✅ ADD THIS ONLY
    community = models.CharField(
        max_length=50,
        choices=[
            ('bihari', 'Bihari Bride'),
            ('tamil', 'Tamil Bride'),
            ('telugu', 'Telugu Bride'),
            ('kannada', 'Kannadiga Bride'),
            ('gujarati', 'Gujarati Bride'),
            ('marathi', 'Marathi Bride'),
            ('bengali', 'Bengali Bride'),
            ('punjabi', 'Punjabi Bride'),
            ('up', 'UP Bride'),
            ('marwari', 'Marwari Bride'),
            ('odia', 'Odia Bride'),
            ('muslim', 'Muslim Bride'),
        ]
    )

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
