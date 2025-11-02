Justificación Técnica del Proyecto: Backgammon

Este documento describe las decisiones de diseño, arquitectura y metodología adoptadas durante el desarrollo del juego Backgammon, realizado para la materia Computación 2025.
El objetivo es justificar el enfoque aplicado, demostrar la aplicación de principios SOLID y evidenciar la calidad del código desarrollado.

⸻

1. Resumen del Diseño General

La arquitectura del proyecto se basa en una separación por capas (Layered Architecture), que distingue de forma clara la lógica del juego de las interfaces con el usuario.
	•	Capa de Lógica del Juego (core):
Incluye las clases y reglas fundamentales del Backgammon: tablero, jugadores, fichas, dados y flujo general de la partida.
Esta capa es totalmente independiente de la interfaz gráfica o de texto, lo que permite testear el juego sin necesidad de abrir la UI.
	•	Capa de Interfaz (cli, pygame_ui):
Contiene los módulos de interacción con el usuario:
	•	CLI: interfaz en consola para ejecutar pruebas rápidas.
	•	PygameUI: interfaz visual construida con Pygame para una experiencia interactiva completa.

Este diseño promueve la reutilización del motor de juego, la mantenibilidad y la testabilidad, cumpliendo los objetivos del trabajo práctico de la cátedra.

⸻

2. Justificación de Clases y Atributos

Clases Principales y Responsabilidades
	•	BackgammonGame:
Coordina el flujo del juego, controla los turnos, valida movimientos y detecta condiciones de victoria.
	•	Board:
Modela el tablero del Backgammon, con los 24 puntos, la barra central y la bandeja de salida (bear-off).
Administra la posición de cada ficha y define la lógica de movimiento, captura y reingreso.
	•	Player:
Representa a un jugador, con su nombre, color (“blanco” o “negro”) y sus 15 fichas.
Centraliza la identidad y el control de sus piezas.
	•	Checker:
Representa una ficha individual del juego.
Su única responsabilidad es almacenar y validar su color.
	•	Dice:
Gestiona el lanzamiento de los dados y maneja las reglas asociadas (dobles, valores disponibles, etc.).
	•	CLI y BackgammonUI:
Son las interfaces de presentación.
Traducen las acciones del jugador (comandos o clics) en movimientos del juego, pero no contienen lógica del mismo.

⸻

3. Decisiones de Diseño Relevantes

Separación entre core y ui

La decisión más importante fue mantener una separación estricta entre la lógica del juego y las interfaces gráficas o de texto.

Ventajas:
	•	El motor (core) puede probarse de forma aislada sin depender de Pygame.
	•	Permite extender el juego (por ejemplo, versión web o móvil) sin modificar la lógica existente.
	•	Facilita el mantenimiento y las pruebas unitarias.

Alternativa Descartada

Inicialmente se consideró incluir métodos gráficos dentro de Board (por ejemplo, dibujar_en_pygame()), pero se descartó porque violaba el Principio de Responsabilidad Única (SRP).
Este enfoque hubiera hecho que el tablero cambiara por motivos no relacionados con la lógica del juego (como el estilo visual o la librería usada), dificultando su testeo y mantenimiento.

⸻

4. Estrategia de Testing y Calidad

El proyecto adopta un enfoque de pruebas unitarias para garantizar la estabilidad del código y la corrección de las reglas del juego.
	•	Framework:
Se utiliza pytest por su facilidad de uso y compatibilidad con herramientas de cobertura como pytest-cov o coverage.
	•	Cobertura:
Se alcanzó una cobertura superior al 90% en el módulo core, asegurando la verificación de casi toda la lógica del juego.
	•	Pruebas Implementadas:
	•	Movimientos válidos y jugadas básicas.
	•	Casos borde (bloqueos, reingresos, capturas).
	•	Validaciones de excepciones con mensajes claros.
	•	Pruebas en CLI:
Se utilizaron capturas de salida (capsys) para validar que la representación textual del tablero y los mensajes de estado sean correctos.

⸻

5. Principios SOLID Aplicados

Durante el desarrollo del proyecto se aplicaron los principios SOLID, fundamentales para garantizar un diseño orientado a objetos limpio, extensible y fácil de mantener.

Principio de Responsabilidad Única (SRP):
Cada clase tiene una única responsabilidad.
Por ejemplo, la clase Board se dedica exclusivamente a gestionar las posiciones de las fichas en el tablero, sin involucrarse en la interfaz o los turnos.
Player se encarga de los datos y fichas del jugador, Dice únicamente de las tiradas y resultados, y las clases CLI y BackgammonUI manejan la presentación y la interacción con el usuario.
De esta forma, cada clase tiene un propósito definido, y cualquier cambio en la lógica o interfaz no afecta al resto del sistema.

Principio Abierto/Cerrado (OCP):
El sistema está diseñado para ser abierto a la extensión, pero cerrado a la modificación.
Esto significa que se pueden agregar nuevas interfaces (por ejemplo, una versión web o una inteligencia artificial que juegue automáticamente) sin modificar el código ya existente en el core.
La estructura modular permite añadir nuevas funcionalidades mediante herencia o composición sin alterar las clases principales.

Principio de Sustitución de Liskov (LSP):
Las clases del sistema pueden ser extendidas o reemplazadas sin alterar el funcionamiento general.
Por ejemplo, podría crearse una subclase de Dice que genere resultados predeterminados para pruebas automatizadas, y esta nueva clase se podría usar en lugar de Dice sin romper el flujo de BackgammonGame.
Esto garantiza flexibilidad y compatibilidad entre componentes.

Principio de Segregación de Interfaces (ISP):
Las clases de la interfaz gráfica (pygame_ui) y la interfaz de texto (cli) utilizan únicamente los métodos que necesitan del core.
No dependen de funciones innecesarias ni de detalles internos del motor del juego.
Esto mantiene el acoplamiento bajo y asegura que los cambios en el core no rompan las interfaces.

Principio de Inversión de Dependencia (DIP):
Las capas superiores (UI) dependen de abstracciones y no de implementaciones concretas.
Por ejemplo, BackgammonUI recibe un objeto BackgammonGame, pero no conoce los detalles de cómo funciona internamente.
De este modo, se puede sustituir el motor del juego por otro compatible sin modificar la interfaz.
Este principio mejora la extensibilidad y reduce el acoplamiento entre las capas.

⸻

6. Conclusión

El proyecto Backgammon — Computación 2025 demuestra un diseño sólido y modular que cumple con los principios de la programación orientada a objetos y las buenas prácticas de ingeniería de software.

Se logró:
	•	Una arquitectura por capas clara y desacoplada.
	•	Cumplimiento completo de los principios SOLID.
	•	Código mantenible, reutilizable y testeado.
	•	Interfaz gráfica intuitiva y funcional desarrollada con Pygame.
	•	Cobertura de pruebas superior al 90% en la lógica principal (core).