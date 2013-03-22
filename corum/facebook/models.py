from django.db import models
from core.models import AbstractBase, Case
from django.conf import settings
import facebook
import os
# Create your models here.


class Account(AbstractBase):
    case = models.ForeignKey(Case)
    username = models.CharField(max_length=50)
    date_raised = models.DateTimeField(auto_now_add=True)

    def fetch(self):
        pass

    def get_url(self):
        pass


class Message(AbstractBase):
    account = models.ForeignKey(Account)
    to = models.CharField(max_length=50)
    content = models.TextField()


class Friend(AbstractBase):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=lambda: upload_to())

    def upload_to(instance, filename):
        return os.path.join(settings.MEDIA_ROOT + instance.id + instance.file_extension)


