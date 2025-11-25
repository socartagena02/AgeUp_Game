import pygame
import time
import sys
import math
import random
import os
import csv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import webbrowser
import subprocess  # <- NUEVO IMPORT


pygame.init()
pygame.font.init()
pygame.mixer.init()

ruta_icon = os.path.join(os.path.dirname(__file__),"imagenes_memorice", "favicon-32x32.png")
icon = pygame.image.load(ruta_icon)
pygame.display.set_icon(icon)

DATA_FILE = 'memorice_data.csv'

directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_imagenes = os.path.join(directorio_actual, "imagenes_memorice")

# 🆕 FUNCIÓN PARA ABRIR RANKING
def abrir_ranking():
    """Abre la página de ranking en el navegador web"""
    try:
        url = "http://127.0.0.1:8000/ranking/"
        # Método más confiable para Windows
        subprocess.Popen(f'start {url}', shell=True)
        print("✅ Ranking abierto en el navegador")
    except Exception as e:
        print(f"❌ Error al abrir ranking: {e}")
        print(f"🌐 Por favor, abre manualmente: http://127.0.0.1:8000/ranking/")

niveles = {
    "basico": {
        "nombre": "Básico",
        "niveles": [
            {  # Nivel 1 Básico
                "filas": 2, 
                "columnas": 2,  
                "tiempo": 0.5, 
                "puntos_par": 100,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 60,
                "numero_nivel": 1
            },
            {  # Nivel 2 Básico
                "filas": 2,  
                "columnas": 3, 
                "tiempo": 0.7, 
                "puntos_par": 120,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 75,
                "numero_nivel": 2
            },
            {  # Nivel 3 Básico
                "filas": 2, 
                "columnas": 4, 
                "tiempo": 1.0, 
                "puntos_par": 150,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 90,
                "numero_nivel": 3
            }
        ]
    },
    "intermedio": {
        "nombre": "Intermedio",
        "niveles": [
            {  # Nivel 1 Intermedio
                "filas": 3, 
                "columnas": 2,  
                "tiempo": 1.0, 
                "puntos_par": 150,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 75,
                "numero_nivel": 1
            },
            {  # Nivel 2 Intermedio
                "filas": 3, 
                "columnas": 4,  
                "tiempo": 1.3, 
                "puntos_par": 180,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 90,
                "numero_nivel": 2
            },
            {  # Nivel 3 Intermedio
                "filas": 3, 
                "columnas": 4, 
                "tiempo": 1.5, 
                "puntos_par": 200,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 105,
                "numero_nivel": 3
            }
        ]
    },
    "avanzado": {
        "nombre": "Avanzado",
        "niveles": [
            {  # Nivel 1 Avanzado
                "filas": 4, 
                "columnas": 3, 
                "tiempo": 1.5, 
                "puntos_par": 200,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 90,
                "numero_nivel": 1
            },
            {  # Nivel 2 Avanzado
                "filas": 4, 
                "columnas": 4, 
                "tiempo": 1.8, 
                "puntos_par": 220,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 105,
                "numero_nivel": 2
            },
            {  # Nivel 3 Avanzado
                "filas": 4, 
                "columnas": 5,  
                "tiempo": 2.0, 
                "puntos_par": 250,
                "ancho_ventana": 800,  
                "alto_ventana": 600,
                "tiempo_max": 120,
                "numero_nivel": 3
            }
        ]
    }
}

# Estado del juego
m = "menu"
jugando = "jugando"
ganaste = "ganaste"
tiempo_agotado = "tiempo_agotado"
nivel_completado = "nivel_completado"
registro_ganador = "registro_ganador"
estado_actual = m

# Variables globales para control de niveles
nivel_seleccionado = None
nivel_actual_numero = 1  # Nivel actual dentro de la dificultad
max_nivel_alcanzado = 0

# Configuración de dimensiones para el menú
anchura_pantalla_menu = 800
altura_pantalla_menu = 600
altura_boton = 50
medida_cuadro = 120
nombre_imagen_oc = os.path.join(directorio_imagenes, "gray_pale.png")

# Cargar imagen oculta
try:
    imagen_oculta = pygame.image.load(nombre_imagen_oc)
    imagen_oculta = pygame.transform.scale(imagen_oculta, (medida_cuadro, medida_cuadro))
except:
    imagen_oculta = pygame.Surface((medida_cuadro, medida_cuadro))
    imagen_oculta.fill((150, 150, 150))

# Colores
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (31, 136, 229)
color_verde = (76, 175, 80)
color_rojo = (244, 67, 54)
color_morado = (156, 39, 176)
color_naranja = (255, 194, 59)
color_Nbasico = (255, 107, 130)
color_Nintermedio = (174, 107, 255)
color_Navanzado = (255, 203, 107)
color_amarillo = (255, 235, 59)
color_rosado_oscuro = (33, 8, 23)
color_celeste = (184, 255, 228)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 48)
fuente_grande = pygame.font.SysFont("Arial", 36)
fuente_media = pygame.font.SysFont("Arial", 24)
fuente_pequena = pygame.font.SysFont("Arial", 18)

