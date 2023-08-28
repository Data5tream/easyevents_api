from rest_framework import serializers

from .models import Event, User


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    class Meta:
        model = Event
        fields = [
            'id', 'creator', 'title', 'description', 'max_participants',
            'start_date', 'end_date', 'signup_start', 'signup_end', 'participants'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'creator', 'title', 'description', 'max_participants',
            'start_date', 'end_date', 'signup_start', 'signup_end', 'participants'
        ]


class UserSerializer(serializers.ModelSerializer):
    created_events = EventSerializer(many=True, read_only=True)
    joined_events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'created_events', 'joined_events']
