from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import uuid


class AbstractBase(models.Model):

    id = models.CharField(max_length=36, primary_key=True, editable=False)

    def __init__(self, *args, **kwargs):
        super(AbstractBase, self).__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

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
    date_raised = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

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
    location_object = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(ContentType)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return str(self.latitude) + ", " + str(self.longitude)
