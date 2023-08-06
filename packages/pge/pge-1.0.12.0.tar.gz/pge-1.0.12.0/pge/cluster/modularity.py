import leidenalg
import igraph as ig
import networkx as nx
import numpy as np


def find_best_partition(graph):
    if graph.directed():
        g = ig.Graph.from_networkx(graph.get_nx_graph())
        res_p = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition).membership

        res = []
        for com in np.unique(res_p):
            res.append(set([g.vs[node]["_nx_name"] for node in np.arange(len(res_p)) if res_p[node] == com]))
        return res
    else:
        return nx.algorithms.community.greedy_modularity_communities(graph.get_nx_graph())
