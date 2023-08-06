import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph
from pge.model.growth.bsc.init import BasicGrowth


class SchemaGrowth(BasicGrowth):
    def __init__(self, graph, deg, params, schema):
        BasicGrowth.__init__(self, graph, deg, params)
        self.schema = schema

    def make_copy(self, gr):
        if gr.directed():
            graph = nx.MultiDiGraph()
        else:
            graph = nx.MultiGraph()

        count = 0
        for edge in gr.get_edges():
            graph.add_edge(edge[0], edge[1], key="old-"+str(count))
            count += 1
        return SGraph(graph)

    def proceed(self, n, save=None, attr="cnt"):
        self.count = 0
        nw_graph = self.make_copy(self.gr)
        nx.set_node_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nx.set_edge_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nw_graph = self.new_load(nw_graph)

        count = self.gr.size()
        for _ in np.arange(n):
            print(_)
            if self.stop():
                break

            nw_graph = self.prep(nw_graph)
            self.add(nw_graph)
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node == 1:
                self.new_edge_add(nw_graph, (attr, _))
            else:
                self.new_node_add(nw_graph, str(count), (attr, _), new_node)
                count += 1
        if save is None:
            return nw_graph
        else:
            self.save(nw_graph, save)

    def probs(self, graph):
        return []
