from django.shortcuts import render,render_to_response, HttpResponseRedirect
from django.views.generic import TemplateView, DetailView
from django.http import HttpRequest, request
from .forms import UserForm
from django.core.urlresolvers import reverse_lazy
from moodle.models import LeaderTeacher, Persona
from moodle.forms import LeaderTeacherForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from moodle.funciones import VerificaUsuario

# Create your views here.

class Index(TemplateView):
	template_name = 'inicio/index.html'

class SignupLeaderTeacher(TemplateView):
	template_name = 'inicio/signup.html'
	userform = UserForm(prefix='user')
	leaderTeacherForm = LeaderTeacherForm(prefix='leader')

	def get_context_data(self, **kwargs):
		context = super(SignupLeaderTeacher, self).get_context_data(**kwargs)
		if 'userform' not in context:
			context['userform'] = self.userform
		if 'leaderTeacherForm' not in context:
			context['leaderTeacherForm'] = self.leaderTeacherForm
		return context

	def post(self, request,*args,**kwargs):
		userform = UserForm(request.POST, prefix='user')
		leaderTeacherForm = LeaderTeacherForm(request.POST, prefix='leader')
		if userform.is_valid() and leaderTeacherForm.is_valid():
			user = userform.save(commit=False)
			user.set_password(userform.cleaned_data['password'])
			user.save()
			leader = leaderTeacherForm.save(commit=False)
			leader.usuario = user
			leader.save()
			grupo = Group.objects.get(name='leader')
			user.groups.add(grupo)
			# return reverse_lazy('index')
		return render(request, self.template_name, self.get_context_data(**kwargs))

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			# return render(request, self.template_name, context_instance=RequestContext(request.user))
			# return render(request, self.template_name, self.get_context_data(**kwargs))
			return HttpResponseRedirect(reverse_lazy('index'))
		else:
			return render(request, self.template_name, self.get_context_data(**kwargs))

class Perfil(TemplateView):
	template_name = 'inicio/perfil.html'
	usuario_actual=''

	def get_context_data(self, **kwargs):
		context = super(Perfil, self).get_context_data(**kwargs)
		self.usuario_actual = self.request.user
		ver_grupo = VerificaUsuario()
		grupo = ver_grupo.buscarGrupo(self.usuario_actual)
		context[grupo] = grupo
		return context