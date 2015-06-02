from django.conf.urls import include, url, patterns
from django.contrib import admin
from .views import LeaderDetalles, BuscarLeaderTeacher, TipoReportes, CursoDetalles, BuscarCursos, ListarNota, MatricularLeaderTeacher, MasterDetalles, MasterCursos

leader_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', LeaderDetalles.as_view(), name="detalles_leader"),
)

secretaria_urls = patterns ('',
    #url(r'^(?P<id_secretaria>\d+)/$', SecretariaDetalles.as_view(), name="detalles_secretaria"),
    url(r'^docentes-inscritos$', BuscarLeaderTeacher.as_view(), name="ver_docentes_inscritos"),
    url(r'^(?P<id_persona>\d+)_(?P<id_curso>\d+)/$', MatricularLeaderTeacher.as_view(), name="matricular_docente"),
)

admin_urls = patterns ('',
    url(r'^reportes$', TipoReportes.as_view(), name="admin_reportes"),
)

curso_urls = patterns ('',
    url(r'^(?P<id_curso>\d+)/$', CursoDetalles.as_view(), name="detalles_curso"),
    url(r'^buscar$', BuscarCursos.as_view(), name="buscar_cursos"),
)

master_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', MasterDetalles.as_view(), name="detalles_master"),
    url(r'^(?P<id_persona>\d+)/cursos$', MasterCursos.as_view(), name="cursos"),
    #url(r'^buscar$', BuscarMaster.as_view(), name="master_cursos"),
)


urlpatterns = patterns ('',
	url(r'^leader/', include(leader_urls)),
    url(r'^master/', include(master_urls)),
	url(r'^secretaria/', include(secretaria_urls)),
	url(r'^admin/', include(admin_urls)),
	url(r'^curso/', include(curso_urls)),
)