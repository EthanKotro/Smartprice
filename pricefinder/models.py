from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField() 

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255)