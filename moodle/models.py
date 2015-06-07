from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Persona(models.Model):

    opt_sexo = ((0, 'Masculino'), (1, 'Femenino'))
    id = models.CharField(max_length=15, primary_key=True) # id es cedula
    sexo = models.SmallIntegerField(choices=opt_sexo)
    fecha_nacimiento = models.DateField()
    celular = models.BigIntegerField()
    fijo = models.BigIntegerField(blank=True, null=True)
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
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    @models.permalink
    def get_absolute_url(self):
        return ("detalles_curso", [self.id])

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

class Matricula(models.Model):
    opt_estado_matricula = ((0, 'Matriculado'), (1, 'No Matriculado'),(2, 'En Espera de Matricula'))
    identificacion_leader_teacher = models.ForeignKey(LeaderTeacher) #models.CharField(max_length=60)
    identificacion_curso = models.ForeignKey(Curso) #models.CharField(max_length=60)
    estado_matricula = models.PositiveSmallIntegerField(choices=opt_estado_matricula)
    nota_final_curso = models.CharField(max_length=60, default=0)

class MasterTeacher(Persona):

    #cohorte_id = models.ForeignKey(Cohorte)
    tiempo_experiencia = models.CharField(max_length=2)
    @models.permalink
    def get_absolute_url(self):
        return ("cursos", [self.id])

class Cohorte(models.Model):
    opt_semestre = ((0, 'Febrero-Junio'), (1, 'Agosto-Diciembre'))
    id = models.CharField(max_length=60, primary_key=True) #identificador unico de cohorte
    semestre = models.SmallIntegerField(choices  = opt_semestre, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    curso = models.ForeignKey(Curso)
    master = models.ForeignKey(MasterTeacher, null=True, blank=True)

    def __str__(self):
        return self.id

    @models.permalink
    def get_absolute_url(self):
        return ("detalles_cohorte", [self.id])

    def get_semestre(self):
        if self.semestre == 0:
            return 'Febrero-Junio'
        elif self.semestre == 1:
            return 'Agosto-Diciembre'
        else:
            return 'None'

class RegistroNotas(models.Model):#antes se llamaba ternaria
    actividad = models.ForeignKey(Actividad)
    cohorte = models.ForeignKey(Cohorte)
    leader_teacher = models.ForeignKey(LeaderTeacher)
    nota = MinMaxFloat(min_value=1.0, max_value=5.0)

    def __str__(self):
        return self.nota

''' EN REVISION
class HistorialAcademico(models.Model):
    opt_tipo_estudio = ((0, 'Bachillerato'), (1, 'Pregrado'),(2, 'Posgrado'),(3, 'Especializacion'),(4, 'Maestria'),(5, 'Doctorado'))
    titulo = models.CharField(max_length=100, null=True, blank=True)
    tipoEstudio = models.PositiveSmallIntegerField(choices=opt_tipo_estudio)
    institucionAcre = models.CharField(max_length = 100, null=True, blank=True)
    fecha_realizacion = models.DateField(null=True, blank=True)
    persona = models.ForeignKey(Persona, null = True)
    '''

class Leader_Cohorte(models.Model):
    cohorte_id = models.ForeignKey(Cohorte)
    leader_id = models.ForeignKey(LeaderTeacher)


''' EN REVISION
class NivelEscolar(models.Model):
    NIVELES = ((0,'Transicion'), (1,'Educacion Inicial'), (2, 'Educacion basica primaria'),
               (3, 'Educacion basica secundaria'), (4, 'Educacion media'),
               (5, 'Nivel Superior'))
    nombre = models.SmallIntegerField(choices = NIVELES)
    soporte = models.FileField(upload_to='Documentos_Soporte')
    '''

''' EN REVISION
class HistorialLaboral(models.Model):
    tiempolaborado = models.CharField(max_length = 2)
    nivelEscolar = models.ForeignKey(NivelEscolar)
    '''

class DatosDemograficos(models.Model):
    opt_tipo_vivienda = ((0, 'Apartaestudio'), (1, 'Apartamento'), (2, 'Casa'))
    opt_caracter_vivienda = ((0, 'Arrendada'), (1, 'Familiar'), (2, 'Propia'))
    opt_estado_civil = ((0, 'Viudo'), (1, 'Soltero'), (2, 'Divorciado'), (3, 'Union Libre'), (4, 'Casado'))
    id = models.OneToOneField(Persona, primary_key=True) #Cedula LT o MT
    estrato = MinMaxFloat(min_value=0, max_value=6)
    tipo_vivienda = models.PositiveSmallIntegerField(choices=opt_tipo_vivienda)
    caracter_vivienda = models.PositiveSmallIntegerField(choices=opt_caracter_vivienda)
    personas_convive = models.CharField(max_length=2)
    estado_civil = models.PositiveSmallIntegerField(choices=opt_estado_civil)
    numero_hijos = models.CharField(max_length=2)
    ciudad_nacimiento = models.CharField(max_length=20)