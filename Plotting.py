import multiprocessing as mp
import time
import numpy as np
from ProcessPlotter import ProcessPlotter
from NeuralPlot import DrawNN

class NBPlot:
    def __init__(self):
        self.data = None
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def setData(self, data):
        self.data = data

    def plot(self, finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
        else:
            send(self.data)
