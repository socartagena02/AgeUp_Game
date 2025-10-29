// CONFIGURACIÓN DE NIVELES
const CONFIG_NIVELES = {
    basico: {
        colores: ['purple', 'blue', 'yellow', 'green'],
        velocidad: 1000,
        puntosBase: 150,
        nombre: "Básico"
    },
    intermedio: {
        colores: ['purple', 'blue', 'yellow', 'green', 'orange', 'red'],
        velocidad: 800,
        puntosBase: 200,
        nombre: "Intermedio"
    },
    avanzado: {
        colores: ['purple', 'blue', 'yellow', 'green', 'orange', 'red', 'turquese', 'cyan'],
        velocidad: 700,
        puntosBase: 250,
        nombre: "Avanzado"
    }
};

// VARIABLES GLOBALES PARA EL JUEGO
let sequence = [];
let playerSequence = [];
let level = 0;
let score = 0;
let isPlayerTurn = false;
let configActual = CONFIG_NIVELES.basico;

let colorButtons, startButton, scoreDisplay, levelDisplay, backtoMenu;

function mostrarMensaje(mensaje, tipo = 'info') {
    const mensajeAnterior = document.getElementById('game-message');
    if (mensajeAnterior) {
        mensajeAnterior.remove();
    }
    
    const mensajeElement = document.createElement('div');
    mensajeElement.id = 'game-message';
    mensajeElement.className = `game-message ${tipo}`;
    mensajeElement.innerHTML = `
        <i class="${tipo === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${mensaje}
    `;

    document.body.appendChild(mensajeElement);
    
    setTimeout(() => {
        mensajeElement.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        mensajeElement.classList.remove('show');
        setTimeout(() => {
            if (mensajeElement.parentNode) {
                mensajeElement.remove();
            }
        }, 500);
    }, 2000);
}

function playSound(soundElement) {
    if (!soundElement) return false;
    try {
        soundElement.pause(); 
        soundElement.currentTime = 0;
        soundElement.volume = 1; 
        return soundElement.play().then(() => true).catch(e => {
            console.log("Error reproduciendo sonido:", e);
            return false;
        });
    } catch (error) {
        console.log("Error con elemento de audio:", error);
        return false;
    }
}

