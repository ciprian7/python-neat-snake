#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import math
from Network import Network
import numpy as np

width = 490
height = 490
dotSize = 10
speed = 60


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
        self.color = random.choices(range(256), k=3)
        self.stepsWithoutFood = 0

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
        self.stepsWithoutFood += 1
        self.steps += 1
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
            self.stepsWithoutFood = 0
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
        foodCheck = [x / width for x in self.checkFood(foodPos)]
        relCollisions = [x / width for x in self.relativeCollisions(foodPos)]

        input = [
            int(collisions[0]),
            int(collisions[1]),
            int(collisions[2]),

            foodCheck[0],
            foodCheck[1],
            foodCheck[2],

            relCollisions[0] / width,
            relCollisions[1] / width,
            relCollisions[2] / width
        ]
        # input[3] = self.angle(foodPos)

        return input

    def angle(self, foodPos):
        appleVector = np.array(foodPos) - np.array(self.position)
        snakeVector = np.array(self.position) - np.array(self.position)

        appleNormVector = np.linalg.norm(appleVector)
        snakeNormVector = np.linalg.norm(snakeVector)
        if appleNormVector == 0:
            appleNormVector = 10
        if snakeNormVector == 0:
            snakeNormVector = 10

        appleDirectionNormalized = appleVector / appleNormVector
        snkaeDirectionNormalized = snakeVector / snakeNormVector
        angle = math.atan2(appleDirectionNormalized[1] * snkaeDirectionNormalized[0] -
                           appleDirectionNormalized[0] * snkaeDirectionNormalized[1],
                           appleDirectionNormalized[1] * snkaeDirectionNormalized[1] +
                           appleDirectionNormalized[0] * snkaeDirectionNormalized[0]) / math.pi
        return angle

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

    def wall(self, position):
        x = position[0]
        y = position[1]
        return x * dotSize >= width or \
               y * dotSize >= height or \
               x <= 0 or \
               y <= 0

    def distWalls(self):
        x = self.position[0]
        y = self.position[1]
        return [
            distance(self.position, (x, 0)),
            distance(self.position, (x, height)),
            distance(self.position, (0, y)),
            distance(self.position, (width, y))
        ]

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

    def northdistCheck(self, foodPos):
        x = self.position[0]
        y = self.position[1]
        dist = min(self.distWalls())

        for block in self.body:
            if y > block[1] and x == block[0]:
                otherDist = distance(self.position, block)
                dist = dist if dist <= otherDist else otherDist

        return dist

    def southdistCheck(self, foodPos):
        x = self.position[0]
        y = self.position[1]
        dist = min(self.distWalls())

        for block in self.body:
            if y < block[1] and x == block[0]:
                otherDist = distance(self.position, block)
                dist = dist if dist <= otherDist else otherDist

        return dist

    def eastdistCheck(self, foodPos):
        x = self.position[0]
        y = self.position[1]
        dist = min(self.distWalls())

        for block in self.body:
            if y == block[1] and x < block[0]:
                otherDist = distance(self.position, block)
                dist = dist if dist <= otherDist else otherDist

        return dist

    def westdistCheck(self, foodPos):
        x = self.position[0]
        y = self.position[1]
        dist = min(self.distWalls())

        for block in self.body:
            if y == block[1] and x > block[0]:
                otherDist = distance(self.position, block)
                dist = dist if dist <= otherDist else otherDist

        return dist

    def checkFood(self, foodPos):
        x = self.position[0]
        y = self.position[1]
        dist = distance(self.position, foodPos)

        match self.direction:
            case 'UP':
                forward = [x, y - 1]
                left = [x - 1, y]
                right = [x + 1, y]
                distances = [
                    distance(forward, foodPos),
                    distance(left, foodPos),
                    distance(right, foodPos)
                ]
                collisions = [
                    distances[0] if distances[0] < dist else -1,
                    distances[1] if distances[1] < dist else -1,
                    distances[2] if distances[2] < dist else -1
                ]
                return collisions
            case 'DOWN':
                forward = [x, y + 1]
                left = [x + 1, y]
                right = [x - 1, y]
                distances = [
                    distance(forward, foodPos),
                    distance(left, foodPos),
                    distance(right, foodPos)
                ]
                collisions = [
                    distances[0] if distances[0] < dist else -1,
                    distances[1] if distances[1] < dist else -1,
                    distances[2] if distances[2] < dist else -1
                ]
                return collisions
            case 'LEFT':
                forward = [x - 1, y]
                left = [x, y + 1]
                right = [x, y - 1]
                distances = [
                    distance(forward, foodPos),
                    distance(left, foodPos),
                    distance(right, foodPos)
                ]
                collisions = [
                    distances[0] if distances[0] < dist else -1,
                    distances[1] if distances[1] < dist else -1,
                    distances[2] if distances[2] < dist else -1
                ]
                return collisions
            case 'RIGHT':
                forward = [x + 1, y]
                left = [x, y - 1]
                right = [x, y + 1]
                distances = [
                    distance(forward, foodPos),
                    distance(left, foodPos),
                    distance(right, foodPos)
                ]
                collisions = [
                    distances[0] if distances[0] < dist else -1,
                    distances[1] if distances[1] < dist else -1,
                    distances[2] if distances[2] < dist else -1
                ]

                return collisions
            case _:
                return None

    def relativeCollisions(self, foodPos):
        match self.direction:
            case 'UP':
                return [
                    self.northdistCheck(foodPos),
                    self.westdistCheck(foodPos),
                    self.eastdistCheck(foodPos)
                ]
            case 'DOWN':
                return [
                    self.southdistCheck(foodPos),
                    self.eastdistCheck(foodPos),
                    self.westdistCheck(foodPos)
                ]
            case 'LEFT':
                return [
                    self.westdistCheck(foodPos),
                    self.southdistCheck(foodPos),
                    self.northdistCheck(foodPos)
                ]
            case 'RIGHT':
                return [
                    self.eastdistCheck(foodPos),
                    self.northdistCheck(foodPos),
                    self.southdistCheck(foodPos)
                ]
            case _:
                return None


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
    def __init__(self, brain=None):
        self.snake = Snake()
        self.foodSpawner = FoodSpawer()
        if brain is None:
            self.brain = Network()
        else:
            self.brain = brain

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
            self.snake.score += abs(self.snake.score) * (math.sqrt(self.snake.size()) + 1)
            self.foodSpawner.setFoodOnScreen(False)

        if self.snake.score <= - 40 or self.snake.stepsWithoutFood > 100:
            self.snake.dead = True

        if self.snake.dead is True:
            del self

    def gameOver(self):
        pass

    def exit(self):
        pygame.quit()

    def drawText(self, string, position, window):
        font = pygame.font.SysFont("arial", 16)
        text = font.render(str(string), True, (255, 255, 153))
        window.blit(text, position)

    def drawLine(self, start, end, window):
        pygame.draw.line(window, (255, 0, 0), start, end)

    def getBrain(self):
        self.brain.setScore(self.snake.score)
        self.brain.setLength(self.snake.size())
        self.brain.setSteps(self.snake.steps)
        return self.brain
