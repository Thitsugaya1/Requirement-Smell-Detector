from os import name
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
import json
#from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.regex_helper import Choice
from django.views.generic import TemplateView, View
from .models import *
from .forms import *
from .smellDetector import *

"""class FormWizardView(SessionWizardView):
    template_name = "proyectos/requisitos-usuario/"
    form_list = [userRequirementForm1, userRequirementForm2]
    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })"""

class Cache():
	def __init__(self, user, admin):
		global username
		global administrador
		username = user
		if admin == "Si":
			administrador = True
		else:
			administrador = False

	def getData():
		return username, administrador
	
class CacheProyecto():
	def __init__(self, project):
		global proyecto
		proyecto = project

	def getProyecto():
		return proyecto

class CacheProyectoBoss():
	def __init__(self, boss):
		global jefe
		jefe = boss
	
	def getBoss():
		return jefe

class CacheRequisito():
	def __init__(self, requisito):
		global req
		req = requisito

	def getRequisito():
		return req

# Create your views here.
def login_admin(request):
	usuarios = []
	for usuario in Cuenta.objects.values():
		usuarios += [usuario]

	if request.method == 'POST':
        # Process the request if posted data are available
		email = request.POST['email']
		password = request.POST['password']
        # Check username and password combination if correct
		loginUser = False
		for usuario in usuarios:
			if usuario['correo'] == email and usuario['contraseña'] == password:
				loginUser = True
				break
		if loginUser:
			for users in Cuenta.objects.values():
				if users['correo'] == email: 
					Cache(users['nombre_usuario'], users['admin'])
					break
			#login(request, username)
			return home(request)
		else:
            # Incorrect credentials, let's throw an error to the screen.
			return render(request, 'accounts/login.html', {'error_message': 'Incorrect username and / or password.'})
	# No post data availabe, let's just show the page to the user.
	return render(request, 'accounts/login.html')

