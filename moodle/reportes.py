from .models import InstitucionEducativa, LeaderTeacher, Matricula, Curso, Cohorte, RegistroNotas

class BuscarReportes():

	def reportes(self, criterio, tipo):

		if tipo == 0:
			instituciones = InstitucionEducativa.objects.filter(departamento=criterio)
			leaders = LeaderTeacher.objects.filter(institucion__in=instituciones, matricula__estado_matricula=0)
			return leaders

		elif tipo == 2:
			#leader = LeaderTeacher.objects.get(id=criterio)
			reporte = RegistroNotas.objects.filter(leader_teacher__id = criterio).values('nota', 'actividad__titulo')
			return reporte

		elif tipo == 3:
			curso = Curso.objects.get(nombre=criterio)
			resultado = []
			cursos = Matricula.objects.filter(identificacion_curso_id=curso.id)
			for cursoaprobado in cursos:
				if float(cursoaprobado.nota_final_curso) >= 3.0:
					resultado.append(cursoaprobado)
			return resultado;

	def reportes2(self, criterio1, criterio2):

		leaders_dpto = InstitucionEducativa.objects.filter(departamento=criterio2)
		curso = Curso.objects.get(nombre=criterio1)
		leaders = LeaderTeacher.objects.filter(institucion__in=leaders_dpto, matricula__estado_matricula = 0, 
			matricula__identificacion_curso = curso.id)
		print (leaders)
		return leaders