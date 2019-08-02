from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    expire_date = models.DateTimeField()
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} Sayi ({self.quantity}) Qitmeti({self.price})"

    class Meta:
        ordering = ["-id"]


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)

    create_date = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Sales, self).__init__(*args, **kwargs)
        self.cache_quantity = self.quantity

    def __str__(self):
        return f"{self.product.name}"

