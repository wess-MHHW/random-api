from rest_framework import viewsets, mixins

from .serializers import TaskListSerializer, TaskSerializer, AttachementSerializer

from .models import Task, TaskList, Attachement

from .permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditAttachementElseNone

class TaskListViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAllowedToEditTaskListElseNone]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]

class AttachementViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Attachement.objects.all()
    serializer_class = AttachementSerializer
    permission_classes = [IsAllowedToEditAttachementElseNone]