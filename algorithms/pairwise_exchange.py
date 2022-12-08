import networkx as nx
from itertools import permutations, combinations
from random import choice

import dijkstra

MultiNodes = list[nx.nodes]

def multiNodes_to_starGraph(multi_nodes: MultiNodes) -> nx.DiGraph:
    
    graph = nx.DiGraph()
    
    # get tuple of every possible combination, permutations allowed NOT duplicates
    paths_to_find = permutations(multi_nodes, 2)
    
    # add to graph every weighted edge and store path with it
    for edge in paths_to_find:
        
        weight, path_found = dijkstra.dijkstra(*edge)
        graph.add_weighted_edges_from([(*edge, weight)], path=path_found)      
    
    return graph

def starGraph_to_ringGraph(starGraph: nx.DiGraph) -> nx.Graph:
    ringGraph = nx.Graph()
    
    # randomly pick a node
    start_node = list(starGraph.nodes)[0]
    
    # get nearest node
    nearest_node, properties = min(starGraph[start_node].items(), key=lambda edge: edge[1]["weight"])
    
    ringGraph.add_edge((start_node, nearest_node), **properties)
    
    search_node = nearest_node
    
    while not all(node in ringGraph for node in starGraph.nodes):
        # get a sorted list of the nearest node
        sorted_nearest_nodes = sorted(starGraph[search_node].items(), key=lambda edge: edge[1]["weight"])
        for nearest_node, properties in sorted_nearest_nodes:
            if nearest_node not in ringGraph:
                ringGraph.add_edges_from((search_node, nearest_node), **properties)
    
    ringGraph.add_edge(start_node, nearest_node, **starGraph[start_node][nearest_node])


def exchange_nodes(starGraph: nx.DiGraph, ringGraph: nx.Graph, recursion: int):
    edges = list(ringGraph.edges)
    switch_edge1 = edges.pop(choice(edges))
    
    # remove neighbor edges
    edges = [edge for edge in edges if switch_edge1[0] in edge or switch_edge1[1] in edge]
    switch_edge2 = edges.pop(choice(edges))
    
    ringGraph.remove_edges_from([switch_edge1, switch_edge2])
    
    # swap edges
    switch_edge1[1], switch_edge2[1] = switch_edge2[1], switch_edge1[1]
    ringGraph.add_edge(*switch_edge1, starGraph.get_edge_data(*switch_edge1))
    ringGraph.add_edge(*switch_edge2, starGraph.get_edge_data(*switch_edge2))
    
    # return swapped graph
    if recursion == 0:
        return ringGraph
    
    new_ringGraph = exchange_nodes(starGraph, ringGraph, recursion - 1)
    
    # return the smallest weighted paths
    if new_ringGraph.size(weight="weight") < ringGraph.size(weight="weight"):
        return new_ringGraph
    
    return ringGraph
    

def pairwise_exchange(multinodes: MultiNodes, recursion) -> nx.graph:
    star_graph = multiNodes_to_starGraph(multinodes)
    ring_graph = starGraph_to_ringGraph(star_graph)
    
    exchange_nodes(star_graph, ring_graph, recursion)
