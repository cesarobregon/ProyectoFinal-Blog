from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy

# Create your views here.

class registrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    
    def form_valid(self,form):
        messages.success(self.request, 'Registro Exitoso. Por favor, inicia sesion')
        form.save()
        
        return redirect('apps.usuario:login')

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Login Exitoso')
        
###class LogoutUsuario(LogoutView):
#    template_name = 'registration/logout.html'
#    
#    def get_success_url(self):
#        messages.success(self.request, 'Logout Exitoso')
#        
#        return reverse('apps.usuario:logout')

class LogoutUsuario(LogoutView):
    next_page = reverse_lazy('path_home')  

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Logout exitoso')
        return super().dispatch(request, *args, **kwargs)