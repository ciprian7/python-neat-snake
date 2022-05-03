from main import *

size = 3000
brains = []
def fitness():
    pass

def first():
    global brains
    brains = []
    for i in range (0, size):
        print("Snake #%d" % (i+1))
        game = Game()
        game.play()
        brains.append(game.getBrain())

pygame.init()
first()

brains.sort(key=lambda x: -x.score)
print(brains[0])
