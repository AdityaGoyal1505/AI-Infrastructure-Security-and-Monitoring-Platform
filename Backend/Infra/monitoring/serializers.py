from rest_framework import serializers #type: ignore
from django.contrib.auth import get_user_model #type: ignore

from .models import Workspace, Event


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password',
            'role',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get(
                'role',
                'viewer'
            )
        )

        return user


class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Workspace

        fields = [
            'id',
            'name',
            'description',
            'api_key',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'api_key',
            'created_at',
        ]


class EventSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event

        fields = [
            'source_service',
            'event_type',
            'severity',
            'message',
            'raw_log',
            'metadata',
        ]