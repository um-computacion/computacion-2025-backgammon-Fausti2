"""
Módulo CLI. Define la clase CLI (interfaz de texto del Backgammon).

El juego comienza de esta forma : 
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
  mover     -> <origen> <destino> -> mueve una ficha (ej.: mover 0 5)
  volver    -> regresa al menú principal
  jugadas   -> lista movimientos legales con los dados actuales

"""

from core.board import Board
from core.player import Player
from core.dice import Dice
from core.game import BackgammonGame


class CLI:
    def __init__(self):
        # El juego se crea cuando el usuario elige "Empezar juego" en el menú
        self.board: Board | None = None
        self.blanco: Player | None = None
        self.negro: Player | None = None
        self.dice: Dice | None = None
        self.game: BackgammonGame | None = None

    # ================== Ayuda / Visualización ==================
    def _imprimir_ayuda(self) -> None:
        print("Comandos disponibles:")
        print("  ayuda     -> muestra esta ayuda")
        print("  salir     -> termina la aplicación")
        print("  tablero   -> muestra cantidad de fichas por punto (0..23)")
        print("  turno     -> muestra de quién es el turno")
        print("  tirar     -> tira los dados y muestra el resultado")
        print("  reiniciar -> vuelve a la posición inicial estándar")
        print("  mover     -> <origen> <destino> -> mueve una ficha (ej.: mover 0 5)")
        print("  volver    -> regresa al menú principal")
        print("  jugadas   -> lista movimientos legales con los dados actuales")

    def _mostrar_reglas(self) -> None:
        reglas = """
REGLAS DE BACKGAMMON

1) Tablero y objetivo
• Dos jugadores (blanco y negro), 15 fichas por color.
- El objetivo es sacar (bear-off) todas tus fichas del tablero antes que el rival.

2) Sentido de movimiento
- Blanco mueve hacia índices MAYORES (de 0 → 23).
- Negro mueve hacia índices MENORES (de 23 → 0).

3) Tiradas y dobles
- En tu turno tirás dos dados (comando: tirar).
- Si sale doble (ej: 3-3), tenés cuatro movimientos de 3.

4) Movimientos válidos
- Podés usar cada dado con la MISMA ficha o con fichas distintas.
- No podés mover a un punto con 2+ fichas del rival (punto bloqueado).
- Si el destino tiene 1 ficha rival, la COMÉS: esa ficha va a la barra.

5) Barra (fichas comidas)
- Si tenés fichas en la barra, estás OBLIGADO a reingresar antes de cualquier otro movimiento.
- Para entrar desde la barra:
  - BLANCO: 'mover -1 <destino> blanco' (destino = 24 - dado → 23..18).
  - NEGRO : 'mover -1 <destino> negro'  (destino = dado - 1 → 0..5).
- No podés entrar a un punto bloqueado (2+ rivales). Si hay 1 rival, lo comés.

6) Uso de dados (obligatoriedad)
- Debés usar la mayor cantidad de dados posible.
-  Si sólo podés usar uno, usá el movimiento MÁS alto.
- Cuando se consumen todos los dados, el turno cambia.

7) Bear-off (sacar fichas)
- Sólo podés sacar fichas cuando TODAS las tuyas están en el cuadrante final:
  - BLANCO: 18..23
  - NEGRO : 0..5
- Se saca con número exacto (distancia al borde). Se permite un número mayor
sólo si no hay fichas más lejos que la que querés sacar.
  - BLANCO: destino 24
  - NEGRO : destino -1

8) Final del juego
- Gana quien primero se queda sin fichas en el tablero y en la barra.
"""
        print(reglas)

    def _mostrar_estado(self) -> None:
        turno = self.game.get_current_player().get_color()
        dados = self.game.get_rolled_values()
        print(f"\nTurno: {turno}")
        print("Dados disponibles:", dados if dados else "(sin tirar)")
        print(self.board.to_ascii())

    def _menu_principal(self) -> str:
        print("\n====== Menú principal ======")
        print("1) Empezar juego")
        print("2) Reglas")
        print("3) Ayuda")
        print("4) Salir")
        op = input("Elegí una opción [1-4]: ").strip().lower()
        return "4" if op == "salir" else op

    def _prompt_turno(self) -> str:
        turno = self.game.get_current_player().get_color()
        dados = self.game.get_rolled_values()
        visor = "[" + ", ".join(map(str, dados)) + "]" if dados else "-"
        return f"({turno} | dados: {visor}) > "

    
    def _valid_point(p: int) -> bool:
        return (p in range(24)) or (p in (-1, 24))  # -1 negro sale, 24 blanco sale

    def _chequear_ganador(self) -> bool:
        ganador = self.game.get_winner()
        if ganador:
            print(f"\n¡{ganador.capitalize()} ganó la partida! 🎉")
            return True
        return False

    def _imprimir_jugadas(self) -> None:
        moves = self.game.legal_moves()
        if not moves:
            print("No hay movimientos legales con los dados actuales.")
            return

        def _pt(x: int) -> str:
            if x == -1:
                return "barra"
            if x == 24:
                return "salida(24)"
            return str(x)

        print("Movimientos legales:")
        for i, (s, e, d) in enumerate(moves, 1):
            print(f"  {i:>2}) {_pt(s)} -> {_pt(e)}  usando dado {d}")

    # ================== Flujo ==================
    def _nuevo_juego(self) -> None:
        self.board = Board()
        self.board.setup_standard()
        self.blanco = Player("Blanco", "blanco")
        self.negro = Player("Negro", "negro")
        self.dice = Dice()
        self.game = BackgammonGame(self.board, self.blanco, self.negro, self.dice)

    def _reiniciar(self) -> None:
        self._nuevo_juego()
        print("Partida reiniciada: tablero, turno y dados en estado inicial.")
        self._mostrar_estado()

    # ================== programa principal ==================
    def cmdloop(self) -> None:
        while True:
            opcion = self._menu_principal()

            if opcion == "4":
                print("¡Hasta luego!")
                return

            if opcion == "3":
                self._imprimir_ayuda()
                continue

            if opcion == "2":
                self._mostrar_reglas()
                continue

            if opcion != "1":
                print("Opción inválida. Probá 1..4.")
                continue

            # === 1) Empezar juego ===
            self._nuevo_juego()
            print("\nComienza el juego. Escribí 'ayuda' para ver comandos.")
            print("Usá 'volver' para regresar al menú, o 'salir' para cerrar la aplicación.")
            self._mostrar_estado()
            if self._chequear_ganador():
                break

            while True:
                try:
                    partes = input(self._prompt_turno()).strip().split()
                    if not partes:
                        continue
                    cmd = partes[0].lower()

                    if cmd == "salir":
                        print("¡Hasta luego!")
                        return

                    if cmd in {"volver", "menu"}:
                        print("Volviendo al menú principal…")
                        break

                    if cmd == "ayuda":
                        self._imprimir_ayuda()
                        continue

                    if cmd == "tablero":
                        self._mostrar_estado()
                        continue

                    if cmd == "turno":
                        print("Turno de:", self.game.get_current_player().get_color())
                        continue

                    if cmd == "tirar":
                        valores = self.game.roll_dice()
                        print("Dados tirados:", valores)
                        if not self.game.can_play():
                            print("No hay movimientos legales; pasás el turno.")
                            self.game.end_turn()
                            self._mostrar_estado()
                            continue
                        self._mostrar_estado()
                        continue

                    if cmd in {"jugadas", "legales"}:
                        self._imprimir_jugadas()
                        continue

                    if cmd in {"mover", "move"}:
                        if len(partes) != 3:
                            print("Uso: mover <origen:int> <destino:int>")
                            continue
                        try:
                            origen = int(partes[1])
                            destino = int(partes[2])
                        except ValueError:
                            print("Origen/Destino deben ser enteros.")
                            continue

                        color = self.game.get_current_player().get_color()

                        if not self._valid_point(origen) or not self._valid_point(destino):
                            print("Punto inválido: debe ser 0..23 (o -1/24 solo barra/bear-off).")
                            continue

                        try:
                            self.game.move(origen, destino, color)
                        except ValueError as e:
                            print("Error:", e)
                            continue

                        print(f"Movida {color}: {origen} -> {destino}")
                        self._mostrar_estado()

                        if self._chequear_ganador():
                            break
                        continue

                    if cmd == "reiniciar":
                        self._reiniciar()
                        continue

                    # sugerencias si ingresan sólo números
                    if cmd.isdigit():
                        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                            print(f"Parece un movimiento. Usá: mover {partes[0]} {partes[1]}")
                            continue
                        print("Comando no reconocido. Escribí 'ayuda' para ver opciones.")
                        continue

                    print("Comando no reconocido. Escribí 'ayuda' para ver opciones.")
                except Exception as e:
                    print("Error:", e)  
                    