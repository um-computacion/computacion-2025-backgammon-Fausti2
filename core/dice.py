import random

class Dice:
 
    def __init__(self):
        self.__values = []

    def roll(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        if die1 == die2:  
            self.__values = [die1, die1, die2, die2]
        else:
            self.__values = [die1, die2]

        return self.__values

    def get_values(self):
        return self.__values

    def set_values(self, values):
        if all(1 <= v <= 6 for v in values):
            self.__values = values
        else:
            raise ValueError("Los valores deben estar entre 1 y 6") 
        
        