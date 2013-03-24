from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^admin/', include(admin.site.urls)),)

for app in settings.INSTALLED_APPS:
    print app
    if app.startswith("django"):
        continue
    urlpatterns += patterns('', url(r'^%s/' % (app), include('%s.urls' % (app))),)
