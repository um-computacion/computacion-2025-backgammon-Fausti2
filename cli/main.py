"""
Comandos iniciales:
  ayuda     -> muestra esta ayuda
  salir     -> termina la aplicación
  tablero   -> muestra cantidad de fichas por punto (0..23)
  turno     -> muestra de quién es el turno
  tirar     -> tira los dados y muestra el resultado
  reiniciar -> vuelve a la posición inicial estándar
  mover <origen> <destino> <color> -> mueve una ficha (ej.: mover 0 5 blanco)
""" 
from core.board import Board  
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame

def _imprimir_ayuda() -> None:
    print("Comandos disponibles:")
    print("  ayuda     -> muestra esta ayuda")
    print("  salir     -> termina la aplicación")
    print("  tablero   -> muestra cantidad de fichas por punto (0..23)")
    print("  turno     -> muestra de quién es el turno")
    print("  tirar     -> tira los dados y muestra el resultado")
    print("  reiniciar -> vuelve a la posición inicial estándar")
    print("  mover <origen> <destino> <color> -> mueve una ficha (ej.: mover 0 5 blanco)") 



def mostrar_tablero_texto(board: Board) -> None:
    cantidades = [len(board.get_point(i)) for i in range(24)]
    duenos = [board.owner_at(i) or "-" for i in range(24)]
    print("Puntos (0..23) | Cantidades:", cantidades)
    print("Dueño por punto|           :", duenos)


def main() -> None:
    print("Backgammon CLI (ES). Escribí 'ayuda' para ver comandos. Para salir: 'salir'.")


  # Creo el tablero y lo dejo en posición inicial estándar
    board = Board() 
    board.setup_standard()
    blanco = Player("Blanco", "blanco")
    negro = Player("Negro", "negro")
    dice = Dice()
    game = BackgammonGame(board, blanco, negro, dice) 

    while True:
        try:
            partes = input("> ").strip().split()
            if not partes:
                continue
            cmd = partes[0].lower()

            if cmd == "salir":
                print("¡Hasta luego!")
                break

            if cmd == "ayuda":
                _imprimir_ayuda()
                continue 

            if cmd == "tablero":
                print(board.to_ascii())
                continue

            if cmd == "turno":
                print("Turno de:", game.get_current_player().get_color())
                continue

            if cmd == "tirar":
                valores = game.roll_dice()
                print("Dados tirados:", valores)
                continue
                
            if cmd == "reiniciar":
                board.setup_standard()
                print("Tablero reiniciado a la posición inicial.")
                continue
    # ----Mover ficha----
            if cmd in {"mover", "move"}:
             if len(partes) != 4:
                print("Uso: mover <origen:int> <destino:int> <color:blanco|negro>")
                continue

             origen = int(partes[1])
             destino = int(partes[2])
             color = partes[3].lower()

             if color not in {"blanco", "negro"}:
              print("Color inválido. Usá: blanco | negro")
              continue

            # Llama a la lógica existente en BackgammonGame (esta valida que haya ficha del color en 'origen')
            game.move(origen, destino, color)
            print(f"Movida {color}: {origen} -> {destino}")
            continue

        except Exception as exc:
        # Errores típicos: índice fuera de rango o no hay ficha del color en el origen
         print("Error:", exc)
if __name__ == "__main__":
    main() 


