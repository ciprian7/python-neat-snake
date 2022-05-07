import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from NeuralPlot import DrawNN


class ProcessPlotter:
    def __init__(self):
        self.x = []
        self.y = []

    def setData(self, data):
        self.data = data

    def terminate(self):
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            data = self.pipe.recv()
            if data is None:
                self.terminate()
                return False
            else:
                avgLengths = data[0]
                maxLengths = data[1]
                avgSteps = data[2]
                best = data[3]
                if best is not None:
                    topology = best.topology
                    weights = best.weights
                    self.drawNN(topology, weights)
                self.ax.plot(avgLengths, color='green', linestyle='solid', label='test')
                self.ax.plot(maxLengths, color='blue', linestyle='solid', label='test')
                self.ax.plot(avgSteps, color='red', linestyle='solid', label='test')
        self.fig.canvas.draw()
        self.nn.canvas.draw()
        return True

    def drawNN(self, topology, weights):

        n_layers = len(topology)
        left = .1
        right = .9
        bottom = .1
        top = .9
        v_spacing = (top - bottom) / float(max(topology))
        h_spacing = (right - left) / float(len(topology) - 1)
        # Nodes
        for n, layer_size in enumerate(topology):
            layer_top = v_spacing * (layer_size - 1) / 2. + (top + bottom) / 2.
            for m in range(layer_size):
                circle = plt.Circle((n * h_spacing + left, layer_top - m * v_spacing), v_spacing / 4.,
                                    color='w', ec='k', zorder=4)
                self.bx.add_artist(circle)
        # Edges
        for n, (layer_size_a, layer_size_b) in enumerate(zip(topology[:-1], topology[1:])):
            layer_top_a = v_spacing * (layer_size_a - 1) / 2. + (top + bottom) / 2.
            layer_top_b = v_spacing * (layer_size_b - 1) / 2. + (top + bottom) / 2.
            for m in range(layer_size_a):
                for o in range(layer_size_b):
                    line = plt.Line2D([n * h_spacing + left, (n + 1) * h_spacing + left],
                                      [layer_top_a - m * v_spacing, layer_top_b - o * v_spacing], c='k')
                    if weights[n][m][o] > 0:
                        line.set_color('r')
                    else:
                        line.set_color('g')
                    line.set_linewidth(0.5)
                    self.bx.add_artist(line)

    def __call__(self, pipe):
        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        self.nn = plt.figure(figsize=(6, 6))
        self.bx = self.nn.gca()
        self.bx.axis('off')
        timer = self.fig.canvas.new_timer(interval=100)
        timer.add_callback(self.call_back)
        timer.start()
        plt.show()