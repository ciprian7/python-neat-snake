from threading import Thread

import pygame
import math
from main import dotSize, distance, speed
from launcher import log, TAG_INFO

debug = False


class Play:
    def __init__(self, games):
        self.games = games
        self.best = [None, 0]

    def over(self):
        for game in self.games:
            if game.snake.dead is False:
                return False

        return True

    def play(self, window):
        pygame.display.set_caption('Snake')
        fps = pygame.time.Clock()
        while not self.over():
            window.fill(pygame.Color(0, 0, 0))
            for game in self.games:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                            game.snake.changeDirTo('RIGHT')
                        if event.key == pygame.K_w:
                            game.snake.changeDirTo('UP')
                        if event.key == pygame.K_s:
                            game.snake.changeDirTo('DOWN')
                        if event.key == pygame.K_a:
                            game.snake.changeDirTo('LEFT')
                if not game.snake.dead:
                    foodPos = game.foodSpawner.spawnFood()
                    #game.snake.move(foodPos)
                    if game.snake.score >= 0:
                        for pos in game.snake.getBody():
                            pygame.draw.rect(window, game.snake.color,
                                             pygame.Rect(pos[0], pos[1], dotSize, dotSize))
                        pygame.draw.rect(window, game.snake.color,
                                         pygame.Rect(foodPos[0], foodPos[1], dotSize, dotSize))
                    if game.snake.checkCollision() == 1:
                        game.snake.dead = True
                        game.gameOver()

                    thread = Thread(target=self.logic, args=(game, foodPos))
                    thread.start()
                    
                    #self.logic(game, foodPos)


                    if game.snake.size() > self.best[1]:
                        if game.brain != self.best[0]:
                            self.best = [game.brain, game.snake.size()]
                            log(TAG_INFO, "\tNew best in current generation (length: %d)" % (self.best[1]))
                        else:
                            self.best[1] = game.snake.size()
                            log(TAG_INFO, "\tCurrent best still outperforming (length: %d)" % (self.best[1]))

            pygame.display.flip()
            fps.tick(speed)

        return {
            "best": self.best
        }

    
    def logic(self, game, foodPos):
        input = game.snake.getInput(foodPos)
        output = game.brain.think(input)
        game.interpret(output, foodPos)