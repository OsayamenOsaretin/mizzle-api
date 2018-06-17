import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class AccountManager(BaseUserManager):
    """
    custom Manager class required for django custom user
    """

    def create_user(self, username, email, password):
        """
        create normal user, validating the existence of username, email
        and password
        """
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have a email.')
        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        create superuser but making is_superuser and is_staff fields
        True
        """
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Event(models.Model):
    """
    Model for events created by users, artistes
    """
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


class User(AbstractBaseUser, PermissionsMixin):

    """
    Custom User class for authorization with tokens
    """

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tell DJANGO the usermanager class that should manage this type
    objects = AccountManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        """
        accessed as profile.token because of the property decorator
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        expiry_date = datetime.now() + timedelta(days=3)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(expiry_date.strftime('%s')),
            'username': self.username,
            'email': self.email,
            }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Artiste(models.Model):

    """
    Artistes are tied to Users, but have extra information
    peculiar to Artistes
    """

    bio = models.TextField(max_length=3000, blank=True, default='')
    record_label = models.CharField(max_length=100, blank=True, default='')
    events = models.ManyToManyField(
        'Event',
        related_name='performer'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
