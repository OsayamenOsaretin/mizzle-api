from django.conf.urls import url
from .views import RegistrationView, LoginView


urlpatterns = [
    url(r'^users/?$', RegistrationView.as_view()),
    url(r'^users/login/?$', LoginView.as_view()),
]
