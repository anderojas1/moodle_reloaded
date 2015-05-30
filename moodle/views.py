from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import LeaderTeacher, Persona, InstitucionEducativa
from django.views.generic import TemplateView
from .funciones import VerificaUsuario

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
		print(self.institucion.id)

		if self.usuario == usuario_actual:
			context['editar'] = 'editable'

		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(usuario_actual)

		context[grupo] = grupo
		return context