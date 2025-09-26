# Automated Reports
## Coverage Report
```text
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
cli/__init__.py             0      0   100%
core/__init__.py            0      0   100%
core/board.py              68     20    71%   26, 43-44, 51, 63, 71, 77, 79, 98-111
core/checker.py            11      0   100%
core/dice.py               17      0   100%
core/game.py               37      1    97%   22
core/player.py             26      2    92%   31, 38
pygame_ui/__init__.py       0      0   100%
tests/__init__.py           0      0   100%
tests/test_board.py        39      0   100%
tests/test_checker.py      22      1    95%   45
tests/test_dice.py         23      1    96%   55
tests/test_game.py         41      1    98%   66
tests/test_player.py       28      0   100%
-----------------------------------------------------
TOTAL                     312     26    92%

```
## Pylint Report
```text
************* Module main.py
main.py:1:0: F0001: No module named main.py (fatal)
************* Module test.py
test.py:1:0: F0001: No module named test.py (fatal)

```
