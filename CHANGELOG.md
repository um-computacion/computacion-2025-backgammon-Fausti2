# Changelog

## 23-08-2025
### Agregado
Estructura inicial del proyecto:
  Carpeta `core` con las clases principales (`board.py`, `player.py`, `dice.py`, `checker.py`, `game.py`).
  Carpeta `cli` 
  Carpeta `pygame_ui` 
  Carpeta `tests` 
  Archivo `.gitignore` 


## 25-08-2025
### Agregado
Documentación inicial del proyecto:
   `README.md`
   `JUSTIFICACION.md`
    Archivos `prompts`
Se agregó el codigo de la clase "Dice` para manejar los dados del juego.

## 26-08-2025
### Agregado
configuracion de circle ci 

## 27-08-2025
### Agregado
- Agregar el código de `test_dice`.  
- Crear el archivo `test_checker` y su implementación de código en `checker.py`.  
- Agregar el código de `test_checker`.  

### Modificado
- Cambiar el código de `dice.py` para corregir problemas detectados al ejecutar los tests.

## 31-08-2025
### Agregado
- Se agregó el código de la clase `Player`.
- Se realizó el código de `test_player`.

### Modificado
- Se modificaron los códigos creados agregando atributos con prefijo `__` y la implementación de setters/getters.
- Se agregó la implementación de setters/getters en los tests.

## 12-09-2025
### Agregado
- Se mejoró `test_dice` y `test_checker`.

### Modificado
- Se cambió la estructura del `CHANGELOG.md`.

## 13-09-2025
### Agregado 
- Se agrego lo requerido del readme (nombre y apellido del autor) 
- Agregue el codigo de clase board y sus test 

### Modificado
- Se cambió la estructura del `CHANGELOG.md`. 

## 14-09-2025
### Agregado 

### Modificado 
- Estructura de documentación para que se vea ordenada en Git. 

## 15-09-2025
### Agregado 
- Empece realizando el codigo de "game.py" creando la funciones para guardar tablero, jugadores y dados, y poder cambiar de turno.
- continue con las funciones para "game.py" agregando roll_dice y get_rolled_values para manejar tiradas del turno.
- Agregue agregué el método move para poder mover una ficha de un punto a otro usando el tablero 
### Modificado 
- Cambie comentarios de la clase board 

## 24-09-2025
### Agregado 
- Termine de realizar el codigo de "game.py" 

## 25-09-2025
### Agregado 
- Empece realizando los tests de "test_game" que cubren la instanciación básica del juego con tablero, jugadores y dados.
- Se agregó validación del turno inicial (empieza siempre el jugador blanco).
- Se agregó validación del cambio de turno mediante el método "end_turn()". 
