
import networkx as nx

def christofides(G, weight="weight"):

    tree = nx.minimum_spanning_tree(G, weight=weight) 
    L = G.copy()
    L.remove_nodes_from([end_node for end_node, degree in tree.degree if not (degree % 2)])

    graph = nx.MultiGraph()
    graph.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, weight=weight)

    graph.add_edges_from(edges)

    return shortcutting(nx.eulerian_circuit(graph))


def shortcutting(path):
    """Remove duplicate nodes in the path"""
    nodes = []
    for start_node, end_node in path:
        if end_node in nodes:
            continue
        if not nodes:
            nodes.append(start_node)
        nodes.append(end_node)
    nodes.append(nodes[0])
    return nodes
    
