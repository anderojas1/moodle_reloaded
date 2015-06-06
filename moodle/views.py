from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import LeaderTeacher, Persona, InstitucionEducativa, Curso, Area, Matricula, MasterTeacher, Cohorte
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from .funciones import VerificaUsuario, BuscarDocentes, MatricularLeaderTeacherCohorte, CohorteMasterTeacher
from .forms import Buscar, NotasPorEstudiante, EstudiantesCurso, EstudiantesDepartamentoCurso
from .reportes import BuscarReportes
from .funciones import CalculaNotaLeader
from .models import Actividad, Curso
from .forms import ActividadForm, CursoForm
from .models import Actividad, NivelEscolar
from .forms import ActividadForm, NivelEscolarForm
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
		print(len(matriculas))
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
		leader = self.ver_grupo.buscarLeaderTeacher(self.request.user)
		self.curso = Curso.objects.get(id=context['id_curso'])
		try:
			verificar = Matricula.objects.get(identificacion_leader_teacher=leader.id, 
				identificacion_curso=self.curso.id)
			context['exito'] = 'Usted ya se matriculó a este curso'
		except ObjectDoesNotExist:
			matricula = Matricula(identificacion_leader_teacher=leader, identificacion_curso=self.curso,
				estado_matricula=2)
			matricula.save()
			context['exito'] = 'Se ha realizado la matrícula exitosamente'
		
		self.usuario_actual = self.request.user
		grupo = self.ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		self.curso = Curso.objects.get(id=context['id_curso'])
		context['curso'] = self.curso

		area = Area.objects.get(id=self.curso.area_id)
		context['area'] = area
		return render(request, self.template_name, context)

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
			self.cohortes = Cohorte.objects.all()
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

class MasterCohorte(TemplateView):

	template_name = 'moodle/detalles_cohorte.html'

	def get_context_data(self, **kwargs):
		context = super(MasterCohorte, self).get_context_data(**kwargs)
		usuario = self.request.user
		persona = Persona.objects.get(id=kwargs['id_persona'])
		master = MasterTeacher.objects.get(id=persona.id)
		context['master'] = master
		context['persona'] = persona

		return context

############################################################################
##				Nuevo codigo
############################################################################
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

		print(self.usuario_actual.username)

		grupo = ver_grupo.buscarGrupo(self.usuario_actual)

		context[grupo] = grupo
		return context

class ActividadFormulario(TemplateView):
	template_name = 'moodle/formulario_actividad.html'
	actividadForm = ActividadForm(prefix='actividad')

	def get_context_data(self, **kwargs):
		context = super(ActividadFormulario, self).get_context_data(**kwargs)
		if 'actividadForm' not in context:
			context['actividadForm'] = self.actividadForm
		return context

	def post(self, request,*args,**kwargs):
		actividadForm = ActividadForm(request.POST, prefix='actividad')
		if actividadForm.is_valid():
			actividad = actividadForm.save(commit=False)
			actividad.save()
		return render(request, self.template_name, self.get_context_data(**kwargs))	


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
		print (kwargs)

		return context


class GuardarNivelEscolar(TemplateView):

	template_name = 'moodle/guardar_nivel_escolar.html'
	nivelEscolarForm = NivelEscolarForm(prefix='nivel_escolar')

	def get_context_data(self, **kwargs):
		context = super(GuardarNivelEscolar, self).get_context_data(**kwargs)
		if 'nivelEscolarForm' not in context:
			context['nivelEscolarForm'] = self.nivelEscolarForm
		return context

	def post(self, request, *args, **kwargs):
		nivelEscolarForm = NivelEscolarForm(request.POST)
		if nivelEscolarForm.is_valid():
			obj = NivelEscolar.get_objects(nombre = nivelEscolarForm.cleaned_data.get("nombre")).exists()

			if obj == False:
				nivelEscolarForm.save()
			else:
				pass

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(request.user)
		context = super(GuardarNivelEscolar, self).get_context_data(**kwargs)
		context[grupo] = grupo

		if grupo == 'leader':
			return render(request, 'detalles_leader')
		else:
			return render(request, 'detalles_master')