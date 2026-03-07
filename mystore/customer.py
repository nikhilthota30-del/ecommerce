from django.db import models

class Customer(models.Model):
    # Changed to lowercase 'first_name' to follow Django/Python standards
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100) # Increased length for future hashing

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Optimized email check logic
    def ifemailExists(self):
        return Customer.objects.filter(email=self.email).exists()