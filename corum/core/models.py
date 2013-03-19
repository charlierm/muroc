from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User class, overrides django's User model
    for additional attributes.
    """

    def __unicode__(self):
        return self.username
