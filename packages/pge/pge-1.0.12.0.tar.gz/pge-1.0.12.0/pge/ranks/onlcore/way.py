import numpy as np

from dtg.stationary.dierckx import stat_exponential
from dtg.stationary.giratis import stat
from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_exes_comm(gr, nodes, params, mn=True, kgaps=None, un=True):
        res = []
        if kgaps is not None:
            x = gr.subgraph(nodes).size_edge()

        oths = gr.get_ids(stable=True)
        oths = oths[~np.isin(oths, nodes)]
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)
            cls_oth = gr.get_attributes(params_[0], oths)
            ex_tmp = 1
            ex = 1
            u = np.max(cls)
            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u], un=un, others=oths[cls_oth > u])[1])

                if ts.size == 0:
                    continue

                if kgaps is not None:
                    ts = np.where(ts > kgaps, ts - kgaps, 0) * (ts.size + 1)/x
                    a = (ts[ts > 0]).size
                    b = (ts[ts == 0]).size
                    L = np.sum(ts)

                    ex = min([1, 0.5 *
                              (
                            1 + (2 * a + b) / (L) - np.sqrt((1 + (2 * a + b) / L) ** 2 - 8 * a / L)
                    )])
                else:
                    if np.max(ts) > 2:
                        ex = min(
                        [
                            1,
                            2
                            * np.mean(ts - 1) ** 2
                            / (np.mean(np.multiply(ts - 1, ts - 2))),
                            ]
                        )
                    else:
                        ex = min([1, 2 * np.mean(ts) ** 2 / (np.mean(ts ** 2))])
                if mn:
                    if ex < 1:
                        break
                else:
                    if 1 > ex >= ex_tmp > 0:
                        ex = ex_tmp
                        break
                ex_tmp = ex
            res.append((ex, u))
        return res

    @staticmethod
    def get_view(gr, nodes, params):
        res = []

        # ds = np.array([gr.count_in_degree(node) for node in gr.get_ids()])
        ds = np.array([gr.count_in_degree(node) for node in nodes])
        for params_ in params:
            cls = gr.get_attributes(params_[0], nodes)

            for u in np.unique(cls)[::-1]:
                ts = np.array(gr.get_all_short_pathes(nodes[cls > u])[1])

                res.append(np.mean(ds[cls > u]) / ts.size)
        return res, np.unique(cls)[::-1]

    @staticmethod
    def get_test_comm(gr, nodes, level, param):
        if nodes.size == 0:
            return (0, 0), (0, 0)

        cls = gr.get_attributes(param, nodes)
        ts = gr.get_all_short_pathes(nodes[cls > level], plain=True)[1]
        if ts.size == 0:
            return (0, 0), (stat(cls), np.mean(cls))

        q = np.sum(gr.get_attributes(param) > level) / gr.size()
        return (
            (
                stat_exponential(ts, q),
                q
                * np.sum([np.sum(ti) for ti in ts])
                / np.sum([np.size(ti) for ti in ts]),
            ),
            (stat(cls), np.mean(cls)),
        )
