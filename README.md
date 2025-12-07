# 🎮 AgeUp_games 
**AgeUp_games** es un sistema híbrido web/escritorio de minijuegos cognitivos diseñada especificamente para Terapia Ocupacional Geriátrica 🩺.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Estado](https://img.shields.io/badge/estado-en%20desarrollo-yellow)
![Versión](https://img.shields.io/badge/versión-2.0.0-green)

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
## Entorno virtual
- python -m venv venv

**Su activación:**
- .\venv\Scripts\activate

# Instalar dependencias
- pip install django
- pip install pygame
- pip install pymysql
- npm install bootstrap@5.3.8
- pip install numpy
- pip install pandas
- pip install -U scikit-learn
- pip install gtts
- pip install elevenlabs
- pip install python-dotenv
- pip install matplotlib
- pip install seaborn

# Ejecutar
- cd cognitivos
- python manage.py runserver

# Mockup y aplicación funcionando

## Mockup

### Menú principal de juegos
![Menu_Principal](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/1-Menu_general.png)

### Interfaz del memorice y dificultad básica
![Menu_memorice](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/2-Menu_memorice.png)
![memorice_basico](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/3-Nivel_basico.png)

### Interfaz del simón dice y dificultad básica
![menu-simonDice](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/4-simon_says-menu.png)
![simonDice_basico](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/5-simon_says-nivelBasico.png)

### Ranking
![ranking](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/mockup/6-ranking.png)

## Aplicación funcionando

### Menú principal de juegos
![menuPrincipal](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/1-menu_general.png)

### Memorice
![interfazMemorice](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/2-memorice-menu.png)
![memorice-nivelBasico](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/3-memorice-nivelBasico.png)

### Simón dice
![interfaz-simonDice](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/4-simonDice-interfaz.png)
![simonDice-nivelBasico](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/5-simonDice-nivelBasico.png)

### Ranking
![ranking](evidencias/Fases/Fase%202/Evidencias_Proyecto/Evidencias_sistema/6-ranking.png)

# Acceder a: 
http://127.0.0.1:8000

## 📁 Estructura 

- **AgeUp_Game/**
  - **cognitivos/** - App Django principal
    - `manage.py` - Administrador Django
    - **cognitivos/** - Frontend y Backend
      - `settings.py` - Iniciación del servidor
      - `urls.py` - Rutas principales  
      - `views.py` - Vistas y lógica
      - `wsgi.py` - Servidor
    - **static/** - Archivos estáticos
      - **assets/** - Recursos gráficos
      - **css/**
        - `style.css` - Estilos principales
      - **js/**
        - `script.js` - JavaScript principal
      - **secuencia_colores/** - Simon Dice
        - **js/**
        - **musica/**
        - **style/**
          - `style.css` - CSS menú
          - **secuencia_colores/** - Simon Dice css
    - **templates/** - Plantillas HTML
      - `template.html` - Plantilla base
      - `memorice_interfaz.html` - Interfaz Memorice
      - **secuencia_colores/** - Simon Dice
  - **memorice/** - Juego memorice
    - **imagenes_memorice/** - 12 formas geométricas
    - `memorice.py` - Script del juego
  - **doc/** - Documentos pedidos por el docente #1
    - `plan_trabajo.pdf`  
  - **evidencias/** - Documentos pedidos por el docente #2
    - **Fases/**
      - **Fase 1/**
      - **Fase 2/**
      - **Fase 3/**
    - **commits_equipo/**
      - `sofia_cartagena.md`
      - `allen_rodriguez.md`
      - `esteban_rodriguez.md`
    - `contributors_github.png`
  - `README.md`
  
Desarrollado con ❤️ para las funcionarias de mi centro de práctica