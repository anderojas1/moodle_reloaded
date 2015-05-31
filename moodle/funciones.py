from django.contrib.auth.models import Group
from .models import Persona, LeaderTeacher, SecretariaEducacion

class VerificaUsuario():

	def buscarGrupo(self, usuario):
		id_grupo = usuario.groups.all()
		try:
			grupo = Group.objects.get(id=id_grupo).name
		except Group.DoesNotExist:
			grupo = 'otro'
		#print (grupo)
		return grupo

	def buscarPersona(self, usuario):
		persona = Persona.objects.get(usuario_id=usuario.id)
		#print (teacher)
		return persona

	def buscarSecretaria(self, usuario):
		print (usuario.id)
		secretaria = SecretariaEducacion.objects.get(usuario_id=usuario.id)
		return secretaria