function inicializarMenu() {    
    const soundClick = document.getElementById('sound-click');
    const soundHover = document.getElementById('sound-hover');
    const soundMenu = document.getElementById('sound-menu');
    const volumeOn = document.getElementById('volume-on');
    const volumeOff = document.getElementById('volume-off');
    
    console.log("Elementos de audio encontrados:", {
        menu: !!soundMenu,
        click: !!soundClick,
        hover: !!soundHover
    });

    let musicaActiva = true;
    
    if (volumeOn && volumeOff) {
        volumeOn.addEventListener('click', () => {
            if (soundMenu) {
                soundMenu.volume = 0;
                volumeOn.style.display = 'none';
                volumeOff.style.display = 'inline';
                musicaActiva = false;
                mostrarMensaje('Sonido desactivado', 'info');
            }
        });
        
        volumeOff.addEventListener('click', () => {
            if (soundMenu) {
                soundMenu.volume = 0.5;
                volumeOff.style.display = 'none';
                volumeOn.style.display = 'inline';
                musicaActiva = true;
                mostrarMensaje('Sonido activado', 'success');
            }
        });
    }

    let musicaIniciada = false;
    
    function iniciarMusica() {
        if (!musicaIniciada && soundMenu && musicaActiva) {
            soundMenu.volume = 1;
            soundMenu.loop = true;
            soundMenu.play().catch(e => {
                console.log("Error reproduciendo música:", e);
            });
            musicaIniciada = true;
            console.log("Música de fondo iniciada");
        }
    }

    function manejarPrimeraInteraccion() {
        iniciarMusica();
        document.removeEventListener('click', manejarPrimeraInteraccion);
        document.removeEventListener('keydown', manejarPrimeraInteraccion);
        document.removeEventListener('touchstart', manejarPrimeraInteraccion);
    }

    document.addEventListener('click', manejarPrimeraInteraccion);
    document.addEventListener('keydown', manejarPrimeraInteraccion);
    document.addEventListener('touchstart', manejarPrimeraInteraccion);

    // DECLARAR LAS VARIABLES ANTES DE USARLAS
    const nivelBasico = document.getElementById('basico');
    const nivelIntermedio = document.getElementById('intermedio');
    const nivelAvanzado = document.getElementById('avanzado');
    const volverInicio = document.getElementById('volver-inicio'); 

    if (nivelBasico) {
        nivelBasico.addEventListener('click', () => {
            iniciarMusica();
            playSound(soundClick);
            mostrarMensaje('Iniciando nivel básico, ¡Recuerda los colores!', 'info');
            redirigirANivel('basico');
        });
        
        nivelBasico.addEventListener('mouseenter', () => {
            playSound(soundHover);
        });
    }
    
    if (nivelIntermedio) {
        nivelIntermedio.addEventListener('click', () => {
            iniciarMusica();
            playSound(soundClick);
            mostrarMensaje('Iniciando nivel intermedio, ¡Recuerda los colores!', 'info');
            redirigirANivel('intermedio');
        });
        
        nivelIntermedio.addEventListener('mouseenter', () => {
            playSound(soundHover);
        });
    }
    
    if (nivelAvanzado) {
        nivelAvanzado.addEventListener('click', () => {
            iniciarMusica();
            playSound(soundClick);
            mostrarMensaje('Iniciando nivel avanzado, ¡Recuerda los colores!', 'info');
            redirigirANivel('avanzado');
        });
        
        nivelAvanzado.addEventListener('mouseenter', () => {
            playSound(soundHover);
        });
    }

    if (volverInicio) {
        volverInicio.addEventListener('click', () => {
            playSound(soundClick);
            mostrarMensaje('Volviendo al inicio', 'info');
            setTimeout(() => {
                window.location.href = '/';  
            }, 1000);
        });
    }

    setTimeout(() => {
        if (!musicaIniciada && soundMenu) {
            console.log("Intentando iniciar música automáticamente");
            iniciarMusica();
        }
    }, 2000);
}

function redirigirANivel(nivel) {
    console.log(`Redirigiendo al nivel: ${nivel}`);
    const rutasNiveles = {
        'basico': '/simon-dice/basico/',        
        'intermedio': '/simon-dice/intermedio/', 
        'avanzado': '/simon-dice/avanzado/' 
    };
    
    const ruta = rutasNiveles[nivel];
    if (ruta) {
        setTimeout(() => {
            window.location.href = ruta;
        }, 1000);
    } else {
        console.error(`Nivel no encontrado: ${nivel}`);
    }
}

function inicializarJuego(nivel = 'basico') {
    configActual = CONFIG_NIVELES[nivel];
    sequence = [];
    playerSequence = [];
    level = 0;
    score = 0;
    isPlayerTurn = false;
    
    updateDisplays();
    setupColorButtons();
    
    console.log(`Juego inicializado en nivel: ${configActual.nombre}`);
    mostrarMensaje(`Nivel ${configActual.nombre} cargado. ¡Haz click en "Iniciar juego"!`, 'info');
}

function setupColorButtons() {
    const todosColores = ['purple', 'blue', 'yellow', 'green', 'orange', 'red', 'pink', 'turquese', 'cyan'];
    
    todosColores.forEach(color => {
        const button = document.getElementById(color);
        if (button) {
            if (configActual.colores.includes(color)) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        }
    });
}

function updateDisplays() {
    if (scoreDisplay) scoreDisplay.textContent = score;
    if (levelDisplay) levelDisplay.textContent = level;
}

function getRandomColor() {
    const colors = configActual.colores;
    return colors[Math.floor(Math.random() * colors.length)];
}

function flashButton(color) {
    const button = document.getElementById(color);
    if (!button) return;
    
    button.classList.add('sequence-active');
    setTimeout(() => {
        button.classList.remove('sequence-active');
    }, 600);
}

function flashButtonClick(color) {
    const button = document.getElementById(color);
    if (!button) return;
    
    button.classList.add('click-active');
    setTimeout(() => {
        button.classList.remove('click-active');
    }, 300);
}

