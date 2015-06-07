from django.conf.urls import include, url, patterns
from django.contrib import admin
from .views import LeaderDetalles, BuscarLeaderTeacher, TipoReportes, CursoDetalles
from .views import BuscarCursos, ListarNota, MatricularLeaderTeacher, MasterDetalles, CohortesCursos
from .views import RegistrarCurso
from .views import BorrarCurso, UpdateDatosCurso, CohortesCursos, UpdateCohorte, ActividadesCohortes
from .views import DetallesCohorte, ActividadDetalles, ActividadFormulario, RegistrarDemograficos
from .views import AgregarHistoriaAcademico, AgregarHistoriaLaboral, AgregarSoporteLaboral

leader_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', LeaderDetalles.as_view(), name="detalles_leader"),
    url(r'^demograficos/(?P<id_persona>\d+)/$', RegistrarDemograficos.as_view(), name="demograficos_leader"), #Nuevo!
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
    url(r'^cohortes/', CohortesCursos.as_view(), name="cursos"),

)

curso_urls = patterns ('',
    url(r'^(?P<id_curso>\d+)/$', CursoDetalles.as_view(), name="detalles_curso"),
    url(r'^buscar$', BuscarCursos.as_view(), name="buscar_cursos"),
    url(r'^(?P<id_curso>\d+)/delete$', BorrarCurso.as_view(), name="borrar_curso"),
    url(r'^(?P<pk>\d+)/update$', UpdateDatosCurso.as_view(), name="update_curso"),
    url(r'^(?P<id_curso>\d+)/cohortes$', CohortesCursos.as_view(), name="cohortes_curso"),
    url(r'^(?P<id_curso>\d+)/(?P<id_cohorte>\d+)$', DetallesCohorte.as_view(), name="detalles_cohorte"),
    #url(r'^(?P<id_curso>\d+)/(?P<id_cohorte>\d+)/update$', UpdateCohorte.as_view(), name="update_cohorte"),
    url(r'^(?P<id_curso>\d+)/(?P<pk>\d+)/update$', UpdateCohorte.as_view(), name="update_cohorte"),
)

master_urls = patterns ('',
    url(r'^(?P<id_persona>\d+)/$', MasterDetalles.as_view(), name="detalles_master"),
    url(r'^(?P<id_persona>\d+)/cursos/$', CohortesCursos.as_view(), name="cursos"),
    url(r'^(?P<id_persona>\d+)/cursos/(?P<id_curso>\d+)/(?P<id_cohorte>\d+)/$', 
        DetallesCohorte.as_view(), name="detalles_cohorte"),
    url(r'^(?P<id_persona>\d+)/cursos/(?P<id_curso>\d+)/(?P<id_cohorte>\d+)/actividades$', 
        ActividadesCohortes.as_view(), name="actividades_cohorte"),
    url(r'^(?P<id_persona>\d+)/cursos/(?P<id_curso>\d+)/(?P<id_cohorte>\d+)/(?P<id_actividad>\d+)$', 
        ActividadDetalles.as_view(), name="detalles_actividad"),
    #url(r'^actividad/(?P<id_actividad>\d+)/$', ActividadDetalles.as_view(), name="detalles_actividad"), #Nuevo!
    url(r'^(?P<id_persona>\d+)/cursos/(?P<id_curso>\d+)/(?P<id_cohorte>\d+)/actividades/registrar$', 
        ActividadFormulario.as_view(), name="registrar_actividad"), #Nuevo!
    url(r'^demograficos/(?P<id_persona>\d+)/$', RegistrarDemograficos.as_view(), name="demograficos_master"), #Nuevo!
    #url(r'^buscar$', BuscarMaster.as_view(), name="master_cursos"),
)

nivel_escolar_urls = patterns ('',
    #url(r'^(?P<id_persona>\d+)/$', GuardarNivelEscolar.as_view(), name="guardar_nivel_escolar")

)

historial_prueba = patterns('',
    url(r'^(?P<id_persona>\d+)/laboral/$', AgregarHistoriaLaboral.as_view(), name="agregar_laboral"),
    url(r'^(?P<id_persona>\d+)/academico/$', AgregarHistoriaAcademico.as_view(), name="agregar_academico"),
    url(r'^(?P<id_persona>\d+)/soporte/$', AgregarSoporteLaboral.as_view(), name="agregar_soporte"),
)


urlpatterns = patterns ('',
	url(r'^leader/', include(leader_urls)),
    url(r'^master/', include(master_urls)),
	url(r'^secretaria/', include(secretaria_urls)),
	url(r'^admin/', include(admin_urls)),
	url(r'^curso/', include(curso_urls)),
    url(r'^nivel_escolar/', include(nivel_escolar_urls)),
    url(r'^historial/', include(historial_prueba))
)