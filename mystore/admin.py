from django.contrib import admin
from .models import Product, Category, Customer, Order


class Categoryinfo(admin.ModelAdmin):
    list_display=["name"]
class Productinfo(admin.ModelAdmin):
    list_display=["name","category","price"]


# Register your models here.
admin.site.register(Product,Productinfo)
admin.site.register(Category,Categoryinfo)
admin.site.register(Customer)
admin.site.register(Order)
