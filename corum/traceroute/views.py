# Create your views here.
import simplekml
from django.http import HttpResponse
from traceroute.models import TracerouteResult
from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required


class Format:
    KML = 'kml'
    GEOJSON = 'geojson'
    JSON = 'json'

def traceroute_serialise(request, traceroute_id, format):
    tr = TracerouteResult.objects.get(pk=traceroute_id)
    if format == Format.KML:
        kml = simplekml.Kml()
        kml.newlinestring(name="Traceroute", description="Traceroute",
                          coords=tr.line.coords)
        return HttpResponse(kml.kml())

    elif format == Format.GEOJSON:
        return HttpResponse(tr.line.geojson)

    elif format == Format.JSON:
        hops = []
        for hop in tr.hops:
            h = {}
            h['location'] = [hop.location.y, hop.location.x]
            h['rtt'] = hop.rtt
            h['ip_address'] = hop.ip_address
            h['hostname'] = hop.hostname
            h['hop_num'] = hop.hop_num
            hops.append(h)
        return HttpResponse(json.dumps(hops))

def traceroute_result(request, traceroute_id):
    tr = TracerouteResult.objects.get(pk=traceroute_id)
    return render(request, 'result.html', {'result': tr})
