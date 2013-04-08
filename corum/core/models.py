from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from django.template import defaultfilters
from django.core.urlresolvers import reverse
from django.contrib.admin.util import NestedObjects
import uuid

class CustomManager(models.Manager):

    use_for_related_fields = True

    def visible(self):
        return self.filter(hidden=False)

    def hidden(self):
        return self.filter(hidden=True)


class AbstractBase(models.Model):

    id = models.CharField(max_length=36, primary_key=True, editable=False)
    hidden = models.BooleanField(editable=False, default=False)
    objects = CustomManager()
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        """
        Create object uuid on init if not already set.
        """
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

    def get_related_objects(self):
        collector = NestedObjects(using='default')
        collector.collect([self])
        return collector.nested()

    class Meta:
        abstract = True


class User(AbstractUser, AbstractBase):
    """
    Custom User class, overrides django's User model
    for additional attributes.
    """

    current_case = models.ForeignKey('Case', null=True)

    def __unicode__(self):
        return self.username


class Case(AbstractBase):
    """
    Acts as a top level container class for all cases.

    Every bit of forensic data will belong to a case. It is
    possible to list all types of ForeignKeys so it would be easy
    to implement features as apps.

    A case can relate to itself, thus a subcase is no different to a case.

    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, editable=False)
    description = models.TextField()
    date_raised = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent_case = models.ForeignKey('self', blank=True, null=True)

    @property
    def is_subcase(self):
        """
        Checks whether the case has a parent case, thus making it 
        a subcase. A subcase cannot parent another case.

        """
        if self.parent_case:
            return True
        else:
            return False

    def clean(self):
        """
        Ensures the parent case is not already a subcase 
        before saving.
        """

        if self.parent_case and self.parent_case.is_subcase:
            raise ValidationError('Parent case is already a subcase, cannot attach cases to subcases')

        if self == self.parent_case:
            raise ValidationError('Parent case can not be self')

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Case, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:case_detail', args=[str(self.slug)])

    def __unicode__(self):
        return self.name


class AbstractTarget(AbstractBase):
    """
    Base class for all targets. Both UserTarget and
    HostTarget extend this.
    """
    description = models.TextField()
    case = models.ForeignKey(Case)
    location = models.PointField(null=True)

    class Meta:
        abstract = True


class UserTarget(AbstractTarget):
    """
    UserTarget are human targets, apps such as Twitter
    and facebook can be run against them.
    """
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()

    def get_absolute_url(self):
        return reverse('core:usertarget_detail', args=[self.case.slug, str(self.id)])

    def __unicode__(self):
        return self.name


class HostTarget(AbstractTarget):
    """
    A host target represents a machine target, e.g a website.
    """
    host = models.CharField(max_length=240)

    def get_absolute_url(self):
        return reverse('core:hosttarget_detail', args=[self.case.slug, str(self.id)])

    def __unicode__(self):
        return self.host


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


class Tag(AbstractBase):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
