from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import LeaderTeacher, Persona, InstitucionEducativa, Curso, Area, Matricula, MasterTeacher, Cohorte
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from .funciones import VerificaUsuario, BuscarDocentes, MatricularLeaderTeacherCohorte, CohorteMasterTeacher
from .forms import Buscar, NotasPorEstudiante, EstudiantesCurso, EstudiantesDepartamentoCurso, DatosDemograficosForm
from .reportes import BuscarReportes
from .funciones import CalculaNotaLeader
from .models import Actividad, Curso, RegistroNotas, ActividadesCohorte
from .forms import ActividadForm, CursoForm, CohorteForm
from .models import Actividad, Curso, DatosDemograficos
from .forms import ActividadForm, CursoForm
from .models import Actividad, Curso, HistorialAcademico, HistorialLaboral
from .forms import ActividadForm, CursoForm, HistorialAcademicoForm, HistorialLaboralForm
from .models import Actividad
from .forms import ActividadForm, RegistroNotasForm
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

# Create your views here.

class LeaderDetalles(TemplateView):
	template_name = 'moodle/detalles_leader.html'
	persona = None
	leader = None
	usuario = None
	institucion = None

	def get_context_data(self, **kwargs):
		context = super(LeaderDetalles, self).get_context_data(**kwargs)
		usuario_actual = self.request.user

		self.persona = Persona.objects.get(pk=self.kwargs['id_persona'])
		if 'persona' not in context:
			context['persona'] = self.persona

		self.leader = LeaderTeacher.objects.get(id=self.kwargs['id_persona'])
		if 'leader' not in context:
			context['leader'] = self.leader

		self.usuario = User.objects.get(id=self.persona.usuario_id)
		if 'usuario' not in context:
			context['usuario'] = self.usuario

		self.institucion = InstitucionEducativa.objects.get(nombre=self.leader.institucion)
		if 'institucion' not in context:
			context['institucion'] = self.institucion

		if self.usuario.id == usuario_actual.id:
			context['editar'] = 'editable'

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario_actual)

		context[grupo] = grupo
		return context

class BuscarLeaderTeacher(TemplateView):
	template_name = 'moodle/buscar_docentes.html'
	docentes = None
	secretaria = None

	def get_context_data(self, **kwargs):
		context = super(BuscarLeaderTeacher, self).get_context_data(**kwargs)
		usuario_actual = self.request.user

		buscar_secretaria = VerificaUsuario()
		self.secretaria = buscar_secretaria.buscarSecretaria(usuario_actual)

		buscar_docentes = BuscarDocentes()
		matriculas = buscar_docentes.buscarDocentesInscritos(self.secretaria)
		curso_docente = [[0 for x in range(2)] for x in range(len(matriculas))]
		for i, matricula in enumerate (matriculas):
			docente = LeaderTeacher.objects.get(id = matricula.get().identificacion_leader_teacher_id)
			curso = Curso.objects.get(id = matricula.get().identificacion_curso_id)
			curso_docente[i][0] = docente
			curso_docente[i][1] = curso
			#docentes.append(docente)
			#cursos.append(curso
		context['secretaria'] = self.secretaria
		context['curso_docentes'] = curso_docente

		return context

