

from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from ml_app import views

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template':'home.html'}),
    url(r'^(?P<user_id>\d+)/$', views.user_info),
    url(r'^song/(?P<song_id>\d+)/$', views.song_info),
    url(r'^new/(?P<user_id>\d+)', views.users_json),
)
