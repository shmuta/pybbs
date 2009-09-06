from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(.*)', 'django.views.static.serve', {'document_root': 'media/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^pybbs/', include('pybbs.bbs.urls')),
    (r'^i18n/',  include('django.conf.urls.i18n')),
	(r'^accounts/', include('pybbs.registration.urls')),
)