class CursoDetalles(TemplateView):
	template_name = 'moodle/detalles_curso.html'
	curso = None
	usuario_actual = None
	ver_grupo = VerificaUsuario()

	def get_context_data(self, **kwargs):
		context = super(CursoDetalles, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user
		grupo = self.ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		self.curso = Curso.objects.get(id=context['id_curso'])
		context['curso'] = self.curso

		area = Area.objects.get(id=self.curso.area_id)
		context['area'] = area

		return context

	def post(self, request, *args, **kwargs):
		context = super(CursoDetalles, self).get_context_data(**kwargs)
		self.curso = Curso.objects.get(id=context['id_curso'])
		context['curso'] = self.curso

		self.usuario_actual = self.request.user
		grupo = self.ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo
		area = Area.objects.get(id=self.curso.area_id)
		context['area'] = area

		if grupo == 'leader':			
			
			leader = self.ver_grupo.buscarLeaderTeacher(self.request.user)
			try:
				verificar = Matricula.objects.get(identificacion_leader_teacher=leader.id, 
					identificacion_curso=self.curso.id)
				context['exito'] = 'Usted ya se inscribió a este curso'
			except ObjectDoesNotExist:
				matricula = Matricula(identificacion_leader_teacher=leader, identificacion_curso=self.curso,
					estado_matricula=2)
				matricula.save()
				context['exito'] = 'Se ha realizado la inscripción exitosamente'
				return render(request, self.template_name, context)

		elif grupo == 'admin':
			return redirect('/campus/curso/' + kwargs['id_curso'] + '/cohortes')


class BuscarCursos(TemplateView):
	template_name = 'moodle/buscar_cursos.html'
	cursos = []
	usuario_actual = None

	def get_context_data(self, **kwargs):
		context = super(BuscarCursos, self).get_context_data(**kwargs)

		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		self.cursos = Curso.objects.all().exclude(estado=False)
		context['cursos'] = self.cursos

		return context

	def post(self, request, *args, **kwargs):
		context = super(BuscarCursos, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo
		print("entró a crear curso")
		return redirect('/campus/admin/registro/curso')

class ListarNota(TemplateView):
	template_name = 'app/listar_nota.html'
	notas = None
	criterioBusqueda = ''

	def get_context_data(self, **kwargs):
		context = super(ListarNota, self).get_context_data(**kwargs)
		self.criterioBusqueda = self.kwargs.get('busqueda', '')
		print (iri_to_uri(urlquote(self.criterioBusqueda)))
		reporte = Ternaria.objects.filter(leader_teacher__cedula = str(self.criterioBusqueda)).values('nota', 'actividad__titulo')
		self.notas = reporte
		if 'notas' not in context:
			context['notas'] = self.notas
		if 'criterioBusqueda' not in context:
			context['criterioBusqueda'] = self.criterioBusqueda

		return context

	def post(self, request, *args, **kwargs):
		busqueda = None
		try:
			busqueda = request.POST.get('search', None)
		except KeyError:
			busqueda = None

		if busqueda is not None:
			return HttpResponseRedirect('ternaria/buscar/' + iri_to_uri(urlquote(busqueda)))

		return HttpResponseRedirect('ternaria')

class MatricularLeaderTeacher(TemplateView):
	template_name = 'moodle/matricular_leader.html'

	def get_context_data(self, **kwargs):
		context = super(MatricularLeaderTeacher, self).get_context_data(**kwargs)
		print(kwargs)
		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		curso = Curso.objects.get(id=kwargs['id_curso'])
		context['curso'] = curso

		leader = LeaderTeacher.objects.get(id=kwargs['id_persona'])
		context['profesor'] = leader
		persona = Persona.objects.get(id=kwargs['id_persona'])
		usuario = User.objects.get(id=persona.usuario_id)
		context['nombre'] = usuario

		matricularLeader = MatricularLeaderTeacherCohorte()
		matricularLeader.matricular(leader, curso)
		return context

class TipoReportes(TemplateView):

	template_name = 'moodle/reportes.html'

	def get_context_data(self, **kwargs):
		context = super(TipoReportes, self).get_context_data(**kwargs)
		departamentoForm = Buscar()
		context['departamento'] = departamentoForm
		"""cursoForm = CursosMayorAsistentes()
		context['cursos_mas'] = cursoForm"""
		notasForm = NotasPorEstudiante()
		context['notas_estudiante'] = notasForm

		cursoGanadoForm = EstudiantesCurso()
		context['estudiantes_curso'] = cursoGanadoForm

		estudiantesDptoCurso = EstudiantesDepartamentoCurso()
		context['estud_dpto_curso'] = estudiantesDptoCurso

		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		return context

	def post(self, request,*args,**kwargs):
		context = super(TipoReportes, self).get_context_data(**kwargs)
		########## De departamentos ############

		#departamentoForm = Buscar(request.POST)
		"""if departamentoForm.is_valid():			
			criterio = departamentoForm.cleaned_data.get('departamento')
			busqueda = BuscarReportes()
			resultado = busqueda.reportes(criterio, 0)
			print(resultado)
			context['res_leader'] = resultado"""

		########### De notas por estudiante ############

		"""notasForm = NotasPorEstudiante(request.POST)
		if notasForm.is_valid:
			criterio = notasForm.cleaned_data.get('cedula')
			busqueda = BuscarReportes()
			resultado = busqueda.reportes(criterio, 2)
			context['notas'] = resultado"""

		########### DE ESTUDIANTES QUE HAN APROBADO UN CURSO ################

		cursoGanadoForm = EstudiantesCurso(request.POST)
		if cursoGanadoForm.is_valid():
			criterio = cursoGanadoForm.cleaned_data.get('curso')
			busqueda = BuscarReportes()
			resultado = busqueda.reportes(criterio, 3)
			context['aprobados'] = resultado
			print (resultado)

		############ DE ESTUDIANTES DE UN CURSO POR DEPARTAMENTO ################
		"""estudiantesDptoCurso = EstudiantesDepartamentoCurso(request.POST)
		if estudiantesDptoCurso.is_valid():
			criterio1 = estudiantesDptoCurso.cleaned_data.get('curso')
			criterio2 = estudiantesDptoCurso.cleaned_data.get('departamento')
			busqueda = BuscarReportes()
			resultado = busqueda.reportes2(criterio1, criterio2)
			context['estu_dpto_curso'] = resultado"""

		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo
		return render(request, self.template_name, context)

class MasterDetalles(TemplateView):
	template_name = 'moodle/detalles_master.html'
	persona = None
	master = None
	usuario = None

	def get_context_data(self, **kwargs):
		context = super(MasterDetalles, self).get_context_data(**kwargs)
		usuario_actual = self.request.user

		self.persona = Persona.objects.get(pk=self.kwargs['id_persona'])
		if 'persona' not in context:
			context['persona'] = self.persona

		self.master = MasterTeacher.objects.get(id=self.kwargs['id_persona'])
		if 'master' not in context:
			context['master'] = self.master

		self.usuario = User.objects.get(id=self.persona.usuario_id)
		if 'usuario' not in context:
			context['usuario'] = self.usuario

		if self.usuario.id == usuario_actual.id:
			context['editar'] = 'editable'

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario_actual)

		context[grupo] = grupo
		return context

class CohortesCursos(TemplateView):
	template_name = 'moodle/cohortes.html'
	cohortes = None
	usuario = None

	def get_context_data(self, **kwargs):
		context = super(CohortesCursos, self).get_context_data(**kwargs)
		self.usuario = self.request.user

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario)

		context[grupo] = grupo

		if grupo == 'master':
			persona = Persona.objects.get(id=kwargs['id_persona'])#if master
			master = MasterTeacher.objects.get(id=persona.id)#if master
			context['master'] = master#if master

			buscar_cohortes = CohorteMasterTeacher()#if master
			self.cohortes = buscar_cohortes.buscar(master)#if master
			context['persona'] = persona#if master

		elif grupo == 'admin':
			self.cohortes = Cohorte.objects.filter(curso=kwargs['id_curso'])
			print(self.cohortes)

		context['cohortes'] = self.cohortes
		context['usuario'] = self.usuario

		cursos_cohortes = [[0 for x in range(2)] for x in range(len(self.cohortes))]

		for i, cohorte in enumerate (self.cohortes):
			curso = Curso.objects.get(id=cohorte.curso_id)
			cursos_cohortes[i][0] = cohorte
			cursos_cohortes[i][1] = curso
		context['cursos_cohortes'] = cursos_cohortes
		print(cursos_cohortes)

		return context

