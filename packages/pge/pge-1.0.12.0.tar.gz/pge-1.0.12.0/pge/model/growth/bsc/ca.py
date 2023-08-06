import networkx as nx
import numpy as np

from pge.model.growth.bsc.basic import SchemaGrowth


class CAGrowth(SchemaGrowth):
    def prep(self, graph):
        rs = nx.clustering(graph.get_nx_graph())
        graph.set_attrs("clust", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        return graph

    def choice(self, graph, sz, tp="in"):
        nodes = graph.get_ids(stable=True)
        probs = self.probs(graph)

        nodes, probs = nodes[probs > 0], probs[probs > 0]
        if probs.size == 0:
            return np.random.choice(graph.get_ids(stable=True), sz, replace=False)
        probs = probs / np.sum(probs)
        if np.sum(np.isnan(probs)):
            probs = np.ones(probs.size)/probs.size
        return np.random.choice(nodes, sz, replace=False, p=probs)

    def probs(self, graph):
        rs = np.power(graph.get_attributes("clust"), self.param[0]) + self.param[1]
        rs[np.isnan(rs)] = 0
        return rs
