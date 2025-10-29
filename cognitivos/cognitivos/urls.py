# cognitivos/urls.py
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index'), 

    path('memorice_script/', views.memorice_script, name='memorice_script'),
    path('simon-dice/', views.simon_dice_view, name='simon_dice'),
    path('traza-camino/', views.traza_camino_view, name='traza_camino'),
]