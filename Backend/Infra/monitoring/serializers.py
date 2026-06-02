from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import (
    Workspace,
    Event,
    NodeStatus
)

User = get_user_model()


class RegisterSerializer(
    serializers.ModelSerializer
):

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

        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get(
                'role',
                'viewer'
            )
        )


class WorkspaceSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Workspace

        fields = '__all__'


class EventSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Event

        fields = '__all__'


class NodeStatusSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = NodeStatus

        fields = '__all__'