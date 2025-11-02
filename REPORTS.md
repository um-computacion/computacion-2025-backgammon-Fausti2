# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
cli/__init__.py              2      0   100%
cli/cli.py                 168     22    87%   128-129, 135-136, 140, 142, 190, 196, 200-201, 223-226, 257-262, 276-278
core/__init__.py             0      0   100%
core/board.py              125      0   100%
core/checker.py             11      0   100%
core/dice.py                17      0   100%
core/game.py               195     29    85%   31, 80-81, 108, 136, 157, 163, 181, 217, 248, 256, 291-316
core/player.py              26      2    92%   31, 38
pygame_ui/__init__.py        5      2    60%   8-10
pygame_ui/constants.py      33      4    88%   55-58
pygame_ui/game_ui.py       124    110    11%   4-5, 12-37, 41-62, 65-77, 81-87, 90-101, 105-134, 137-140, 144-161
pygame_ui/renderer.py      163    147    10%   3-4, 19-26, 29-35, 38-39, 42-58, 62-66, 70-79, 82-85, 90-121, 125-151, 155-168, 172-186, 191-243
tests/__init__.py            0      0   100%
tests/test_board.py        100      1    99%   173
tests/test_checker.py       22      1    95%   45
tests/test_cli.py           70      1    99%   156
tests/test_dice.py          23      1    96%   55
tests/test_game.py         171      1    99%   269
tests/test_player.py        28      0   100%
------------------------------------------------------
TOTAL                     1283    321    75%

```
## Pylint Report
```text
************* Module test.py
test.py:1:0: F0001: No module named test.py (fatal)
************* Module main
main.py:1:0: C0114: Missing module docstring (missing-module-docstring)
main.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 0.00/10


```
