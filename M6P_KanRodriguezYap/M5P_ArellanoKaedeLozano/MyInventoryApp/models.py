from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def GetName(self):
        return self.name

    def __str__(self):
        return f'Supplier: {self.name}, City: {self.city}, Country: {self.country}, Created At: {self.created_at}'

class WaterBottle(models.Model):
    SKU = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    mouth_size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    supplied_by = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    current_quantity = models.IntegerField()

    def __str__(self):
        return f'SKU: {self.SKU}, Brand: {self.brand}, Mouth Size: {self.mouth_size}, Size: {self.size}, Color: {self.color}, Supplied By: {self.supplied_by.name}, cost: {self.cost}, Current Quantity: {self.current_quantity}'
    
class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def __str__(self):
        return f'Account: {self.username}'