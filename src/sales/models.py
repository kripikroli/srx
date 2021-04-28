from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def get_sales_customer(self):
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name

    def get_sales_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id

    def __str__(self):
        return f"{self.id}, product: {self.product.name}, quantity: {self.quantity}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created_at is None:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()


    def __str__(self):
        return f"Sales amount: {self.total_price}"

class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_name}"
