from django.urls import path
from .views import *
from . import views
from django.conf import settings

app_name = 'accounts'

urlpatterns = [
    path('', views.login_admin, name='login'),
    path('dashboard/', views.home, name='dashboard'),
    path('proyectos/', views.projects, name="proyecto"),
    path('proyectos/proyectoDashboard/', views.projectsDetails, name="projects-dash"),
    path('proyectos/projectParticipants/', views.participantes, name="participantes"),
    path('proyectos/requisitos-usuario/', views.projectsUserReqs, name="requisitos-usuario"),
    path('proyectos/requisitos-usuario/agregar-requisito-usuario/', views.addUserReq, name='agregar-requisito-usuario'),
    path('proyectos/requisitos-usuario/editar-requisito-usuario/', views.editRequisitoUsuario, name='editar-requisito-usuario'),
    path('proyectos/requisitos-sistema/', views.projectsSysReqs, name="requisitos-sistema"),
    path('proyectos/requisitos-sistema/agregar-requisito-sistema/', views.addSysReq, name='agregar-requisito-sistema'),
    path('usuarios/', views.users, name="usuario"),
    path('proyectos/requisitos-usuario/analisis', views.analisisRU, name="analisis-user-req"),
    path('proyectos/requisitos-sistema/analisis', views.analisisRS, name="analisis-sys-req"),
    path('proyectos/requisitos-usuario/editar-requisito-sistema/', views.editRequisitoSistema, name='editar-requisito-sistema'),
]