from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'users/home.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado

    def get_success_url(self):
        return reverse_lazy('home')  # Reemplaza 'home' con la URL a la que quieras redirigir

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige a la página de login después de cerrar sesión
    template_name = 'users/logged_out.html'  # Asegúrate de tener esta plantilla
