from rest_framework import serializers
from api.models import Artiste, Event, User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('created', 'title', 'poster', 'description', 'location')


class UserSerializer(serializers.ModelSerializer):
    events = EventSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('alias', 'email', 'location', 'events')


class ArtisteSerializer(serializers.ModelSerializer):
    events = EventSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Artiste
        fields = ('bio', 'record_label', 'user', 'events')
