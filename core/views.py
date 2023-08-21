from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from .models import Event
from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer, EventSerializer


class ProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)
