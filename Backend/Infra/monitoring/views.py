import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_event_task
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import FileResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken #type:ignore
from .serializers import (
    RootCauseAnalysisSerializer,
    RecommendationSerializer,
    HealthScoreSerializer,
    AnomalySerializer,
    RCAInsightSerializer,
    RiskPredictionSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
    WorkspaceSetupSerializer
)
from monitoring.models import *

from .ai.chatbot import ask_inframind

class RegisterView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken #type:ignore
from rest_framework_simplejwt.exceptions import TokenError #type:ignore

class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)

        refresh_token = str(refresh)

        response = Response(

            {
                "user": UserSerializer(user).data
            },

            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None"   # change
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None"   # change
        )

        return response
    
class LogoutView(APIView):

    def post(self, request):

        response = Response(

            {"message": "Logged out successfully"},

            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")

        response.delete_cookie("refresh_token")

        return response
    
class CookieTokenRefreshView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        refresh_token = request.COOKIES.get(

            "refresh_token"

        )

        if not refresh_token:

            return Response(

                {

                    "detail":

                    "Refresh token missing"

                },

                status=401

            )

        try:

            refresh = RefreshToken(

                refresh_token

            )

            access_token = str(

                refresh.access_token

            )

            response = Response(

                {

                    "message":

                    "Token refreshed"

                }

            )

            response.set_cookie(

                key="access_token",

                value=access_token,

                httponly=True,

                secure=False,

                samesite="Lax",

                max_age=60 * 60

            )

            return response

        except TokenError:

            return Response(

                {

                    "detail":

                    "Invalid refresh token"

                },

                status=401

            )
        
class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)

class WorkspaceListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        workspaces = Workspace.objects.filter(user=request.user).order_by("-created_at")

        serializer = WorkspaceSerializer(workspaces,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):

        serializer = WorkspaceCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():

            workspace = serializer.save()

            return Response(WorkspaceSerializer(workspace).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class WorkspaceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_workspace(self, request, workspace_id):

        return get_object_or_404(Workspace,id=workspace_id,user=request.user)

    def get(self, request, workspace_id):

        workspace = self.get_workspace(request,workspace_id)

        serializer = WorkspaceSerializer(workspace)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, workspace_id):

        workspace = self.get_workspace(request,workspace_id)

        serializer = WorkspaceSerializer(workspace,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workspace_id):

        workspace = self.get_workspace(request,workspace_id)

        workspace.delete()

        return Response(
            {
                "message": "Workspace deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

class WorkspaceSetupView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_id):

        workspace = get_object_or_404(

            Workspace,

            id=workspace_id,

            user=request.user
        )

        data = {

            "workspace_id": workspace.id,

            "workspace_name": workspace.name,

            "api_key": workspace.api_key,

            "download_url":f"/api/workspaces/{workspace.id}/agent/"
        }

        serializer = WorkspaceSetupSerializer(data)

        return Response(

            serializer.data,

            status=status.HTTP_200_OK
        )
class DownloadAgentView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_id):

        workspace = get_object_or_404(

            Workspace,

            id=workspace_id,

            user=request.user

        )


        base_dir = os.path.dirname(

            settings.BASE_DIR

        )


        agent_path = os.path.join(

            base_dir,

            "telemetry-agent",

            "monitoring-agent.zip"

        )


        print("Agent Path :", agent_path)

        print(

            "Exists :",

            os.path.exists(agent_path)

        )


        if not os.path.exists(agent_path):

            return Response(

                {

                    "error":

                    "Agent package not found"

                },

                status=404

            )


        response = FileResponse(

            open(

                agent_path,

                "rb"

            ),

            as_attachment=True,

            filename="monitoring-agent.zip",

            content_type="application/zip"

        )


        response["Content-Disposition"] = (

            'attachment; '

            'filename="monitoring-agent.zip"'

        )


        return response
