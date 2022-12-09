from graph_tools import ConstructGraph
from algorithms import dijkstra, ant_colony
import osmnx as ox

def construct_graph(graph, nodesgeocode, algorithm1 = dijkstra.dijkstra, algorithm2=ant_colony):
    """Construct a graph with only the nodes latitude and longitude to visit with the algorithm1 and solve the TSP problem with the algorithm2

    Args:
        graph: The original graph
        places: A list of duos of latitude and longitude of the nodes to visit: (latitude, longitude)
        algorithm1: The algorithm to use to construct the new graph
        algorithm2: The algorithm to use to solve the TSP problem

    Returns:
        The path to visit the nodes in the order given by the algorithm2
    """
    nodes = []

    #Find the nodes corresponding to the places
    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))

    #Create a graph with only the nodes to visit with the algorithm1
    simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1)

    #Solve the TSP problem with the algorithm2

    #return the solution
    