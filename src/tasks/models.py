import os
from typing import Any
from uuid import uuid4
from django.db import models
from django.utils.deconstruct import deconstructible
from users.models import Profile
from house.models import House

# Create your models here.
@deconstructible
class GenerateAttachementFilePath(object):
    def __call__(self,instance, filename) :
        extention = filename.split('.')[-1]
        path = f"media/tasks/{instance.task.id}/attachements"
        name = f"{instance.id}.{extention}"
        return os.path.join(path, name)

attachement_image_path = GenerateAttachementFilePath()

class Status(models.TextChoices):
        UNCOMPLETED = 'uncompleted', 'Uncompleted'
        COMPLETED = 'completed', 'Completed'


class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='lists')
    created_by = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="lists"
    )
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UNCOMPLETED
    )

    def __str__(self):
        return f"{self.id}-{self.name}"


class Task(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_tasks"
    )
    completed_by = models.ForeignKey(
       Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="completed_tasks"
    )
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UNCOMPLETED
    )

    def __str__(self):
        return f"{self.id}-{self.name}"



class Attachement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4(),editable=False) 
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachement_image_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="attachements")

    def __str__(self):
        return f"{self.id}-{self.name}"