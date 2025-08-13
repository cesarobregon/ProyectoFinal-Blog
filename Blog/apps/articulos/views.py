
from django.shortcuts import render
from django.views.generic.detail import DetailView    #Esto es una vista preparada para mostrar el detalle de un proyecto
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Articulo            #Esto es necesario para traer lo que está en la clase Producto
from .forms import FormularioCrearArticulo


from django.contrib import messages     #Todo esto es para el boton de editar
from django.shortcuts import redirect
from django.urls import reverse


class soloMod(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Moderador').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied  # Si está logueado pero no es moderador → 403
        return super().handle_no_permission()  # Si no está logueado → lo lleva a login


def Listar_Articulos(request):
    todos = Articulo.objects.all().order_by('-fecha_publicacion')  # ⬅️ Ordena del más nuevo al más viejo
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
        context['es_moderador'] = (
            self.request.user.is_authenticated
            and self.request.user.groups.filter(name='Moderador').exists()
        )
        return context



class Crear_Articulo(soloMod, CreateView):
    model = Articulo
    template_name = 'articulos/crear.html'
    form_class = FormularioCrearArticulo
    success_url = reverse_lazy('articulos:path_listar_articulos')
    


class EditarArticuloView(UpdateView):
    model = Articulo
    form_class = FormularioCrearArticulo
    template_name = 'articulos/editar.html'

    def get_success_url(self):
        return reverse('articulos:path_detalle_articulo', kwargs={'pk': self.object.pk})
    
    



class EliminarArticuloView(DeleteView):
    model = Articulo
    template_name = 'articulos/eliminar.html'
    success_url = reverse_lazy('articulos:path_listar_articulos')
    
    
