from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=(0.00), blank=True)
    image = models.CharField(max_length=228, default = None, blank = True, null = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Use 
    listed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['product']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['product']),
            models.Index(fields=['listed_date']),
        ]
    

   
    def __str__(self):
        return self.product
    

class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Us
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - ${self.bid_amount}"
    

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user}: {self.comment} on {self.created_at}"


class Watchlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Winner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=64, default = None)

    def __str__(self):
        return f"{self.product}"

