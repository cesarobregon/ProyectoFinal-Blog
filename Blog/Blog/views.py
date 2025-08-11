

from django.shortcuts import render

from apps.articulos.models import Articulo


def Home(request):       
    
    ultimos_articulos = Articulo.objects.order_by('-creado')[:3]  # Los 3 más recientes
    es_moderador = request.user.is_authenticated and request.user.groups.filter(name='Moderador').exists()
    
    return render(request, 'home.html', {'ultimos_articulos': ultimos_articulos,'es_moderador': es_moderador})

