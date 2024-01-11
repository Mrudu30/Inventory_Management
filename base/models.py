from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=30,null=False,default='item')
    weight = models.FloatField()
    value = models.FloatField()
    date_added = models.DateTimeField(null=False,default=timezone.now)
    
    def __str__(self):
        return self.pname
    

class Inventory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,default="Add A Name To Your Inventory")
    date_created = models.DateTimeField(null=False,default=timezone.now)
    products_present = models.ManyToManyField(Product)
    
    def __str__(self) -> str:
        return self.name    
