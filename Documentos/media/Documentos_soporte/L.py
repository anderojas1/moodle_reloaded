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

	def haySiguiente(self, arregloMatricula):
		if((self.__index + 1) < len(arregloMatricula)):
			return True
		else:
			return False

	def hayAnterior(self):
		if(self.__index > 0):
			return True
		else:
			return False

	def actual(self, arregloMatricula):
		return arregloMatricula[self.__index]

	def siguiente(self, arregloMatricula):
		if self.haySiguiente():
			self.__index = self.__index + 1
		return arregloMatricula[self.__index]

	def anterior(self, arregloMatricula):
		if self.hayAnterior():
			self.__index = self.__index - 1
		return arregloMatricula[self.__index]

	def primero(self, arregloMatricula):
		self.__index = 0
		return arregloMatricula[self.__index]

class IteradorMatricula():
	__listaMatriculas = []
	__iterador = Iterador()

	def __init__(self, listaMatriculas):
		self.__listaMatriculas = listaMatriculas

	def actual(self):
		return self.__iterador.actual(self.__listaMatriculas)

	def siguiente(self):
		return self.__iterador.siguiente(self.__listaMatriculas)

	def anterior(self):
		return self.__iterador.anterior(self.__listaMatriculas)

	def primero(self):
		return self.__iterador.primero(self.__listaMatriculas)

	def haySiguiente(self):
		return self.__iterador.haySiguiente(self.__listaMatriculas)

#****************FINAL Funciones extra para BuscarDocentes FINAL*****************


class BuscarDocentes():

	def buscarDocentesInscritos(self, secretaria):

		instituciones = InstitucionEducativa.objects.filter(secretaria_id=secretaria.id)
		docentes = LeaderTeacher.objects.filter(institucion_id__in=instituciones)
		#print (docentes)

		#************************
		iterador = IteradorMatricula(docentes)
		docentesMatriculados = []

		if(iterador.actual() != None):
			matriculado = Matricula.objects.filter(identificacion_leader_teacher=iterador.actual().id, estado_matricula=2)
			if(len(matriculado)!=0):
				docentesMatriculados.append(matriculado)

		while (iterador.haySiguiente()):
			print("asd")
			matriculado = Matricula.objects.filter(identificacion_leader_teacher=iterador.actual().id, estado_matricula=2)
			if(len(matriculado)!=0):
				docentesMatriculados.append(matriculado)
		return docentesMatriculados