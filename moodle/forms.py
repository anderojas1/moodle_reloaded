from django.forms import ModelForm
from django import forms
from .models import LeaderTeacher, Curso, RegistroNotas, Actividad, Curso, Cohorte, MasterTeacher
from .models import LeaderTeacher, RegistroNotas, Actividad
from .models import LeaderTeacher, Curso, RegistroNotas, Actividad, Curso
from .models import LeaderTeacher, RegistroNotas, Actividad, DatosDemograficos
from .models import HistorialAcademico, HistorialLaboral, SoporteLaboralNuevo
class LeaderTeacherForm(ModelForm):

	class Meta:
		model = LeaderTeacher
		fields = ['id', 'sexo', 'fecha_nacimiento', 'celular', 'fijo', 'institucion']
		"""widgets = {
			'id': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Cédula',
				}),
			'fecha_nacimiento': forms.DateInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Fecha Nacimiento dd/mm/aa',
				}),
			'celular': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Celular',
				}),
			'fijo': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Teléfono Fijo',
				}),
		}"""

	def clean(self):

		cedula = self.cleaned_data.get('id')
		cedula_exist = LeaderTeacher.objects.filter(id=cedula).exists()

		if cedula_exist:
			self.add_error('id', 'La cédula ' + cedula + ' ya se encuentra registrada')

class Buscar(forms.Form):
	opciones = (('Amazonas', 'Amazonas'), ('Caqueta', 'Caqueta'), ('Cauca', 'Cauca'), ('Huila', 'Huila'),
		('Nariño', 'Nariño'),('Putumayo', 'Putumayo'), ('Tolima', 'Tolima'),('Valle del Cauca', 'Valle del Cauca'))
	departamento = forms.ChoiceField(label='departamento', choices=opciones)

"""class CursosMayorAsistentes(forms.Form):
	cursos = Curso.objects.all()
	todos = ()
	for curso in cursos:
		tupla = (curso.nombre, curso.nombre)
		todos += tupla

	print (todos)
	cursos = form.ChoiceField(label='cursos', choices=todos)"""

class NotasPorEstudiante(forms.Form):
	cedula = forms.CharField(label= 'cedula', max_length=15)

class EstudiantesCurso(forms.Form):
	curso = forms.CharField(label= 'curso', max_length=100)

class EstudiantesDepartamentoCurso(forms.Form):
	curso = forms.CharField(label= 'curso', max_length=100)
	opciones = (('Amazonas', 'Amazonas'), ('Caqueta', 'Caqueta'), ('Cauca', 'Cauca'), ('Huila', 'Huila'),
		('Nariño', 'Nariño'),('Putumayo', 'Putumayo'), ('Tolima', 'Tolima'),('Valle del Cauca', 'Valle del Cauca'))
	departamento = forms.ChoiceField(label='departamento', choices=opciones)

############################################################################
##				Nuevo codigo
############################################################################
#from .models import RegistroNotas, Actividad
#+------------------------------------------+
#+					COHORTE					+
#+------------------------------------------+

class RegistroNotasForm(ModelForm):

	class Meta:
		model = RegistroNotas
		fields = ['actividad', 'cohorte', 'leader_teacher', 'nota']
		widgets = {
			'actividad': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Actividad',
				}),
			'cohorte': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Cohorte',
				}),
			'leader_teacher': forms.DateInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Leader Teacher',
				}),
			'nota': forms.DateInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Nota',
				})
		}
		
#+------------------------------------------+
#+				ACTIVIDAD					+
#+------------------------------------------+

class ActividadForm(ModelForm):

	class Meta:
		model = Actividad
		fields = ['descripcion', 'titulo', 'fecha_fin', 'fecha_inicio', 'porcentaje']
		"""widgets = {
			'descripcion': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Descripcion Actividad',
				}),
			'titulo': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Titulo Actividad',
				}),
			'fecha_fin': forms.DateInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Fecha de Fin dd/mm/aa',
				}),
			'fecha_inicio': forms.DateInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Fecha de Inicio dd/mm/aa',
				}),
			'porcentaje': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Porcentaje de la Actividad',
				}),
		}"""


################# CLASE CURSOFORM ###########################

class CursoForm (ModelForm):

	 class Meta():
	 	
	 	model = Curso
	 	fields = ['id', 'nombre', 'area', 'descripcion']
	 	widgets = {
			'id': forms.TextInput(attrs={
				'id': 'inputName3',
				'class': 'form-control',
				'type': 'text',
				'placeholder': 'Identificación Curso',
			}),
			'nombre': forms.TextInput(attrs={
				'id': 'inputName3',
				'class': 'form-control',
				'type': 'text',
				'placeholder': 'Nombre Curso',
			}),
			'descripcion': forms.TextInput(attrs={
				'id': 'inputName3',
				'class': 'form-control',
				'type': 'textarea',
				'placeholder': 'Descripción Curso',
			}),
			#'area': forms.SelectInput
		}

################################################################

class CohorteForm(ModelForm):

	class Meta:
		model = Cohorte
		fields = ['semestre', 'fecha_inicio', 'fecha_fin', 'master']

	def clean(self):
		cleaned_data = super(CohorteForm, self).clean()
		return cleaned_data
	


"""class NivelEscolarForm(ModelForm):
	class Meta:
		model = NivelEscolar
		fields = ['nombre', 'soporte']"""

class DatosDemograficosForm(ModelForm):
	class Meta:
		model = DatosDemograficos
		fields = ['estrato', 'tipo_vivienda', 'caracter_vivienda', 'personas_convive', 'estado_civil', 'numero_hijos','ciudad_nacimiento']

class HistorialAcademicoForm(ModelForm):
    class Meta:
        model = HistorialAcademico
        fields = ['titulo', 'tipoEstudio', 'fechaRealizacion', 'institucionAcree', 'evidencia']
        widgets = {
			'titulo': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Titulo',
			}),
			'tipoEstudio': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Tipo de estudio',
			}),
			'fechaRealizacion': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'date',
				'placeholder': 'Decba de realizacion',
			}),
			'institucionAcree': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Institucion Acree',
			}),
			'evidencia': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Evidencia',
			}),
			#'area': forms.SelectInput
		}

class HistorialLaboralForm(ModelForm):
    class Meta:
        model = HistorialLaboral
        fields = ['tiempoLaborado','nivelesEscolares', 'areasDesempenio', 'gradosLaborales']
        widgets = {
			'tiempoLaborado': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Tiempo laborado',
			}),
			'nivelesEscolares': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Niveles escolares',
			}),
			'areasDesempenio': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Areas de desempeno',
			}),
			'gradosLaborales': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Grados laborales',
			}),
			#'area': forms.SelectInput
		}

class SoporteLaboralNuevoform(ModelForm):
    class Meta:
        model = SoporteLaboralNuevo
        fields = ['tiempo', 'nombreInsti', 'docSoporte']
        widgets = {
        'tiempo': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Tiempo',
			}),
			'nombreInsti': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'Nombre de la institucion',
			}),
			'docSoporte': forms.TextInput(attrs={
				'class': 'campos_formularios',
				'type': 'text',
				'placeholder': 'documento de soporte',
			})
		}