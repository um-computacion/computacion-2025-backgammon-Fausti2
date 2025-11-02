# Backgammon Computacion 2025
## Alumno: Faustino De Lucia 

### Descripción 

Juego clásico de Backgammon desarrollado en Python, con un motor de juego independiente (core), una interfaz de línea de comandos (CLI) y una interfaz gráfica (GUI) con Pygame. 

El proyecto aplica una arquitectura por capas y principios de diseño SOLID, promoviendo código limpio, mantenible y fácil de probar.

### Características Principales
- Motor de juego autocontenido: sin dependencias de interfaz.
- Interfaz gráfica clara y funcional (Pygame):
- Barra central para fichas comidas.
- Bandeja lateral con conteo de fichas retiradas (bear-off).
- Turno actual y dados visibles en pantalla.
- Interfaz CLI funcional: ideal para probar reglas y comandos.
- Diseño orientado a pruebas : cobertura >90% en la lógica del juego.

### Estructura del Proyecto
- core/         → Lógica del juego: Board, Player, Dice, BackgammonGame
- cli/          → Interfaz de texto (comandos)
- pygame_ui/    → Interfaz gráfica: game_ui , Renderer, constants 
- tests/        → Pruebas unitarias del core (+ CLI)
- main.py       → Menú principal (elige CLI o Pygame)
- requirements.txt 

### Requisitos Previos
- Python 3.12+ 
- pip actualizado

Instalación
### 1️⃣ Clonar el repositorio
git clone <URL_DE_TU_REPO>
cd computacion-2025-backgammon-Fausti2

### 2️⃣ Crear y activar entorno virtual
python -m venv .venv

### En macOS / Linux:
source .venv/bin/activate

### En Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

### 3️⃣ Instalar dependencias
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt

# Cómo Ejecutar

## Opción A — Interfaz Gráfica (Pygame)
`python main.py`

### Controles Principales
T → Tirar los dados
Click → Seleccionar y mover ficha (origen → destino)
Si hay fichas en barra, clickeá directamente el destino válido
R → Reiniciar partida
J → Mostrar jugadas legales en consola
H → Mostrar ayuda en pantalla
ESC / Q / V → Salir o volver 

### Elementos en Pantalla
Turno visible en el cuadrante izquierdo.
Dados en el canal central .
Barra central con fichas comidas (según color).
Bandeja lateral mostrando solo el número de fichas en bear-off.

## Opción B — Interfaz de Texto (CLI)
`python -m cli.cli`

### Comandos disponibles
tirar	Lanza los dados
mover <origen> <destino>	Mueve una ficha según los dados
jugadas	Muestra jugadas legales disponibles
reiniciar	Reinicia la partida
salir	Cierra el programa

## Cómo Jugar (Interfaz Gráfica)
### Objetivo
Ser el primer jugador en retirar las 15 fichas del tablero (bear-off).

### Flujo de Turnos
- Presioná T para tirar los dados.
- Hacé click en una ficha tuya (o en el punto de entrada si estás en barra).
- Hacé click en el destino válido.
- Repetí hasta consumir los dados.
- Si no hay movimientos posibles, cambia el turno automáticamente.

## Reglas Esenciales
- Captura: si caés en un punto con 1 ficha rival, la capturás (va a la barra).
- Bloqueo: no podés entrar a un punto con 2 o más fichas rivales.
- Prioridad de barra: si tenés fichas en barra, deben reingresar antes de mover otras.
- Bear-off: solo cuando las 15 fichas estén en tu cuadrante. Si no hay fichas más lejos, se puede usar dado mayor.

## Indicadores Visuales
- Turno: texto claro en el lado izquierdo.
- Dados: ubicados en el canal central.
- Barra: columna central para fichas comidas.
- Bandeja lateral: muestra cuántas fichas sacaste. 

## Tests 
### Ejecutar tests 
bash
`pytest`

