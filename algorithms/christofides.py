
import networkx as nx
from networkx.utils import pairwise


def christofides(G, weight="weight"):
   
    # Remove selfloops if necessary
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)
    # Check that G is a complete graph
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    # 1. Create a minimum spanning tree T of G.
    tree = nx.minimum_spanning_tree(G, weight=weight) 

    # 2. Let O be the set of vertices with odd degree in T. By the handshaking lemma, O has an even number of vertices.
    L = G.copy()
    L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])

    # 3. Find a minimum-weight perfect matching M in the induced subgraph given by the vertices from O.
    MG = nx.MultiGraph()
    MG.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, weight=weight)

    # 4. Combine the edges of M and T to form a connected multigraph H in which each vertex has even degree.
    MG.add_edges_from(edges)

    # 5. Form an Eulerian circuit in H.
    # 6. Make the circuit found in previous step into a Hamiltonian circuit by skipping repeated vertices (shortcutting).
    return _shortcutting(nx.eulerian_circuit(MG))


def _shortcutting(circuit):
    """Remove duplicate nodes in the path"""
    nodes = []
    for u, v in circuit:
        if v in nodes:
            continue
        if not nodes:
            nodes.append(u)
        nodes.append(v)
    nodes.append(nodes[0])
    return nodes


def traveling_salesman_problem(G, weight="weight", nodes=None, cycle=True, method=None):
    if nodes is None:
        nodes = list(G.nodes)

    dist = {}
    path = {}
    for n, (d, p) in nx.all_pairs_dijkstra(G, weight=weight):
        dist[n] = d
        path[n] = p

    if G.is_directed():
        # If the graph is not strongly connected, raise an exception
        if not nx.is_strongly_connected(G):
            raise nx.NetworkXError("G is not strongly connected")
        GG = nx.DiGraph()
    else:
        GG = nx.Graph()
    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            GG.add_edge(u, v, weight=dist[u][v])
    best_GG = christofides(GG, weight)

    if not cycle:
        # find and remove the biggest edge
        (u, v) = max(pairwise(best_GG), key=lambda x: dist[x[0]][x[1]])
        pos = best_GG.index(u) + 1
        while best_GG[pos] != v:
            pos = best_GG[pos:].index(u) + 1
        best_GG = best_GG[pos:-1] + best_GG[:pos]

    best_path = []
    for u, v in pairwise(best_GG):
        best_path.extend(path[u][v][:-1])
    best_path.append(v)
    return best_path