# Variables globales del juego
cuadros = []
anchura_pantalla = anchura_pantalla_menu
altura_pantalla = altura_pantalla_menu
boton = None
ultimos_segundos = None
puede_jugar = True
juego_iniciado = False
x1, y1 = None, None
x2, y2 = None, None
puntuacion = 0
puntuacion_total = 0

total_clicks = 0
total_fallos = 0
edad = ""
apodo = ""
patologias = ""
genero = ""
tiempos_reaccion = []
parejas_encontradas = 0
mostrar_imagen_seg = 0.5

# Variables del tiempo
tiempo_inicio_nl = 0
tiempo_restante = 0
tiempo_limite = 90
tiempo_extra_pareja_encontrada = 10

# Variables para mostrar imágenes al inicio
mostrar_al_inicio = False
tiempo_inicio_juego = 0
duracion_muestra_inicio = 1.2

# Botones
boton_volver = pygame.Rect(0, 0, 200, 60)
boton_reintentar = pygame.Rect(0, 0, 200, 60)
boton_menu_tiempo = pygame.Rect(0, 0, 200, 60)
boton_siguiente_nivel = pygame.Rect(0, 0, 200, 60)
boton_guardar_datos = pygame.Rect(300, 480, 200, 50)

# Botones de género con emojis (POSICIONES CORREGIDAS)
boton_femenino = pygame.Rect(250, 400, 150, 50)    # Botón para Femenino
boton_masculino = pygame.Rect(420, 400, 150, 50)   # Botón para Masculino

# Campos de registro
registro_apodo = pygame.Rect(250, 220, 300, 40)
registro_edad = pygame.Rect(250, 280, 300, 40)
registro_patologias = pygame.Rect(250, 340, 300, 40)

# Input para registro
input_activo = "apodo"
texto_apodo_input = ""
texto_edad_input = ""
texto_patologias_input = ""
texto_genero_input = ""

