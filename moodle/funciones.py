from django.contrib.auth.models import Group

class VerificaUsuario():

	def buscarGrupo(self, usuario):
		id_grupo = usuario.groups.all()
		try:
			grupo = Group.objects.get(id=id_grupo).name
		except Group.DoesNotExist:
			grupo = 'otro'
		#print (grupo)
		return grupo
