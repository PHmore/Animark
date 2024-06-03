# Como feito pelo professor usamos a view do sistema básico de configuração na própria pasta raiz

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
class Login (View):
	
	def get(self, request):
		contexto = {'mensagem':''}
		print("Entrou no get")
		if not request.user.is_authenticated:
			return render(request, 'aut_usuario/login.html',contexto)
		else:
			return redirect("/veiculo")

	def post(self, request):

		# Obtém as credenciais de autenticação do formulário
		# O 'usuario' e a 'senha' devem ser os mesmo nomeados na view
		usuario = request.POST.get ('email',None)
		senha = request.POST.get('senha',None)

		# Verifica as credenciais de autenticação fornecidas
		user = authenticate(request, username=usuario, password=senha)
		print("Qualquer coisa")
		if user is not None:

			# Verifica se o usuário ainda está ativo no sistema
			if user.is_active:
				login(request, user)
				# return HttpResponse('Usuário autenticacao com sucesso!')
				return redirect("/veiculo")

			return render(request, 'aut_usuario/login.html',{'mensagem': 'Usuário inativo'})
		print('Usuário ou senha inválido')
		return render(request, 'aut_usuario/login.html',{'mensagem':'Usuário ou senha incorretos'})
	
# Caso formos em Inspercionar, Aplicativos e formos em cookies veremos que os cookies de sessão foram apagados
class Logout (View):
	def get(self, request):
		logout(request)
		return redirect(settings.LOGIN_URL)
	
class Cadastro (View):
	def get(self, request):
		print("Renderizando cadastro")
		return render(request,'aut_usuario/cadastro.html')
	
	def post(self, request):
		username = request.POST.get('email',None)
		email = request.POST.get('email',None)
		senha = request.POST.get('senha',None)
		print("Realizando cadastro de: email: ",email," Senha: ",senha)
		
		user = User.objects.filter(email=email).first()
		
		if user:
			return HttpResponse("Já existe um usuário com este email")
		
		user = User.objects.create_user(username=username, email=email, password=senha)
		if user:
			return HttpResponse("Usuário criado com sucesso")

    

# def index(request):
# 	return render(request,'index.html')

# def cadastro(request):
# 	return render(request,'cadastro.html')