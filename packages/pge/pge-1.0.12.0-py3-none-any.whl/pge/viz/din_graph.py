import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from pge.init.classes.graph import SGraph
from pge.ranks.rank import estimate_rank


def plot_spread(graph, frm, name, st, to="dir/tmp/",
                draw_args=None, draw=nx.kamada_kawai_layout):
    if draw_args is None:
        draw_args = {
            "font_size": 8,
            "font_weight": 'bold',
            "edge_color": '0.4'}
    Path(to).mkdir(parents=True, exist_ok=True)

    js = np.unique(graph.get_attributes(frm))
    pos = draw(graph.gr)

    if graph.directed():
        estimate_rank(graph, "one")
        nd_s = graph.get_attributes("one")
    else:
        nd_s = np.array([graph.count_degree(node) for node in graph.get_ids()])
    nd_s = (nd_s - np.min(nd_s)) / np.max(nd_s)
    nd_s = nd_s * 40

    for j in np.arange(np.min(js), st):
        fig = plt.figure(dpi=300)
        colrs = np.where(graph.get_attributes(frm) <= j, "red", "grey")

        nx.draw_networkx(graph.gr, pos, with_labels=False, node_color=colrs, node_size=nd_s, **draw_args)

        plt.tight_layout()
        plt.savefig(to + name + "-" + str(j) + ".png", format="PNG")


def plot_evolve(graph, frm, name, to="dir/tmp/",
                draw_args=None, draw=nx.kamada_kawai_layout):
    if draw_args is None:
        draw_args = {
            "node_color": 'red',
            "font_size": 8,
            "font_weight": 'bold'}
    Path(to).mkdir(parents=True, exist_ok=True)

    mx = np.max(graph.get_edge_attributes(frm))
    js = np.unique(np.append(
        graph.get_edge_attributes(frm),
        graph.get_edge_attributes(frm + "_end", noneval=mx)
    )
    )
    edges = graph.get_edges(stable=True)
    nodes = graph.get_ids(stable=True)
    edges_bth = graph.get_edge_attributes(frm)
    edges_death = graph.get_edge_attributes(frm + "_end", noneval=mx)

    nodes_bth = graph.get_attributes(frm)
    nodes_death = graph.get_attributes(frm + "_end", noneval=mx)

    pos = draw(graph.gr)
    for j in np.arange(np.min(js), np.max(js)):
        fig = plt.figure(dpi=300)
        if graph.directed():
            sub = SGraph(nx.MultiDiGraph())
        else:
            sub = SGraph(nx.MultiGraph())

        nds = nodes[(nodes_bth <= j) & ((nodes_death > j) | (nodes_death == -1))]
        nwes = edges[(edges_bth <= j) & ((edges_death > j) | (edges_death == -1))]
        nwes = [nwes_ for nwes_ in nwes if np.sum(np.isin(nwes_, nds)) == 2]
        sub.add_nodes(nds)
        sub.add_edges(nwes)

        if graph.directed():
            estimate_rank(sub, "one")
            nd_s = sub.get_attributes("one")
        else:
            nd_s = np.array([sub.count_degree(node) for node in sub.get_ids()])
        nd_s = (nd_s - np.min(nd_s)) / np.max(nd_s)
        nd_s = nd_s * 15

        nx.draw_networkx(sub.gr, {k: pos[k] for k in pos.keys()}, with_labels=False, node_size=nd_s, **draw_args)

        plt.tight_layout()
        plt.savefig(to + name + "-" + str(j) + ".png", format="PNG")
