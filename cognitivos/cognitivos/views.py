import os
import subprocess
import sys

from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'template.html', context)

def memorice_script(request):
    if request.method == 'POST':
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            project_root = os.path.dirname(base_dir)
            
            memorice_path = os.path.join(project_root, 'memorice', 'memorice.py')
            
            print(f"🔍 Buscando en: {memorice_path}")
            print(f"📁 Existe: {os.path.exists(memorice_path)}")
            
            if not os.path.exists(memorice_path):
                memorice_path = os.path.join(project_root, 'memorice.py')
                print(f"🔍 Buscando alternativa: {memorice_path}")
                print(f"📁 Existe: {os.path.exists(memorice_path)}")
            
            if os.path.exists(memorice_path):
                print("✅ Juego Cargando..")
                game_dir = os.path.dirname(memorice_path)
                subprocess.Popen([sys.executable, memorice_path], cwd=game_dir, shell=True)
        except Exception as e:
            m_error = f"Error: {str(e)}"
        return render(request, 'memorice_interfaz.html')

def simon_dice_view(request):
    return render(request, 'secuencia_colores/index.html')

def nivel_basico_view(request):
    return render(request, 'secuencia_colores/nivel-basico.html')

def nivel_intermedio_view(request):
    return render(request, 'secuencia_colores/nivel-intermedio.html')

def nivel_avanzado_view(request):
    return render(request, 'secuencia_colores/nivel-avanzado.html')

def traza_camino_view(request):
    return render(request, 'traza_camino_interfaz.html')