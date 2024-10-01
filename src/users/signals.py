from django.contrib.auth.models import User
from users.models import Profile
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

@receiver(signal=post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(signal=pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username= f"{instance.first_name}-{instance.last_name}".lower()
        counter = 1
        while User.objects.filter(username=username):
            username= f"{instance.first_name}-{instance.last_name}-{counter}".lower()
            counter += 1
        print("username", username)
        instance.username = username
