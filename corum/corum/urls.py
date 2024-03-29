from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'corum.views.home', name='home'),
    # url(r'^corum/', include('corum.foo.urls')),
    url(r'^', include('core.urls', namespace='core')),
    url(r'^traceroute/', include('traceroute.urls')),
    url(r'^login/$', 'core.views.custom_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)