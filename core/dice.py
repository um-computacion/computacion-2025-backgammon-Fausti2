import random

class Dice:
 
    def __init__(self):
        self._values = []

    def roll(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        if die1 == die2:  
            self._values = [die1, die1, die2, die2]
        else:
            self._values = [die1, die2]

        return self._values

    def get_values(self):
        return self._values
