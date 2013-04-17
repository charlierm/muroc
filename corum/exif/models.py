from django.contrib.gis.db import models
from core.models import User, Case, AbstractBase
import tasks
# Create your models here.


class ExifData(AbstractBase):
    case = models.ForeignKey(Case)
    image = models.ImageField(upload_to='exif')
    created_by = models.ForeignKey(User)
    location = models.PointField(null=True, blank=True)

    #TODO: When changes are made to the image it needs to update the exif!
    #   or make the exif write once.

    def get_exif(self):
        tasks.get_exif(self)

    def remove_exif(self):
        self.exiftag_set.all().delete()

    @property
    def tags(self):
        return self.exiftag_set.all()

    def __unicode__(self):
        return self.image.name


class ExifTag(AbstractBase):
    image = models.ForeignKey(ExifData)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

    def __unicode__(self):
        return "ExifTag: %s" % (self.key)
