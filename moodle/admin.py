from django.contrib import admin
from .models import MasterTeacher, Matricula, RegistroNotas, Actividad, Cohorte, LeaderTeacher, SecretariaEducacion, InstitucionEducativa, Persona, Curso, Area

# Register your models here.

admin.site.register(LeaderTeacher)
admin.site.register(SecretariaEducacion)
admin.site.register(InstitucionEducativa)
admin.site.register(Persona)
admin.site.register(Curso)
admin.site.register(Area)
admin.site.register(Cohorte)
admin.site.register(Actividad)
admin.site.register(RegistroNotas)
admin.site.register(Matricula)
admin.site.register(MasterTeacher)