class DetallesCohorte(TemplateView):

	template_name = 'moodle/detalles_cohorte.html'

	def get_context_data(self, **kwargs):
		context = super(DetallesCohorte, self).get_context_data(**kwargs)
		usuario = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario)
		print(kwargs)
		curso = Curso.objects.get(id=kwargs['id_curso'])
		context['curso'] = curso
		cohorte = Cohorte.objects.get(id=kwargs['id_cohorte'])
		context['cohorte'] = cohorte

		context[grupo] = grupo		
		if grupo == 'master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona
			

		return context

	def post(self, request, *args, **kwargs):
		return redirect('/campus/curso/' + kwargs['id_curso'] + '/' + kwargs['id_cohorte'] + '/update')

class UpdateCohorte(UpdateView):
	model = Cohorte
	fields = ['semestre', 'fecha_inicio', 'fecha_fin', 'master']
	template_name_suffix = '_update_form'

	
	def get_context_data(self, **kwargs):
		context = super(UpdateCohorte, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post (self, request, *args, ** kwargs):
		form = CohorteForm(request.POST)
		if form.is_valid():
			semestre = form.cleaned_data.get('semestre')
			fecha_inicio = form.cleaned_data.get('fecha_inicio')
			fecha_fin = form.cleaned_data.get('fecha_fin')
			master = form.cleaned_data.get('master')

			cohorte = Cohorte.objects.get(id=kwargs['pk']) #<-->
			cohorte.semestre = semestre
			cohorte.fecha_inicio = fecha_inicio
			cohorte.fecha_fin = fecha_fin
			cohorte.master = master
			cohorte.save(update_fields=['semestre', 'fecha_inicio', 'fecha_fin', 'master'])
		return redirect('/campus/curso/' + kwargs['id_curso'] + '/' + kwargs['pk'])
"""class UpdateCohorte(TemplateView):
	template_name = 'moodle/cohorte_update_form.html'

	def get_context_data(self, **kwargs):
		context = super(UpdateCohorte, self).get_context_data(**kwargs)
		form = CohorteForm()
		cohorte = Cohorte.objects.get(id=kwargs['id_cohorte'])
		context['cohorte'] = cohorte
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo
		context['form'] = form

		return context

	def post (self, request, *args, ** kwargs):		
		context = super(UpdateCohorte, self).get_context_data(**kwargs)
		form = CohorteForm(request.POST, empty_permitted=True)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo
		print(kwargs)

		if form.is_valid():
			semestre = form.cleaned_data.get('semestre')
			fecha_inicio = form.cleaned_data.get('fecha_inicio')
			fecha_fin = form.cleaned_data.get('fecha_fin')
			master = form.cleaned_data.get('master')

			cohorte = Cohorte.objects.get(id=kwargs['id_cohorte'])
			cohorte.semestre = semestre
			cohorte.fecha_inicio = fecha_inicio
			cohorte.fecha_fin = fecha_fin
			cohorte.master = master
			cohorte.save(update_fields=['semestre', 'fecha_inicio', 'fecha_fin', 'master'])

		return redirect('/campus/curso/' + kwargs['id_curso'] + '/' + kwargs['id_cohorte'])"""

class ActividadesCohortes(TemplateView):
	template_name = 'moodle/actividades_cohorte.html'

	def get_context_data(self, **kwargs):
		context = super(ActividadesCohortes, self).get_context_data(**kwargs)
		cohorte = Cohorte.objects.get(id=kwargs['id_cohorte'])
		curso = Curso.objects.get(id=kwargs['id_curso'])
		context['curso'] = curso
		usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario_actual)
		context[grupo] = grupo

		if grupo=='master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona

		actividades = Actividad.objects.filter(id__in=(ActividadesCohorte.objects.filter(cohorte=cohorte.id)))
		
		if len(actividades) > 0:
			context['actividades'] = actividades
			print (actividades)

		return context