function playSequence() {
    isPlayerTurn = false;
    let i = 0;
    
    const interval = setInterval(() => {
        flashButton(sequence[i]);
        i++;
        if (i >= sequence.length) {
            clearInterval(interval);
            setTimeout(() => {
                isPlayerTurn = true;
            }, 500);
        }
    }, configActual.velocidad);
}

function startFirstLevel() {
    level = 1;
    score = 0;
    isPlayerTurn = false;
    playerSequence = [];
    sequence = [getRandomColor()];
    
    updateDisplays();
    
    setTimeout(() => {
        playSequence();
    }, 1500);
}

function nextLevel() {
    const pointsEarned = (level + 1) * configActual.puntosBase;
    score += pointsEarned;
    level++;
    
    isPlayerTurn = false;
    playerSequence = [];
    sequence.push(getRandomColor());
    
    updateDisplays();
  
    mostrarMensaje(`¡Nivel ${level-1} completado!`, 'success');
    
    setTimeout(() => {
        mostrarMensaje(`Nivel ${level}, ¡Recuerda los colores!`, 'info');
        setTimeout(() => {
            playSequence();
        }, 1000);
    }, 2000);
}

function resetGame() {
    sequence = [];
    playerSequence = [];
    level = 0;
    score = 0;
    isPlayerTurn = false;
    updateDisplays();
}

function handlePlayerInput(color) {
    if (!isPlayerTurn) return;
    
    if (!configActual.colores.includes(color)) return;
    
    playerSequence.push(color);
    flashButtonClick(color);

    const currentStep = playerSequence.length - 1;

    if (playerSequence[currentStep] !== sequence[currentStep]) {
        document.body.classList.add('error');
        mostrarMensaje('¡Ups!,¡No iba por ahí!', 'error');
        
        setTimeout(() => {
            document.body.classList.remove('error');
            mostrarMensaje(`Para la proxima tendras mejor suerte, tu puntaje final: ${score}`, 'error');
            setTimeout(() => {
                resetGame();
            }, 2000);
        }, 1000);
    } else {
        mostrarMensaje('¡Bien hecho!', 'success');
        
        if (playerSequence.length === sequence.length) {
            isPlayerTurn = false;
            setTimeout(() => {
                nextLevel();
            }, 1000);
        }
    }
}

function inicializarPaginaJuego(nivel) {
    console.log(`Inicializando juego para nivel: ${nivel}`);
   
    colorButtons = document.querySelectorAll('.colorButton');
    startButton = document.getElementById('start-game');
    scoreDisplay = document.getElementById('score');
    levelDisplay = document.getElementById('level');
    backtoStart = document.getElementById('volver-menu');
 
    colorButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const color = e.target.id;
            handlePlayerInput(color);
        });
    });

    if (startButton) {
        startButton.addEventListener('click', () => {
            if (level === 0) {
                resetGame();
                startFirstLevel();
            }
        });
    }
    
    if (backtoStart) {
        backtoStart.addEventListener('click', () => {
            mostrarMensaje('Volviendo al menú principal', 'info');
            setTimeout(() => {
                window.location.href = '/'; 
            }, 1000);
        });
    }

    inicializarJuego(nivel);
    updateDisplays();
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Página cargada, detectando tipo de página...");
   
    const esMenuPrincipal = document.getElementById('levels-container');
    const esPaginaJuego = document.getElementById('game');
    
    if (esMenuPrincipal) {
        inicializarMenu();
    } else if (esPaginaJuego) {
        console.log("Inicializando página de juego");
    } else {
        console.log("Página no reconocida");
    }
});

const style = document.createElement('style');
style.textContent = `
    .game-message {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%) translateY(-100px);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.5s ease;
        border: 2px solid;
    }
    
    .game-message.show {
        transform: translateX(-50%) translateY(0);
    }
    
    .game-message.success {
        border-color: #28a745;
        background: rgba(40, 167, 69, 0.9);
    }
    
    .game-message.error {
        border-color: #dc3545;
        background: rgba(220, 53, 69, 0.9);
    }
    
    .game-message.info {
        border-color: #17a2b8;
        background: rgba(23, 162, 184, 0.9);
    }
    
    .game-message i {
        font-size: 20px;
    }
`;
document.head.appendChild(style);