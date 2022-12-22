from graph_tools import ConstructGraph, input_generator
from algorithms import ant_colony, christofides, dijkstra, pairwise_exchange
import osmnx as ox
import time as timestamp

def create_graph(nodesgeocode):
    graph = input_generator.graph_from_coordinates_array(nodesgeocode)

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
    
    return graph

def tsp_solver(nodesgeocode, algorithm1 = "Dijkstra", algorithm2="Christofides"):
    """Construct a graph with only the nodes latitude and longitude to visit with the algorithm1 and solve the TSP problem with the algorithm2

    Args:
        places: A list of duos of latitude and longitude of the nodes to visit: (latitude, longitude)
        algorithm1: The algorithm to use to construct the new graph
        algorithm2: The algorithm to use to solve the TSP problem

    Returns:
        The path to visit the nodes in the order given by the algorithm2
    """
    if(algorithm2=="Christofides"):
        algorithm2 = "christofides"
    elif(algorithm2=="Ant Algorithm"):
        algorithm2 = "ant_colony"
    else:
        raise ValueError("Unknown 2nd algorithm")
    
    graph = create_graph(nodesgeocode)

    #add travel times to nodes
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)

    #Find the nodes corresponding to the places
    nodes = []
    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))

    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    print(algorithm2)
    if algorithm2 == "Pairwise exchange":
        print(algorithm2)
        ring_graph = pairwise_exchange(graph, nodes, len(nodes))
        
    dictionnary, simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1, algorithm2)
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

    #return the solution
    return graph, path, time, nodesgeocode