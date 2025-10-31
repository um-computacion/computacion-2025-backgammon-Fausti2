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
        cli = CLI()
        cli.cmdloop()
    elif opcion == "2":
        juego_ui = BackgammonUI()
        juego_ui.run()
    else:
        print("Opción inválida")

if __name__ == "__main__":
    main()



