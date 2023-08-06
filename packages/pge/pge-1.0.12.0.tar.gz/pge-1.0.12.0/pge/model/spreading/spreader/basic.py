import numpy as np


class SpreadingModel(object):
    def __init__(self, graph):
        self.graph = graph
        self.initial_status = {}
        self.received = {}
        self.times = []
        self.rs = 0

    def update(self, tm):
        fl = []
        for val in self.received.values():
            fl = np.append(fl, list(val))
        fl = np.unique(fl, return_counts=True)
        if tm == 0:
            self.times = [[fl[0][i], fl[1][i], 0] for i in np.arange(fl[0].size)]
        else:
            for i in np.arange(fl[0].size):
                if self.times[i][1] < self.rs and self.times[i][1] != fl[1][i]:
                    self.times[i][1] = fl[1][i]
                    self.times[i][2] = tm

    def set_initial_status(self, configuration):
        self.initial_status = configuration

    def iteration_bunch_comm(self, num_iter, tick, rs):
        return

    def iteration(self):
        return None, True
