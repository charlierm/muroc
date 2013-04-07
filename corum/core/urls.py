from django.conf.urls import patterns, url
from core.views import CaseListView, DefaultCaseView


uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('',
                       url(r'^cases/$', CaseListView.as_view()),
                       url(r'^cases/(?P<case_name>.{0,100})/default/$', DefaultCaseView.as_view())
                       )
