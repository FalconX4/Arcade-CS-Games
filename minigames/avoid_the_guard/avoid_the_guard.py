import pygame
import input_map
from minigames import minigame
from minigames import multiplayer
from entities import PersoPlayer
from entities import PersoLeprechaun

class AvoidTheGuard(multiplayer.Minigame):
    name = 'Avoid the guards!'
    max_duration = 10000

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)

        self.width = game.GAME_WIDTH
        self.height = game.GAME_HEIGHT

    def init(self):
        self.background = pygame.image.load("./res/img/avoid_the_guard/Background.png").convert()

        self.players = [PersoPlayer(50, 300, "./res/img/avoid_the_guard/Player1.png", self.difficulty), \
                        PersoPlayer(700, 300, "./res/img/avoid_the_guard/Player2.png", self.difficulty), ]
        self.enemies = []
        self.initEnnemies()

        self.score = [self.players[0].life, self.players[1].life]

        self.currentTime = pygame.time.get_ticks()/1000.0

    def initEnnemies(self):
        for index in range(self.difficulty+3):
            self.enemies.append(PersoLeprechaun(375, 300, "./res/img/avoid_the_guard/Guard.png", self.difficulty, self.players))

    def tick(self):
        self.score[0] = self.players[0].life
        self.score[1] = self.players[1].life

        self.events()
        self.update(pygame.time.get_ticks()/1000.0 - self.currentTime)
        self.draw()

        self.currentTime = pygame.time.get_ticks()/1000.0

    def get_results(self):
        if self.players[0].life > self.players[1].life:
            return [True, False]
        elif self.players[0].life < self.players[1].life:
            return [False, True]
        else:
            return [False, False]

    def update(self, timeElapsed):
        for player in self.players:
            player.update(timeElapsed)

        for enemy in self.enemies:
            enemy.update(timeElapsed)

        self.checkEnnemyCollisions()

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        for player in self.players:
            player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

    def events(self):
        pygame.event.get()
        for i in range(2):
            keys = input_map.get_player_keys(i)
            if keys[input_map.UP]:
                self.players[i].move("up")
            if keys[input_map.RIGHT]:
                self.players[i].move("right")
            if keys[input_map.DOWN]:
                self.players[i].move("down")
            if keys[input_map.LEFT]:
                self.players[i].move("left")
            if keys[input_map.ACTION]:
                self.hit(i)

    def checkEnnemyCollisions(self):
        for ennemy in self.enemies:
            for player in self.players:
                if ennemy.sprite.rect.colliderect(player.sprite.rect):
                    player.life -= 1
                    self.elapsed_ms = 10000

    def hit(self, player):
        if self.players[player].hit():
            other = abs(player-1)
            if not self.players[other].isHurt() and self.players[player].sprite.rect.colliderect(self.players[other].sprite.rect):
                self.players[other].hurt(self.players[player].pos)
