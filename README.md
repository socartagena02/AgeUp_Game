# 🎮 AgeUp_games 
**AgeUp_games** es un sistema híbrido web/escritorio de minijuegos cognitivos diseñada especificamente para Terapia Ocupacional Geriátrica 🩺.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)
![Versión](https://img.shields.io/badge/versión-1.0.0-green)

## 👾 Caracteristicas
### 🧩 Minijuegos Interactivos

- **🧠 Memorice**: Ejercita la memoria visual emparejando formas y colores con tiempos adaptados por nivel.
- **🗺️ Localización Geográfica** *(próximamente)*: Desarrolla orientación cognitiva identificando calles de Limache, Valparaíso.
- **🎨 Simons say**: Mejora la memoria secuencial con patrones de colores.

### ♿ Diseño

- **⏱️ Temporizadores** según la dificultad de los niveles.
- **📊 Progresión gradual** en complejidad
- **🎯 Feedback** para reforzamiento positivo.
- **🖥️ Interfaz accesible** con alto contraste y textos legibles.

### ♿ Accesibilidad
- Feedback visual y auditivo suave.
- Ranking independiente en cada minijuego.
- Compatible para monitores táctiles.

## 🏥 Público Objetivo
- **Adultos mayores** en proceso de terapia ocupacional.

## 🛠️ Tecnologías
- **Backend**: Django 5.2.6
- **Lenguaje**: Python +3.11  
- **Librerías**: Pygame, boostrap 
- **Base de datos**: MySQL

## 🀄 Instalación
```bash
## Clona el repositorio
git clone https://github.com/socartagena02/AgeUp_Game.git
cd AgeUp_Game
```
# Instalar dependencias
pip install django
pip install pygame
pip install pymysql
npm install bootstrap@5.3.8

# Ejecutar
cd cognitivos
python manage.py runserver

## 📁 Estructura 

- **AgeUp_Game/**
  - **cognitivos/** - App Django principal
    - **cognitivos/** - Configuración
      - `settings.py` - Configuración general
      - `urls.py` - Rutas principales  
      - `views.py` - Vistas y lógica
      - `wsgi.py` - Servidor
    - **static/** - Archivos estáticos
      - **assets/** - Recursos gráficos
        - `assets_fondo.png`
        - `logo_hospi.png` 
        - `Memorice_icon.png`
        - `simon_dice_icon.png`
        - `trazar_camino.png`
      - **css/**
        - `style.css` - Estilos principales
      - **js/**
        - `script.js` - JavaScript principal
      - **secuencia_colores/** - Simon Dice
        - **js/**
          - `main.js` - Menú principal
          - `nivel-basico.js` - Nivel 1
          - `nivel-intermedio.js` - Nivel 2
          - `nivel-avanzado.js` - Nivel 3
        - **musica/**
          - `Persona - Pix.mp3` - Música fondo
          - `sound-14.mp3` - Sonido click
          - `sound6.wav` - Sonido hover
        - **style/**
          - `style.css` - CSS menú
          - `common.css` - CSS común
          - `nivel-basico.css` - Nivel 1
          - `nivel-intermedio.css` - Nivel 2
          - `nivel-avanzado.css` - Nivel 3
    - **templates/** - Plantillas HTML
      - `template.html` - Plantilla base
      - `memorice_interfaz.html` - Interfaz Memorice
      - **secuencia_colores/** - Simon Dice
        - `index.html` - Menú principal
        - `nivel-basico.html` - Nivel 1
        - `nivel-intermedio.html` - Nivel 2
        - `nivel-avanzado.html` - Nivel 3
  - **memorice/** - Juego de memoria
    - **imagenes_memorice/** - 12 formas geométricas
      - `circulo_lila.png`
      - `cruz_azul.png`
      - `cuadrado.png`
      - `Estrella_amarilla.png`
      - `gray_pale.png`
      - `heart_corazon.png`
      - `Hexagono.png`
      - `images.jpeg`
      - `images.png`
      - `media_luna_rosa.png`
      - `pentagono_fucsia.png`
      - `rombo_naranja.png`
      - `triangulo.png`
    - `memorice.py` - Script del juego
  - `manage.py` - Administrador Django
  - `db.sqlite3` - Base de datos
Desarrollado con ❤️ para las funcionarias de mi centro de práctica