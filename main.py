#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import math
from Network import Network

width = 490
height = 490
dotSize = 10
speed = 60

window = pygame.display.set_mode((width + dotSize, height + dotSize))

def distance(_from, _to):
    return math.sqrt((_from[0] - _to[0]) ** 2 + (_from[1] - _to[1]) ** 2)


class Snake:

    def __init__(self):
        self.radians = None
        self.steps = 0
        self.score = 0
        self.dead = False
        self.position = [random.randrange(1, 50) * dotSize,
                         random.randrange(1, 50) * dotSize]
        self.body = [self.position]
        self.direction = 'RIGHT'
        self.changeDirectionTo = self.direction

    def changeDirTo(self, dir):
        if dir == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if dir == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if dir == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if dir == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def size(self):
        return len(self.body)

    def turnLeft(self):
        match self.direction:
            case 'UP':
                self.changeDirTo('LEFT')
                return
            case 'DOWN':
                self.changeDirTo('RIGHT')
                return
            case 'LEFT':
                self.changeDirTo('DOWN')
                return
            case 'RIGHT':
                self.changeDirTo('UP')
                return
            case _:
                return

    def turnRight(self):
        match self.direction:
            case 'UP':
                self.changeDirTo('RIGHT')
                return
            case 'DOWN':
                self.changeDirTo('LEFT')
                return
            case 'LEFT':
                self.changeDirTo('UP')
                return
            case 'RIGHT':
                self.changeDirTo('DOWN')
                return
            case _:
                return

    def move(self, foodPos):
        if self.direction == 'RIGHT':
            self.position[0] += dotSize
        if self.direction == 'LEFT':
            self.position[0] -= dotSize
        if self.direction == 'UP':
            self.position[1] -= dotSize
        if self.direction == 'DOWN':
            self.position[1] += dotSize
        self.body.insert(0, list(self.position))
        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0

    def checkCollision(self):
        if self.position[0] > width or self.position[0] < 0:
            return 1
        elif self.position[1] > height or self.position[1] < 0:
            return 1
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return 1
        return 0

    def getHeadPos(self):
        return self.position

    def getBody(self):
        return self.body

    def getInput(self, foodPos):
        self.radians = math.atan2(foodPos[1] - self.position[1], foodPos[0] - self.position[0])

        collisions = self.checkBodyCollisions()
        input = [0, 0, 0, 0]

        input[0] = collisions[0]
        input[1] = collisions[1]
        input[2] = collisions[2]
        input[3] = math.sin(math.radians(self.radians))

        return input

    def getRadians(self):
        return self.radians

    def checkBodyCollisions(self):
        collisions = [0, 0, 0]
        match self.direction:
            case 'UP':
                collisions[0] = self.northBodyCheck()
                collisions[1] = self.westBodyCheck()
                collisions[2] = self.eastBodyCheck()
                return collisions
            case 'DOWN':
                collisions[0] = self.southBodyCheck()
                collisions[1] = self.eastBodyCheck()
                collisions[2] = self.westBodyCheck()
                return collisions
            case 'LEFT':
                collisions[0] = self.westBodyCheck()
                collisions[1] = self.southBodyCheck()
                collisions[2] = self.northBodyCheck()
                return collisions
            case 'RIGHT':
                collisions[0] = self.eastBodyCheck()
                collisions[1] = self.northBodyCheck()
                collisions[2] = self.southBodyCheck()
                return collisions
            case _:
                return collisions

        return collisions

    def northBodyCheck(self):
        x = self.position[0]
        y = self.position[1]
        hasBody = 0

        for block in self.body:
            if y > block[1] and x == block[0]:
                hasBody = 1

        return hasBody

    def southBodyCheck(self):
        x = self.position[0]
        y = self.position[1]
        hasBody = 0

        for block in self.body:
            if y < block[1] and x == block[0]:
                hasBody = 1

        return hasBody

    def eastBodyCheck(self):
        x = self.position[0]
        y = self.position[1]
        hasBody = 0

        for block in self.body:
            if y == block[1] and x < block[0]:
                hasBody = 1

        return hasBody

    def westBodyCheck(self):
        x = self.position[0]
        y = self.position[1]
        hasBody = 0

        for block in self.body:
            if y == block[1] and x > block[0]:
                hasBody = 1

        return hasBody

    def think(self, foodPos):
        input = self.getInput(foodPos)


