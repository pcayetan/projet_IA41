from graph_tools import ConstructGraph
import osmnx as ox

def construct_graph(nodesgeocode, algorithm1 = "Dijkstra", algorithm2="ant_colony"):
    """Construct a graph with only the nodes latitude and longitude to visit with the algorithm1 and solve the TSP problem with the algorithm2

    Args:
        places: A list of duos of latitude and longitude of the nodes to visit: (latitude, longitude)
        algorithm1: The algorithm to use to construct the new graph
        algorithm2: The algorithm to use to solve the TSP problem

    Returns:
        The path to visit the nodes in the order given by the algorithm2
    """
    nodes = []

    minlat = min([float(latitude) for latitude, longitude in nodesgeocode])
    maxlat = max([float(latitude) for latitude, longitude in nodesgeocode])
    minlon = min([float(longitude) for latitude, longitude in nodesgeocode])
    maxlon = max([float(longitude) for latitude, longitude in nodesgeocode])

    #Padding to get a bigger area
    padding = 0.01
    minlat -= padding
    maxlat += padding
    minlon -= padding
    maxlon += padding

    #Download the graph of the area
    graph = ox.graph_from_bbox(maxlat, minlat, maxlon, minlon, network_type='drive')

    #add travel times to nodes
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)

    #Find the nodes corresponding to the places
    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))

    #Create a graph with only the nodes to visit with the algorithm1
    simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1)

    #Solve the TSP problem with the algorithm2

    #return the solution
    return graph, nodes
    