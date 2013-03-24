from django.conf.urls import patterns, url

uuid = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'


urlpatterns = patterns('',
    #url(r'^$', 'twitter.views.home')
    url(r'^case/(?P<twitter_case_id>%s)/$' % (uuid), 'twitter.views.case'),
    )
