from django.forms import ModelForm
from django import forms
from .models import LeaderTeacher


class LeaderTeacherForm(ModelForm):

	class Meta:
		model = LeaderTeacher
		fields = ['id', 'sexo', 'fecha_nacimiento', 'celular', 'fijo', 'institucion']
		widgets = {
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
		}

	def clean(self):

		cedula = self.cleaned_data.get('id')
		cedula_exist = LeaderTeacher.objects.filter(id=cedula).exists()

		if cedula_exist:
			self.add_error('id', 'La cédula ' + cedula + ' ya se encuentra registrada')