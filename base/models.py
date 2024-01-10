from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30,null=False,default='item')
    weight = models.FloatField()
    value = models.FloatField()

class Inventory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(null=False,default=timezone.now)
    products_present = models.ManyToManyField(Product)
    
    def __str__(self) -> str:
        return self.name