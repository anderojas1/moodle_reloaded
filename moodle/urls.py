from django.conf.urls import include, url, patterns
from django.contrib import admin
from .views import LeaderDetalles, BuscarLeaderTeacher, TipoReportes, CursoDetalles, BuscarCursos, ListarNota, MatricularLeaderTeacher, MasterDetalles, MasterCursos
from .views import MasterCohorte, ActividadDetalles, ActividadFormulario
from .views import RegistrarCurso
from .views import MasterCohorte, ActividadDetalles, ActividadFormulario, GuardarNivelEscolar
from .views import BorrarCurso


leader_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', LeaderDetalles.as_view(), name="detalles_leader"),
)

secretaria_urls = patterns ('',
    #url(r'^(?P<id_secretaria>\d+)/$', SecretariaDetalles.as_view(), name="detalles_secretaria"),
    url(r'^docentes-inscritos$', BuscarLeaderTeacher.as_view(), name="ver_docentes_inscritos"),
    url(r'^(?P<id_persona>\d+)_(?P<id_curso>\d+)/$', MatricularLeaderTeacher.as_view(), name="matricular_docente"),
)

registrar_urls = patterns ('',
    url(r'^curso/$', RegistrarCurso.as_view(), name="registrar_curso"),
)

admin_urls = patterns ('',
    url(r'^reportes$', TipoReportes.as_view(), name="admin_reportes"),
    url(r'^registro/', include(registrar_urls)),
)

curso_urls = patterns ('',
    url(r'^(?P<id_curso>\d+)/$', CursoDetalles.as_view(), name="detalles_curso"),
    url(r'^buscar$', BuscarCursos.as_view(), name="buscar_cursos"),
    url(r'^(?P<id_curso>\d+)/delete$', BorrarCurso.as_view(), name="borrar_curso"),
)

master_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', MasterDetalles.as_view(), name="detalles_master"),
    url(r'^(?P<id_persona>\d+)/cursos/$', MasterCursos.as_view(), name="cursos"),
    url(r'^(?P<id_persona>\d+)/cursos/(?P<id_cohorte>\d+)/$', MasterCohorte.as_view(), name="detalles_cohorte"),
    url(r'^actividad/(?P<id_actividad>\d+)/$', ActividadDetalles.as_view(), name="detalles_actividad"), #Nuevo!
    url(r'^registrar_actividad$', ActividadFormulario.as_view(), name="registrar_actividad") #Nuevo!
    #url(r'^buscar$', BuscarMaster.as_view(), name="master_cursos"),
)

nivel_escolar_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', GuardarNivelEscolar.as_view(), name="guardar_nivel_escolar")

)


urlpatterns = patterns ('',
	url(r'^leader/', include(leader_urls)),
    url(r'^master/', include(master_urls)),
	url(r'^secretaria/', include(secretaria_urls)),
	url(r'^admin/', include(admin_urls)),
	url(r'^curso/', include(curso_urls)),
    url(r'^nivel_escolar/', include(nivel_escolar_urls))
)