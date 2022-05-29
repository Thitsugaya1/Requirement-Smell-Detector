from .models import *

def addUserRequirement(request, codigo, titulo, prioridad, tipo, fuente, costo, estabilidad, urgencia, estado, descripcion):
	user = RequisitoDeUsuario(codigo = "RU"+str(codigo), titulo = titulo, prioridad = prioridad, tipe = tipo, fuente = fuente, estabilidad = estabilidad, urgencia = urgencia, estado = estado, costo = costo, descripcion = descripcion, version = 1, proyecto_id = "Null de momento")
	user.save()