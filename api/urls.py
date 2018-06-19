from django.conf.urls import url
from .views import (RegistrationView,
                    LoginView,
                    EventView)


urlpatterns = [
    url(r'^users/?$', RegistrationView.as_view()),
    url(r'^users/login/?$', LoginView.as_view()),
    url(r'^events/?$', EventView.as_view()),
]
