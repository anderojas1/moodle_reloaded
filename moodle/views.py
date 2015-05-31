from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import LeaderTeacher, Persona, InstitucionEducativa, Curso, Area
from django.views.generic import TemplateView
from .funciones import VerificaUsuario, BuscarDocentes

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
		buscar_docentes.buscarDocentesInscritos(self.secretaria)

		context['secretaria'] = self.secretaria
		context['docentes'] = self.docentes

		return context

class CursoDetalles(TemplateView):
	template_name = 'moodle/detalles_curso.html'
	curso = None
	usuario_actual = None

	def get_context_data(self, **kwargs):
		context = super(CursoDetalles, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo

		self.curso = Curso.objects.get(id=context['id_curso'])
		context['curso'] = self.curso

		area = Area.objects.get(id=self.curso.area_id)
		context['area'] = area

		return context

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