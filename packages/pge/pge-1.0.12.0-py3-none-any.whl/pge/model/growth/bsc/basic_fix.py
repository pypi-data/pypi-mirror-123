import numpy as np

from pge.model.growth.bsc.basic import SchemaGrowth


class FixSchemaGrowth(SchemaGrowth):
    def proceed(self, n, save=None, attr="cnt"):
        nw_graph = self.make_copy(self.gr)
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, 0)
            nw_graph.set_attr(node, attr + "_end", -1)

        for edge in nw_graph.get_edges():
            nw_graph.set_edge_data(edge[0], edge[1], attr, 0)
            nw_graph.set_edge_data(edge[0], edge[1], attr + "_end", -1)
        graph = self.prep(self.make_copy(self.gr))

        count = self.gr.size()
        for _ in np.arange(n):
            print(_, graph.size())
            if self.stop():
                break

            graph = self.prep(graph)
            self.add(graph)
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node == 1:
                node1, node2 = self.new_edge_add(graph, (attr, _))
                nw_graph.add_edge(node1, node2, str(self.count-1), {attr[0]: _, attr + "_end": -1})
            else:
                node = self.remove(graph)
                graph.del_node(node)
                graph = self.prep(graph)
                nw_graph.set_attr(node, attr + "_end", _)

                frms = nw_graph.gr.edges(node)
                if nw_graph.directed():
                    frms = np.append(frms, nw_graph.gr.in_edges(node))

                for node_ in frms:
                    if len(node_) == 3:
                        if nw_graph.get_edge_data(node_[0], node_[1], attr + "_end", key=node_[2]) == -1:
                            nw_graph.set_edge_data(node_[0], node_[1], attr + "_end", _, key=node_[2])
                    else:
                        if nw_graph.get_edge_data(node_[0], node_[1], attr + "_end") == -1:
                            nw_graph.set_edge_data(node_[0], node_[1], attr + "_end", _)

                edges = self.new_node_add(graph, str(count), (attr, _), new_node)
                for node in edges:
                    if len(node_) == 3:
                        nw_graph.add_edge(node[0], node[1], key=str(node[2]), prms={attr: _, attr + "_end": -1})
                    else:
                        nw_graph.add_edge(node[0], node[1], prms={attr: _, attr + "_end": -1})
                nw_graph.set_attr(str(count), attr + "_end", -1)
                nw_graph.set_attr(str(count), attr, _)
                count += 1
        if save is None:
            return nw_graph
        else:
            self.save(nw_graph, save)

    @staticmethod
    def remove(graph):
        return None
