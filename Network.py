import numpy as np
import random
import string

globalId = 1


class Network:
    def __init__(self, weights=None, biases=None):
        self.inputSize = 9
        self.hiddenSize = [27, 18]
        self.outputSize = 3

        if len(self.hiddenSize) == 1:
            self.topology = [self.inputSize, self.hiddenSize[0], self.outputSize]

        else:
            if len(self.hiddenSize) == 2:
                self.topology = [self.inputSize, self.hiddenSize[0], self.hiddenSize[1], self.outputSize]


        if weights is None:
            if len(self.hiddenSize) == 1:
                self.weights = [
                    np.random.randn(self.inputSize, self.hiddenSize[0]),
                    np.random.randn(self.hiddenSize[0], self.hiddenSize[0]),
                    np.random.randn(self.hiddenSize[0], self.outputSize)
                ]
            else:
                if len(self.hiddenSize) == 2:
                    self.weights = [
                        np.random.randn(self.inputSize, self.hiddenSize[0]),
                        np.random.randn(self.hiddenSize[0], self.hiddenSize[0]),
                        np.random.randn(self.hiddenSize[0], self.hiddenSize[1]),
                        np.random.randn(self.hiddenSize[1], self.outputSize)
                    ]

        else:
            self.weights = weights

        if biases is None:
            if len(self.hiddenSize) == 1:
                self.biases = [
                    np.random.rand(1, self.hiddenSize[0]),
                    np.random.rand(1, self.hiddenSize[0]),
                    np.random.rand(1, self.outputSize)
                ]
            else:
                if len(self.hiddenSize) == 2:
                    self.biases = [
                        np.random.rand(1, self.hiddenSize[0]),
                        np.random.rand(1, self.hiddenSize[0]),
                        np.random.rand(1, self.hiddenSize[1]),
                        np.random.rand(1, self.outputSize)
                    ]

        else:
            self.biases = biases

        self.score = 0
        self.length = 0
        self.steps = None

        self.id = (''.join(random.choice(string.ascii_letters) for i in range(10)))

    def think(self, input):
        z = np.array(input).dot(self.weights[0]) + self.biases[0]
        a = np.tanh(z)

        for i in range(1, len(self.topology)):
            z = \
                a.dot(self.weights[i])\
                + self.biases[i]
            a = np.tanh(z)

        maxIndex = np.argmax(z[0])

        return maxIndex

    def setScore(self, score):
        self.score = score

    def setLength(self, length):
        self.length = length

    def setSteps(self, steps):
        self.steps = steps

    def __str__(self):
        return "Score: " + str(self.score) + "Length: " + str(self.length)
