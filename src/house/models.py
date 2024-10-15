import os
from uuid import uuid4
from django.db import models
from django.utils.deconstruct import deconstructible
from users.models import Profile

# Create your models here.
@deconstructible
class GenerateHouseImagePath(object):
    def __call__(self,instance, filename) :
        extention = filename.split('.')[-1]
        path = f"media/houses/{instance.id}/images/"
        name = f"house_image.{extention}"
        return os.path.join(path, name)
    
house_image_path = GenerateHouseImagePath()

class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100)
    image = models.FileField(blank=True, upload_to=house_image_path)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    manager = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, related_name='managed_house')
    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    uncompleted_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} | {self.name}"
    
