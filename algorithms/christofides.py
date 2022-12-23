from heapq import heappop, heappush
from networkx import MultiGraph, Graph, max_weight_matching
from itertools import count
from copy import deepcopy

    
def christofides(dictionary, weight="time"):
    """Compute an approximation of the shortest path between all the nodes of the dictionary
    Uses Christofides Algorithm to solve the traveling's salesman problem (TSP).
    
    Parameters:
    ---------------
    dictionary: python dictionary, complete graph
    weight: weight used in the dictionary
    
    Returns:
    an approximation of the shortest path between the dictionary's nodes
    """
    D = deepcopy(dictionary)
    for start_node in D:
        for end_node in D[start_node]:
            if start_node == end_node:
                continue
            D[start_node][end_node].pop("path")
    G = Graph(D)
    tree = minimum_spanning_tree(G, weight=weight)
    L = G.copy()
    L.remove_nodes_from([end_node for end_node, degree in tree.degree if not (degree % 2)])
    graph = MultiGraph()
    graph.add_edges_from(tree.edges)
    edges = min_weight_matching(L, weight=weight)
    graph.add_edges_from(edges)
    path = shortcutting(eulerian_circuit(graph))
    return path


def prim_graph(G, weight="time"):
    """Compute a the edges of a minimim spanning tree (mst) for a graph
    Uses Prim's algorithm

    Parameters:
    ---------------
    G: nx.Graph 
    weight: weight used in the graph
    
    Returns:
    An iterator containing the edges of the mst
    """
    push = heappush
    pop = heappop
    nodes = set(G)
    c = count()
    while nodes:
        u = nodes.pop()
        frontier = []
        visited = {u}
        
        for v, d in G.adj[u].items():
            wt = d.get(weight, 1)
            push(frontier, (wt, next(c), u, v, d))
        while nodes and frontier:
            W, _, u, v, d = pop(frontier)
            if v in visited or v not in nodes:
                continue
            yield u, v, d
            # update frontier
            visited.add(v)
            nodes.discard(v)
            for w, d2 in G.adj[v].items():
                if w in visited:
                    continue
                new_weight = d2.get(weight, 1)
                push(frontier, (new_weight, next(c), v, w, d2))

    
def minimum_spanning_tree(G, weight="time"):
    """Compute a the edges of a minimim spanning tree (mst) for a graph
    Compute the minimum spanning tree for a graph using Prim's algorithm
    
    Parameters:
    ---------------
        G: nx.Graph 
        weight: weight used in the graph
    
    Returns:
        T_graph: nx.Graph containing the minimum spanning tree of G
    """
    edges_mst_prim_graph = prim_graph(G, weight=weight)
    T_graph = Graph()  # Same graph class as Gs
    T_graph.add_nodes_from(G.nodes.items())
    T_graph.add_edges_from(edges_mst_prim_graph)
    return T_graph

    
def min_weight_matching(G, weight="time"):
    """Compute a minimally weighted matching of G
    Uses networkx's function max_weight_matching, 
    only the inversion to get the min is done here.
    Parameters:
    ---------------
        G: nx.Graph 
        weight: weight used in the graph
    
    Returns:
        A minimally weighted matching of G
    """
    G_edges = G.edges(data=weight, default=1)
    max_weight = 1 + max(w for _, _, w in G_edges)
    InvG = Graph()
    edges = ((u, v, max_weight - w) for u, v, w in G_edges)
    InvG.add_weighted_edges_from(edges, weight=weight)
    return max_weight_matching(InvG, maxcardinality=True, weight=weight)
    
    
def shortcutting(path):
    """Removes the nodes through which the path comes through twice
    Parameters:
    ---------------
        path: list 
    
    Returns:
        nodes: list
    """
    nodes = []
    for start_node, end_node in path:
        if end_node in nodes:
            continue
        if not nodes:
            nodes.append(start_node)
        nodes.append(end_node)
    nodes.append(nodes[0])
    return nodes
    
def eulerian_circuit(G):
    """Create an eulerian circuit for graph G
    ---------------
        G: nx.Graph 
    
    Yield:
        vertex of the eulerian circuit
    """
    G = G.copy()
    source = next(iter(G))
    degree = G.degree
    edges = G.edges
    vertex_stack = [source]
    last_vertex = None
    
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex)
            last_vertex = current_vertex
            vertex_stack.pop()
        else:
            triple = next(iter(edges(current_vertex, keys=True)))
            _, next_vertex, next_key = triple
            vertex_stack.append(next_vertex)
            G.remove_edge(current_vertex, next_vertex, next_key)

