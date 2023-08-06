import numpy as np

from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.optimize import fsolve

from dtg.tail.estimate.hill import HillEstimator
from dtg.tail.mse import boot_estimate


class Backs:
    @staticmethod
    def estimate(graph, opt=None):
        return -1, -1, -1, -1, -1


class Snapshot(Backs):
    @staticmethod
    def prt(dl, ss, n, bt):
        if ss[0][0] == 0:
            n_ = ss[1][0]
        else:
            n_ = 0
        return ((n_ / n) + bt) / (1 - (n_ / n) * (dl / (1 + dl * (1 - bt))))

    def estimate(self, graph, opt="Nelder-Mead"):
        bt = 1 - graph.size() / graph.size_edge()

        ins = np.unique([graph.count_in_degree(node) for node in graph.get_ids()], return_counts=True)
        outs = np.unique([graph.count_out_degree(node) for node in graph.get_ids()], return_counts=True)

        def sn_dl_in_0(x):
            sm = [0]
            for i in np.arange(1, np.max(ins[0])):
                N = np.sum((ins[1])[ins[0] > i])
                sm.append((N/graph.size_edge())*(i/(i+x)*(1+x*(1-bt))))
            return np.sum(sm)-Snapshot.prt(x, ins, graph.size_edge(), bt)

        dl_in = fsolve(sn_dl_in_0, np.array([1]))[0]
        alp = Snapshot.prt(dl_in, ins, graph.size_edge(), bt) - bt

        def sn_dl_out_0(x):
            sm = [0]
            for i in np.arange(1, np.max(outs[0])):
                N = np.sum((outs[1])[outs[0] > i])
                sm.append((N/graph.size_edge())*(i/(i+x)*(1+x*(1-bt))))
            return np.sum(sm)-Snapshot.prt(x, ins, graph.size_edge(), bt)

        dl_out = fsolve(sn_dl_out_0, np.array([1]))[0]
        gm = Snapshot.prt(dl_out, outs, graph.size_edge(), bt) - bt

        alp = alp*(1-bt)/(alp+gm)
        gm = 1 - bt - alp

        def sn_dl_in_1(x):
            sm = [0]
            for i in np.arange(np.max(ins[0])):
                N = np.sum((ins[1])[ins[0] > i])
                sm.append((N / graph.size_edge()) * (1 / (i + x)))
            return np.sum(sm) - ((1-alp-bt)/x) - ((alp+bt)*(1-bt)/(1+x*(1-bt)))
        dl_in = fsolve(sn_dl_in_1, np.array([1]))[0]

        def sn_dl_out_1(x):
            sm = [0]
            for i in np.arange(np.max(outs[0])):
                N = np.sum((outs[1])[outs[0] > i])
                sm.append((N / graph.size_edge()) * (1 / (i + x)))
            return np.sum(sm) - ((1-gm-bt)/x) - ((gm+bt)*(1-bt)/(1+x*(1-bt)))
        dl_out = fsolve(sn_dl_out_1, np.array([1]))[0]

        return alp, bt, gm, dl_in, dl_out


def evi_ins_sub(x, x_, dl_in, dl_out, a, v_in):
    return x**(v_in+dl_in+a*dl_out)*np.exp(x*(-(np.cos(x_)**(1/a)))-(x**a)*np.sin(x_))


def evi_ins(x, alp, bt, gm, v_in, v_out, a):
    res = quad(evi_ins_sub, 0, np.inf, args=(x,
                                             EVI.dl_in(v_in, alp, bt, gm),
                                             EVI.dl_out(v_out, alp, bt, gm),
                                             a, v_in))

    return (gm / EVI.dl_in(v_in, alp, bt, gm)) * (np.cos(x) ** (((EVI.dl_in(v_in, alp, bt, gm) + 1) / a) - 1)) * (
                    np.sin(x) ** (EVI.dl_out(v_out, alp, bt, gm) - 1)) * res[0]


def evi_outs_sub(x, x_, dl_in, dl_out, a, v_in):
    return x**(a-1+v_in+dl_in+a*dl_out)*np.exp(x*(-(np.cos(x_)**(1/a)))-(x**a)*np.sin(x_))


def evi_outs(x, alp, bt, gm, v_in, v_out, a):
    res = quad(evi_outs_sub, 0, np.inf, args=(x,
                                              EVI.dl_in(v_in, alp, bt, gm),
                                              EVI.dl_out(v_out, alp, bt, gm),
                                              a, v_in))

    return (gm / EVI.dl_out(v_out, alp, bt, gm)) * (np.cos(x) ** (EVI.dl_in(v_in, alp, bt, gm) / a - 1)) * (
            np.sin(x) ** EVI.dl_out(v_out, alp, bt, gm)) * res[0]


class EVI(Backs):
    @staticmethod
    def dl_in(v, alp, bt, gm):
        return (v * (alp + bt) - 1) / (alp + gm)

    @staticmethod
    def dl_out(v, alp, bt, gm):
        return (v * (gm + bt) - 1) / (alp + gm)

    @staticmethod
    def estimate(graph, opt=(1, "Nelder-Mead")):
        bt = np.round(1 - graph.size() / graph.size_edge(), 5)

        v_in = boot_estimate(
            HillEstimator,
            np.array([graph.count_in_degree(node) for node in graph.get_ids()]),
            1 / 2,
            2 / 3,
            30
        )[0]
        v_out = boot_estimate(
            HillEstimator,
            np.array([graph.count_out_degree(node) for node in graph.get_ids()]),
            1 / 2,
            2 / 3,
            30
        )[0]

        def alp_opt(x, a):
            if np.abs(a) > 1:
                return np.infty

            lgs = []
            for node in graph.get_ids():
                in_n, out_n = graph.count_in_degree(node), graph.count_out_degree(node)
                if np.sqrt(in_n ** (2 * a) + out_n ** 2) > opt[0]:
                    x_ = np.arctan(out_n / (in_n ** a))

                    lgs.append(
                        evi_ins(x_, x, bt, 1 - bt - x, v_in, v_out, a)
                        + evi_outs(x_, x, bt, 1 - bt - x, v_in, v_out, a)
                    )

            return -np.sum(np.log(lgs))

        res = minimize(alp_opt, np.array([0.5, 0.5]), method=opt[1], tol=1e-6)
        alp = res.x[0]

        gm = 1 - alp - bt
        return alp, bt, gm, EVI.dl_in(v_in, alp, bt, gm), EVI.dl_out(v_out, alp, bt, gm)
