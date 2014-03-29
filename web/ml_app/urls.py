

from django.conf.urls import patterns, url

from ml_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)/$', views.user_page, name='user_page')
)
