from copy import deepcopy
from pytrad.graph.Edge import Edge

def meek(cg):
    '''
    Run Meek rules

    Parameters
    ----------
    cg : a CausalGraph object

    Returns
    -------
    cg_new : a CausalGraph object
    '''

    cg_new = deepcopy(cg)

    UT = cg_new.find_unshielded_triples()
    Tri = cg_new.find_triangles()
    Kite = cg_new.find_kites()

    Loop = True

    while Loop:
        Loop = False
        for (i, j, k) in UT:
            if cg_new.is_fully_directed(i, j) and cg_new.is_undirected(j, k):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[j], cg_new.G.nodes[k])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[j], cg_new.G.nodes[k], -1, 1))
                Loop = True

        for (i, j, k) in Tri:
            if cg_new.is_fully_directed(i, j) and cg_new.is_fully_directed(j, k) and cg_new.is_undirected(i, k):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[i], cg_new.G.nodes[k])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[i], cg_new.G.nodes[k], -1, 1))
                Loop = True

        for (i, j, k, l) in Kite:
            if cg_new.is_undirected(i, j) and cg_new.is_undirected(i, k) and cg_new.is_fully_directed(j, l) \
                    and cg_new.is_fully_directed(k, l) and cg_new.is_undirected(i, l):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[i], cg_new.G.nodes[l])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[i], cg_new.G.nodes[l], -1, 1))
                Loop = True

    return cg_new


def definite_meek(cg):
    '''
    Run Meek rules over the definite unshielded triples

    Parameters
    ----------
    cg : a CausalGraph object

    Returns
    -------
    cg_new : a CausalGraph object
    '''

    cg_new = deepcopy(cg)

    Tri = cg_new.find_triangles()
    Kite = cg_new.find_kites()

    Loop = True

    while Loop:
        Loop = False
        for (i, j, k) in cg_new.definite_non_UC:
            if cg_new.is_fully_directed(i, j) and cg_new.is_undirected(j, k):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[j], cg_new.G.nodes[k])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[j], cg_new.G.nodes[k], -1, 1))
                Loop = True
            elif cg_new.is_fully_directed(k, j) and cg_new.is_undirected(j, i):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[j], cg_new.G.nodes[i])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[j], cg_new.G.nodes[i], -1, 1))
                Loop = True

        for (i, j, k) in Tri:
            if cg_new.is_fully_directed(i, j) and cg_new.is_fully_directed(j, k) and cg_new.is_undirected(i, k):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[i], cg_new.G.nodes[k])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[i], cg_new.G.nodes[k], -1, 1))
                Loop = True

        for (i, j, k, l) in Kite:
            if ((j, l, k) in cg_new.definite_UC or (k, l, j) in cg_new.definite_UC) \
                    and ((j, i, k) in cg_new.definite_non_UC or (k, i, j) in cg_new.definite_non_UC) \
                    and cg_new.is_undirected(i, l):
                edge1 = cg_new.G.get_edge(cg_new.G.nodes[i], cg_new.G.nodes[l])
                if edge1 is not None:
                    cg_new.G.remove_edge(edge1)
                cg_new.G.add_edge(Edge(cg_new.G.nodes[i], cg_new.G.nodes[l], -1, 1))
                Loop = True

    return cg_new

