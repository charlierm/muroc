from celery import task
from django.contrib.gis.geos import *


@task()
def start_traceroute(traceroute_case):
    from models import TracerouteHop, TracerouteResult
    from traceroute.troute import Traceroute

    # TODO: Locations should be run in a seperate thread to reduce waiting
    # times.
    for location in traceroute_case.locations.all():
        t = Traceroute(ip_address=traceroute_case.host,
                       country=location.code)
        hops = t.traceroute()

        r = TracerouteResult(location=location,
                             traceroute=traceroute_case)
        r.save()

        for hop in hops:
            print hop
            h = TracerouteHop(traceroute=r)
            h.hostname = hop['hostname']
            h.hop_num = hop['hop_num']
            h.rtt = float(hop['rtt'].replace(" ms", ""))
            h.location = Point(hop['longitude'], hop['latitude'])
            h.ip_address = hop['ip_address']
            h.save()
