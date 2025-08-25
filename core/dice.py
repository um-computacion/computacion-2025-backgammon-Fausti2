import random

class Dice:
 
    def __init__(self):
        self.__values__ = []

    def roll(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        if die1 == die2:  
            self.__values__ = [die1, die1, die2, die2]
        else:
            self.__values__ = [die1, die2]

        return self.__values__

    def get_values(self):
        return self.__values__
