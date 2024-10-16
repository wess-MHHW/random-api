from rest_framework import serializers
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True,view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='tasklist-detail', source='lists')
    class Meta:
        model = House
        fields = ['id','image','name','created_on','manager','description','members_count','points', 'completed_tasks_count','uncompleted_tasks_count', 'members', 'task_list',"url"]
        read_only_fields = ['points', 'completed_tasks_count','uncompleted_tasks_count']