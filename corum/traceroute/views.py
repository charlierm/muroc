# Create your views here.
import simplekml
from django.http import HttpResponse
from traceroute.models import TracerouteResult
from django.shortcuts import render

class Format:
    KML = 'kml'
    GEOJSON = 'json'


def traceroute_serialise(request, traceroute_id, format):
    tr = TracerouteResult.objects.get(pk=traceroute_id)
    if format == Format.KML:
        kml = simplekml.Kml()
        kml.newlinestring(name="Traceroute", description="Traceroute",
                          coords=tr.line.coords)
        return HttpResponse(kml.kml())

    elif format == Format.GEOJSON:
        print tr.line.geojson
        return HttpResponse(tr.line.geojson)


def traceroute_result(request, traceroute_id):
    return render(request, 'result.html')
