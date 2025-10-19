"""
Menú principal:
  1) Empezar juego
  2) Reglas
  3) Ayuda
  4) Salir

Comandos dentro de la partida:
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

# ================== Ayuda / Visualización ==================
def _imprimir_ayuda() -> None:
    print("Comandos disponibles:")
    print("  ayuda     -> muestra esta ayuda")
    print("  salir     -> termina la aplicación")
    print("  tablero   -> muestra cantidad de fichas por punto (0..23)")
    print("  turno     -> muestra de quién es el turno")
    print("  tirar     -> tira los dados y muestra el resultado")
    print("  reiniciar -> vuelve a la posición inicial estándar")
    print("  mover <origen> <destino> <color> -> mueve una ficha (ej.: mover 0 5 blanco)") 



def _mostrar_reglas() -> None:
    # completar luego
    print("REGLAS (a completar):") 

def _mostrar_estado(board: Board, game: BackgammonGame) -> None:
    """Imprime turno, dados disponibles y el tablero ASCII."""
    turno = game.get_current_player().get_color()
    dados = game.get_rolled_values()
    print(f"\nTurno: {turno}")
    print("Dados disponibles:", dados if dados else "(sin tirar)")
    print(board.to_ascii())

def _menu_principal() -> str:
    print("\n====== Menú principal ======")
    print("1) Empezar juego")
    print("2) Reglas")
    print("3) Ayuda")
    print("4) Salir")
    op = input("Elegí una opción [1-4]: ").strip().lower()
    # permitir escribir "salir" además de 4
    return "4" if op == "salir" else op

def _prompt_turno(game: BackgammonGame) -> str:
    turno = game.get_current_player().get_color()
    dados = game.get_rolled_values()
    visor = "[" + ", ".join(map(str, dados)) + "]" if dados else "-"
    return f"({turno} | dados: {visor}) > "

def _chequear_ganador(game: BackgammonGame) -> bool:
    ganador = game.get_winner()
    if ganador:
        print(f"\n¡{ganador.capitalize()} ganó la partida! 🎉")
        return True
    return False

# ================== Programa principal ==================

def main() -> None:
    # Menú principal
    while True:
        opcion = _menu_principal()

        if opcion == "4":
            print("¡Hasta luego!")
            return

        if opcion == "3":  # Ayuda
            _imprimir_ayuda()
            continue

        if opcion == "2":  # Reglas
            _mostrar_reglas()
            continue

        if opcion != "1":
            print("Opción inválida. Probá 1..4.")
            continue 

        # === 1) Empezar juego ===
        board = Board()
        board.setup_standard()
        blanco = Player("Blanco", "blanco")
        negro  = Player("Negro", "negro")
        dice   = Dice()
        game   = BackgammonGame(board, blanco, negro, dice)

        print("\nComienza el juego. Escribí 'ayuda' para ver comandos.")
        print("Usá 'volver' para regresar al menú, o 'salir' para cerrar la aplicación.")
        _mostrar_estado(board, game)  # Estado inicial visible
        if _chequear_ganador(game):
         break 

        while True:
            try:
                partes = input(_prompt_turno(game)).strip().split()
                if not partes:
                    continue
                cmd = partes[0].lower()

                # ---- salir (cierra la app) ----
                if cmd == "salir":
                    print("¡Hasta luego!")
                    return

                # ---- volver (regresa al menú) ----
                if cmd in {"volver", "menu"}:
                    print("Volviendo al menú principal…")
                    break

                # ---- ayuda / tablero / turno ----
                if cmd == "ayuda":
                    _imprimir_ayuda()
                    continue

                if cmd == "tablero":
                    _mostrar_estado(board, game)
                    continue

                if cmd == "turno":
                    print("Turno de:", game.get_current_player().get_color())
                    continue

                # ---- tirar ----
                if cmd == "tirar":
                    valores = game.roll_dice()
                    print("Dados tirados:", valores)
                    _mostrar_estado(board, game)
                    if _chequear_ganador(game):
                     break
                    continue

                # ---- mover ( move) ----
                if cmd in {"mover", "move"}:
                    if len(partes) != 4:
                        print("Uso: mover <origen:int> <destino:int> <color:blanco|negro>")
                        continue
                    origen  = int(partes[1])
                    destino = int(partes[2])
                    color   = partes[3].lower()
                    game.move(origen, destino, color)
                    print(f"Movida {color}: {origen} -> {destino}")
                    _mostrar_estado(board, game) 
                    if _chequear_ganador(game):
                     break
                    continue

                # ---- reiniciar ----
                if cmd == "reiniciar":
                    board.setup_standard()
                    print("Tablero reiniciado a la posición inicial.")
                    _mostrar_estado(board, game)
                    continue

                if cmd.isdigit():
                    if len(partes) == 3 and partes[0].isdigit() and partes[1].isdigit():
                        origen  = partes[0]
                        destino = partes[1]
                        color   = partes[2]
                        print(f"Parece un movimiento. Usá: mover {origen} {destino} {color}")
                        continue

                    if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                        print("Parece un movimiento. Usá: mover <origen> <destino> <color:blanco|negro>")
                        continue
                    
                print("Comando no reconocido. Escribí 'ayuda' para ver opciones.")
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    # Ejecutar con: python -m cli.main
    main() 
    