class FoodSpawer:

    def __init__(self):
        self.position = [random.randrange(1, 50) * dotSize,
                         random.randrange(1, 50) * dotSize]
        self.isFoodOnScreen = True

    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(1, 50) * dotSize,
                             random.randrange(1, 50) * dotSize]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b

class Game:
    def __init__(self):
        self.snake = Snake()
        self.foodSpawner = FoodSpawer()
        self.brain = Network()



    def interpret(self, output, foodPos):
        distThen = distance(self.snake.getHeadPos(), foodPos)
        match output:
            case 0:
                pass
            case 1:
                self.snake.turnLeft()
                pass
            case 2:
                self.snake.turnRight()
            case _:
                pass

        if self.snake.move(foodPos) == 1:
            self.foodSpawner.setFoodOnScreen(False)

        distNow = distance(self.snake.getHeadPos(), foodPos)

        if distNow < distThen:
            self.snake.score += 1
        else:
            self.snake.score -= 1.5

        if self.snake.position == foodPos:
            self.snake.score += self.snake.score * (self.snake.size() + 1)
            self.foodSpawner.setFoodOnScreen(False)

        if self.snake.score < - 40:
            self.snake.dead = True

    def gameOver(self):
        print("qqq")

    def exit(self):
        pygame.quit()

    def drawText(self,string, position):
        font = pygame.font.SysFont("arial", 16)
        text = font.render(str(string), True, (255, 255, 153))
        window.blit(text, position)

    def drawLine(self,start, end, window):
        pygame.draw.line(window, (255, 0, 0), start, end)

    def play(self):
        pygame.display.set_caption('Snake')
        fps = pygame.time.Clock()
        while not self.snake.dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.snake.changeDirTo('RIGHT')
                    if event.key == pygame.K_w:
                        self.snake.changeDirTo('UP')
                    if event.key == pygame.K_s:
                        self.snake.changeDirTo('DOWN')
                    if event.key == pygame.K_a:
                        self.snake.changeDirTo('LEFT')
            foodPos = self.foodSpawner.spawnFood()
            window.fill(pygame.Color(0, 0, 0))
            for pos in self.snake.getBody():
                pygame.draw.rect(window, pygame.Color(0, 225, 0),
                                 pygame.Rect(pos[0], pos[1], dotSize, dotSize))
            pygame.draw.rect(window, pygame.Color(225, 0, 0),
                             pygame.Rect(foodPos[0], foodPos[1], dotSize, dotSize))
            if self.snake.checkCollision() == 1:
                self.snake.dead = True
                self.gameOver()
            pygame.display.set_caption('Snake | Score : ' + str(self.snake.score))

            input = self.snake.getInput(foodPos)
            output = self.brain.think(input)
            self.interpret(output, foodPos)
            radians = self.snake.getRadians()
            headPos = self.snake.getHeadPos()
            startX = headPos[0] / dotSize
            startY = headPos[1] / dotSize
            headPos = self.snake.getHeadPos()
            foodDist = distance(headPos, foodPos)
            endX = startX + round(math.cos(radians)) * foodDist
            endY = startY + round(math.sin(radians)) * foodDist
            self.drawLine([startX * dotSize, startY * dotSize], [endX * dotSize, endY * dotSize], window)

            obst = "Obstalce: "
            if input[0] == 1:
                obst += "AHEAD "
            if input[1] == 1:
                obst += "LEFT "
            if input[2] == 1:
                obst += "RIGHT "

            self.snake.steps += 1
            self.drawText(obst, [0, 10])
            self.drawText("Steps: " + str(self.snake.steps), [0, 30])
            self.drawText("Score: " + str(self.snake.score), [0, 50])

            pygame.display.flip()
            fps.tick(speed)

        print("Score %2.f | Length: %d | Steps: %d" % (self.snake.score, self.snake.size(), self.snake.steps))

    def getBrain(self):
        self.brain.setScore(self.snake.score)
        return self.brain
