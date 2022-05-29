from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Cuenta)
admin.site.register(Proyecto)
admin.site.register(AsignacionJefeProyecto)
admin.site.register(AsignacionProyecto)
admin.site.register(RequisitoDeUsuario)
admin.site.register(AnalizisRu)
admin.site.register(RequisitoSistema)
admin.site.register(AnalizisRs)
admin.site.register(SmellDescription)
admin.site.register(AnalizisRsDesc)
admin.site.register(AnalisisRuDesc)