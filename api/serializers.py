from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import User, Event

from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializes registration and creates a new user"""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('Invalid email address')

        if password is None:
            raise serializers.ValidationError('Invalid password')

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
            }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class EventSerializer(serializers.ModelSerializer):
    artistes = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['created',
                  'title',
                  'poster',
                  'description',
                  'location',
                  'date',
                  'ticket_purchase',
                  'artistes',
                  'creator']

        validators = [
                UniqueTogetherValidator(
                    queryset=Event.objects.all(),
                    fields=('title', 'description', 'date')
                )
        ]

        def create(self, validated_data):
            artistes_data = validated_data.pop('artistes')
            event = Event.objects.create(**validated_data)
            for artiste in artistes_data:
                user = User.objects.get_or_create(username=artiste)
                event.artistes.add(user)
            return event
