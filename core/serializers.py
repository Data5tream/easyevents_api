from rest_framework import serializers

from .models import Event, User


class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Event
        fields = [
            'id', 'creator', 'title', 'description', 'max_participants',
            'start_date', 'end_date', 'signup_start', 'signup_end'
        ]


class UserSerializer(serializers.ModelSerializer):
    created_events = EventSerializer(many=True, read_only=True)
    joined_events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'created_events', 'joined_events']
