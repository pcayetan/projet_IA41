
import networkx as nx

def christofides(G, test="weight"):
   
    print("Remove selfloops if necessary")
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)

    tree = nx.minimum_spanning_tree(G, weight=test) 
    L = G.copy()
    L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])

    MG = nx.MultiGraph()
    MG.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, weight=test)

    MG.add_edges_from(edges)

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
    
