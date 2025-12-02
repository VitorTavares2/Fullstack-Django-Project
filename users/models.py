from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Adress = models.CharField(max_length = 255, blank = True, null = True)
    City = models.CharField(max_length = 100 ,blank = True , null = True) 
    State = models.CharField(max_length = 2, blank = True, null = True)
    ZIPCODE = models.CharField(max_length = 20, blank = True, null = True)
    phone = models.CharField(max_length = 11 , blank  = True , null = True)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

