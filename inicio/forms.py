from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
# Create your models here.

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
        	'first_name': forms.TextInput(attrs = {
        		'class': 'campos_formularios',
        		'type': 'text',
        		'placeholder': 'Nombres'
        	}),
        	'last_name': forms.TextInput(attrs= {
        		'class': 'campos_formularios',
        		'type': 'text',
        		'placeholder': 'Apellidos'
        	}),
        	'email': forms.TextInput(attrs={
        		'class': 'campos_formularios',
        		'type': 'text',
        		'placeholder': 'Correo Electrónico'
        	}),
        	'username': forms.TextInput(attrs={
        		'class': 'campos_formularios',
        		'type': 'text',
        		'placeholder': 'Usuario'
        	}),
        	'password': forms.PasswordInput(attrs={
        		'class': 'campos_formularios',
        		'type': 'password',
        		'placeholder': 'Contraseña'
        	}),
        }

    def clean(self):

        usuario = self.cleaned_data.get('username')
        usuario_exist = User.objects.filter(username=usuario).exists()
        print (usuario_exist)
        print (usuario)

        if usuario_exist:
            self.add_error('username', 'El usuario ya está registrado')