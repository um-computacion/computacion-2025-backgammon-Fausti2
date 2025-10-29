# main.py (punto de entrada)
from cli.cli import CLI
# from pygame_ui.app import UI  # interfaz gráfica futura 

def main():
    cli = CLI()
    cli.cmdloop()

if __name__ == "__main__":
    main()  
    