#  from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import EventList
from django.conf.urls import url


urlpatterns = [
    url(r'^events/$', EventList.as_view()),
]

#  urlpatterns = format_suffix_patterns(urlpatterns)
