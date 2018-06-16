from django.conf.urls import patterns, url

from leiabox_web_ui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^setProgram$', views.setProgram, name='setProgram'),
    url(r'^setVolume$', views.setVolume, name='setVolume'),
    url(r'^buttonDown$', views.buttonDown, name='buttonDown'),
    url(r'^buttonUp$', views.buttonUp, name='buttonUp'),
    url(r'^getStatus$', views.getStatus, name='getStatus'),
)
