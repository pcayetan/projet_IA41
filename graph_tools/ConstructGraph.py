from algorithms import dijkstra
from algorithms import astar
import networkx as nx
#Construct a graph representation of the network of places to visited ready to be used by a TSP solver.

def construct_graph(graph, nodes, algorithm1= "dijkstra", algorithm2="ant_colony", weight="weight"):
    """Construct a graph representation of the network of places to visited ready to be used by a TSP solver.
    The graph is represented as a dictionary of dictionaries. The keys are the nodes of the graph,
    and the values are dictionaries containing the time needed to travel between the node and its neighbors and 
    the path to take to reach them.
    
    Parameters:
    graph (networkx graph): the graph of the network
    nodes (list): the list of nodes to visit
    
    Returns:
    dict: the graph representation
    """

    
    #Select the algorithm to use
    if algorithm1 == "Dijkstra":
        print("Dijkstra")
        function = dijkstra.dijkstra
    elif algorithm1 == "A*":
        print("A*")
        function = astar.astar
    else:
        raise ValueError("Unknown algorithm")


    #Create a graph with only the nodes to visit
    if(algorithm2 == "ant_colony"):
        G = {node: {} for node in nodes}
    elif(algorithm2 == "christofides"):
        G = nx.Graph()
        dic_path = {node: {} for node in nodes}
        for start_node in nodes:
            for end_node in nodes:
                if start_node == end_node:
                    continue
                time, path = function(graph, start_node, end_node)
                
    else:
        raise ValueError("Unknown algorithm")

    for start_node in nodes:
            for end_node in nodes:
                if start_node == end_node:
                    continue
                #Find the shortest path between the two nodes NOTE: sad to have to 
                time, path = function(graph, start_node, end_node)
                if(algorithm2 == "ant_colony"):
                    if(time != float("inf")):
                        #Add the path to the graph
                        G[start_node][end_node] = {"time": time, "path": path}
                elif(algorithm2 == "christofides"):
                    dic_path[start_node][end_node] = path
                    G.add_edge(start_node, end_node, weight=time)
                else:
                    raise ValueError("Unknown algorithm")

    # c'est moche
    if(algorithm2 == "christofides"):
        G = (G,dic_path)
    return G
    

