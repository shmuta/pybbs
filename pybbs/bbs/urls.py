from django.conf.urls.defaults import *
    
urlpatterns = patterns('pybbs.bbs',
    (r'^$', 'views.index'),
    (r'^create/$', 'views.create'),
    (r'^create_theme/$', 'views.create_theme'),
    (r'^rss.xml$','views.rss'),
    (r'^(?P<message_id>\d+)/$', 'views.detail'),
    (r'^(?P<message_id>\d+)/reply/$', 'views.reply'),
)

