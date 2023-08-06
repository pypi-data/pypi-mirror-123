import numpy as np
import networkx as nx
from scipy.linalg import eigvalsh


def phi(gr, nodes, other=None):
    if gr.directed():
        ind_i = np.arange(gr.size())[
            np.array([node in nodes for node in gr.get_ids()])]
        if other is not None:
            ind_j = np.arange(gr.size())[
                np.array([node in other for node in gr.get_ids()])]
        else:
            ind_j = np.arange(gr.size())[
                np.array([node not in nodes for node in gr.get_ids()])]
        pi = gr.get_stat_dist()
        c = np.sum(pi[ind_i])
        v = np.sum(pi[ind_j])

        p = gr.get_prob_matrix()
        w = np.multiply(p, pi)

        p1 = np.sum(w[np.ix_(ind_j, ind_i)])
        p2 = np.sum(w[np.ix_(ind_i, ind_j)])
        return np.max([p1 / c, p2 / v])
    else:
        try:
            return nx.algorithms.cuts.conductance(gr.get_nx_graph(), nodes, other)
        except:
            return 0


def conductance_speed(gr):
    if gr.directed():
        p = gr.get_prob_matrix()
        pi = gr.get_stat_dist()
        l = np.eye(pi.size)

        pi1 = np.sqrt(np.diag(pi**-1))
        pi = np.sqrt(np.diag(pi))

        l = np.subtract(l, np.add(np.dot(pi, np.dot(p, pi1)), np.dot(pi1, np.dot(np.transpose(p), pi)))/2)
        ls = np.abs(eigvalsh(l))
        ls = np.sort(ls)[1]
        return np.mean([ls / 2, np.sqrt(ls * 2)])
    else:
        ls = nx.normalized_laplacian_spectrum(gr.get_nx_graph())
        ls = np.sort(ls)[1]
        return np.mean([ls / 2, np.sqrt(1-ls*2)])


def weak_conductance(gr, attr):  # todo вложение
    nx.set_node_attributes(gr.get_nx_graph(), 0, attr)
    comms = sorted(
        nx.algorithms.community.greedy_modularity_communities(gr.get_nx_graph()),
        key=len,
        reverse=True,
    )

    updatable = True
    while updatable:
        comms_ = []
        updatable = False
        for comm in comms:
            ph = phi(gr, comm)
            if ph == 0:
                comms_.append(comm)
                continue

            vars = []
            vars_comm = []
            for node_out in gr.get_out_degrees(comm, un=True):
                if node_out in comm:
                    continue

                try:
                    vars.append(phi(gr, [node_out] + comm))
                    vars_comm.append([node_out] + comm)
                except:
                    continue

            if len(vars) == 0:
                comms_.append(comm)
                updatable = updatable or False
                continue

            mn = np.min(vars)
            if mn <= ph:
                for i in np.arange(len(vars)):
                    if vars[i] == mn:
                        comms_.append(vars_comm[i])
                        updatable = updatable or True
            else:
                comms_.append(comm)
                updatable = updatable or False
        comms = comms_

    for com in comms:
        if len(com) == 1:
            gr.set_attr(list(com)[0], attr, 0)
            continue
        ph = conductance(gr.subgraph(com))
        for node in com:
            gr.set_attr(node, attr, max(gr.get_attr(node, attr), ph))
