from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditarPerfilForm

def home(request):
    return render(request, 'users/home.html')

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado

    def get_success_url(self):
        user = self.request.user
        # Lista ordenada de grupos y sus correspondientes nombres de URL
        group_redirects = [
            ('Contadora', 'finanzas:home'),
            ('Visualizador', 'finanzas:home'),
            # Añade más grupos y sus URLs aquí si es necesario
        ]

        # Iterar sobre los grupos según el orden definido y redirigir al primero que coincida
        for group_name, url_name in group_redirects:
            if user.groups.filter(name=group_name).exists():
                return reverse_lazy(url_name)

        # URL por defecto si el usuario no pertenece a ningún grupo específico
        return reverse_lazy('finanzas:home')  # Reemplaza con tu URL por defecto

    def form_invalid(self, form):
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige a la página de login después de cerrar sesión
    template_name = 'users/logged_out.html'  # Asegúrate de tener esta plantilla



def perfil_usuario(request):
    # Obtenemos el usuario actual
    usuario = request.user

    # Pasamos la información del usuario al contexto para usar en el template
    context = {
        'usuario': usuario,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'users/editar_perfil.html', context)