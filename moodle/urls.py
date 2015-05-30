from django.conf.urls import include, url, patterns
from django.contrib import admin
from .views import LeaderDetalles

leader_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', LeaderDetalles.as_view(), name="detalles_leader"),
)


urlpatterns = patterns ('',
	url(r'^leader/', include(leader_urls)),
)