from graph_tools import ConstructGraph
from algorithms import ant_colony
import osmnx as ox
import time as timestamp

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

    print(minlat, maxlat, minlon, maxlon)

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

    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1)
    end = timestamp.time()
    print("Time to construct the graph: ", end - start)

    #If there is only two nodes, return the path between them
    if len(nodesgeocode) == 2:
        path = simplified_graph[nodes[0]][nodes[1]]["path"]
        return graph, path, simplified_graph[nodes[0]][nodes[1]]["time"]

    #Mesure the time to run the second algorithm
    start = timestamp.time()
    #Solve the TSP problem with the algorithm2
    colony = ant_colony.ant_colony(simplified_graph, nodes[0],n_ants=25)
    
    simplified_path, time = colony.run()
    end = timestamp.time()
    print("Time to solve the TSP problem: ", end - start)

    #Find the path in the original graph
    path = [nodes[0]]
    for i in range(len(simplified_path)-1):
        path += simplified_graph[simplified_path[i]][simplified_path[i+1]]["path"][1:]
    
    #sort the geocode in the same order as the path
    nodesgeocode = [nodesgeocode[nodes.index(node)] for node in simplified_path]
        

    #return the solution
    return graph, path, time, nodesgeocode
    