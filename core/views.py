from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status

from .models import Event, EventUpdate
from .permissions import IsOwnerOrAdmin, IsInOrganizerGroup
from .serializers import UserSerializer, EventSerializer, EventDetailSerializer, EventUpdateSerializer


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsInOrganizerGroup]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsInOrganizerGroup]

    def get(self, request):
        updates = EventUpdate.objects.filter(event__creator=request.user).order_by('-timestamp')[:10]
        events = Event.objects.filter(creator=request.user, deleted=False)
        update_serializer = EventUpdateSerializer(updates, many=True)
        events_serializer = EventSerializer(events, many=True)

        return Response(data={
            'updates': update_serializer.data,
            'events': events_serializer.data
        })


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsInOrganizerGroup, IsOwnerOrAdmin]

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)


class EventDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, IsInOrganizerGroup, IsOwnerOrAdmin]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk)

        # This should not be necessary, as it should be handled by the `IsOwnerOrAdmin` permission, but the perm
        # somehow doesn't work here, so we are using this workaround.
        if event.creator == request.user or request.user.groups.filter(name="admin").exists():
            serializer = EventDetailSerializer(event)
            return Response(serializer.data)

        raise Http404

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
