import networkx as nx
import osmnx as ox
from itertools import permutations, combinations
from random import choice

from algorithms import dijkstra


def multiNodes_to_starGraph(graph: nx.MultiDiGraph, multi_nodes: list[nx.nodes], algo=dijkstra.dijkstra) -> nx.DiGraph:
    
    star_graph = nx.DiGraph()
    
    # get tuple of every possible combination, permutations allowed NOT duplicates
    paths_to_find = permutations(multi_nodes, 2)
    
    # add to graph every weighted edge and store path with it
    for edge in paths_to_find:
        
        weight, path_found = algo(graph, *edge)
        star_graph.add_weighted_edges_from([(*edge, weight)], path=path_found)      
    
    return star_graph

def starGraph_to_ringGraph(star_graph: nx.DiGraph) -> nx.DiGraph:
    ring_graph = nx.DiGraph()
    
    # randomly pick a node
    start_node = list(star_graph.nodes)[0]
    
    # get nearest node
    nearest_node, properties = min(star_graph[start_node].items(), key=lambda edge: edge[1]["weight"])
    
    # add weight and node
    ring_graph.add_edge(start_node, nearest_node, weight = properties["weight"])
    
    search_node = nearest_node
    
    while not all(node in ring_graph for node in star_graph.nodes):
        # get a sorted list of the nearest node
        sorted_nearest_nodes = sorted(star_graph[search_node].items(), key=lambda edge: edge[1]["weight"])
        for nearest_node, properties in sorted_nearest_nodes:
            if nearest_node not in ring_graph:
                ring_graph.add_edge(search_node, nearest_node, weight = properties["weight"])
                search_node = nearest_node
                break
    
    ring_graph.add_edge(search_node, start_node, weight=star_graph[start_node][nearest_node]["weight"])

    return ring_graph

def get_path_graphs(ring_graph: nx.DiGraph)-> list[nx.DiGraph]:
    path_graph_list = [component for component in nx.weakly_connected_components(ring_graph)]
    
    return path_graph_list

def exchange_nodes(star_graph: nx.DiGraph, ring_graph: nx.DiGraph, recursion: int):
    edges = list(ring_graph.edges)
    
    #get a random edge and convert to list
    switch_edge1 = list(edges.pop(edges.index(choice(edges))))
    switch_edge1.append(star_graph.get_edge_data(*switch_edge1, "weight"))
    
    # remove neighbor edges of the nodes in switch_edge1
    edges = [edge for edge in edges if not(switch_edge1[0] in edge or switch_edge1[1] in edge)]

    #get a random edge and convert to list
    switch_edge2 = list(edges.pop(edges.index(choice(edges))))
    switch_edge2.append(star_graph.get_edge_data(*switch_edge2, "weight"))
    ring_graph.remove_edges_from([switch_edge1, switch_edge2])
    
    # swap edges
    switch_edge1[1], switch_edge2[0] = switch_edge2[0], switch_edge1[1]
       
    # ring graph is currently composed of 2 path graphs
    list_path_graph_nodes = get_path_graphs(ring_graph)
    
    # create the 2 path graphs
    path_graph_A = ring_graph.copy()
    path_graph_A.remove_nodes_from(list_path_graph_nodes[0])
    path_graph_B = ring_graph.copy()
    path_graph_B.remove_nodes_from(list_path_graph_nodes[1])
    
    # find the path graph to reverse
    graph_reversed = None
    if switch_edge1[1] in path_graph_A:
        if path_graph_A.predecessors(switch_edge1[1]):
            path_graph_A = path_graph_A.reverse()
            graph_reversed = path_graph_A
        else:
            path_graph_B = path_graph_B.reverse()
            graph_reversed = path_graph_B
    else:
        if path_graph_B.predecessors(switch_edge1[1]):
            path_graph_B = path_graph_B.reverse()
            graph_reversed = path_graph_B
        else:
            path_graph_A = path_graph_A.reverse()
            graph_reversed = path_graph_A
    
    # update weights of reversed path
    weighted_edges = [(*edge, star_graph[edge[0]][edge[1]]["weight"]) for edge in graph_reversed.edges]
    graph_reversed.add_weighted_edges_from(weighted_edges)
    
    # reconstruct graph
    ring_graph = nx.union(path_graph_A, path_graph_B)
    ring_graph.add_edges_from([switch_edge1, switch_edge2])
    
    print(f"recursion: {recursion} size: ", ring_graph.size(weight="weight"))
    
    # return swapped graph
    if recursion == 1:
        return ring_graph
    
    new_ring_graph = exchange_nodes(star_graph, ring_graph.copy(), recursion - 1)

    # return the smallest weighted paths
    if new_ring_graph.size(weight="weight") < ring_graph.size(weight="weight"):
        return new_ring_graph
    
    return ring_graph


def ring_graph_to_multinodes(ring_graph: nx.DiGraph, start_node):
    multinodes = []
    search_node = start_node
    for i in range(len(ring_graph.nodes)):
        for adj in ring_graph.adj[search_node]:
            multinodes.append(adj)
        
        search_node = adj
    return multinodes
    
    

def pairwise_exchange(graph, multinodes: list[nx.nodes], recursion) -> nx.graph:
    star_graph = multiNodes_to_starGraph(graph, multinodes)
    ring_graph = starGraph_to_ringGraph(star_graph)
    
    ring_graph = exchange_nodes(star_graph, ring_graph, recursion)

    multinodes = ring_graph_to_multinodes(ring_graph, start_node=multinodes[0])
    
    return multinodes

if __name__=="__main__":
    distance = 11656.196759887971
    midpoint = (47.63491834896677, 6.830560597944681)

    # locations = ['UTBM', 'lion de belfort, belfort', 'Av. Jean Jaurès, belfort, France']
    # coord = [(47.58821915, 6.865861151133005), (47.63665715, 6.86457499503841), (47.6565055, 6.8458507)]
    node_list = [401460669, 321842925, 340177948, 346135377]


    graph = ox.graph_from_point(midpoint, dist=distance/2, network_type='drive', simplify=False)

    # node_list = [ox.nearest_nodes(graph, *geocode[::-1]) for geocode in geocode_list]
    # node_list = [321842925, 340177948, 1625586214]

    multinodes = pairwise_exchange(graph, node_list, 4)

    print(multinodes)