from django.contrib.gis.db import models
from core.models import User, Case, AbstractBase
from django.conf import settings
from traceroute import tasks
from django.contrib.gis.geos import LineString


class TracerouteCase(AbstractBase):
    case = models.ForeignKey(Case)
    host = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    locations = models.ManyToManyField('StartLocation')

    def start_traceroute(self):
        tasks.start_traceroute.delay(self)

    @property
    def results(self):
        return self.tracerouteresult_set.all()

    def __unicode__(self):
        return self.host


class TracerouteResult(AbstractBase):
    traceroute = models.ForeignKey(TracerouteCase)
    location = models.ForeignKey('StartLocation')

    @property
    def hops(self):
        return self.traceroutehop_set.all()

    @property
    def line(self):
        return LineString([hop.location for hop in self.hops])

    def __unicode__(self):
        return self.location.location


class TracerouteHop(AbstractBase):
    traceroute = models.ForeignKey(TracerouteResult)
    hostname = models.CharField(max_length=200)
    rtt = models.FloatField()
    hop_num = models.IntegerField()
    ip_address = models.IPAddressField()
    location = models.PointField()

    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.hop_num) + ": " + self.ip_address

    class Meta:
        ordering = ["hop_num"]


class StartLocation(AbstractBase):
    location = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    def __unicode__(self):
        return self.location

    class Meta:
        ordering = ["location"]
