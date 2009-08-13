from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^pybbs/$', 'pybbs.bbs.views.index'),
    #(r'^pybbs/(?P<message_id>\d+)/$', 'pybbs.bbs.views.detail'),
    #(r'^pybbs/(?P<message_id>\d+)/reply/$', 'pybbs.bbs.views.reply'),
    (r'^admin/', include(admin.site.urls)),
)