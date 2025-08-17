from django.urls import path
from . import views

app_name = 'apps.categorias'

urlpatterns = [
    path('', views.lista_categorias, name='lista_categorias'),
    path('<int:categoria_id>/', views.filtrar_por_categoria, name='filtrar_categoria'),
]