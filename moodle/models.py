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

class InstitucionEducativa(models.Model):

	opt_zona = ((0, 'Urbana'), (1, 'Urbana Marginal'), (2, 'Rural'), (3, 'Rural de Difícil Acceso'))
	opt_modalidad = ((0, 'Académica'), (1, 'Técnica'))
	opt_orientacion_etnoeducativa = ((0, 'Ninguna'), (1, 'Rom'), (2, 'Afrocolombiana'), (3, 'Indígena'))
	id = models.CharField(max_length=10, primary_key=True) #id es código dane
	nombre = models.CharField(max_length=100)
	municipio = models.CharField(max_length=50)
	zona = models.SmallIntegerField(choices=opt_zona)
	modalidad = models.SmallIntegerField(choices=opt_modalidad)
	orientacion_etnoeducativa = models.SmallIntegerField(choices=opt_orientacion_etnoeducativa)
	secretaria = models.ForeignKey(SecretariaEducacion)

	def __str__(self):
		return self.nombre


class LeaderTeacher(Persona):

	institucion = models.ForeignKey(InstitucionEducativa)

	

