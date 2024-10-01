from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail")
    class Meta:
        model = Profile
        fields = ["id","user","image","url"]

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required = False)
    old_password = serializers.CharField(write_only=True, required = False)
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "old_password","url", "profile"]

    def validate(self, data):
        method = self.context['request'].method
        password = data.get('password', None)
        if method == 'POST':
            if password is None:
                raise serializers.ValidationError({'details':'Password is required.'})
        elif method == 'PUT' or method == 'PATCH':
             old_password = data.get('old_password', None)
             if password is not None and old_password is None:
                raise serializers.ValidationError({'details':'Old password is required.'})
        return data




    def create(self, validated_data):
        password = validated_data.pop("password")
        user= User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        try:
            password = validated_data.pop('password', None)
            old_password = validated_data.pop('old_password', None)

            if password and old_password:
                if instance.check_password(old_password):
                    instance.set_password(password)
                    instance.save()
                else:
                    raise Exception('Old password is incorrect.')
        except Exception as error:
            raise serializers.ValidationError({'details':error})

        return super().update(instance, validated_data)