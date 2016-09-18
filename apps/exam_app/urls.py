from django.conf.urls import url
from . import views
from views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^pokes$', views.pokes),
    url(r'^poke/(?P<id>\d+)$', views.pokeUser),
]