class EventIngestView(APIView):
# ac5b2164-c5a3-4ff8-8806-9621cc78807e
    authentication_classes = []
    permission_classes = []

    def post(self,request):

        api_key = request.headers.get("X-API-KEY")

        if not api_key:

            return Response(

                {
                    "error":"API key missing"
                },

                status=401
            )

        try:

            Workspace.objects.get(api_key=api_key)

        except Workspace.DoesNotExist:

            return Response(

                {
                    "error":"Invalid API key"
                },

                status=401
            )

        payload = request.data.copy()

        payload["api_key"] = api_key

        process_event_task.delay(payload)

        return Response(

            {
                "status":"accepted"
            },

            status=202
        )


class BatchEventIngestView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self,request):

        api_key = request.headers.get("X-API-KEY")

        if not api_key:

            return Response(

                {
                    "error":"API key missing"
                },

                status=401
            )

        try:

            Workspace.objects.get(api_key=api_key)

        except Workspace.DoesNotExist:

            return Response(

                {
                    "error":"Invalid API key"
                },

                status=401
            )

        events = request.data.get("events",[])
        for event in events:
            print("RECEIVED EVENT")
            print(event)
            print("TYPE:", event.get("event_type"))

            event["api_key"] = api_key
            process_event_task.delay(event)
        return Response(

            {
                "accepted":len(events)
            },

            status=202
        )

class AIInsightsView(APIView):

    def get(self, request):

        workspace_id = request.GET.get("workspace")

        if not workspace_id:

            return Response(

                {
                    "error": "workspace query parameter is required"
                },

                status=400

            )

        latest_rca = RootCauseAnalysis.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()

        latest_health_score = HealthScore.objects.filter(workspace_id=workspace_id).order_by("-updated_at").first()

        recommendations = Recommendation.objects.filter(workspace_id=workspace_id).order_by("-created_at")[:5]

        anomalies = Anomaly.objects.filter(workspace_id=workspace_id).order_by("-created_at")[:10]

        insights = RCAInsight.objects.filter(workspace_id=workspace_id).order_by("-occurrence_count")[:2]

        alerts_count = Alert.objects.filter(

            workspace_id=workspace_id,

            status="OPEN"

        ).count()

        anomaly_count = Anomaly.objects.filter(workspace_id=workspace_id).count()

        risk_prediction = RiskPrediction.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()


        return Response({

            "latest_rca":RootCauseAnalysisSerializer(latest_rca).data

            if latest_rca

            else None,


            "health_score":HealthScoreSerializer(latest_health_score).data

            if latest_health_score

            else None,


            "recommendations":RecommendationSerializer(recommendations,many=True).data,


            "recent_anomalies":AnomalySerializer(anomalies,many=True).data,


            "top_insights":RCAInsightSerializer(insights,many=True).data,


            "alerts_count":alerts_count,


            "anomaly_count":anomaly_count,


            "risk_prediction":RiskPredictionSerializer(risk_prediction).data

            if risk_prediction

            else None

        })

class AITrendView(APIView):

    def get(self, request):

        workspace_id = request.GET.get("workspace")

        insights = (RCAInsight.objects.filter(workspace_id=workspace_id).order_by("-occurrence_count"))

        serializer = RCAInsightSerializer(insights,many=True)

        return Response(serializer.data)

class RiskPredictionView(APIView):

    def get(self, request):

        workspace_id = request.GET.get("workspace")

        predictions = (RiskPrediction.objects.filter(workspace_id=workspace_id).order_by("-risk_score"))

        serializer = RiskPredictionSerializer(predictions,many=True)

        return Response(serializer.data)

class AIChatView(APIView):

    def post(self,request):

        workspace_id = request.data.get("workspace")

        question = request.data.get("question")


        if not workspace_id:

            return Response(

                {

                    "error":"workspace required"

                },

                status=400

            )


        if not question:

            return Response(

                {

                    "error":"question required"

                },

                status=400

            )


        answer = ask_inframind(workspace_id,question)


        return Response(

            {

                "answer":answer

            }

        )