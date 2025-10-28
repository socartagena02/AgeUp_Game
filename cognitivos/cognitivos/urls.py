# cognitivos/urls.py
from django.urls import path
from . import views  # El punto . importa views.py de la misma carpeta

urlpatterns = [
    # 1. Vista del menú principal (el carrusel)
    path('', views.index, name='index'), 

    # 2. Vistas para cada juego (ESTAS SON LAS NUEVAS)
    path('memorice/', views.memorice_view, name='memorice'),
    path('simon-dice/', views.simon_dice_view, name='simon_dice'),
    path('traza-camino/', views.traza_camino_view, name='traza_camino'),
]