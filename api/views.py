from django.shortcuts import render

from api.models import User, Event, Artiste
from api.serializers import EventSerializer, ArtisteSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

# Create your views here.


class EventList(generics.ListCreateAPIView):
    """
    List all the events
    """
    # TODO: Paginate events
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArtisteList(APIView):
    """
    List all the registered artistes
    """
    def get(self, request, format=None):
        artistes = Artiste.object.all()
        serializer = ArtisteSerializer(artistes, many=True)
        return Response(serializer.data)


class UserList(generics.ListCreateAPIView):
    """
    List all the users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
