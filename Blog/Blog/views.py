from django.shortcuts import render

from apps.articulos.models import Articulo


def Home(request):
    # Artículo destacado (si no hay, cae al más reciente)
    articulo_destacado = (
        Articulo.objects.filter(destacado=True).order_by("-creado").first()
        or Articulo.objects.order_by("-creado").first()
    )

    # Últimos 3, excluyendo el destacado para no repetir
    ultimos_articulos = (
        Articulo.objects.exclude(pk=getattr(articulo_destacado, "pk", None))
        .order_by("-creado")[:4]
    )

    es_moderador = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Moderador").exists()
    )

    ctx = {
        "articulo_destacado": articulo_destacado,
        "ultimos_articulos": ultimos_articulos,
        "es_moderador": es_moderador,
    }
    return render(request, "home.html", ctx)