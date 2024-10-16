from rest_framework import serializers

from house.models import House

from .models import Task, TaskList, Attachement

class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="task-detail")

    class Meta:
        model = TaskList
        fields = ['id', 'name', 'description', 'status', 'created_on', 'created_by', 'house', 'tasks', 'url']
        read_only_fiekds = ['created_on', 'status']

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(),
    view_name='tasklist-detail' )
    attachements = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='attachement-detail')

    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError("Tasklist doesn't belong to the house that the user is part of.")
        else :
            return value

    def create(self, validated_data):
        user_profile = self.context['request'].user.profile
        task = Task.objects.create(**validated_data)
        task.created_by = user_profile
        task.save()
        return task

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'created_on', 'completed_on', 'created_by', 'completed_by', 'task_list', 'attachements', 'url']
        read_only_fiekds = ['created_on', 'created_by', 'completed_on', 'completed_by','status']

class AttachementSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), view_name='task-detail')

    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs['task']
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in user_profile.house.lists.all():
            raise serializers.ValidationError({"task":"Tasklist doesn't belong to the house that the user is part of."})
        else :
            return attrs

    class Meta:
        model = Attachement
        fields = ['id', 'created_on', 'data', 'task']
        read_only_fiekds = ['created_on']


