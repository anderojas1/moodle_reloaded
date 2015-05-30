from django.contrib import admin
from .models import LeaderTeacher, SecretariaEducacion, InstitucionEducativa, Persona

# Register your models here.

admin.site.register(LeaderTeacher)
admin.site.register(SecretariaEducacion)
admin.site.register(InstitucionEducativa)
admin.site.register(Persona)