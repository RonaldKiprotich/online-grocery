from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# Create your models here.
# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.IntegerField(null=True)

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    email = models.EmailField(blank=True)

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    email = models.EmailField(blank=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = CloudinaryField('image')
    cost = models.DecimalField(blank=False, decimal_places=1, max_digits=5)
    units_remaining = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return f'{self.name} category'

    def create_category(self):
        self.save()

    def delete_category(self):
        self.delete()

    @classmethod
    def find_category(cls, category_id):
        return cls.objects.filter(id=category_id) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =  CloudinaryField('image')
    items = models.TextField()
    contact = models.IntegerField(null=True)
    email = models.EmailField()
    location_address = models.CharField(max_length=300, null=True) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def create_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()  

class Unit(models.Model):
    image_of_good = models.ImageField(upload_to='units/')
    name_of_good = models.CharField(max_length=250)
    mass_of_good_in_kgs = models.IntegerField(blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='units')
    added = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return f"/unit/{self.id}"
 
    def save_unit(self):
        self.save()

    def delete_unit(self):
        self.delete()

    def __str__(self):
        return f'{self.user} Unit'
    
    @classmethod
    def get_user_units(cls,user):
        return cls.objects.filter(user=user)
    
    @classmethod
    def get_category_units(cls,category):
        return cls.objects.filter(category=category)
    
    @classmethod
    def all_units(cls):
        return cls.objects.all()

    @classmethod
    def find_unit(cls, unit_id):
        return cls.objects.filter(id=unit_id) 
    
