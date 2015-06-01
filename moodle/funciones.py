from django.contrib.auth.models import Group
from .models import Persona, LeaderTeacher, SecretariaEducacion, InstitucionEducativa

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
		secretaria = SecretariaEducacion.objects.get(usuario_id=usuario.id)
		return secretaria

	def buscarLeaderTeacher(self, usuario):
		persona = self.buscarPersona(usuario)
		leader = LeaderTeacher.objects.get(id=persona.id)
		return leader

class BuscarDocentes():

	def buscarDocentesInscritos(self, secretaria):
		instituciones = InstitucionEducativa.objects.filter(secretaria_id=secretaria.id)
		docentes = LeaderTeacher.objects.filter(institucion_id__in=instituciones)
		#print (docentes)

		#************************
		#return nuevo arreglo con metodo de filtro con iterador
		#*************************

	#Aquí el método
	#Retorna el nuevo arreglo