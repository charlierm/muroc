from django.conf.urls import patterns, url

uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'


urlpatterns = patterns('',
    url(r'^result/(?P<traceroute_id>%s).(?P<format>.+)$' % (uuid), 'traceroute.views.traceroute_serialise'),
    url(r'^result/(?P<traceroute_id>%s)$' % (uuid), 'traceroute.views.traceroute_result'),
    )
