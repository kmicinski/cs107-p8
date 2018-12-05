# The `LevelState` class keeps track of all of the critical
# information about the player during the level.
class LevelState:
    def __init__(self, initialHP):
        # The amount of "fuel" the player has
        self.hp   = initialHP
        self.won  = False
        self.over = False

    # Decrease the amount of fuel by i
    def decrementFuel(self,i):
        self.hp = self.hp - i
        if (self.hp <= 0):
            self.over = True

    # Decrease the amount of fuel by i
    def incrementFuel(self,i):
        self.hp += i

    # Set whether the game has been won
    def setWon(self):
        self.won  = True
        self.over = True

    # Check whether the game is over or not
    def gameOver(self):
        return self.over

    # Get whether the game has been won or not.
    def hasWon(self):
        return self.won
