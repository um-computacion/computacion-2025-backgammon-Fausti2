"""
Comandos iniciales:
  ayuda     -> muestra esta ayuda
  salir     -> termina la aplicación
  tablero   -> muestra cantidad de fichas por punto (0..23)
"""
from core.board import Board  # tablero con 24 puntos y barra


def _imprimir_ayuda() -> None:
    print("Comandos disponibles:")
    print("  ayuda     -> muestra esta ayuda")
    print("  salir     -> termina la aplicación")
    print("  tablero   -> muestra cantidad de fichas por punto (0..23)") 


def _render_tablero(board: Board) -> None:
    cantidades = [len(board.get_point(i)) for i in range(24)]
    duenos = [board.owner_at(i) or "-" for i in range(24)]
    print("Puntos (0..23) | Cantidades:", cantidades)
    print("Dueño por punto|           :", duenos)


def main() -> None:
    print("Backgammon CLI (ES). Escribí 'ayuda' para ver comandos. Para salir: 'salir'.")


  # Creo el tablero y lo dejo en posición inicial estándar
    board = Board() 
    board.setup_standard()


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
                _render_tablero(board) 
                continue

            print("Comando no reconocido. Escribí 'ayuda' para ver opciones.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main() 

    