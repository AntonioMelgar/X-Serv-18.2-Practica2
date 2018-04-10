#!/usr/bin/python3

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import url

formulario = """
 <form action="" method="POST">
  URL:<br>
  <input type="text" name="URL" value=""><br>
  <input type="submit" value="Enviar">
</form> 
"""

def guardar(elem, num_elem):
	g = url(original = elem, acortada = '/' + str(num_elem))
	g.save()

def Modo_POST(recurso, lista):
	if recurso == "":
		respuesta = formulario + 'Error: introduce la url que desee acortar' + '<br>'

	else: 
		if (recurso.find('http') == 0) or (recurso.find('https') == 0):
			respuesta = recurso
		else:
			respuesta = 'http://' + recurso 
		
		try:
			url_compleja = url.objects.get(original=respuesta)

			respuesta = formulario + '<html><body><p><a href = "' + respuesta + '">' + url_compleja.acortada + '</a> --> <a href = "' + respuesta + '">' + respuesta + '<br></a></p></body></html>'
			
		except url.DoesNotExist:
			num_elem = 0
			for URL in lista:
				num_elem += 1	
		
			guardar(respuesta, num_elem)

			respuesta = formulario + '<html><body><p><a href = "' + respuesta + '"> /' + str(num_elem) + '</a> --> <a href = "' + respuesta + '">' + respuesta + '<br></a></p></body></html>'		
		
	
	return respuesta		
			

def Modo_GET_mostrar(lista):
	salida = ""
	for URL in lista:
		salida += '<p><a href = ' + '"' + URL.original + '">' + URL.acortada + '</a> --> <a href = "' + URL.original + '">' + URL.original + '<br>'
		
	respuesta = '<html><body>' + formulario + salida + '</a></p></body></html></html>'			
	
	return respuesta

def Modo_GET_redirect(acort):
	try:
		url_compleja = url.objects.get(acortada=acort)
		url_orig = url_compleja.original
		
		respuesta = url_orig
		logic = True

	except url.DoesNotExist:
		respuesta = "Dicha url acortada no existe, prueba otra vez"
		logic = False

	return respuesta, logic

@csrf_exempt
def barra(request):
	if request.method == "GET":
		lista = url.objects.all()
		respuesta = Modo_GET_mostrar(lista)	
		
	elif request.method == "POST":
		lista = url.objects.all()
		respuesta = Modo_POST(request.POST['URL'], lista)

	return HttpResponse(respuesta)

def redirect(request, numero):
	if request.method == "GET":
		acort = "/" + numero
		respuesta, logic = Modo_GET_redirect(acort)
	
	if logic == True:
		return HttpResponseRedirect(respuesta)
	
	else:
		return HttpResponse(respuesta)




