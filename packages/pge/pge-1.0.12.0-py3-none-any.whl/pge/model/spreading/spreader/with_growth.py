import numpy as np

from pge.model.growth.bsc.basic import SchemaGrowth
from pge.model.growth.created import PASchemaFreeEvolve
from pge.model.spreading.spreader.basic import SpreadingModel


class DeltaCheck(SchemaGrowth):
    def __init__(self, graph, deg, params, schema, delta):
        SchemaGrowth.__init__(self, graph, deg, params, schema)
        self.delta = delta

    def add(self, graph):
        return


class PASpread(PASchemaFreeEvolve, SpreadingModel):
    def __init__(self, graph, deg, params, schema, rs, received=None, in_direct=False):
        if received is None:
            self.received = {str(node): {1} for node in graph.get_ids()}
        else:
            self.received = received
        self.initial_status = {
            k: self.received[k].copy() for k in self.received.keys()
        }
        self.rs = rs
        self.update(0)
        self.in_direct = in_direct
        PASchemaFreeEvolve.__init__(self, graph, deg, params, schema)

    def stop(self):
        return self.rs <= np.min([time[1] for time in self.times])

    def new_node_add(self, graph, to, attrs, tp=None):
        edges = super().new_node_add(graph, to, attrs, tp)
        nodes = []
        for edge in edges:
            if edge[0] != to:
                nodes.append(edge[0])
            else:
                nodes.append(edge[1])

        rs = set()
        check = (self.in_direct is False and ((tp == 1 and graph.directed() is False) or tp == 2)) or (
                self.in_direct and ((tp == 1 and graph.directed() is False) or tp == 0))
        if check:
            for node in nodes:
                rs.update(self.received[str(node)])
        self.received.update({to: rs})

        if check:
            self.update(attrs[1] + 1)

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
        gr.add_edge(node1, node2, attrs[1] + 1, {attrs[0]: attrs[1] + 1})

        if self.in_direct:
            (self.received[str(node2)]).update(self.received[str(node1)])
        else:
            (self.received[str(node1)]).update(self.received[str(node2)])
        self.update(attrs[1] + 1)

    def new_load(self, gr):
        self.received = {
            k: self.initial_status[k].copy() for k in self.initial_status.keys()
        }
        return gr


class PADeltaSpread(PASpread, DeltaCheck):
    def __init__(self, graph, deg, params, schema, rs, delta, received=None):
        self.delta = delta
        self.deltas = [1]
        PASpread.__init__(self, graph, deg, params, schema, rs, received)
        self.ms = np.unique(self.received.values()).size

    def stop(self):
        return self.deltas[-1] <= self.delta

    def add(self, graph, sz=100):
        lns = []
        for _ in np.arange(sz):
            new_node = np.random.choice(len(self.schema), p=self.schema)
            nw_1 = self.received.copy()
            if new_node == 1:
                node1, node2 = str(self.choice(graph, 1, tp="out")[0]), str(self.choice(graph, 1, tp="in")[0])
                nw_1[node2].update(self.received[node1])
            else:
                if new_node != 0:
                    if self.deg[1][0] == "const":
                        nodes = self.choice(graph, self.deg[1][1], tp="out")
                    else:
                        nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

                    rs = set()
                    for node in nodes:
                        rs.update(self.received[str(node)])
                    nw_1.update({"tst": rs})
            lns = np.append(lns, np.unique([list(i_) for i_ in nw_1.values() if len(i_) > 0], return_counts=True)[1])
        lns = np.unique(np.reshape(lns, (self.ms, sz)), axis=1, return_counts=True)
        lns = (lns[0], np.reshape(lns[1], lns[0].shape))
        self.deltas.append(np.sum(lns[1][lns[0] < self.rs]/sz))