class ActividadDetalles(TemplateView):
	template_name = 'moodle/detalles_actividad.html'
	actividad = None
	usuario_actual = None

	def get_context_data(self, **kwargs):
		context = super(ActividadDetalles, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user

		self.actividad = Actividad.objects.get(id=self.kwargs['id_actividad'])
		if 'actividad' not in context:
			context['actividad'] = self.actividad

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		if grupo=='master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona
		return context

class ActividadFormulario(TemplateView):
	template_name = 'moodle/formulario_actividad.html'
	actividadForm = ActividadForm(prefix='actividad')

	def get_context_data(self, **kwargs):
		context = super(ActividadFormulario, self).get_context_data(**kwargs)
		if 'actividadForm' not in context:
			context['actividadForm'] = self.actividadForm

		usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario_actual)
		context[grupo] = grupo

		if grupo == 'master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			context['persona'] = persona
		return context

	def post(self, request,*args,**kwargs):
		actividadForm = ActividadForm(request.POST, prefix='actividad')
		if actividadForm.is_valid():
			titulo = actividadForm.cleaned_data.get('titulo')
			descripcion = actividadForm.cleaned_data.get('descripcion')
			fecha_inicio = actividadForm.cleaned_data.get('fecha_inicio')
			fecha_fin = actividadForm.cleaned_data.get('fecha_fin')
			porcentaje = actividadForm.cleaned_data.get('porcentaje')
			actividad = Actividad(descripcion=descripcion, titulo=titulo, fecha_fin=fecha_fin,
				fecha_inicio=fecha_inicio, porcentaje=porcentaje)
			actividad.save()
			cohorte = Cohorte.objects.get(id=kwargs['id_cohorte'])
			cohorte_actividad = ActividadesCohorte(cohorte=cohorte, actividad=actividad)
			cohorte_actividad.save()

		return redirect('/campus/master/' + kwargs['id_persona'] + '/cursos/' + kwargs['id_curso'] + '/' +
			kwargs['id_cohorte'] + '/actividades')


