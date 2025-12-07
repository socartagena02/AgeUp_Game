from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views  

urlpatterns = [
    path('', views.index, name='index'), 

    path('memorice_script/', views.memorice_script, name='memorice_script'),
    path('simon-dice/', views.simon_dice_view, name='simon_dice_view'),
    path('simon-dice/basico/', views.nivel_basico_view, name='nivel_basico'),
    path('simon-dice/intermedio/', views.nivel_intermedio_view, name='nivel_intermedio'),
    path('simon-dice/avanzado/', views.nivel_avanzado_view, name='nivel_avanzado'),
    path('traza-camino/', views.traza_camino_view, name='traza_camino'),
    path('tts-eleven/', views.tts_eleven, name="tts-eleven"),
    path('ranking/', views.ranking, name="ranking"),
    path('evaluacion/', views.evaluacion, name="evaluacion"),
]

re_path(r'^favicon\ico$',
        RedirectView.as_view(
            url = staticfiles_storage.url('assets/favicon.ico'),  # Carpeta de imagenes 
            permanent =False
        ),
       name="favicon" 
    ),