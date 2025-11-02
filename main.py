# main.py
from cli.cli import CLI
from pygame_ui.game_ui import BackgammonUI

def main():
    print("=" * 40)
    print("  BACKGAMMON")
    print("=" * 40)
    print("1. Modo CLI")
    print("2. Modo Pygame")
    print("=" * 40)

    opcion = input("Elige (1/2): ").strip()
    if opcion == "1":
        CLI().cmdloop()
    elif opcion == "2":
        BackgammonUI().run()   # <-- sin pasar game
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()
