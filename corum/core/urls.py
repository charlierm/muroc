from django.conf.urls import patterns, url
from core.views import *


uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('',
                       url(r'^cases/$', CaseListView.as_view()),
                       url(r'^cases/(?P<slug>.{0,100})/$', CaseDetailView.as_view(), name='case_detail'),
                       url(r'^cases/(?P<case_name>.{0,100})/default/$', DefaultCaseView.as_view()),
                       url(r'^cases/create/$', CreateCaseView.as_view()),
                       )
