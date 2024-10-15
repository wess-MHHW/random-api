from rest_framework import serializers

from house.models import House

from .models import Task, TaskList, Attachement

class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')

    class Meta:
        model = TaskList
        fields = ['id', 'name', 'description', 'status', 'created_on', 'created_by', 'house', 'url']
        read_only_fiekds = ['created_on', 'status']

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), view_name='tasks-list-detail')

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'created_on', 'completed_on', 'created_by', 'completed_by', 'task_list', 'url']
        read_only_fiekds = ['created_on', 'created_by', 'completed_on', 'completed_by']

class AttachementSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), view_name='task-detail')

    class Meta:
        model = Attachement
        fields = ['id', 'created_on', 'data', 'task']
        read_only_fiekds = ['created_on']


