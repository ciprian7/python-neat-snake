TAG_GENERAL = "GENERAL"
TAG_INFO = "NEW BEST"

size = 10
elitism = 0.2
mutationChance = 0.3

games = []
brains = []
generation = 1
globalBestLength = 0

avgLengths = []
maxLengths = []
avgSteps = []



def log(tag, message):
    print("[%s] \t %s" % (tag, message))


def first():
    global games, globalBestLength
    games = []
    brain = None
    try:
        with open('network', 'rb') as file:
            brain = pickle.load(file)
            globalBestLength = brain.length
    except:
        pass

    for i in range(0, size):
        if brain is None:
            game = Game()
        else:
            game = Game(brain)
        games.append(game)

    play = Play(games)
    result = play.play(window)
    return [games, result]


def collect():
    global brains
    brains = []
    for game in games:
        brains.append(game.getBrain())

    brains.sort(key=lambda x: -x.length)
    return brains


def newPopulation():
    global games, brains
    games = []
    for i in range(0, size):
        game = Game(brains[i])
        games.append(game)
    window = pygame.display.set_mode((width + dotSize, height + dotSize))
    play = Play(games)
    results = play.play(window)
    return [games, results]


def mutate():
    global brains, mutationChance
    for brain in brains[int(len(brains) * elitism):]:
        numMutations = np.random.randint(1, len(brain.weights))
        chance = np.random.uniform(0, 1)
        if mutationChance > chance:
            for _ in range(numMutations):
                index = np.random.randint(0, len(brain.weights))
                cell = np.random.randint(0, len(brain.weights[index]))
                randomValue = np.random.choice(
                    np.arange(-1, 1, step=0.001),
                    size=(1),
                    replace=False
                )
                old = brain.weights[index]
                brain.weights[index][cell] = brain.weights[index][cell] + randomValue
            # print("old: %s  => new: %s" % (old,  brain.weights[index]))


def crossover():
    global games, brains, elitism
    eliteSize = elitism * len(brains)
    offspringSize = int(len(brains) * (1 - elitism))
    offsprings = []
    for i in range(offspringSize):
        while True:
            motherIdx = random.randint(0, brains.shape[0] - 1)
            fatherIdx = random.randint(0, brains.shape[0] - 1)
            # print(str(i)+": "+str(motherIdx) + " " + str(fatherIdx))

            if motherIdx != fatherIdx and (motherIdx > eliteSize or fatherIdx > eliteSize):
                biases = []
                weights = []

                for k in range(len(brains[motherIdx].weights)):
                    if random.uniform(0, 1) < 0.5:
                        biases.append(brains[motherIdx].biases[k])
                        weights.append(brains[motherIdx].weights[k])
                    else:
                        biases.append(brains[fatherIdx].biases[k])
                        weights.append(brains[fatherIdx].weights[k])

                brain = Network(weights, biases)
                offsprings.append(brain)
                i += 1
                break

    return offsprings


def avgLength():
    global brains

    length = 0
    for brain in brains:
        length += brain.length

    return length / len(brains)

def getAvgSteps():
    global brains

    steps = 0
    for brain in brains:
        steps += brain.steps

    return steps / len(brains)

def write(brain):
    with open('network', 'wb') as file:
        pickle.dump(brain, file)


def stats():
    global brains

    values = {
        "avg_length": avgLength(),
        "max_length": brains[0].length,
        "avg_steps": getAvgSteps()
    }

    avgLengths.append(values["avg_length"])
    maxLengths.append(values["max_length"])
    avgSteps.append(values["avg_steps"])

    log(TAG_GENERAL, "Generation #%d results: \tStats: %s" % (generation, values))


def plot():
    global avgLengths
    plt.plot(avgLengths)
    plt.show()
    plt.close()


def neat():
    pl = NBPlot()
    pl.setData(
        (
            avgLengths,
            maxLengths,
            avgSteps,
            None
        )
    )
    pl.plot()
    global generation, games, brains, globalBestLength
    generation += 1
    [games, results] = first()

    while True:
        #pl.plot(finished=True)
        # print("Generation #%d" % (generation))
        brains = np.array(collect())
        stats()
        pl.setData(
            (
                avgLengths,
                maxLengths,
                avgSteps,
                results["best"][0]
            )
        )
        pl.plot()
        offsprings = crossover()
        elite = brains[:int(elitism * size)]
        brains = [*elite, *offsprings]
        mutate()
        if (brains[0].length > globalBestLength):
            log(TAG_INFO, "Saving new best (length: %d, previous %d)" % (brains[0].length, globalBestLength))
            globalBestLength = brains[0].length
            write(brains[0])
        generation += 1
        [games, results] = newPopulation()


def main():
    global pl
    neat()


if __name__ == '__main__':
    import pickle

    from main import *
    from Play import Play
    from Plotting import NBPlot
    import matplotlib.pyplot as plt
    import numpy as np
    from NeuralPlot import DrawNN

    window = pygame.display.set_mode((width + dotSize, height + dotSize))
    main()
