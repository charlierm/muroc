from django.db import models
from django.contrib.auth.models import AbstractUser

class AbstractBase(models.Model):

    class Meta():
        abstract=True


class User(AbstractUser):
    """
    Custom User class, overrides django's User model
    for additional attributes.
    """

    def __unicode__(self):
        return self.username



class Case(AbstractBase):
    case_title = models.CharField(max_length=255)   