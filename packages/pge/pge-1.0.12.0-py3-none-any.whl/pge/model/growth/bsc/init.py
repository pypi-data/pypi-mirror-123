import networkx as nx


class BasicGrowth:
    def __init__(self, graph, deg, params):
        self.gr = graph
        self.deg = deg
        if graph.directed():
            self.param = params
        else:
            self.param = (params, )
        self.count = 0

    def choice(self, gr, sz, tp="in"):
        return []

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
        gr.add_edge(node1, node2, str(self.count), {attrs[0]: attrs[1]})
        self.count += 1
        return node1, node2

    def new_node_add(self, graph, to, attrs, tp=None):
        if tp == 0:
            if self.deg[0][0] == "const":
                nodes = self.choice(graph, self.deg[0][1], tp="in")
            else:
                nodes = self.choice(graph, self.deg[0][0](self.deg[0][1]), tp="in")
        else:
            if self.deg[1][0] == "const":
                nodes = self.choice(graph, self.deg[1][1], tp="out")
            else:
                nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

        edges = []
        for node in nodes:
            if tp == 0:
                graph.add_edge(to, node, key=str(self.count), prms={attrs[0]: attrs[1]})
                edges.append((to, node, self.count))
            else:
                graph.add_edge(node, to, key=str(self.count), prms={attrs[0]: attrs[1]})
                edges.append((node, to, self.count))
            self.count += 1
        graph.set_attr(to, attrs[0], attrs[1])
        return edges

    def prep(self, graph):
        return graph

    def make_copy(self, gr):
        return gr

    def proceed(self, n, save=None, attr="cnt"):
        if save is None:
            return None

    @staticmethod
    def save(gr, to):
        if gr.multiedges() is False:
            for edge in gr.gr.edges(data=True):
                del edge[2]["key"]
        nx.write_graphml(gr.get_nx_graph(), to + ".graphml")

    def new_load(self, gr):
        return gr

    def stop(self):
        return False

    def add(self, graph):
        return

