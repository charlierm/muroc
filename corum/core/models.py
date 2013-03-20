from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class AbstractBase(models.Model):
    class Meta:
        abstract = True


class User(AbstractUser):
    """
    Custom User class, overrides django's User model
    for additional attributes.
    """

    def __unicode__(self):
        return self.username


class Case(AbstractBase):
    """
    Acts as a top level container class for all cases.

    Every bit of forensic data will belong to a case. It is
    possible to list all types of ForeignKeys so it would be easy
    to implement features as apps.

    """
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class Location(AbstractBase):
    """
    Although we could use GeoDjango to assist in storing spacial data,
    for now this class will do. It implements a GenericForeignKey so
    we can attach it to any object type.

    GenericForeignKey fields are set in exactly the same manner as normal
    ForeignKey fields.

    """
    location_object = generic.GenericForeignKey('content_type', 'id')
    content_type = models.ForeignKey(ContentType)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return str(self.latitude) + ", " + str(self.longitude)
