import networkx as nx

from pge.init.classes.graph import SGraph
from pge.model.growth.bsc.basic import SchemaGrowth


class SimpleGrowth(SchemaGrowth):
    def __init__(self, graph, deg, params):
        super(SchemaGrowth, self).__init__(graph, (deg, ), params)
        self.schema = [1]
        self.param = params

    def make_copy(self, gr):
        if gr.directed():
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()

        count = 0
        for edge in gr.get_edges():
            graph.add_edge(edge[0], edge[1], key="old-" + str(count))
            count += 1
        return SGraph(graph)
