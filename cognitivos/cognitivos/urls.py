from django.contrib import admin
from django.urls import path
from cognitivos import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('memorice_script/', views.memorice_script, name='memorice_script')

    
]
