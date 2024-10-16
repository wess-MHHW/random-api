from rest_framework import viewsets, mixins, filters

from .serializers import TaskListSerializer, TaskSerializer, AttachementSerializer

from .models import Task, TaskList, Attachement

from rest_framework.decorators import action

from .models import Status

from django.utils import timezone

from rest_framework.response import Response

from rest_framework import status as s

from .permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditAttachementElseNone

from django_filters.rest_framework import DjangoFilterBackend

class TaskListViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAllowedToEditTaskListElseNone]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]
    filter_backends = [filters.SearchFilter ,DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['status',]

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        user_profile= self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset
    
    @action(detail=True, methods=['PATCH'])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data['status']
            if status == Status.UNCOMPLETED:
                if task.status == Status.COMPLETED:
                    task.status = Status.UNCOMPLETED
                    task.complete_on=None
                    task.complete_by=None
                else:
                    raise Exception('Task is already marked as uncompleted.')
            elif status == Status.COMPLETED:
                if task.status == Status.UNCOMPLETED:
                    task.status = Status.COMPLETED
                    task.complete_on=timezone.now()
                    task.complete_by=profile
                else:
                    raise Exception('Task is already marked as completed.')
            else:
                raise Exception('Task status is invalid.')
            
            task.save()
            serializer = TaskSerializer(instance=task, context={'request':request})
            return Response(serializer.data, status=s.HTTP_200_OK)

        except Exception as e:
            return Response({'detail':str(e)}, status=s.HTTP_400_BAD_REQUEST)



class AttachementViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Attachement.objects.all()
    serializer_class = AttachementSerializer
    permission_classes = [IsAllowedToEditAttachementElseNone]