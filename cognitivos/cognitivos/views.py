# cognitivos/views.py
from django.shortcuts import render

def index(request):
    """
    Esta es tu vista del MENÚ PRINCIPAL (el carrusel).
    """
    context = {}
    return render(request, 'template.html', context)

# --- VISTAS PARA LOS JUEGOS ---
# (Estas son las funciones que faltaban y que causaron el error)

def memorice_view(request):
    """
    Esta vista carga el HTML del juego Memorice.
    """
    # (Asegúrate de tener 'memorice_interfaz.html' en 'templates')
    return render(request, 'memorice_interfaz.html')

def simon_dice_view(request):
    """
    Esta vista carga el HTML del juego Simon Dice.
    """
    # (Asegúrate de crear 'simon_dice_interfaz.html' en 'templates')
    return render(request, 'simon_dice_interfaz.html')

def traza_camino_view(request):
    """
    Esta vista carga el HTML del juego Traza mi Camino.
    """
    # (Asegúrate de crear 'traza_camino_interfaz.html' en 'templates')
    return render(request, 'traza_camino_interfaz.html')