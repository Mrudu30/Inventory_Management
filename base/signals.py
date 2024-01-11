from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inventory

@receiver(post_save, sender=User)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(user=instance)