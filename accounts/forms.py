from django import forms
from django.forms import fields, widgets
from .models import *

class projectForms(forms.ModelForm):
	class Meta:
		model = Proyecto
		fields = ('id_proyecto', 'name', 'descripcion', 'estado')

class projectSelectForm(forms.Form):
	project = forms.ChoiceField(label='Proyecto')


class userForms(forms.ModelForm):
	class Meta:
		model = Cuenta
		fields = ('nombre_usuario', 'correo', 'contraseña', 'admin')

class asignarProyectoForm(forms.ModelForm):
	class Meta:
		model = AsignacionProyecto
		fields = ('cuenta', 'proyecto_id')

class userRequirementForm(forms.ModelForm):
	class Meta:
		model = RequisitoDeUsuario
		fields = ('codigo', 'titulo', 'prioridad', 'tipo', 'fuente', 'estabilidad', 'urgencia', 'estado', 'costo', 'descripcion', 'version', 'proyecto_id')

class systemRequirementForm(forms.ModelForm):
	class Meta:
		model = RequisitoSistema
		fields = ('codigo', 'titulo', 'tipo', 'costo','urgencia', 'estado', 'descripcion', 'version', 'proyecto_id', 'requisito_usuario_codigo')

class analisisRUform(forms.ModelForm):
	class Meta:
		model = AnalizisRu
		fields = ('smell_codigo', 'version', 'ru_codigo')

class analisisRSform(forms.ModelForm):
	class Meta:
		model = AnalizisRs
		fields = ('smell_codigo', 'version', 'rs_codigo')

class analisisRUDescform(forms.ModelForm):
	class Meta:
		model = AnalisisRuDesc
		fields = ('smell_codigo', 'version', 'ru_codigo')

class analisisRSDescform(forms.ModelForm):
	class Meta:
		model = AnalizisRsDesc
		fields = ('smell_codigo', 'version', 'rs_codigo')

class userRequirementForm1(forms.Form):
	codigo = forms.CharField(max_length=5)
	titulo = models.CharField(max_length=200)
	prioridad = forms.CharField(max_length=200)
	descripcion = models.CharField(max_length=1000)

class userRequirementForm2(forms.Form):
	tipo = forms.CharField(max_length=200)
	fuente = forms.CharField(max_length=200)
	estabilidad = forms.CharField(max_length=200)
	urgencia = forms.CharField(max_length=200)
	estado = forms.CharField(max_length=200)
	costo = forms.CharField(max_length=200)