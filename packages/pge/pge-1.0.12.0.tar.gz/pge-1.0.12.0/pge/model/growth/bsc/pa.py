import numpy as np

from pge.model.growth.bsc.basic import SchemaGrowth


class PAGrowth(SchemaGrowth):
    def prep(self, graph):
        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def choice(self, gr, sz, tp="in"):
        ids = gr.get_ids(stable=True)
        probs = gr.get_attributes("dg_" + tp) + self.param[tp != "in"]
        probs = probs / np.sum(probs)
        probs, ids = probs[probs > 0], ids[probs > 0]
        return np.random.choice(ids, sz, replace=False, p=probs)
