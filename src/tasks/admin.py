from django.contrib import admin
from .models import Task, TaskList, Attachement

# Register your models here.
class AdminTask(admin.ModelAdmin):
    readonly_fields = ('id', 'created_on', )

class AdminTaskList(admin.ModelAdmin):
    readonly_fields = ('id', 'created_on', )

class AdminAttachement(admin.ModelAdmin):
    readonly_fields = ('id', 'created_on', )

admin.site.register(Task, AdminTask)
admin.site.register(TaskList, AdminTaskList)
admin.site.register(Attachement, AdminAttachement)