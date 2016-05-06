from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.loader import get_template
from models import Pages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
# Create your views here.

@csrf_exempt
def mostrar(request, resource):

	cont_type = "text/html"

	if request.method == "GET":
		try:
			res = Pages.objects.get(name=resource)
			respuesta = res.page
			if res.name[0:3] == "css":
				cont_type = "text/css"
			else:
				template = get_template('index.html')
				return HttpResponse(template.render(Context({'page' : respuesta})), content_type='text/html')
		except ObjectDoesNotExist:
			return HttpResponse(resource + " does not exist")

	elif request.method == "PUT":
		body = request.body
		page = Pages(name=resource, content=body)
		page.save()
		respuesta = "Nuevo contenido insertado correctamente!"

	else:
		return HttpResponse("Metodo incorrecto")

	return HttpResponse(respuesta, content_type=cont_type)
