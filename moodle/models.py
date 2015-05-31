from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Persona(models.Model):

	opt_sexo = ((0, 'Masculino'), (1, 'Femenino'))
	id = models.CharField(max_length=15, primary_key=True) # id es cedula
	sexo = models.SmallIntegerField(choices=opt_sexo)
	fecha_nacimiento = models.DateField()
	celular = models.IntegerField()
	fijo = models.IntegerField(blank=True, null=True)	
	usuario = models.OneToOneField(User)

	def __str__(self):
		return self.usuario.first_name+" "+self.usuario.last_name

	def get_sexo(self):
		if self.sexo == 0:
			return 'Masculino'
		else:
			return 'Femenino'

class SecretariaEducacion(models.Model):

	id = models.CharField(max_length=10, primary_key=True) # id es código
	nombre = models.CharField(max_length=50)
	usuario = models.OneToOneField(User)

	def __str__(self):
		return self.nombre

	@models.permalink
	def get_search_url(self):
		return ("ver_docentes_inscritos", [self.id])

class InstitucionEducativa(models.Model):

	opt_zona = ((0, 'Urbana'), (1, 'Urbana Marginal'), (2, 'Rural'), (3, 'Rural de Difícil Acceso'))
	opt_modalidad = ((0, 'Académica'), (1, 'Técnica'))
	opt_orientacion_etnoeducativa = ((0, 'Ninguna'), (1, 'Rom'), (2, 'Afrocolombiana'), (3, 'Indígena'))
	id = models.CharField(max_length=10, primary_key=True) #id es código dane
	nombre = models.CharField(max_length=100)
	municipio = models.CharField(max_length=50)
	departamento = models.CharField(max_length=50)
	zona = models.SmallIntegerField(choices=opt_zona)
	modalidad = models.SmallIntegerField(choices=opt_modalidad)
	orientacion_etnoeducativa = models.SmallIntegerField(choices=opt_orientacion_etnoeducativa)
	secretaria = models.ForeignKey(SecretariaEducacion)

	def __str__(self):
		return self.nombre


class LeaderTeacher(Persona):

	institucion = models.ForeignKey(InstitucionEducativa)
	grado_estudio = models.CharField(max_length=60)

	@models.permalink
	def get_absolute_url(self):
		return ("detalles_leader", [self.id])


class Area(models.Model):
	id = models.CharField(max_length=60, primary_key=True)#id es el identificador de la area
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(max_length=200)

	def __str__(self):
		return self.nombre

class Curso(models.Model):
	id = models.CharField(max_length=60, primary_key=True) #id es el codigo del curso
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(max_length=200)
	area = models.ForeignKey(Area)

	def __str__(self):
		return self.id

class Cohorte(models.Model):
	opt_semestre = ((0, 'Febrero-Junio'), (1, 'Agosto-Diciembre'))
	id = models.CharField(max_length=60, primary_key=True) #identificador unico de cohorte
	semestre = models.SmallIntegerField(choices  = opt_semestre)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	curso = models.ForeignKey(Curso)

	def __str__(self):
		return self.id

class Actividad(models.Model):
	id = models.CharField(max_length=60, primary_key=True)#identificador unico de una actividad
	descripcion = models.TextField(max_length=200)
	titulo = models.CharField(max_length=60 )
	fecha_fin = models.DateField()
	fecha_inicio = models.DateField()
	porcentaje = models.CharField(max_length=60)

	def __str__(self):
		return self.id

class MinMaxFloat(models.FloatField):
	def __init__(self, min_value=None, max_value=None, *args, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		super(MinMaxFloat, self).__init__(*args, **kwargs)

	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
		defaults.update(kwargs)
		return super(MinMaxFloat, self).formfield(**defaults)

class RegistroNotas(models.Model):#antes se llamaba ternaria
	actividad = models.ForeignKey(Actividad)
	cohorte = models.ForeignKey(Cohorte)
	leader_teacher = models.ForeignKey(LeaderTeacher)
	nota = MinMaxFloat(min_value=1.0, max_value=5.0)

	def __str__(self):
		return self.nota

class Matricula(models.Model):
	opt_estado_matricula = ((0, 'Matriculado'), (1, 'No Matriculado'),(2, 'En Espera de Matricula'))
	identificacion_leader_teacher = models.ForeignKey(LeaderTeacher) #models.CharField(max_length=60)
	identificacion_curso = models.ForeignKey(Curso) #models.CharField(max_length=60)
	estado_matricula = models.PositiveSmallIntegerField(choices=opt_estado_matricula)
	nota_final_curso = models.CharField(max_length=60, default=0)

class MasterTeacher(Persona):

	cohorte = models.ForeignKey(Cohorte)
	tiempo_experiencia = models.CharField(max_length=2)

class HistorialAcademico(models.Model):
	opt_tipo_estudio = ((0, 'Bachillerato'), (1, 'Pregrado'),(2, 'Posgrado'),(3, 'Especializacion'),(4, 'Maestria'),(5, 'Doctorado'))
	titulo = models.CharField(max_length=100)
	tipoEstudio = models.PositiveSmallIntegerField(choices=opt_tipo_estudio)






	

