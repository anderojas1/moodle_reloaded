from django.contrib.auth.models import Group
from .models import Persona, LeaderTeacher, SecretariaEducacion, InstitucionEducativa, Matricula, RegistroNotas, MasterTeacher
from .models import Persona, Curso, Cohorte, LeaderTeacher, SecretariaEducacion, InstitucionEducativa, Matricula, Cohorte, Leader_Cohorte
from .models import MasterTeacher

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

	def buscarLeaderMatriculado(self):

		leaders = LeaderTeacher.objects.filter(id = Matricula.objects.filter(estado_matricula = 0 ))

		return leaders

#************************CLASE QUE REGISTRA LAS NOTAS DE UN ESTUDIANTE**********************

class RegistrarNota():

	def registrarNota(self, act, cohor, leader, nota_):
		registro = RegistroNotas(actividad = act.id, cohorte = cohor.id, leader_teacher = leader.id, nota = nota_)
		registro.save()

############################################################################
##				Matricular Leader teacher
############################################################################

class MatricularLeaderTeacherCohorte():

	def matricular(self, leader, cursos):

		cohortes = Cohorte.objects.filter(curso=cursos.id)

		if len(cohortes) > 0:
			flag = True
			#print("algo")
			for cohorte in cohortes:
				num_matriculados = Leader_Cohorte.objects.filter(cohorte_id=cohorte.id)
				if len(num_matriculados) < 30:
					matricula = Leader_Cohorte(cohorte_id=cohorte, leader_id=leader)
					matricula.save()
					break

				else:
					masterT = MasterTeacher.objects.get(id=1124124)
					cohorte = Cohorte(id=str(len(Cohorte.objects.all())),semestre=1, fecha_inicio='2015-08-20',
						fecha_fin='2015-10-20', curso = cursos, master = masterT)
					cohorte.save()
					matricula = Leader_Cohorte(cohorte_id=cohorte, leader_id=leader)
					matricula.save()
					flag = False
					break
		else:
			print("no hay nada")
			masterT = MasterTeacher.objects.get(id=1124124)
			print (masterT)
			cohorte = Cohorte(id=str(len(Cohorte.objects.all())),semestre=1, fecha_inicio='2015-08-20',
				fecha_fin='2015-10-20', curso = cursos, master = masterT)
			cohorte.save()
			matricula = Leader_Cohorte(cohorte_id=cohorte, leader_id=leader)
			matricula.save()

		matricula_curso = Matricula.objects.get(identificacion_leader_teacher=leader.id,
			identificacion_curso=cursos.id)
		print (matricula_curso.estado_matricula)
		matricula_curso.estado_matricula = 0;
		matricula_curso.save(update_fields=['estado_matricula'])

############################################################################
##				Cohortes de MasterTeacher
############################################################################

class CohorteMasterTeacher:

	def buscar(self, usuario):
		persona = Persona.objects.get(usuario_id=usuario.id)
		cohortes = Cohorte.objects.filter(master=persona.id)
		return cohortes
