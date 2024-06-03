from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    # Incluindo as urls contidas em auth_usuario
    path('',include('aut_usuario.urls')),
	path('admin/',admin.site.urls),
]