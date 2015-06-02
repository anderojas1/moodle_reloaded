from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import LeaderTeacher, Persona, InstitucionEducativa, Curso, Area, Matricula
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from .funciones import VerificaUsuario, BuscarDocentes, MatricularLeaderTeacherCohorte

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
			print(len(curso_docente))
			print(len(curso_docente[0]))
			docente = LeaderTeacher.objects.get(id = matricula.get().identificacion_leader_teacher_id)
			curso = Curso.objects.get(id = matricula.get().identificacion_curso_id)
			curso_docente[i][0] = docente
			curso_docente[i][1] = curso
			#docentes.append(docente)
			#cursos.append(curso)
		print (curso_docente)
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

		self.cursos = Curso.objects.all()
		context['cursos'] = self.cursos

		return context

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
