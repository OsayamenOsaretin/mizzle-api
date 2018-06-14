from django.db import models
#  from django.contrib.auth.models import User as UserModel

# Create your models here.


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    poster = models.CharField(max_length=500, blank=True, default='')
    description = models.TextField(max_length=3000, blank=True, default='')
    location = models.CharField(max_length=300, blank=True, default='')
    creator = models.ForeignKey('User',
                                related_name="creator",
                                on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class User(models.Model):
    alias = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField()
    location = models.CharField(max_length=300, blank=True, default='')
    events = models.ManyToManyField(
            'Event',
            related_name='attender'
            )


class Artiste(models.Model):
    bio = models.TextField(max_length=3000, blank=True, default='')
    record_label = models.CharField(max_length=100, blank=True, default='')
    events = models.ManyToManyField(
            'Event',
            related_name='performer'
            )
    user = models.OneToOneField(
            'User',
            on_delete=models.CASCADE,
            related_name='user'
            )
