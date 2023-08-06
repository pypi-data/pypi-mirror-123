import numpy as np


def first_order(graph, basis, typ="in", inn=None):
    clss = []
    for _ in np.arange(len(basis)+1):
        clss.append([])

    if inn is None:
        inn = []
        for bs in basis:
            inn = inn + list(bs)

    for node in graph.get_ids():
        fnd = False

        if node in inn:
            continue

        if typ == "in":
            cks = graph.get_in_degrees(node)
        else:
            cks = graph.get_out_degrees(node)

        for i in np.arange(len(basis)):
            for node_ in cks:
                if node_ in basis[i]:
                    fnd = True
                    clss[i].append(node)
                    break

            if fnd:
                break

        if fnd is False:
            clss[-1].append(node)
    return clss


def full_classification(graph, basis, typ="in"):
    clss = []

    inn = []
    while True:
        for bs in basis:
            inn = inn + list(bs)

        print(len(inn))
        res = first_order(graph, basis, typ, inn)
        if np.sum([len(r) for r in res[:len(res)-1]]) < len(res)-1:
            clss = clss + [[res[-1]]]
            break
        else:
            print([len(r) for r in res])
        basis = res[:len(res)-1]
        clss = clss + [basis]
    return clss
