from rest_framework import routers

from .viewsets import TaskListViewSet, TaskViewSet, AttachementViewSet

app_name = 'tasks'

router = routers.DefaultRouter()
router.register('tasks-list', TaskListViewSet)
router.register('tasks', TaskViewSet)
router.register('attachements', AttachementViewSet)