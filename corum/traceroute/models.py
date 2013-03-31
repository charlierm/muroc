from django.db import models
from core.models import User, Case, AbstractBase, Location
from django.conf import settings
import tasks


class TracerouteCase(AbstractBase):
    case = models.ForeignKey(Case)
    host = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    #TODO: The locations that are being searched does not need to be stored in the db,
    # a better approach would be jsut to pass the start_traceroute() method a list of locations to run.
    #
    locations = models.ManyToManyField('StartLocation')

    def start_traceroute(self):
        #TODO: This needs to be checking the location traceroute doesnt already exist, or something along those lines!
        tasks.start_traceroute.delay(self)

    @property
    def results(self):
        return self.tracerouteresult_set.all()


class TracerouteResult(AbstractBase):
    traceroute = models.ForeignKey(TracerouteCase)
    location = models.ForeignKey('StartLocation')

    @property
    def hops(self):
        return self.traceroutehop_set.all()


class TracerouteHop(AbstractBase):
    traceroute = models.ForeignKey(TracerouteResult)
    hostname = models.CharField(max_length=200)
    rtt = models.FloatField()
    hop_num = models.IntegerField()
    ip_address = models.IPAddressField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ["hop_num"]


class StartLocation(AbstractBase):
    location = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __unicode__(self):
        return self.location

    class Meta:
        ordering = ["location"]
