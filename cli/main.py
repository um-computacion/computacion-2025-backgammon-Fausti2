"""
CLI del Backgammon (español) — Paso 1
Comandos iniciales:
  ayuda     -> muestra esta ayuda
  salir     -> termina la aplicación
"""

def _imprimir_ayuda() -> None:
    print("Comandos disponibles:")
    print("  ayuda     -> muestra esta ayuda")
    print("  salir     -> termina la aplicación")

def main() -> None:
    print("Backgammon CLI (ES). Escribí 'ayuda' para ver comandos. Para salir: 'salir'.")

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

            print("Comando no reconocido. Escribí 'ayuda' para ver opciones.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main() 