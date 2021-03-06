from api.serializers import (LoginSerializer,
                             RegistrationSerializer,
                             EventSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.settings import api_settings

from .models import Event


# Create your views here.

class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EventView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request):
        event = request.data
        serializer = self.serializer_class(data=event)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        queryset = Event.objects.all()

        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
