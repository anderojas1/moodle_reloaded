from django.contrib.auth.models import Group
from .models import Persona, LeaderTeacher, SecretariaEducacion, InstitucionEducativa, Matricula

class VerificaUsuario():

	def buscarGrupo(self, usuario):
		id_grupo = usuario.groups.all()
		print(id_grupo)
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

#****************Funciones extra para BuscarDocentes*****************
class Iterador():
	__index = 0

	def haySiguiente(self, arregloDocentes):
		if((self.__index + 1) < len(arregloDocentes)):
			return True
		else:
			return False

	def hayAnterior(self):
		if(self.__index > 0):
			return True
		else:
			return False

	def actual(self, arregloDocentes):
		return arregloDocentes[self.__index]

	def siguiente(self, arregloDocentes):
		if self.haySiguiente():
			self.__index = self.__index + 1
		return arregloDocentes[self.__index]

	def anterior(self, arregloDocentes):
		if self.hayAnterior():
			self.__index = self.__index - 1
		return arregloDocentes[self.__index]

	def primero(self, arregloDocentes):
		self.__index = 0
		return arregloDocentes[self.__index]

class IteradorDocentes():
	__listaDocentes = []
	iterador = Iterador()

	def __init__(self, listaDocentes):
		self.__listaDocentes = listaDocentes

	def actual(self):
		self.iterador.actual(self.__listaDocentes)

	def siguiente(self):
		self.iterador.siguiente(self.__listaDocentes)

	def anterior(self):
		self.iterador.anterior(self.__listaDocentes)

	def primero(self):
		self.iterador.primero(self.__listaDocentes)

	def haySiguiente(self):
		print(self.__listaDocentes)
		self.iterador.haySiguiente(self.__listaDocentes)

#****************FINAL Funciones extra para BuscarDocentes FINAL*****************


class BuscarDocentes():

	def buscarDocentesInscritos(self, secretaria):
		instituciones = InstitucionEducativa.objects.filter(secretaria_id=secretaria.id)
		docentes = LeaderTeacher.objects.filter(institucion_id__in=instituciones)
		#print (docentes)

		#************************
		"""iterador = IteradorDocentes(docentes)
		if iterador is None:
			print (iterador)
		print(docentes)
		docentesMatriculados = []

		iterador.haySiguiente()
		"""
		docentesMatriculados = []
		for matriculado in docentes:

			matriculado = Matricula.objects.filter(identificacion_leader_teacher=matriculado.id, estado_matricula=2)
			#print("entro")
			#print(len(matriculado))
			#print(matriculado)
			print(type(matriculado))
			if(len(matriculado)!=0):
				docentesMatriculados.append(matriculado)
		return docentesMatriculados