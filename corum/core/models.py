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

    @property
    def view_count(self):
        """
        Returns an integer of how many views the current object has.
        """
        model_type = ContentType.objects.get_for_model(self)
        count = ViewLog.objects.filter(content_type__pk=model_type.id,
                                       object_id=self.id).count()
        return count

    class Meta:
        abstract = True


class User(AbstractUser, AbstractBase):
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


class ViewLog(AbstractBase):
    """
    Used for keeping track of view counts of objects. Uses a generic relation
    to be used with any model type. This should be implemented in other apps views.
    """
    logged_object = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=36)
    content_type = models.ForeignKey(ContentType)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def log(cls, model_instance, user):
        """
        classmethod for creating a new view log for the current supplied instance.

        @param model_instance The instance of the object to log.
        @param User The User that viewed the object.
        @return ViewLog returns the newly created ViewLog instance.
        """
        view = cls()
        view.logged_object = model_instance
        view.user = user
        view.save()
        return view
