from django.db import models

# Create your models here.

class Cuenta(models.Model):
	ADMIN = (
		("Si", "Si"),
		("No", "No"),
		)
	nombre_usuario = models.CharField(max_length=200, null=True)
	correo = models.CharField(max_length=200, null=True)
	contraseña = models.CharField(max_length=200, null=True)
	admin = models.CharField(max_length=10, null=False, choices=ADMIN)

	def __str__(self):
		return self.nombre_usuario

class Proyecto(models.Model):
	ESTADO = (
		("Activo", "Activo"),
		("Completado", "Completado"),
		)
	id_proyecto = models.CharField(max_length=200, null=True)
	name = models.CharField(max_length=200, null=True)
	descripcion = models.CharField(max_length=200, null=True)
	estado = models.CharField(max_length=200, null=True, choices=ESTADO)
	
	def __str__(self):
		return self.name

class AsignacionJefeProyecto(models.Model):
	cuenta = models.ForeignKey(Cuenta, null=True, on_delete= models.SET_NULL)
	proyecto_id = models.ForeignKey(Proyecto, null=True, on_delete= models.SET_NULL)

	def __str__(self):
		return str(self.proyecto_id)

class AsignacionProyecto(models.Model):
	cuenta = models.ForeignKey(Cuenta, null=True, on_delete= models.SET_NULL)
	proyecto_id = models.ForeignKey(Proyecto, null=True, on_delete= models.SET_NULL)

	def __str__(self):
		return str(self.proyecto_id)

class RequisitoDeUsuario(models.Model):
	idreq = 1
	versionreq = 1
	TIPE = (
		("Funcional", "Funcional"),
		("No Funcional", "No Funcional"),
		("Restriccion", "Restriccion"),
		("Calidad", "Calidad"),
		)

	ESTADO = (
		("Cumple", "Cumple"),
		("No Cumple", "No Cumple"),
		)

	URGENCIA = (
		("Urgente", "Urgente"),
		("Normal", "Normal"),
		("Si se puede", "Si se puede"),
		)

	PRIORIDAD = (
		("Deseable", "Deseable"),
		("No Deseable", "No Deseable"),
		("Critico", "Critico"),
		)

	ESTABILIDAD = (
		("Transable", "Transable"),
		("Intransable", "Intransable"),
		)

	codigo = models.CharField(max_length=200, default="RU0"+str(idreq))
	titulo = models.CharField(max_length=200, null=True)
	prioridad = models.CharField(max_length=200, null=True, choices=PRIORIDAD)
	tipo = models.CharField(max_length=200, null=True, choices=TIPE)
	fuente = models.CharField(max_length=200, null=True)
#	fecha = models.DateTimeField(auto_now_add=True, null=True)
	estabilidad = models.CharField(max_length=200, null=True, choices=ESTABILIDAD)
	urgencia = models.CharField(max_length=200, null=True, choices=URGENCIA)
	estado = models.CharField(max_length=200, null=True, choices=ESTADO)
	costo = models.CharField(max_length=200, null=True)
	descripcion = models.CharField(max_length=600, null=True)

	version = models.CharField(max_length=200, default=versionreq)
	
	proyecto_id = models.ForeignKey(Proyecto, null=True, on_delete= models.SET_NULL)

	def __str__(self):
		return self.codigo+": "+ self.titulo


class AnalizisRu(models.Model):
#	id_Analisis = 1
#	id_analisis_ru = models.IntegerField(default=id_Analisis)
	smell_codigo = models.CharField(max_length=700, default=" ")
	version = models.CharField(max_length=200, default="1")
	feedback = models.CharField(max_length=800, default=" ")
	ru_codigo = models.ForeignKey(RequisitoDeUsuario, null=True, on_delete= models.SET_NULL)

	class Meta:
		verbose_name="Analisis RU"
		#ordering = ["-created"]  

	def __str__(self):
		return "Analisis del requisito "+str(self.ru_codigo)

class AnalisisRuDesc(models.Model):
#	id_Analisis = 1
#	id_analisis_ru = models.IntegerField(default=id_Analisis)
	smell_codigo = models.CharField(max_length=700, default=" ")
	version = models.CharField(max_length=200, default="1")
	feedback = models.CharField(max_length=800, default=" ")
	ru_codigo = models.ForeignKey(RequisitoDeUsuario, null=True, on_delete= models.SET_NULL)

	class Meta:
		verbose_name="Analisis Descripcion RU"
		#ordering = ["-created"]  

	def __str__(self):
		return "Analisis de la desc. del requisito "+str(self.ru_codigo)

class RequisitoSistema(models.Model):
	versionreq = 1
	idreq = 1
	TIPE = (
        ("Funcional", "Funcional"),
        ("No Funcional", "No Funcional"),
        ("Restriccion", "Restriccion"),
        ("Calidad", "Calidad"),
        )

	ESTADO = (
        ("Cumple", "Cumple"),
        ("No Cumple", "No Cumple"),
        )

	URGENCIA = (
        ("Urgente", "Urgente"),
        ("Normal", "Normal"),
        ("Si se puede", "Si se puede"),
        )

	codigo = models.CharField(max_length=200, default="RS0"+str(idreq))
	titulo = models.CharField(max_length=200, null=True)
	tipo = models.CharField(max_length=200, null=True, choices=TIPE)
	costo = models.CharField(max_length=200, null=True)
	urgencia = models.CharField(max_length=200, null=True, choices=URGENCIA)
	estado = models.CharField(max_length=200, null=True, choices=ESTADO)
	descripcion = models.CharField(max_length=600, null=True)
    
	version = models.CharField(max_length=200, default=versionreq)

	proyecto_id = models.ForeignKey(Proyecto, null=True, on_delete= models.SET_NULL)
	requisito_usuario_codigo = models.ForeignKey(RequisitoDeUsuario, null=True, on_delete= models.SET_NULL)
	
	def __str__(self):
		return self.codigo+": "+ self.titulo

class AnalizisRs(models.Model):
#	idAnalisis = 1
#	id_analisis_rs = models.IntegerField(default=idAnalisis)
	smell_codigo = models.CharField(max_length=700, default=" ")
	version = models.CharField(max_length=200, default="1")
	feedback = models.CharField(max_length=800, default=" ")
	rs_codigo = models.ForeignKey(RequisitoSistema, null=True, on_delete= models.SET_NULL)

	class Meta:
		verbose_name="Analisis RS"
		#ordering = ["-created"]  

	def __str__(self):
		return "Analisis del requisito "+str(self.rs_codigo)

class AnalizisRsDesc(models.Model):
#	idAnalisis = 1
#	id_analisis_rs = models.IntegerField(default=idAnalisis)
	smell_codigo = models.CharField(max_length=700, default=" ")
	version = models.CharField(max_length=200, default="1")
	feedback = models.CharField(max_length=800, default=" ")
	rs_codigo = models.ForeignKey(RequisitoSistema, null=True, on_delete= models.SET_NULL)

	class Meta:
		verbose_name="Analisis Descripcion RS"
		#ordering = ["-created"]  

	def __str__(self):
		return "Analisis de la desc. del requisito "+str(self.rs_codigo)

class SmellDescription(models.Model):
	smell_codigo = models.CharField(max_length=200, null=True)
	smell_titulo = models.CharField(max_length=200, null=True)
	smell_descripcion = models.CharField(max_length=400, null=True)

	def __str__(self):
		return self.smell_codigo + self.smell_titulo
		