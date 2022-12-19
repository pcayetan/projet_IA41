from graph_tools import ConstructGraph, input_generator
from algorithms import ant_colony, christofides, dijkstra
import osmnx as ox
import time as timestamp
from itertools import pairwise
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

    start = timestamp.time()
    graph = input_generator.graph_from_coordinates_array(nodesgeocode)
    nodes = []
    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))
    end = timestamp.time()
    print("Time to create the graph: ", end - start)
    
    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    print(algorithm2)
    dictionnary, simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1, algorithm2)
    end = timestamp.time()
    print("Time to simplify the graph: ", end - start)

    #Mesure the time to run the second algorithm
    start = timestamp.time()
    #If there is only two nodes, return the path between them
    if len(nodesgeocode) == 2:
        path = dictionnary[nodes[0]][nodes[1]]["path"]
        time = dictionnary[nodes[0]][nodes[1]]["time"]
        end = timestamp.time()
        print("Time to find the path: ", end - start)
        return graph, path, time, [nodesgeocode[0],nodesgeocode[1]]
    
    if(algorithm2 == "ant_colony"):
        print("ant_colony")
        #Solve the TSP problem with the algorithm2
        colony = ant_colony.ant_colony(dictionnary, nodes[0],n_ants=25)
        simplified_path, time = colony.run()
        #Find the path in the original graph
    elif algorithm2 == "christofides":
        print("christofides")
        simplified_path = christofides.christofides(simplified_graph, weight="weight")
        time = 0
        for i in range(len(simplified_path)-1):
            time +=  dictionnary[simplified_path[i]][simplified_path[i+1]]["time"]
    
    #Recreate path
    path = [nodes[0]]
    for i in range(len(simplified_path)-1):
        path += dictionnary[simplified_path[i]][simplified_path[i+1]]["path"][1:]
    #sort the geocode in the same order as the path
    nodesgeocode = [nodesgeocode[nodes.index(node)] for node in simplified_path]
    end = timestamp.time()
    print("Time to solve the TSP problem: ", end - start)

    #return the solution
    return graph, path, time, nodesgeocode
