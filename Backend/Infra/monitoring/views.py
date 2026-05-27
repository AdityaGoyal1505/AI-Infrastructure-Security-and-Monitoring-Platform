from rest_framework.decorators import api_view,permission_classes #type: ignore
from rest_framework.permissions import IsAuthenticated,AllowAny #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework import status #type: ignore
 
from .models import Workspace, Event
from .serializers import RegisterSerializer, WorkspaceSerializer, EventSerializer

from .tasks import process_event


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_workspace(request):

    serializer = WorkspaceSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save(
            user=request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def ingest_event(request):

    api_key = request.headers.get(
        'X-API-KEY'
    )

    if not api_key:

        return Response(
            {
                'error': 'API key missing'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:

        workspace = Workspace.objects.get(
            api_key=api_key,
            is_active=True
        )

    except Workspace.DoesNotExist:

        return Response(
            {
                'error': 'Invalid API key'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = EventSerializer(
        data=request.data
    )

    if serializer.is_valid():

        event = serializer.save(
            workspace=workspace
        )

        process_event.delay(
            event.id
        )

        return Response(
            {
                'message': 'Event received',
                'event_id': event.id
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def health_check(request):

    return Response(
        {
            'status': 'healthy'
        }
    )