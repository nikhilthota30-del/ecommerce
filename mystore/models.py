from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User

# 1. Category Model (Must be first so Product can see it)
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self): 
        return self.name

# 2. Customer Model (Must be before Order)

class Customer(models.Model):
    # Add this line to link the UI login to this table
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 3. Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='img')
    desc = models.TextField(default='', blank=True, null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_category_id(get_id):
        if get_id:
            return Product.objects.filter(category=get_id)
        else:
            return Product.objects.all()

# 4. Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Fixed typo here
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=250, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.customer.first_name}"