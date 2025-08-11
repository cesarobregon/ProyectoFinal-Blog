
from django.shortcuts import render
from django.views.generic.detail import DetailView    #Esto es una vista preparada para mostrar el detalle de un proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Articulo            #Esto es necesario para traer lo que está en la clase Producto
from .forms import FormularioCrearArticulo


class soloMod(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderador').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied  # Si está logueado pero no es moderador → 403
        return super().handle_no_permission()  # Si no está logueado → lo lleva a login


def Listar_Articulos(request):
    todos = Articulo.objects.all()
    es_moderador = request.user.is_authenticated and request.user.groups.filter(name='Moderador').exists()
    return render(request, 'articulos/listar.html', {
        'articulos': todos,
        'es_moderador': es_moderador
    })



#VISTA BASADA EN CLASES
class Detalle_Articulo(DetailView):
    
    template_name = 'articulos/detalle.html'
    model = Articulo
    context_object_name = 'articulo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.request.GET.get('orden', 'reciente')  # valor por defecto 'reciente'
        
        # Obtener los comentarios ordenados - corregimos esta parte
        comentarios = self.object.MisComentarios()  # Asegúrate que MisComentarios es el related_name correcto
        
        # Aplicamos el orden
        if orden == 'antiguo':
            comentarios = comentarios.order_by('creado')
        else:
            comentarios = comentarios.order_by('-creado')
        
        context['comentarios'] = comentarios
        return context



class Crear_Articulo(soloMod, CreateView):
    model = Articulo
    template_name = 'articulos/crear.html'
    form_class = FormularioCrearArticulo
    success_url = reverse_lazy('articulos:path_listar_articulos')
    
    
