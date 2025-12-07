import os
import subprocess
import sys
from django.conf  import settings
from elevenlabs  import ElevenLabs
from django.http import HttpResponse
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

# definir tts para Elevenlabs
def tts_eleven(request):
    texto = request.GET.get("texto", "")
    
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API"))
    
    audio = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Voz de Rachel
        model_id="eleven_multilingual_v2",
        text=texto
    )
    
    audio_bytes = b"".join(audio)
    
    response = HttpResponse(audio_bytes, content_type="audio/mpeg")
    response['Content-Disposition'] = 'inline; filename="voz.mp3'
    return response

# Página de Ranking
def ranking(request):
    return render(request, 'ranking_interfaz.html')

# Página de evaluación
def evaluacion(request):
    return render(request, 'evaluacion_interfaz.html')