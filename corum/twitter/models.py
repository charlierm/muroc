from django.db import models
from core.models import AbstractBase, Case
from django.conf import settings


class Account(AbstractBase):
    case = models.ForeignKey(Case)
    username = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    date_raised = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)


class Tweet(AbstractBase):
    date = models.DateField()
    text = models.CharField(max_length=140)

    def __unicode__(self):
        return self.text[0:20]


class TwitterUser(AbstractBase):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    picture = models.ImageField()
    followers = models.IntegerField()
    following = models.IntegerField()
    statuses = models.IntegerField()

    def __unicode__(self):
        return self.username

