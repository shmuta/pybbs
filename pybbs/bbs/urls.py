from django.conf.urls.defaults import *

urlpatterns = patterns('pybbs.bbs',
    (r'^$', 'views.index'),
    (r'^(?P<message_id>\d+)/$', 'views.detail'),
    (r'^(?P<message_id>\d+)/reply/$', 'views.reply'),
)
