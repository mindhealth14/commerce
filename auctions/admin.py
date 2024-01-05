from django.contrib import admin
from .models import  User, Bid, Category, Comment,Product, Winner

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Winner)