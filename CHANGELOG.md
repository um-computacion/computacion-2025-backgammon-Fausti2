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
- Continué con los tests en "test_game" agregando la validación de la tirada de dados.
- Se comprobó que los dados devuelven valores en el rango correcto (1 a 6).
- Se verificó que siempre se obtienen dos valores al lanzar. 
- Agregue validaciones de movimientos de fichas en el tablero.
- Se añadieron pruebas para verificar que al mover fichas se actualicen correctamente los puntos de origen y destino.
- Agregué pruebas para mandar fichas a la barra y también para sacarlas de ahí.(para volver a jugar)

## 26-09-2025
### Agregado 
- Implemente pylint con los archivos necesarios 
- Agregue requerimientos en requirements.txt 
- Cree el archivo coveragerc 

## 29-09-2025
### Agregado 
- Empece realizando "cli/main.py" agregando las primeras funciones 
- Aguregue la funcion en "main.py" que se pueda ver el tablero 
 
## 30-09-2025
### Agregado 
- Agregue en "main.py" para que se pueda ver el quien es el turno y tambien que se pueda tirar los dados 


## 10-10-2025
### Agregado 
- Agregue funcones en "board.py" para mejorar la visualizacion del tablero 
- Segui mejorando la visualizacion del tablero 
- Termine con la visualizacion del tablero 

## 11-10-2025
### Agregado 
- Agregue la funcion de reiniciar en main 
- Agregue en game que al mover las fichas que tengan que coincidir con el valor de la tirada y lo agregue en tmb en main. 
- Realice unas mejoras en cuanto ala visaulizacion del tablero 

## 12-10-2025
### Agregado 
- Cambie el esquema de main para que al jugar se vea de una manera mas simple y facil de entender. Tambien realice correcciones en "game" donde en la dinamica del juego la perjudicaba. 
- Realice correcciones en main y en "game" 
- Segui corregiendo errores en "game" que traian sobre las fichas con los colores 

## 16-10-2025
### Agregado
- Agregue en game funciones (_home_range, _all_in_home, _entry_point, _has_on_bar) que serian
  1 home_range: devuelve el cuadrante final por color 
  2 all_in_home: verifica si todas las fichas del color están en su home y sin barra 
  3 entry_point: calcula el punto de entrada desde barra según el dado 
  4 has_on_bar: indica si hay fichas del color en la barra 
- Segui agregando funciones en game para poder implementar bien las reglas del juego 

## 19-10-2025
### Agregado
- Agregue en game y main la funcion para anunciar el ganador cuando no quedan fichas y cortar la partida 
  1 agregue has_won(), get_winner()  para detectar ganador 
  2 añadi  _chequear_ganador() y lo invoca tras 'mover' y 'tirar' si hay ganador, muestra mensaje. 


## 28-10-2025
### Agregado
- Hice correcciones en game 
- Agregue las reglas en main 

## 29-10-2025
### Agregado
- Agregue mas funciones en main en la parte de move 
- Agregue en game legal_moves y can_play 
- Perfeccionando main agregue la funcion para ver las jugadas que se pueden hacer y arregle la funcion para reiniciar y entre otras cosas 
- Hice correcciones sobre main y cli y lo deje como corresponde 
- Cree el archivo test_cli.py 
- Mejore y amplie los test de game 


## 30-10-2025
### Agregado 
- Realice el codigo de test_cli y mejore core/game 
- Mejore y amplie todos los test necesarios para cubrir mas del 90% 
- Cree el archivo constans.py y realize su respectivo codigo 