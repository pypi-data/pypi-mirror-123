import numpy as np

from pge.model.spreading.spreader.basic import SpreadingModel


class FixSpreadModel(SpreadingModel):
    def __init__(self, graph, in_direct=False):
        super().__init__(graph)
        self.ids = self.graph.get_ids(stable=True)
        self.in_direct = in_direct

    def init(self):
        self.received = {
            k: self.initial_status[k].copy() for k in self.initial_status.keys()
        }
        self.update(0)

    def iteration_bunch_comm(self, num_iter, tick, rs):
        res = []
        self.rs = np.max(rs)
        rs = np.array(rs)

        for _ in np.arange(num_iter):
            n = 1
            self.init()

            count = 0
            while self.rs > np.min([time[1] for time in self.times]):
                if n > tick:
                    break

                self.iteration()
                self.update(n)
                n += 1

                if np.sum(rs[count:] == np.min([time[1] for time in self.times])) > 0:
                    res = np.append(res, [time.copy() for time in self.times])
                    count += 1
                    print(n)

            res = np.append(res, [time.copy() for time in self.times])
        res = np.reshape(res, (res.size // 3, 3))
        return res

    def one_spread(self, tick):
        self.rs = self.graph.size()

        n = 1
        self.init()
        res = {node: 0 for node in self.graph.get_ids() if len(self.received[node]) == 1}

        while self.rs > np.min([time[1] for time in self.times]):
            if n > tick:
                break

            self.iteration()
            self.update(n)
            res.update({node: n for node in self.graph.get_ids() if
                        len(self.received[node]) == 1 and node not in list(res.keys())})
            n += 1

        res.update({node: tick*100 for node in self.graph.get_ids() if node not in list(res.keys())})
        return res, n
