import numpy as np
import networkx as nx

from pge.model.growth.bsc.basic_fix import FixSchemaGrowth


class FixUnGrowth(FixSchemaGrowth):
    @staticmethod
    def remove(graph):
        return np.random.choice(graph.get_ids(stable=True))


class FixDegGrowth(FixSchemaGrowth):
    @staticmethod
    def remove(graph):
        ids = graph.get_ids(stable=True)
        if graph.directed():
            dg = [1/(graph.count_in_degree(node) + graph.count_out_degree(node)+1) for node in ids]
        else:
            dg = [1/(graph.count_degree(node)+1) for node in ids]
        return np.random.choice(ids, p=dg/np.sum(dg))


class FixClustGrowth(FixSchemaGrowth):
    @staticmethod
    def remove(graph):
        ids = graph.get_ids(stable=True)
        rs = nx.clustering(graph.get_nx_graph())
        dg = np.array([1 if rs[node] is np.NaN else 1/(rs[node]+1) for node in ids])
        return np.random.choice(ids, p=dg/np.sum(dg))
