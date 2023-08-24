from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

from .models import Event
from .permissions import IsOwnerOrAdmin, IsInOrganizerGroup
from .serializers import UserSerializer, EventSerializer


class ProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsInOrganizerGroup]

    def get(self, request):
        data = {
            'username': request.user.username
        }
        return Response(data)


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)


class EventDetails(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
