from perso import Perso
import random

class PersoGuard(Perso):
    def __init__(self, x, y, path, difficulty, players):
        self.KEEP_DIR_TIME = 0.25

        Perso.__init__(self, x, y, path, difficulty)
        self.difficulty = difficulty
        self.players = players
        self.keepDirTime = 0.5
        self.dir = 0

    def update(self, timeElapsed):
        Perso.update(self, timeElapsed)

        self.keepDirTime += timeElapsed

        if self.keepDirTime >= self.KEEP_DIR_TIME:
            self.keepDirTime = 0
            self.dir = random.randint(0,3)

        if self.dir == 0:
            self.move("up")
        elif self.dir == 1:
            self.move("right")
        elif self.dir == 2:
            self.move("down")
        elif self.dir == 3:
            self.move("left")