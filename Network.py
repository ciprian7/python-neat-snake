import numpy as np


class Network:
    def __init__(self):
        inputSize = 4
        hiddenSize = 6
        outputSize = 3
        self.weights = [
            np.random.randn(inputSize, hiddenSize),
            np.random.randn(hiddenSize, hiddenSize),
            np.random.randn(hiddenSize, outputSize)
        ]

        self.biases = [
            np.zeros((1, hiddenSize)),
            np.zeros((1, hiddenSize)),
            np.zeros((1, outputSize))
        ]

        self.score = 0

    def think(self, input):
        z1 = np.array(input).dot(self.weights[0]) + self.biases[0]
        a1 = np.tanh(z1)

        z2 = a1.dot(self.weights[1]) + self.biases[1]
        a2 = np.tanh(z2)

        z3 = a2.dot(self.weights[2]) + self.biases[2]

        maxIndex = np.argmax(z3[0])

        return maxIndex

    def setScore(self, score):
        self.score = score

    def __str__(self):
        return "Score: " + str(self.score)