##################### CLASE REGISTRAR CURSO #########################################


class RegistrarCurso(TemplateView):
	template_name = 'moodle/registro/reg_curso.html'
	curso_form = CursoForm()

	def get_context_data(self, **kwargs):
		context = super(RegistrarCurso, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.curso_form

		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarCurso, self).get_context_data(**kwargs)
		curso_form = CursoForm(request.POST)
		print("guardando...")

		if curso_form.is_valid():
			id_curso = curso_form.cleaned_data.get('id')
			print(id_curso)
			curso_form.save()
			context['exito'] = 'OK'
			context['curso'] = Curso.objects.get(id=id_curso)

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return render(request, self.template_name, context)

class BorrarCurso(TemplateView):
	template_name = 'moodle/curso_confirm_delete.html'

	def get_context_data(self, **kwargs):
		context = super(BorrarCurso, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo
		curso = Curso.objects.get(id=kwargs['id_curso'])
		context['curso'] = curso

		return context

	def post(self, request, *args, **kwargs):
		context = super(BorrarCurso, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo
		curso = Curso.objects.get(id=kwargs['id_curso'])
		curso.estado = False
		curso.save(update_fields=['estado'])
		return redirect('/campus/curso/buscar')


class UpdateDatosCurso(UpdateView):
	model = Curso
	fields = ['nombre', 'descripcion', 'area']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(UpdateDatosCurso, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return context

class RegistrarNotas(TemplateView):
	template_name = 'moodle/registro_notas.html'
	notas_form = RegistroNotasForm()

	def get_context_data(self, **kwargs):
		context = super(RegistrarNotas, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.notas_form

		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarNotas, self).get_context_data(**kwargs)
		notas_form = RegistroNotasForm(request.POST)

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		persona = Persona.objects.get(id= kwargs['id_persona'])

		if notas_form.is_valid():
			actividad = notas_form.cleaned_data.get('actividad')
			cohorte = notas_form.cleaned_data.get('cohorte')
			leader_teacher = notas_form.cleaned_data.get('leader_teacher')
			nota = notas_form.cleaned_data.get('nota')

			regNota = RegistroNotas(actividad = actividad, cohorte = cohorte, leader_teacher = leader_teacher, nota = nota)
			regNota.save()

			return redirect('/campus/master/' + kwargs['id_persona'])


class RegistrarDemograficos(TemplateView):
	template_name = 'moodle/registro_demograficos.html'
	demograficos_form = DatosDemograficosForm()

	def get_context_data(self, **kwargs):
		context = super(RegistrarDemograficos, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.demograficos_form

		return context

	def post(self, request, *args, **kwargs):
		context = super(RegistrarDemograficos, self).get_context_data(**kwargs)
		demograficos_form = DatosDemograficosForm(request.POST)

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		persona = Persona.objects.get(id= kwargs['id_persona'])

		if demograficos_form.is_valid():
			idForm = demograficos_form.cleaned_data.get('id')
			estratoForm = demograficos_form.cleaned_data.get('estrato')
			tipo_viviendaForm = demograficos_form.cleaned_data.get('tipo_vivienda')
			caracter_viviendaForm = demograficos_form.cleaned_data.get('caracter_vivienda')
			personas_conviveForm = demograficos_form.cleaned_data.get('caracter_vivienda')
			estado_civilForm = demograficos_form.cleaned_data.get('estado_civil')
			numero_hijosForm = demograficos_form.cleaned_data.get('numero_hijos')
			ciudad_nacimientoForm = demograficos_form.cleaned_data.get('ciudad_nacimiento')

			historialDemografico = DatosDemograficos(id = persona, estrato = estratoForm, tipo_vivienda = tipo_viviendaForm, caracter_vivienda = caracter_viviendaForm, personas_convive = personas_conviveForm, estado_civil = estado_civilForm, numero_hijos = numero_hijosForm, ciudad_nacimiento = ciudad_nacimientoForm)
			historialDemografico.save()

		if context[grupo] == 'leader':
			return redirect('/campus/leader/' + kwargs['id_persona'])

		elif context[grupo] == 'master':
			return redirect('/campus/master/' + kwargs['id_persona'])			
		
		#return render(request, 'profile', context)

class UpdateDemograficos(UpdateView):
	model = DatosDemograficos
	fields = ['estrato', 'tipo_vivienda', 'caracter_vivienda', 'personas_convive', 'estado_civil', 'numero_hijos','ciudad_nacimiento']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(UpdateDemograficos, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)

		demograficos = DatosDemograficos.objects.get(id=kwargs['pk'])
		form = DatosDemograficosForm(request.POST)

		if form.is_valid():
			estrato = form.cleaned_data.get('estrato')
			tipo_vivienda = form.cleaned_data.get('tipo_vivienda')
			caracter_vivienda = form.cleaned_data.get('caracter_vivienda')
			personas_convive = form.cleaned_data.get('caracter_vivienda')
			estado_civil = form.cleaned_data.get('estado_civil')
			numero_hijos = form.cleaned_data.get('numero_hijos')
			ciudad_nacimiento = form.cleaned_data.get('ciudad_nacimiento')

			demograficos.estrato = estrato
			demograficos.tipo_vivienda = tipo_vivienda
			demograficos.caracter_vivienda = caracter_vivienda
			demograficos.personas_convive = personas_convive
			demograficos.estado_civil = estado_civil
			demograficos.numero_hijos = numero_hijos
			demograficos.ciudad_nacimiento = ciudad_nacimiento

			demograficos.save(update_fields=['estrato', 'tipo_vivienda', 'caracter_vivienda', 'personas_convive', 'estado_civil', 'numero_hijos','ciudad_nacimiento'])

		if grupo == 'leader':
			return redirect('/campus/leader/' + kwargs['pk'])

		elif grupo == 'master':
			return redirect('/campus/master/' + kwargs['pk'])


class AgregarHistoriaLaboral(TemplateView):
	template_name = 'moodle/agregar_historial_laboral.html'
	historial_laboral_form = HistorialLaboralForm()

	def get_context_data(self, **kwargs):
		context = super(AgregarHistoriaLaboral, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.historial_laboral_form

		return context		

	def post(self, request, *args, **kwargs):
		context = super(AgregarHistoriaLaboral, self).get_context_data(**kwargs)
		historial_laboral_form = HistorialLaboralForm(request.POST)

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		persona = Persona.objects.get(id= kwargs['id_persona'])

		if historial_laboral_form.is_valid():
			persona_asociadaForm = historial_laboral_form.cleaned_data.get('persona_asociada')
			nombre_institucionForm = historial_laboral_form.cleaned_data.get('nombre_institucion')
			tiempo_laboradoForm = historial_laboral_form.cleaned_data.get('tiempo_laborado')
			niveles_escolaresForm = historial_laboral_form.cleaned_data.get('niveles_escolares')
			areas_desempenioForm = historial_laboral_form.cleaned_data.get('areas_desempenio')
			grados_laboralesForm = historial_laboral_form.cleaned_data.get('grados_laborales')
			evidenciaForm = historial_laboral_form.cleaned_data.get('evidencia')

			historialLaboral = HistorialLaboral(persona_asociada = persona, nombre_institucion = nombre_institucionForm, tiempo_laborado = tiempo_laboradoForm, niveles_escolares = niveles_escolaresForm, areas_desempenio = areas_desempenioForm, grados_laborales = grados_laboralesForm, evidencia = evidenciaForm)
			historialLaboral.save()

		if context[grupo] == 'leader':
			return redirect('/campus/leader/' + kwargs['id_persona'])

		elif context[grupo] == 'master':
			return redirect('/campus/master/' + kwargs['id_persona'])


class UpdateHistorialLaboral(UpdateView):
	model = HistorialLaboral
	fields = ['nombre_institucion', 'tiempo_laborado', 'niveles_escolares', 'areas_desempenio', 'grados_laborales', 'evidencia']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(UpdateHistorialLaboral, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)

		historial_laboral = HistorialLaboral.objects.get(id=kwargs['pk']) #¿?
		form = HistorialLaboralForm(request.POST)

		if form.is_valid():
			nombre_institucion = form.cleaned_data.get('nombre_institucion')
			tiempo_laborado = form.cleaned_data.get('tiempo_laborado')
			niveles_escolares = form.cleaned_data.get('niveles_escolares')
			areas_desempenio = form.cleaned_data.get('areas_desempenio')
			grados_laborales = form.cleaned_data.get('grados_laborales')
			evidencia = form.cleaned_data.get('evidencia')

			historial_laboral.nombre_institucion = nombre_institucion
			historial_laboral.tiempo_laborado = tiempo_laborado
			historial_laboral.niveles_escolares = niveles_escolares
			historial_laboral.areas_desempenio = areas_desempenio
			historial_laboral.grados_laborales = grados_laborales
			historial_laboral.evidencia = evidencia

			historial_laboral.save(update_fields=['nombre_institucion', 'tiempo_laborado', 'niveles_escolares', 'areas_desempenio', 'grados_laborales', 'evidencia'])

		if grupo == 'leader':
			return redirect('/campus/leader/' + kwargs['pk'])

		elif grupo == 'master':
			return redirect('/campus/master/' + kwargs['pk'])


class AgregarHistoriaAcademico(TemplateView):
	template_name = 'moodle/agregar_historial_academico.html'
	historial_academico_form = HistorialAcademicoForm()

	def get_context_data(self, **kwargs):
		context = super(AgregarHistoriaAcademico, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		context['form'] = self.historial_academico_form

		return context

	def post(self, request, *args, **kwargs):
		context = super(AgregarHistoriaAcademico, self).get_context_data(**kwargs)
		historial_academico_form = HistorialAcademicoForm(request.POST)

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		persona = Persona.objects.get(id= kwargs['id_persona'])

		if historial_academico_form.is_valid():
			persona_asociadaForm = historial_academico_form.cleaned_data.get('persona_asociada')
			tituloForm = historial_academico_form.cleaned_data.get('titulo')
			tipo_estudioForm = historial_academico_form.cleaned_data.get('tipo_estudio')
			fecha_realizacionForm = historial_academico_form.cleaned_data.get('fecha_realizacion')
			institucion_acrededoraForm = historial_academico_form.cleaned_data.get('institucion_acrededora')
			evidenciaForm = historial_academico_form.cleaned_data.get('evidencia')

			historialAcademico = HistorialAcademico(persona_asociada = persona, titulo = tituloForm, tipo_estudio = tipo_estudioForm, fecha_realizacion = fecha_realizacionForm, institucion_acrededora = institucion_acrededoraForm, evidencia = evidenciaForm)
			historialAcademico.save()

		if context[grupo] == 'leader':
			return redirect('/campus/leader/' + kwargs['id_persona'])

		elif context[grupo] == 'master':
			return redirect('/campus/master/' + kwargs['id_persona'])


class UpdateHistorialAcademico(UpdateView):
	model = HistorialAcademico
	fields = ['titulo', 'tipo_estudio', 'fecha_realizacion', 'institucion_acrededora', 'evidencia']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):
		context = super(UpdateHistorialAcademico, self).get_context_data(**kwargs)
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)
		context[grupo] = grupo

		return context

	def post(self, request, *args, **kwargs):
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.verGrupo(self.request.user)

		historial_academico = HistorialAcademico.objects.get(id=kwargs['pk']) #¿?
		form = HistorialAcademicoForm(request.POST)

		if form.is_valid():
			titulo = form.cleaned_data.get('titulo')
			tipo_estudio = form.cleaned_data.get('tipo_estudio')
			fecha_realizacion = form.cleaned_data.get('fecha_realizacion')
			institucion_acrededora = form.cleaned_data.get('institucion_acrededora')
			evidencia = form.cleaned_data.get('evidencia')

			historial_academico.titulo = titulo
			historial_academico.tipo_estudio = tipo_estudio
			historial_academico.fecha_realizacion = fecha_realizacion
			historial_academico.institucion_acrededora = institucion_acrededora
			historial_academico.evidencia = evidencia

			historial_academico.save(update_fields=['titulo', 'tipo_estudio', 'fecha_realizacion', 'institucion_acrededora', 'evidencia'])

		if grupo == 'leader':
			return redirect('/campus/leader/' + kwargs['pk'])

		elif grupo == 'master':
			return redirect('/campus/master/' + kwargs['pk'])


class UpdateDatosLeaderTeacher(UpdateView):
	model = Persona
	fields = ['Email', 'sexo', 'fecha_nacimiento', 'Celular', 'fijo']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):

	def post(self, request, *args, **kwargs):
			return redirect('/campus/leader/' + kwargs['pk'])


class UpdateDatosMasterTeacher(UpdateView)
	model = Persona
	fields = ['Email', 'sexo', 'fecha_nacimiento', 'Celular', 'fijo']
	template_name_suffix = '_update_form'

	def get_context_data(self, **kwargs):

	def post(self, request, *args, **kwargs):
			return redirect('/campus/master/' + kwargs['pk'])
'''
class AgregarSoporteLaboral(TemplateView):
	template_name = 'moodle/agregar_soporte_laboral.html'
	soporteLaboralForm = SoporteLaboralNuevoform()

	def get_context_data(self, **kwargs):
		"""
		context = super(AgregarSoporteLaboral, self).get_context_data(**kwargs)
		if 'soporteLaboralForm' not in context:
			context['soporteLaboralForm'] = self.soporteLaboralForm
		return context
		"""

	def post(self, request, *args, **kwargs):
		"""
		soporteLaboralForm = SoporteLaboralNuevoform(request.POST)
		if soporteLaboralForm.is_valid():
			soporteLaboralForm.save()
		return render(request, self.template_name, self.get_context_data(**kwargs))
		"""
'''
#############################################################################################
##				Vistas en detalles por revisar (errores en los htmls correspondientes)
#############################################################################################
"""
class DetallesHistorialAcademico(TemplateView):
	template_name = 'moodle/detalles_academico.html'
	academicos = None
	usuario_actual = None
	personaX = None

	def get_context_data(self, **kwargs):
		context = super(DetallesHistorialAcademico, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user

		self.personaX = Persona.objects.get(id=self.kwargs['id_persona'])
		self.academicos = HistorialAcademico.objects.filter(persona=self.personaX)
		if 'academicos' not in context:
			context['academicos'] = self.academicos

		if 'usuario_actual' not in context:
			context['usuario_actual'] = self.usuario_actual

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		if grupo=='master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona
		if grupo=='leader':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			leader = LeaderTeacher.objects.get(id=persona.id)
			context['leader'] = leader
			context['persona'] = persona
		return context

class DetallesHistorialLaboral(TemplateView):
	template_name = 'moodle/detalles_laboral.html'
	laborales = None
	usuario_actual = None
	personaX = None

	def get_context_data(self, **kwargs):
		context = super(DetallesHistorialLaboral, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user

		self.personaX = Persona.objects.get(id=self.kwargs['id_persona'])
		self.laborales = HistorialLaboral.objects.filter(persona=self.personaX)
		if 'laborales' not in context:
			context['laborales'] = self.laborales

		if 'usuario_actual' not in context:
			context['usuario_actual'] = self.usuario_actual

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		if grupo=='master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona
		if grupo=='leader':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			leader = LeaderTeacher.objects.get(id=persona.id)
			context['leader'] = leader
			context['persona'] = persona
		return context
"""

'''
class DetallesHistorialSoporte(TemplateView):
	template_name = 'moodle/detalles_soporte.html' 
	laborales = None
	soportes = None
	usuario_actual = None
	personaX = None

	def get_context_data(self, **kwargs):
		context = super(DetallesHistorialSoporte, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user

		self.personaX = Persona.objects.get(id=self.kwargs['id_persona'])
		self.laborales = HistorialLaboral.objects.filter(persona=self.personaX)
		for laboral in self.laborales:
			soportesTemporal = SoporteLaboralNuevo.objects.filter(id=laboral.soporteLaboral.id)
			soportes.append(soportesTemporal)
		if 'soportes' not in context:
			context['soportes'] = self.soportes

		if 'usuario_actual' not in context:
			context['usuario_actual'] = self.usuario_actual

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		if grupo=='master':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			master = MasterTeacher.objects.get(id=persona.id)
			context['master'] = master
			context['persona'] = persona
		if grupo=='leader':
			persona = Persona.objects.get(id=kwargs['id_persona'])
			leader = LeaderTeacher.objects.get(id=persona.id)
			context['leader'] = leader
			context['persona'] = persona
		return context
'''