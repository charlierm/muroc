from django.conf.urls import patterns, url
from core.views import *


uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('',
                       url(r'^$', CaseListView.as_view()),
                       url(r'^cases/create/$', CreateCaseView.as_view()),
                       url(r'^cases/(?P<slug>[a-z0-9-]{0,100})/$', CaseDetailView.as_view(), name='case_detail'),
                       url(r'^cases/(?P<slug>[a-z0-9-]{0,100})/user/(?P<pk>%s)$'%uuid, UserTargetDetailView.as_view(), name='usertarget_detail'),
                       url(r'^cases/(?P<slug>[a-z0-9-]{0,100})/host/(?P<pk>%s)$'%uuid, HostTargetDetailView.as_view(), name='hosttarget_detail'),
                       url(r'^cases/(?P<case_name>[a-z0-9-]{0,100})/default/$', DefaultCaseView.as_view()),
                       url(r'^cases/(?P<slug>[a-z0-9-]{0,100})/locations.json$', CaseLocationsView.as_view()),
                       )
