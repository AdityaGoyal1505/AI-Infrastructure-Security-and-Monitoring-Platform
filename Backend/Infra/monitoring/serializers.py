from rest_framework import serializers
from monitoring.models import RootCauseAnalysis,Recommendation
from django.contrib.auth import get_user_model

from .models import (
    Workspace,
    Event,
    NodeStatus,
    User,
    RCAInsight,
    RootCauseAnalysis,
    Recommendation,
    Anomaly,
    HealthScore,
    RiskPrediction
)

User = get_user_model()
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["id","username","email","created_at"]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,min_length=8)

    class Meta:

        model = User

        fields = ["username","email","password"]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        attrs["user"] = user

        return attrs


class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Workspace

        fields = [
            "id",
            "name",
            "description",
            "api_key",
            "is_active",
            "created_at",
            "updated_at"
        ]

        read_only_fields = ["id","api_key","created_at","updated_at"]


class WorkspaceCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Workspace

        fields = ["name","description"]

    def create(self, validated_data):

        user = self.context["request"].user

        workspace = Workspace.objects.create(user=user,**validated_data)

        return workspace

class WorkspaceSetupSerializer(serializers.Serializer):

    workspace_id = serializers.IntegerField()

    workspace_name = serializers.CharField()

    api_key = serializers.UUIDField()

    download_url = serializers.CharField()

class EventSerializer(serializers.ModelSerializer):

    class Meta:

        model = Event

        fields = '__all__'


class NodeStatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = NodeStatus

        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recommendation

        fields = "__all__"


class RCASerializer(serializers.ModelSerializer):

    class Meta:

        model = RootCauseAnalysis

        fields = "__all__"

class RCAInsightSerializer(serializers.ModelSerializer):

    class Meta:

        model = RCAInsight

        fields = "__all__"

class RootCauseAnalysisSerializer(serializers.ModelSerializer):

    class Meta:

        model = RootCauseAnalysis

        fields = "__all__"

class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recommendation

        fields = "__all__"

class AnomalySerializer(serializers.ModelSerializer):

    class Meta:

        model = Anomaly

        fields = "__all__"

class HealthScoreSerializer(serializers.ModelSerializer):

    class Meta:

        model = HealthScore

        fields = "__all__"

class RiskPredictionSerializer(serializers.ModelSerializer):

    class Meta:

        model = RiskPrediction

        fields = "__all__"