def home(request):
	username, administrador = Cache.getData()
	if administrador:
		num_user_requirements = RequisitoDeUsuario.objects.count()
		num_system_requirements = RequisitoSistema.objects.count()
		total_requirements = num_user_requirements+num_system_requirements

		total_proyects = Proyecto.objects.count()
		total_smells = 0
		projectsUser = []
		for project in Proyecto.objects.values():
			projectsUser += [project]

		stats = []
		for project in projectsUser:
			name = project['name']
			total_ru = 0
			total_rs = 0
			smells = 0
			reqs = []
			for userReq in RequisitoDeUsuario.objects.values():
				if project['id'] == userReq['proyecto_id_id']:
					reqs += [userReq['id']]
					total_ru += 1
			for sysReq in RequisitoSistema.objects.values():
				if project['id'] == sysReq['proyecto_id_id']:
					total_rs += 1
					reqs += [sysReq['id']]
			for req in reqs:
				for userReqSmells in AnalizisRu.objects.values():
					if req == userReqSmells['ru_codigo_id'] and userReqSmells['smell_codigo'] != "-":
						smell = userReqSmells['smell_codigo'].split(" ")
						smells += len(smell)
				for sysReqSmells in AnalizisRs.objects.values():
					if req == sysReqSmells['rs_codigo_id'] and sysReqSmells['smell_codigo'] != "-":
						smell = sysReqSmells['smell_codigo'].split(" ")
						smells += len(smell)
			total_smells += smells
			stats += [{
				'name':name, 
				'totalRU':total_ru, 
				'totalRS':total_rs,
				'smells': smells
			}]	
	
	else:
		for user in Cuenta.objects.values():
			if user['nombre_usuario'] == username:
				idUser = user['id']
				break
		
		projectsUser = []
		for project in AsignacionProyecto.objects.values():
			if project['cuenta_id'] == idUser:
				projectsUser += [project]
		
		for project in AsignacionJefeProyecto.objects.values():
			if project['cuenta_id'] == idUser:
				projectsUser += [project]
		
		num_system_requirements = 0
		num_user_requirements = 0
		
		stats = []
		total_smells = 0
		for project in projectsUser:
			for littleProject in Proyecto.objects.values():
				if littleProject['id'] == project['proyecto_id_id']:
					reqs = []
					ru_project = 0
					for userReq in RequisitoDeUsuario.objects.values():
						if littleProject['id'] == userReq['proyecto_id_id']:
							ru_project += 1
							reqs += [userReq['id']]
					rs_project = 0
					for sysReq in RequisitoSistema.objects.values():
						if littleProject['id'] == sysReq['proyecto_id_id']:
							rs_project += 1
							reqs += [sysReq['id']]
					num_system_requirements += rs_project
					num_user_requirements += ru_project
					smells = 0
					for req in reqs:
						for userReqSmells in AnalizisRu.objects.values():
							if req == userReqSmells['ru_codigo_id'] and userReqSmells['smell_codigo'] != "-":
								smell = userReqSmells['smell_codigo'].split(" ")
								smells += len(smell)
						for sysReqSmells in AnalizisRs.objects.values():
							if req == sysReqSmells['rs_codigo_id'] and sysReqSmells['smell_codigo'] != "-":
								smell = sysReqSmells['smell_codigo'].split(" ")
								smells += len(smell)
					total_smells += smells
					stats += [{
						'name':littleProject['name'], 
						'totalRU':ru_project, 
						'totalRS':rs_project,
						'smells': smells,
					}]
		total_requirements = num_user_requirements+num_system_requirements
		total_proyects = len(projectsUser)
	
	form = projectForms(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
	else:
		form = projectForms()

	

	context = {
        'total_requirements':total_requirements,
        'total_proyects':total_proyects,
		'total_smells': total_smells,
        'projects': projectsUser,
        'stats': stats,
		'form': form,
		'admin':administrador,
    }

	return render(request, 'accounts/dashboard.html', context=context)

def projects(request):
	username, administrador = Cache.getData()
	if administrador:
		projects = []
		for project in Proyecto.objects.values():
			projects += [project]

	else:
		for user in Cuenta.objects.values():
			if user['nombre_usuario'] == username:
				idUser = user['id']
				break
		projects = []
		projectsUser = []
		for project in AsignacionProyecto.objects.values():
			if project['cuenta_id'] == idUser:
				project['jefe'] = "No"
				projectsUser += [project]
		
		for project in AsignacionJefeProyecto.objects.values():
			if project['cuenta_id'] == idUser:
				project['jefe'] = "Si"
				projectsUser += [project]

		for project in projectsUser:
			for littleProject in Proyecto.objects.values():
				if littleProject['id'] == project['proyecto_id_id']:
					if project['jefe'] == "Si":
						littleProject['jefe'] = username
					if project['jefe'] == "No":
						for projectsBoss in AsignacionJefeProyecto.objects.values():
							if littleProject['id']==projectsBoss['proyecto_id_id']:
								for user in Cuenta.objects.values():
									if user['id'] == projectsBoss['cuenta_id']:
										littleProject['jefe'] = user['nombre_usuario']
										break
					projects += [littleProject]

	
	if request.method == 'POST':
		form = projectForms(request.POST)
		if form.is_valid():
			form.save()
			form.cleaned_data
			formDetail = projectSelectForm()
		else:
			projectSelected = request.POST['projectDetailSelect']
			CacheProyecto(projectSelected)
			return projectsDetails(request)
	else:
		form = projectForms()
		formDetail = projectSelectForm()
			
	context = {
		'form': form,
		'formDetail': formDetail,
		'admin':administrador,
		'projects': projects
	}
	return render(request, 'accounts/projects.html', context=context)

def users(request):
	username, administrador = Cache.getData()
	users = []
	for user in Cuenta.objects.values():
		users += [user]

	
	if request.method == 'POST':
		nombre_usuario = request.POST['username']
		correo = request.POST['correo']
		minipass = correo.split("@")
		password = minipass[0]
		admin = request.POST['admin']
		data = {
			'nombre_usuario': nombre_usuario,
			'correo': correo,
			'contraseña': password,
			'admin': admin
		}
		form = userForms(data)
		if form.is_valid():
			form.save()

	context = {
		'admin':administrador,
		'users':users,
	}
	return render(request, 'accounts/users.html', context=context)

def addSysReq(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False

	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	requisitosUsuario = []
	for requisito in RequisitoDeUsuario.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			for req in AnalizisRu.objects.values():
				if requisito['id'] == req['ru_codigo_id']:
						requisitosUsuario += [requisito]

	if request.method == 'POST':
		codigo = request.POST['codigoReq']
		titulo = request.POST['tituloReq']
		tipo = request.POST['tipoReq']
		costo = request.POST['costoReq']
		urgencia = request.POST['urgenciaReq']
		estado = request.POST['estadoReq']
		descripcion = request.POST['descripcionReq']
		userReq = request.POST['userReq']

		version = 1
		data = {
			'codigo':codigo,
			'titulo':titulo, 
			'tipo': tipo, 
			'costo': costo,
			'urgencia': urgencia, 
			'estado': estado, 
			'descripcion': descripcion,
			'version': version,
			'proyecto_id': projectDetail['id'], 
			'requisito_usuario_codigo':userReq
		}
		systemReq = systemRequirementForm(data)
		if systemReq.is_valid():
			systemReq.save()
			analisis = Analisis()
			resultado, resultadoDesc = analisis.iniciarAnalisis(titulo, "RS", descripcion)
			for sysRequi in RequisitoSistema.objects.values():
				if sysRequi['titulo'] == titulo:
					idReq = sysRequi['id']
					break
			if resultado == "":
				resultado = "-"
			if resultadoDesc == "":
				resultadoDesc = "-"
			dataAnalisis = {
				'smell_codigo': resultado,
				'version':version,
				'rs_codigo': idReq
			}
			dataAnalisisDesc = {
				'smell_codigo': resultadoDesc,
				'version':version,
				'rs_codigo': idReq
			}
			analisisDeRS = analisisRSform(dataAnalisis)
			if analisisDeRS.is_valid():
				analisisDeRS.save()
				analisisDeRSDesc = analisisRSDescform(dataAnalisisDesc)
				if analisisDeRSDesc.is_valid():
					analisisDeRSDesc.save()
					messages.info(request, 'Requisito guardado con exito')
	context = {
		'userReqs': requisitosUsuario,
		'admin':administrador,
	}
	return render(request, 'accounts/addSysRequirement.html', context=context)

def projectsDetails(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	
	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	idBoss = 0
	participantes = 0
	for asignacion in AsignacionJefeProyecto.objects.values():
		if asignacion['proyecto_id_id'] == projectDetail['id']:
			participantes += 1
			idBoss = asignacion['cuenta_id']
			break

	for asignacion in AsignacionProyecto.objects.values():
		if asignacion['proyecto_id_id'] == projectDetail['id']:
			participantes += 1
	
	boss = " "
	for user in Cuenta.objects.values():
		if user['id'] == idBoss:
			boss = user['nombre_usuario']
			break
	CacheProyectoBoss(boss)

	smells = 0
	requisitosUsuario = 0
	for requisito in RequisitoDeUsuario.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			requisitosUsuario += 1
			for req in AnalizisRu.objects.values():
				if requisito['id'] == req['ru_codigo_id'] and req['smell_codigo'] != "-":
						smell = req['smell_codigo'].split(" ")
						smells += len(smell)

	requisitosSistema = 0
	for requisito in RequisitoSistema.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			requisitosSistema += 1
			for req in AnalizisRs.objects.values():
				if requisito['id'] == req['rs_codigo_id'] and req['smell_codigo'] != "-":
						smell = req['smell_codigo'].split(" ")
						smells += len(smell)
	
	totalReq = requisitosSistema + requisitosUsuario

	context = {
		'user': username,
		'boss': boss,
		'projectName': proyecto,
		'smells': smells,
		'userReq': requisitosUsuario,
		'sysReq': requisitosSistema,
		'totalReq': totalReq,
		'participantes': participantes,
		'admin': administrador,
	}
	return render(request, 'accounts/projects-Dash.html', context=context)

def participantes(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()

	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False
	
	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break

	participant = []
	for asignacion in AsignacionJefeProyecto.objects.values():
		if asignacion['proyecto_id_id'] == projectDetail['id']:
			participant += [asignacion['cuenta_id']]
			break
	for asignacion in AsignacionProyecto.objects.values():
		if asignacion['proyecto_id_id'] == projectDetail['id']:
			participant += [asignacion['cuenta_id']]

	usersNoParticipa = []
	usersParticipa = []
	for user in Cuenta.objects.values():
		if user['admin'] == "No":
			if participant.__contains__(user['id']):
				usersParticipa += [user]
			else:
				usersNoParticipa += [user]

	if request.method == 'POST':
		userSelected = request.POST['userSelect']
		for user in Cuenta.objects.values():
			if user['nombre_usuario'] == userSelected:
				idUser = user['id']
				break
		data = {
			'cuenta':idUser,
			'proyecto_id':projectDetail['id']
		}
		asignarProyecto = asignarProyectoForm(data)
		if asignarProyecto.is_valid():
			asignarProyecto.save()

	context = {
		'bossProject': bossProject,
		'admin': administrador,
		'participantes': usersParticipa,
		'users': usersNoParticipa,
	}

	return render(request, 'accounts/projectParticipants.html', context=context)

def projectsUserReqs(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()

	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False
	
	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	smells = 0
	requisitosUsuario = []
	for requisito in RequisitoDeUsuario.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			
			for req in AnalizisRu.objects.values():
				if requisito['id'] == req['ru_codigo_id']:
					if req['smell_codigo'] != "-":
						smell = req['smell_codigo'].split(" ")
						smells += len(smell)
					else:
						smells += 0
			for reqs in AnalisisRuDesc.objects.values():
				if requisito['id'] == reqs['ru_codigo_id']:
					if reqs['smell_codigo'] != "-":
						smellsDesc = reqs['smell_codigo'].split(" ")
						smells += len(smellsDesc)
					else:
						smells += 0
					
					requisito['cantidad_smells'] = smells
					requisitosUsuario += [requisito]

	if request.method == 'POST':
		reqEdit = request.POST['editReq']
		CacheRequisito(reqEdit)
		return editRequisitoUsuario(request)

	context = {
		'bossProject': bossProject,
		'admin': administrador,
		'reqs': requisitosUsuario,
		'total_user_reqs':len(requisitosUsuario),
		'total_smell': smells,
	}

	return render(request, 'accounts/projectUserReqs.html', context=context)

def projectsSysReqs(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False

	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break

	smells = 0
		
	requisitosSistema = []
	for requisito in RequisitoSistema.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			for req in AnalizisRs.objects.values():
				if requisito['id'] == req['rs_codigo_id']:
					if req['smell_codigo'] != "-":
						smell = req['smell_codigo'].split(" ")
						smells += len(smell)
						requisito['smells'] = req['smell_codigo']
						requisito['cantidad_smells'] = len(smell)
					else:
						requisito['smells'] = req['smell_codigo']
						requisito['cantidad_smells'] = 0
					requisitosSistema += [requisito]
	
	context = {
		'bossProject': bossProject,
		'admin': administrador,
		'reqs': requisitosSistema,
		'total_smell': smells,
	}

	return render(request, 'accounts/projectSysReq.html', context=context)

def addUserReq(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False
	
	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	reqs = 0
	for requisito in RequisitoDeUsuario.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			reqs += 1

	if reqs < 10:
		codigoH = "RU00"+str(reqs)
	else:
		codigoH = "RU0"+str(reqs)

	if request.method == 'POST':
		codigo = codigoH
		titulo = request.POST['tituloReq']
		prioridad = request.POST['prioridadReq']
		tipo = request.POST['tipoReq']
		fuente = request.POST['fuenteReq']
		estabilidad = request.POST['estabilidadReq']
		urgencia = request.POST['urgenciaReq']
		estado = request.POST['estadoReq']
		costo = request.POST['costoReq']
		descripcion = request.POST['descripcionReq']
		version = 1

		data = {
			'codigo':codigo,
			'titulo':titulo,
			'prioridad':prioridad, 
			'tipo': tipo, 
			'fuente':fuente,
			'estabilidad':estabilidad,
			'urgencia': urgencia, 
			'estado': estado,
			'costo': costo,
			'descripcion': descripcion,
			'version': version,
			'proyecto_id': projectDetail['id']
		}

		userRequi = userRequirementForm(data)

		if userRequi.is_valid():
			userRequi.save()
			analisis = Analisis()
			resultado, resultadoDesc, feedbacktitle, feedbackdesc = analisis.iniciarAnalisis(titulo, "RU", descripcion)
			for sysRequi in RequisitoDeUsuario.objects.values():
				if sysRequi['titulo'] == titulo:
					idReq = sysRequi['id']
					break
			if resultado == "":
				resultado = "-"
				feedbacktitle = "-"
			if resultadoDesc == "":
				resultadoDesc = "-"
				feedbackdesc = "-"
			dataAnalisis = {
				'smell_codigo': resultado,
				'version':version,
				'feedback': feedbacktitle,
				'ru_codigo': idReq
			}
			dataAnalisisDesc = {
				'smell_codigo': resultadoDesc,
				'version':version,
				'feedback': feedbackdesc,
				'ru_codigo': idReq
			}
			analisisDeRU = analisisRUform(dataAnalisis)
			analisisDeRUDesc = analisisRUDescform(dataAnalisisDesc)
			if analisisDeRU.is_valid() and analisisDeRUDesc.is_valid():
				analisisDeRU.save()
				analisisDeRUDesc.save()
				messages.info(request, 'Requisito guardado con exito')

	context = {
		'admin':administrador,
		'total_reqs':codigoH,
	}
	return render(request, 'accounts/addUserRequirement.html', context=context)

def analisisRU(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False

	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	analisisReqUsuario = []
	for requisito in RequisitoDeUsuario.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			for req in AnalizisRu.objects.values():
				if requisito['id'] == req['ru_codigo_id'] and requisito['version'] == req['version']:
					requisito['smells'] = req
					for req in AnalisisRuDesc.objects.values():
						if requisito['id'] == req['ru_codigo_id'] and requisito['version'] == req['version']:
							requisito['smells_desc'] = req
							analisisReqUsuario+=[requisito]
							break	
	#print (requisito)
	context = {
		'admin':administrador,
		'analisisRUs':analisisReqUsuario,
	}
	return render(request, 'accounts/analisisUserReq.html', context=context)

def analisisRS(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False

	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break
	
	analisisReqSistema = []
	for requisito in RequisitoSistema.objects.values():
		if requisito['proyecto_id_id'] == projectDetail['id']:
			for req in AnalizisRs.objects.values():
				if requisito['id'] == req['rs_codigo_id'] and requisito['version'] == req['version']:
					requisito['smells'] = req
					for req in AnalizisRs.objects.values():
						if requisito['id'] == req['rs_codigo_id'] and requisito['version'] == req['version']:
							requisito['smells_desc'] = req
							analisisReqSistema+=[requisito]
							break
	#print(requisito)
	context = {
		'admin':administrador,
		'analisiRSs':analisisReqSistema,
	}
	return render(request, 'accounts/analisisSysReq.html', context=context)

def editRequisitoUsuario(request):
	username, administrador = Cache.getData()
	proyecto = CacheProyecto.getProyecto()
	jefeProyecto = CacheProyectoBoss.getBoss()
	reqToEdit = CacheRequisito.getRequisito()
	if username == jefeProyecto:
		bossProject = True
	else:
		bossProject = False
	
	for project in Proyecto.objects.values():
		if project['name'] == proyecto:
			projectDetail = project
			break

	for requi in RequisitoDeUsuario.objects.values():
		if requi['titulo'] == reqToEdit and requi['proyecto_id_id'] == projectDetail['id']:
			reqToEditT=requi['id']
			requisitoToEdit = requi
			break

	requisito = get_object_or_404(RequisitoDeUsuario, pk=reqToEditT)
	print (int(requisitoToEdit['version'])+1)
	
	"""if request.method == 'POST':
		codigo = requisitoToEdit['codigo']
		titulo = request.POST['tituloReqEdit']
		prioridad = request.POST['prioridadReq']
		tipo = request.POST['tipoReq']
		fuente = request.POST['fuenteReq']
		estabilidad = request.POST['estabilidadReq']
		urgencia = request.POST['urgenciaReq']
		estado = request.POST['estadoReq']
		costo = request.POST['costoReq']
		descripcion = request.POST['descripcionReq']
		version = int(requisitoToEdit['version'])+1

		data = {
			'codigo':requisitoToEdit['codigo'],
			'titulo':titulo,
			'prioridad':prioridad, 
			'tipo': tipo, 
			'fuente':fuente,
			'estabilidad':estabilidad,
			'urgencia': urgencia, 
			'estado': estado,
			'costo': costo,
			'descripcion': descripcion,
			'version': version,
			'proyecto_id': requisitoToEdit['proyecto_id']
		}

		edit = userRequirementForm(data, instance=requisito)
		if edit.is_valid():
			edit.save()
			analisis = Analisis()
			resultado, resultadoDesc, feedbacktitle, feedbackdesc = analisis.iniciarAnalisis(titulo, "RU", descripcion)
			for sysRequi in RequisitoDeUsuario.objects.values():
				if sysRequi['titulo'] == titulo:
					idReq = sysRequi['id']
					break
			if resultado == "":
				resultado = "-"
				feedbacktitle = "-"
			if resultadoDesc == "":
				resultadoDesc = "-"
				feedbackdesc = "-"
			dataAnalisis = {
				'smell_codigo': resultado,
				'version':version,
				'feedback': feedbacktitle,
				'ru_codigo': idReq
			}
			dataAnalisisDesc = {
				'smell_codigo': resultadoDesc,
				'version':version,
				'feedback': feedbackdesc,
				'ru_codigo': idReq
			}
			analisisDeRU = analisisRUform(dataAnalisis)
			analisisDeRUDesc = analisisRUDescform(dataAnalisisDesc)
			if analisisDeRU.is_valid() and analisisDeRUDesc.is_valid():
				analisisDeRU.save()
				analisisDeRUDesc.save()
				messages.info(request, 'Requisito editado con exito')

	else:
		formEditReq = userRequirementForm(instance=requisito)"""

	#print (edit)
	context = {
		'admin':administrador,
		'req':requisitoToEdit,
		#'formEdit': formEditReq,
	}
	return render(request, 'accounts/editUserRequirement.html', context=context)