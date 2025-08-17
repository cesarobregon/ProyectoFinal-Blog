from django.shortcuts import render, get_object_or_404
from apps.articulos.models import Articulo
from .models import Categoria  # si tienes un modelo de categorías

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/base_categorias.html', {'categorias': categorias})

def filtrar_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    articulos = Articulo.objects.filter(categoria=categoria)

    context = {
        'categoria': categoria,
        'articulos': articulos
    }
    return render(request, 'categorias/filtrar_categoria.html', context)