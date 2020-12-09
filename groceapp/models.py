from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.IntegerField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/')
    cost = models.DecimalField(blank=False, decimal_places=1, max_digits=5)
    slots_remaining = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return f'{self.name} category'

    def create_category(self):
        self.save()

    def delete_category(self):
        self.delete()

    @classmethod
    def find_category(cls, category_id):
        return cls.objects.filter(id=category_id)   
    