class Cuadro:
    def __init__(self, nombre_imagen):  
        self.mostrar = False
        self.descubierto = False
        self.nombre_imagen = nombre_imagen
        ruta_imagen = os.path.join(directorio_imagenes, nombre_imagen)  
        try:
            self.imagen_real = pygame.image.load(ruta_imagen)
            self.imagen_real = pygame.transform.scale(self.imagen_real, (medida_cuadro, medida_cuadro))
        except:
            self.imagen_real = pygame.Surface((medida_cuadro, medida_cuadro))
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            self.imagen_real.fill(color)
            font = pygame.font.SysFont("Arial", 20)
            text = font.render(nombre_imagen.split("/")[-1], True, (255, 255, 255))
            self.imagen_real.blit(text, (10, medida_cuadro // 2 - 10))

def obtener_config_nivel_actual():
    if nivel_seleccionado and nivel_actual_numero <= len(niveles[nivel_seleccionado]["niveles"]):
        return niveles[nivel_seleccionado]["niveles"][nivel_actual_numero - 1]
    return None

# --- Función para guardar datos de la partida ---
def guardar_datos_partida():
    if total_clicks == 0: 
        return

    tiempo_reaccion_promedio = sum(tiempos_reaccion) / len(tiempos_reaccion) if tiempos_reaccion else 0

    # Datos a guardar
    datos = {
        'apodo': apodo,
        'edad': edad,
        'patologias': patologias,
        'genero': genero,
        'total_clicks': total_clicks,
        'fallos': total_fallos,
        'tiempo_reaccion_promedio': round(tiempo_reaccion_promedio, 2),
        'puntuacion': puntuacion,
        'nivel_dificultad': nivel_seleccionado
    }

    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=datos.keys())
        if not file_exists:
            writer.writeheader() # Escribir encabezado solo si el archivo es nuevo
        writer.writerow(datos)
    print(f"📝 Datos de la partida guardados en {DATA_FILE}")

def tiempo_obtenido():
    global tiempo_restante, tiempo_limite
    tiempo_obtenido = int(tiempo_limite - tiempo_restante) 
    return tiempo_obtenido

def registro_jugador():
    global apodo, edad, patologias, genero, texto_apodo_input, texto_edad_input, texto_patologias_input, texto_genero_input
    
    pantalla_juego.fill(color_azul)
    
    titulo = fuente_titulo.render("¡Guarda el puntaje porfavor!", True, color_blanco)
    instruccion = fuente_media.render("Ingresa tus datos pleasee:", True, color_blanco)
    
    pantalla_juego.blit(titulo, (anchura_pantalla_menu // 2 - titulo.get_width() // 2, 80))
    pantalla_juego.blit(instruccion, (anchura_pantalla_menu // 2 - instruccion.get_width() // 2, 150))
    
    # Dibujar campos de texto
    color_campo_activo = color_amarillo
    pygame.draw.rect(pantalla_juego, color_campo_activo if input_activo == "apodo" else color_blanco, registro_apodo, border_radius=3)
    pygame.draw.rect(pantalla_juego, color_campo_activo if input_activo == "edad" else color_blanco, registro_edad, border_radius=3)
    pygame.draw.rect(pantalla_juego, color_campo_activo if input_activo == "patologias" else color_blanco, registro_patologias, border_radius=3)
    
    # Dibujar botones de género con colores según selección
    color_femenino = color_morado if texto_genero_input == "F" else color_blanco
    color_masculino = color_azul if texto_genero_input == "M" else color_blanco
    
    pygame.draw.rect(pantalla_juego, color_femenino, boton_femenino, border_radius=10)
    pygame.draw.rect(pantalla_juego, color_negro, boton_femenino, 2, border_radius=10)
    
    pygame.draw.rect(pantalla_juego, color_masculino, boton_masculino, border_radius=10)
    pygame.draw.rect(pantalla_juego, color_negro, boton_masculino, 2, border_radius=10)
    
    pygame.draw.rect(pantalla_juego, color_verde, boton_guardar_datos, border_radius=10)
    pygame.draw.rect(pantalla_juego, color_negro, boton_guardar_datos, 2, border_radius=10)
    
    # Textos de los campos
    texto_apodo = fuente_media.render("Apodo: " + texto_apodo_input, True, color_rosado_oscuro)
    texto_edad = fuente_media.render("Edad: " + texto_edad_input, True, color_rosado_oscuro)
    texto_patologia = fuente_media.render("Patologia: " + texto_patologias_input, True, color_rosado_oscuro)
    
    # Textos de los botones de género
    texto_femenino = fuente_media.render("♀️", True, color_negro)
    texto_masculino = fuente_media.render("♂️", True, color_negro)
    texto_guardar = fuente_media.render("Terminar partida", True, color_blanco)
    
    # Etiquetas
    etiqueta_genero = fuente_media.render("Género:", True, color_blanco)
    pantalla_juego.blit(etiqueta_genero, (150, 415))
    
    pantalla_juego.blit(texto_apodo, (260, 230))
    pantalla_juego.blit(texto_edad, (260, 290))
    pantalla_juego.blit(texto_patologia, (260, 350))
    pantalla_juego.blit(texto_femenino, (boton_femenino.centerx - texto_femenino.get_width()//2, 
                                       boton_femenino.centery - texto_femenino.get_height()//2))
    pantalla_juego.blit(texto_masculino, (boton_masculino.centerx - texto_masculino.get_width()//2, 
                                        boton_masculino.centery - texto_masculino.get_height()//2))
    pantalla_juego.blit(texto_guardar, (boton_guardar_datos.centerx - texto_guardar.get_width()//2,
                                        boton_guardar_datos.centery - texto_guardar.get_height()//2))

# FUNCIONES DEL MENÚ DE NIVELES
def crear_botones_niveles():
    botones = {}
    y_pos = 200
    for nivel in niveles:
        botones[nivel] = pygame.Rect(anchura_pantalla_menu // 2 - 150, y_pos, 300, 60)
        y_pos += 80
    return botones

botones_niveles = crear_botones_niveles()

def mostrar_menu_niveles():
    pantalla_juego.fill(color_azul)

    # Título
    titulo = fuente_titulo.render("MEMORICE", True, color_blanco)
    subtitulo = fuente_media.render("Selecciona una dificultad", True, color_blanco)
    
    pantalla_juego.blit(titulo, (anchura_pantalla_menu // 2 - titulo.get_width() // 2, 80))
    pantalla_juego.blit(subtitulo, (anchura_pantalla_menu // 2 - subtitulo.get_width() // 2, 140))

    # Botones de niveles
    mouse_pos = pygame.mouse.get_pos()

    for nivel, rect in botones_niveles.items():
        if nivel == "basico":
            color_normal = color_Nbasico
        elif nivel == "intermedio":
            color_normal = color_Nintermedio
        else: 
            color_normal = color_Navanzado
            
        hover = rect.collidepoint(mouse_pos)
        color = color_blanco if hover else color_normal

        pygame.draw.rect(pantalla_juego, color, rect, border_radius=15)
        pygame.draw.rect(pantalla_juego, color_negro, rect, 3, border_radius=15)

        # Mostrar nombre y cantidad de niveles
        nombre = niveles[nivel]["nombre"]
        total_niveles = len(niveles[nivel]["niveles"])
        texto_principal = fuente_media.render(nombre, True, color_negro if hover else color_blanco)
        texto_secundario = fuente_pequena.render(f"{total_niveles} niveles", True, color_negro if hover else color_blanco)
        
        texto_rect_principal = texto_principal.get_rect(center=(rect.centerx, rect.centery - 10))
        texto_rect_secundario = texto_secundario.get_rect(center=(rect.centerx, rect.centery + 10))
        
        pantalla_juego.blit(texto_principal, texto_rect_principal)
        pantalla_juego.blit(texto_secundario, texto_rect_secundario)

def volver_al_menu():
    global estado_actual, anchura_pantalla, altura_pantalla, pantalla_juego, mostrar_al_inicio
    global nivel_seleccionado, nivel_actual_numero, max_nivel_alcanzado
    
    if total_clicks > 0:  # Solo si hubo partida jugada
        guardar_datos_partida()
    
    estado_actual = m
    anchura_pantalla = anchura_pantalla_menu
    altura_pantalla = altura_pantalla_menu
    mostrar_al_inicio = False
    nivel_seleccionado = None
    nivel_actual_numero = 1
    max_nivel_alcanzado = 0
    pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    
def inicializar_juego(nivel, numero_nivel=1):
    global cuadros, anchura_pantalla, altura_pantalla, boton, mostrar_imagen_seg, nivel_seleccionado, nivel_actual_numero

    nivel_seleccionado = nivel
    nivel_actual_numero = numero_nivel
    config_nivel = obtener_config_nivel_actual()

    if not config_nivel:
        print(f"Error: No se pudo cargar la configuración del nivel {numero_nivel} para {nivel}")
        return

    mostrar_imagen_seg = config_nivel["tiempo"]

    cuadros = []
    nombres_cartas = [  
        "Estrella_amarilla.png",
        "cuadrado.png",
        "circulo_lila.png",
        "heart_corazon.png",
        "Hexagono.png",
        "rombo_naranja.png",
        "media_luna_rosa.png",
        "triangulo.png",
        "pentagono_fucsia.png",
        "cruz_azul.png",
        "estrella_roja.png",
        "circulo_azul.png"
    ]

    total_pares = (config_nivel["filas"] * config_nivel["columnas"]) // 2
    
    # Para el nivel intermedio 2 (3x3) que tiene 9 cuadros, usar 4 parejas
    if config_nivel["filas"] == 3 and config_nivel["columnas"] == 3:
        total_pares = 4
    
    # Asegurarse de no exceder el número de imágenes disponibles
    total_pares = min(total_pares, len(nombres_cartas))
    
    imagenes_usadas = nombres_cartas[:total_pares] * 2
    
    # Si el número total de cuadros es impar, quitar una carta
    total_cuadros = config_nivel["filas"] * config_nivel["columnas"]
    if len(imagenes_usadas) > total_cuadros:
        imagenes_usadas = imagenes_usadas[:total_cuadros]
    elif len(imagenes_usadas) < total_cuadros:
        # Si faltan imágenes, duplicar algunas
        while len(imagenes_usadas) < total_cuadros:
            imagenes_usadas.append(imagenes_usadas[0])
    
    random.shuffle(imagenes_usadas)

    for i in range(config_nivel["filas"]):
        fila = []
        for j in range(config_nivel["columnas"]):
            if imagenes_usadas:
                nombre_imagen = imagenes_usadas.pop()
                cuadro = Cuadro(nombre_imagen)  
                fila.append(cuadro)
        cuadros.append(fila)

    anchura_pantalla = config_nivel["ancho_ventana"]
    altura_pantalla = config_nivel["alto_ventana"]

    global pantalla_juego
    pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))

    ancho_disponible = anchura_pantalla
    alto_disponible = altura_pantalla - altura_boton - 50
    
    cuadro_ancho = min(medida_cuadro, ancho_disponible // config_nivel["columnas"] - 10)
    cuadro_alto = min(medida_cuadro, alto_disponible // config_nivel["filas"] - 10)
    tamaño_cuadro_ajustado = min(cuadro_ancho, cuadro_alto)
    
    global imagen_oculta
    try:
        imagen_oculta = pygame.image.load(nombre_imagen_oc)
        imagen_oculta = pygame.transform.scale(imagen_oculta, (tamaño_cuadro_ajustado, tamaño_cuadro_ajustado))
    except:
        imagen_oculta = pygame.Surface((tamaño_cuadro_ajustado, tamaño_cuadro_ajustado))
        imagen_oculta.fill((150, 150, 150))
    
    for fila in cuadros:
        for cuadro in fila:
            try:
                ruta_completa = os.path.join(directorio_imagenes, cuadro.nombre_imagen)
                cuadro.imagen_real = pygame.image.load(ruta_completa)
                cuadro.imagen_real = pygame.transform.scale(cuadro.imagen_real, (tamaño_cuadro_ajustado, tamaño_cuadro_ajustado))
            except:
                cuadro.imagen_real = pygame.Surface((tamaño_cuadro_ajustado, tamaño_cuadro_ajustado))
                color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                cuadro.imagen_real.fill(color)

    global boton
    anchura_boton = 200
    x_boton = (anchura_pantalla - anchura_boton) // 2
    boton = pygame.Rect(x_boton, altura_pantalla - altura_boton - 10, anchura_boton, altura_boton)

def mostrar_todas_las_imagenes():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = True

def ocultar_todas_las_imagenes():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                cuadro.mostrar = False

def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False

def aleatorizar_cuadros():
    todas_parejas = []
    for fila in cuadros:
        for cuadro in fila:
            todas_parejas.append(cuadro)

    random.shuffle(todas_parejas)

    index = 0
    for i in range(len(cuadros)):
        for j in range(len(cuadros[0])):
            if index < len(todas_parejas):
                cuadros[i][j] = todas_parejas[index]
                index += 1

def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True

def comprobar_si_gana():
    global estado_actual, puntuacion_total, max_nivel_alcanzado
    
    if gana():
        puntuacion_total += puntuacion
        
        # Actualizar máximo nivel alcanzado
        if nivel_actual_numero > max_nivel_alcanzado:
            max_nivel_alcanzado = nivel_actual_numero
        
        # Verificar si es el último nivel
        total_niveles = len(niveles[nivel_seleccionado]["niveles"])
        if nivel_actual_numero == total_niveles:
            estado_actual = registro_ganador  # Ir al registro en lugar de ganaste
        else:
            estado_actual = nivel_completado  # Pasó al siguiente nivel

def actualizar_tiempo():
    global tiempo_restante, juego_iniciado, estado_actual
    
    if juego_iniciado and estado_actual == jugando:
        tiempo_transcurrido = time.time() - tiempo_inicio_nl
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)
        
        if tiempo_restante <= 0:
            juego_iniciado = False
            guardar_datos_partida() # Guardar datos al agotarse el tiempo
            estado_actual = tiempo_agotado 
            
def mostrar_pantalla_tiempo_agotado():
    config_nivel = obtener_config_nivel_actual()
    
    pantalla_juego.fill(color_rojo)
    
    titulo = fuente_titulo.render("¡Tiempo Agotado!", True, color_blanco)
    subtitulo = fuente_grande.render(f"Nivel {nivel_actual_numero} - {niveles[nivel_seleccionado]['nombre']}", True, color_blanco)
    puntos_text = fuente_grande.render(f"Puntos obtenidos: {puntuacion}", True, color_blanco)
    parejas_text = fuente_media.render(f"Parejas encontradas: {parejas_encontradas}", True, color_blanco)
    
    pantalla_juego.blit(titulo, (anchura_pantalla // 2 - titulo.get_width() // 2, 100))
    pantalla_juego.blit(subtitulo, (anchura_pantalla // 2 - subtitulo.get_width() // 2, 170))
    pantalla_juego.blit(puntos_text, (anchura_pantalla // 2 - puntos_text.get_width() // 2, 220))
    pantalla_juego.blit(parejas_text, (anchura_pantalla // 2 - parejas_text.get_width() // 2, 260))
    
    # Botones
    boton_reintentar.center = (anchura_pantalla // 2 - 110, 350)
    boton_menu_tiempo.center = (anchura_pantalla // 2 + 110, 350)
    
    # Botón reintentar
    pygame.draw.rect(pantalla_juego, color_verde, boton_reintentar, border_radius=15)
    pygame.draw.rect(pantalla_juego, color_negro, boton_reintentar, 2, border_radius=15)
    texto_reintentar = fuente_media.render("Reintentar", True, color_blanco)
    texto_rect_reintentar = texto_reintentar.get_rect(center=boton_reintentar.center)
    pantalla_juego.blit(texto_reintentar, texto_rect_reintentar)
    
    # Botón menú
    pygame.draw.rect(pantalla_juego, color_azul, boton_menu_tiempo, border_radius=15)
    pygame.draw.rect(pantalla_juego, color_negro, boton_menu_tiempo, 2, border_radius=15)
    texto_menu = fuente_media.render("Volver al Menú", True, color_blanco)
    texto_rect_menu = texto_menu.get_rect(center=boton_menu_tiempo.center)
    pantalla_juego.blit(texto_menu, texto_rect_menu)

def mostrar_pantalla_nivel_completado():
    config_nivel = obtener_config_nivel_actual()
    total_niveles = len(niveles[nivel_seleccionado]["niveles"])
    
    pantalla_juego.fill(color_verde)
    
    titulo = fuente_titulo.render("¡Nivel Completado!", True, color_blanco)
    subtitulo = fuente_grande.render(f"Nivel {nivel_actual_numero} - {niveles[nivel_seleccionado]['nombre']}", True, color_blanco)
    puntos_text = fuente_grande.render(f"Puntos: {puntuacion}", True, color_blanco)
    progreso_text = fuente_media.render(f"Progreso: {nivel_actual_numero}/{total_niveles}", True, color_blanco)
    
    pantalla_juego.blit(titulo, (anchura_pantalla // 2 - titulo.get_width() // 2, 100))
    pantalla_juego.blit(subtitulo, (anchura_pantalla // 2 - subtitulo.get_width() // 2, 170))
    pantalla_juego.blit(puntos_text, (anchura_pantalla // 2 - puntos_text.get_width() // 2, 220))
    pantalla_juego.blit(progreso_text, (anchura_pantalla // 2 - progreso_text.get_width() // 2, 260))
    
    # Botones
    if nivel_actual_numero < total_niveles:
        boton_siguiente_nivel.center = (anchura_pantalla // 2 - 110, 350)
        boton_menu_tiempo.center = (anchura_pantalla // 2 + 110, 350)
        
        # Botón siguiente nivel
        pygame.draw.rect(pantalla_juego, color_amarillo, boton_siguiente_nivel, border_radius=15)
        pygame.draw.rect(pantalla_juego, color_negro, boton_siguiente_nivel, 2, border_radius=15)
        texto_siguiente = fuente_media.render("Siguiente Nivel", True, color_negro)
        texto_rect_siguiente = texto_siguiente.get_rect(center=boton_siguiente_nivel.center)
        pantalla_juego.blit(texto_siguiente, texto_rect_siguiente)
    else:
        boton_menu_tiempo.center = (anchura_pantalla // 2, 350)
    
    # Botón menú
    pygame.draw.rect(pantalla_juego, color_azul, boton_menu_tiempo, border_radius=15)
    pygame.draw.rect(pantalla_juego, color_negro, boton_menu_tiempo, 2, border_radius=15)
    texto_menu = fuente_media.render("Volver al Menú", True, color_blanco)
    texto_rect_menu = texto_menu.get_rect(center=boton_menu_tiempo.center)
    pantalla_juego.blit(texto_menu, texto_rect_menu)

def reiniciar_juego():
    global juego_iniciado, puntuacion, parejas_encontradas, x1, y1, x2, y2, puede_jugar, ultimos_segundos, total_clicks, total_fallos, tiempos_reaccion
    global mostrar_al_inicio, tiempo_inicio_juego

    juego_iniciado = False
    puntuacion = 0
    parejas_encontradas = 0
    x1, y1 = None, None
    x2, y2 = None, None
    puede_jugar = True
    ultimos_segundos = None
    mostrar_al_inicio = False

    ocultar_todos_los_cuadros()
    aleatorizar_cuadros()

    # Reiniciar métricas
    total_clicks = 0
    total_fallos = 0
    tiempos_reaccion = []

def inicio_juego():
    global juego_iniciado, puntuacion, parejas_encontradas, mostrar_al_inicio, tiempo_inicio_juego, total_clicks, total_fallos, tiempos_reaccion
    global tiempo_inicio_nl, tiempo_restante, tiempo_limite

    aleatorizar_cuadros()
    ocultar_todos_los_cuadros()

    mostrar_al_inicio = True
    tiempo_inicio_juego = time.time()
    tiempo_inicio_nl = time.time()
    
    config_nivel = obtener_config_nivel_actual()
    if config_nivel:
        tiempo_limite = config_nivel["tiempo_max"]
    
    tiempo_restante = tiempo_limite
    mostrar_todas_las_imagenes()
    
    juego_iniciado = True
    puntuacion = 0
    parejas_encontradas = 0

    # Reiniciar métricas para la nueva partida
    total_clicks = 0
    total_fallos = 0
    tiempos_reaccion = []

def dibujar_barra_tiempo():
    if tiempo_limite <= 0:
        return
        
    ancho_barra = 200
    alto_barra = 20
    x_barra = anchura_pantalla - ancho_barra - 20
    y_barra = altura_pantalla - altura_boton - 30

    porcentaje = tiempo_restante / tiempo_limite

    if porcentaje > 0.5:
        color = color_verde
    elif porcentaje > 0.25:
        color = color_naranja
    else:
        color = color_rojo
    
    pygame.draw.rect(pantalla_juego, color_gris, (x_barra, y_barra, ancho_barra, alto_barra))
    pygame.draw.rect(pantalla_juego, color, (x_barra, y_barra, ancho_barra * porcentaje, alto_barra))
    pygame.draw.rect(pantalla_juego, color_negro, (x_barra, y_barra, ancho_barra, alto_barra), 2)

# Crear ventana inicial
pantalla_juego = pygame.display.set_mode((anchura_pantalla_menu, altura_pantalla_menu))
pygame.display.set_caption("Memorice - Sistema de Múltiples Niveles")

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API"))

def hablar(texto):
    try:
        audio = client.text_to_speech.convert(
            voice_id = "pNInz6obpgDQGcFmaJgB",
            model_id = "eleven_multilingual_v2",
            text =texto
        )
        output_path = "tts_temp.mp3"
        save(audio, output_path)
        pygame.mixer.music.load(output_path)
        pygame.mixer.music.play()
    except Exception as e:
        print("Error al reproducir", e)


# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

hablar("Holaa, bienvenido/da jugador, este juego tiene 3 dificultades, basico, intermedio y avanzado, Seleccione una dificultad y ¡a jugar!")

while ejecutando:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        elif event.type == pygame.KEYDOWN:
            if estado_actual == registro_ganador:
                if input_activo == "apodo":
                    if event.key == pygame.K_BACKSPACE:
                        texto_apodo_input = texto_apodo_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_activo = "edad"
                    else:
                        if len(texto_apodo_input) < 15:
                            texto_apodo_input += event.unicode
                
                elif input_activo == "edad":
                    if event.key == pygame.K_BACKSPACE:
                        texto_edad_input = texto_edad_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_activo = "patologias"
                    else:
                        if event.unicode.isdigit() and len(texto_edad_input) < 3:
                            texto_edad_input += event.unicode
                
                elif input_activo == "patologias":
                    if event.key == pygame.K_BACKSPACE:
                        texto_patologias_input = texto_patologias_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_activo = "genero"
                    else:
                        if len(texto_patologias_input) < 20:
                            texto_patologias_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado_actual == m:
                for nivel, rect in botones_niveles.items():
                    if rect.collidepoint(event.pos):
                        inicializar_juego(nivel, 1)
                        estado_actual = jugando
                        inicio_juego()
                        break

            elif estado_actual == jugando:
                if mostrar_al_inicio:
                    continue
                
                x, y = event.pos
                if boton.collidepoint(x, y):
                    reiniciar_juego()
                    inicio_juego()
                    continue

                if puede_jugar and juego_iniciado:
                    config_nivel = obtener_config_nivel_actual()
                    if not config_nivel:
                        continue
                        
                    ancho_disponible = anchura_pantalla
                    alto_disponible = altura_pantalla - altura_boton - 50
                    ancho_cuadro = min(medida_cuadro, ancho_disponible // config_nivel["columnas"] - 10)
                    alto_cuadro = min(medida_cuadro, alto_disponible // config_nivel["filas"] - 10)
                    tamaño_actual = min(ancho_cuadro, alto_cuadro)

                    margen_x = (anchura_pantalla - (tamaño_actual * config_nivel["columnas"])) // 2
                    margen_y = (alto_disponible - (tamaño_actual * config_nivel["filas"])) // 2

                    click_x, click_y = x, y

                    grid_left = margen_x
                    grid_top = margen_y
                    grid_right = margen_x + tamaño_actual * config_nivel["columnas"]
                    grid_bottom = margen_y + tamaño_actual * config_nivel["filas"]

                    if not (grid_left <= click_x < grid_right and grid_top <= click_y < grid_bottom):
                        continue

                    cuadro_x = int((click_x - margen_x) // tamaño_actual)
                    cuadro_y = int((click_y - margen_y) // tamaño_actual)

                    cuadro_x = max(0, min(cuadro_x, len(cuadros[0]) - 1))
                    cuadro_y = max(0, min(cuadro_y, len(cuadros) - 1))

                    cuadro_actual = cuadros[cuadro_y][cuadro_x]

                    if cuadro_actual.descubierto or cuadro_actual.mostrar:
                        continue

                    total_clicks += 1 # Contar cada click válido

                    if x1 is None:
                        x1, y1 = cuadro_x, cuadro_y
                        cuadros[y1][x1].mostrar = True
                        tiempo_inicio_par = time.time() # Iniciar cronómetro para reacción
                    else:
                        x2, y2 = cuadro_x, cuadro_y
                        cuadros[y2][x2].mostrar = True
                        
                        # Guardar tiempo de reacción para este par
                        tiempos_reaccion.append(time.time() - tiempo_inicio_par)
                        
                        if cuadros[y1][x1].nombre_imagen == cuadros[y2][x2].nombre_imagen: 
                            cuadros[y1][x1].descubierto = True
                            cuadros[y2][x2].descubierto = True
                            puntuacion += config_nivel["puntos_par"]
                            parejas_encontradas += 1
                            
                            tiempo_restante += tiempo_extra_pareja_encontrada
                            tiempo_limite += tiempo_extra_pareja_encontrada
                            
                            x1, y1 = None, None
                            x2, y2 = None, None
                            comprobar_si_gana()
                            if estado_actual != jugando: # Si se completó el nivel/juego
                                guardar_datos_partida()
                        else:
                            total_fallos += 1 # Contar fallo
                            ultimos_segundos = time.time()
                            puede_jugar = False

            elif estado_actual == nivel_completado:
                if nivel_actual_numero < len(niveles[nivel_seleccionado]["niveles"]):
                    if boton_siguiente_nivel.collidepoint(event.pos):
                        # Avanzar al siguiente nivel
                        siguiente_nivel = nivel_actual_numero + 1
                        inicializar_juego(nivel_seleccionado, siguiente_nivel)
                        estado_actual = jugando
                        inicio_juego()
                
                if boton_menu_tiempo.collidepoint(event.pos):
                    volver_al_menu()
                    
            elif estado_actual == registro_ganador:
                if registro_apodo.collidepoint(event.pos):
                    input_activo = "apodo"
                elif registro_edad.collidepoint(event.pos):
                    input_activo = "edad"
                elif registro_patologias.collidepoint(event.pos):
                    input_activo = "patologias"
                elif boton_femenino.collidepoint(event.pos):
                    texto_genero_input = "F"  # Selecciona Femenino
                elif boton_masculino.collidepoint(event.pos):
                    texto_genero_input = "M"  # Selecciona Masculino
                elif boton_guardar_datos.collidepoint(event.pos):
                    # Guardar datos y volver al menú
                    apodo = texto_apodo_input
                    edad = texto_edad_input
                    patologias = texto_patologias_input
                    genero = "Femenino" if texto_genero_input == "F" else "Masculino" if texto_genero_input == "M" else ""
                    guardar_datos_partida()
                    
                    # 🆕 ABRIR RANKING AUTOMÁTICAMENTE
                    abrir_ranking()
                    
                    volver_al_menu()
                    
            elif estado_actual == tiempo_agotado:
                if boton_reintentar.collidepoint(event.pos):
                    reiniciar_juego()
                    inicio_juego()
                    estado_actual = jugando
                elif boton_menu_tiempo.collidepoint(event.pos):
                    # 🆕 ABRIR RANKING también al perder
                    abrir_ranking()
                    volver_al_menu()
    
    actualizar_tiempo()
    
    # --- DIBUJADO ---
    if estado_actual == m:
        mostrar_menu_niveles()

    elif estado_actual == jugando:
        pantalla_juego.fill(color_blanco)
        
        config_nivel = obtener_config_nivel_actual()
        if not config_nivel:
            continue
            
        if mostrar_al_inicio:
            tiempo_actual = time.time()
            if tiempo_actual - tiempo_inicio_juego >= duracion_muestra_inicio:
                mostrar_al_inicio = False
                ocultar_todas_las_imagenes()
                
        if not puede_jugar and ultimos_segundos:
            if time.time() - ultimos_segundos >= mostrar_imagen_seg:
                if x1 is not None and y1 is not None and not cuadros[y1][x1].descubierto:
                    cuadros[y1][x1].mostrar = False
                if x2 is not None and y2 is not None and not cuadros[y2][x2].descubierto:
                    cuadros[y2][x2].mostrar = False
                x1 = y1 = x2 = y2 = None
                ultimos_segundos = None
                puede_jugar = True

        # Calcular tamaño de cuadro 
        ancho_disponible = anchura_pantalla
        alto_disponible = altura_pantalla - altura_boton - 50
        ancho_cuadro = min(medida_cuadro, ancho_disponible // config_nivel["columnas"] - 10)
        alto_cuadro = min(medida_cuadro, alto_disponible // config_nivel["filas"] - 10)
        tamaño_cuadro_ajustado = min(ancho_cuadro, alto_cuadro)
        
        # Calcular margen para centrar
        margen_x = (anchura_pantalla - (tamaño_cuadro_ajustado * config_nivel["columnas"])) // 2
        margen_y = (alto_disponible - (tamaño_cuadro_ajustado * config_nivel["filas"])) // 2

        # Dibujar cuadros
        for y, fila in enumerate(cuadros):
            for x, cuadro in enumerate(fila):
                rect_x = margen_x + x * tamaño_cuadro_ajustado + 2
                rect_y = margen_y + y * tamaño_cuadro_ajustado + 2
                rect = pygame.Rect(rect_x, rect_y, tamaño_cuadro_ajustado - 4, tamaño_cuadro_ajustado - 4)
                
                shadow_rect = pygame.Rect(rect_x + 2, rect_y + 2, tamaño_cuadro_ajustado - 4, tamaño_cuadro_ajustado - 4)
                pygame.draw.rect(pantalla_juego, (200, 200, 200), shadow_rect, border_radius=5)

                if cuadro.mostrar or cuadro.descubierto:
                    pantalla_juego.blit(cuadro.imagen_real, rect)
                    if cuadro.descubierto:
                        pygame.draw.rect(pantalla_juego, color_verde, rect, 3, border_radius=5)
                else:
                    pantalla_juego.blit(imagen_oculta, rect)

                border_color = color_verde if cuadro.descubierto else color_negro
                pygame.draw.rect(pantalla_juego, border_color, rect, 2, border_radius=5)

        # Mensaje de memorizar imágenes
        if mostrar_al_inicio:
            tiempo_restante_muestra = duracion_muestra_inicio - (time.time() - tiempo_inicio_juego)
            mensaje = fuente_media.render(f"Memoriza las imágenes: {tiempo_restante_muestra:.1f}s", True, color_rojo)
            pantalla_juego.blit(mensaje, (anchura_pantalla // 2 - mensaje.get_width() // 2, 10))

        # Panel inferior
        panel_info = pygame.Rect(0, altura_pantalla - altura_boton - 40, anchura_pantalla, 40)
        pygame.draw.rect(pantalla_juego, (240, 240, 240), panel_info)
        pygame.draw.line(pantalla_juego, color_gris, (0, altura_pantalla - altura_boton - 40),
                         (anchura_pantalla, altura_pantalla - altura_boton - 40), 2)

        # Información del juego
        total_parejas = (config_nivel["filas"] * config_nivel["columnas"]) // 2
        if config_nivel["filas"] == 3 and config_nivel["columnas"] == 3:
            total_parejas = 4  # Caso especial para 3x3
            
        texto_nivel = fuente_pequena.render(f"Dificultad: {niveles[nivel_seleccionado]['nombre']}", True, color_negro)
        texto_num_nivel = fuente_pequena.render(f"Nivel: {nivel_actual_numero}/3", True, color_negro)
        texto_puntos = fuente_pequena.render(f"Puntos: {puntuacion}", True, color_negro)
        texto_parejas = fuente_pequena.render(f"Parejas: {parejas_encontradas}/{total_parejas}", True, color_negro)
        texto_tiempo = fuente_pequena.render(f"Tiempo: {int(tiempo_restante)}s", True, color_negro)

        pantalla_juego.blit(texto_nivel, (10, altura_pantalla - altura_boton - 30))
        pantalla_juego.blit(texto_num_nivel, (180, altura_pantalla - altura_boton - 30))
        pantalla_juego.blit(texto_puntos, (300, altura_pantalla - altura_boton - 30))
        pantalla_juego.blit(texto_parejas, (450, altura_pantalla - altura_boton - 30))
        pantalla_juego.blit(texto_tiempo, (600, altura_pantalla - altura_boton - 30))

        # Barra de tiempo
        dibujar_barra_tiempo()

        # Mensaje de tiempo extra
        if parejas_encontradas > 0:
            tiempo_extra_texto = fuente_pequena.render(f"+{tiempo_extra_pareja_encontrada}s por pareja", True, color_verde)
            pantalla_juego.blit(tiempo_extra_texto, (anchura_pantalla // 2 - tiempo_extra_texto.get_width() // 2, altura_pantalla - altura_boton - 60))

    elif estado_actual == nivel_completado:
        mostrar_pantalla_nivel_completado()

    elif estado_actual == registro_ganador:
        registro_jugador()

    elif estado_actual == tiempo_agotado:
        mostrar_pantalla_tiempo_agotado()

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()