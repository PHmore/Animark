# Como feito pelo professor usamos a view do sistema básico de configuração na própria pasta raiz

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .serializers import RegisterSerializer

# Create your views here.
class Login (View):
	
	def get(self, request):
		contexto = {'mensagem':''}
		print("Entrou no get")
		if not request.user.is_authenticated:
			return render(request, 'aut_usuario/login.html',contexto)
		else:
			return redirect("/to_do_list")

	def post(self, request):

		# Obtém as credenciais de autenticação do formulário
		# O 'usuario' e a 'senha' devem ser os mesmo nomeados na view
		usuario = request.POST.get ('email',None)
		senha = request.POST.get('senha',None)

		# Verifica as credenciais de autenticação fornecidas
		user = authenticate(request, username=usuario, password=senha)
		if user is not None:

			# Verifica se o usuário ainda está ativo no sistema
			if user.is_active:
				login(request, user)
				# return HttpResponse('Usuário autenticacao com sucesso!')
				return redirect("/to_do_list")

			return render(request, 'aut_usuario/login.html',{'mensagem': 'Usuário inativo'})
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
			
			return render(request, 'aut_usuario/cadastro.html',{'mensagem':'Já existe um usuário com este email'})
		
		user = User.objects.create_user(username=username, email=email, password=senha)
		if user:
			
			return render(request, 'to_do_list',{'mensagem':'Usuário cadastrado com sucesso'})

class LoginAPI(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(
			data = request.data,
			context={
				'request':request
			}
		)
		serializer.is_valid(raise_exception=True)
		user=serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'id':user.id,
			'nome':user.first_name,
			'email':user.email,
			'token':token.key
		})
	
class LogoutAPI(APIView):
    def post(self, request):
        if request.auth:
            request.auth.delete()
        logout(request)
        return Response({'mensagem': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)

# views.py

class CadastroAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def index(request):
# 	return render(request,'index.html')

# def cadastro(request):
# 	return render(request,'cadastro.html')