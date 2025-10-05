from django.http import HttpResponse
from django.shortcuts import render
import subprocess
def index(request):
    context = {
    }
    return render(request, 'template.html', context)
def memorice_script(request):
    try:
        juego_path = r'C:\Users\Acer\Desktop\AgeUp_Game\memorice\memorice.py'
        subprocess.Popen(['python', juego_path])
        m = "¡Memorice ya se esta ejecutando!"
    
    except Exception as e:
        m_error = f"Error: {str(e)}"
    return render(request, 'memorice_interfaz.html', {'mensaje': m})