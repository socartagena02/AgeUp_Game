from django.contrib import admin
from django.urls import path
from cognitivos import views


urlpatterns = [
    path('inicio/', views.index, name='index'),
    path('admin/', admin.site.urls),
  #  path('memorice/', )

    
]
