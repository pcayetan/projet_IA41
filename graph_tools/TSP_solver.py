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
    nodes = []

    start = timestamp.time()
    graph = input_generator.graph_from_coordinates_array(nodesgeocode)
    
    if(algorithm2=="Christofides"):
        algorithm2 = "christofides"
    elif(algorithm2=="Ant Algorithm"):
        algorithm2 = "ant_colony"
    else:
        raise ValueError("Unknown 2nd algorithm")
    
    

    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))
    end = timestamp.time()
    print("Time to create the graph: ", end - start)
    
    
    
    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    print(algorithm2)
    simplified_graph = ConstructGraph.construct_graph(graph, nodes, algorithm1, algorithm2)
    end = timestamp.time()
    print("Time to simplify the graph: ", end - start)

    #Mesure the time to run the second algorithm
    start = timestamp.time()
    #If there is only two nodes, return the path between them
    if len(nodesgeocode) == 2:
        if algorithm2 == "christofides":
            path = simplified_graph[1][0][1]
        else:
            path = simplified_graph[nodes[0]][nodes[1]]["path"]
        end = timestamp.time()
        print("Time to find the path: ", end - start)
        return graph, path
    

    
    if(algorithm2 == "ant_colony"):
        print("ant_colony")
        #Solve the TSP problem with the algorithm2
        colony = ant_colony.ant_colony(simplified_graph, nodes[0],n_ants=25)
        simplified_path, time = colony.run()
        #Find the path in the original graph
        path = [nodes[0]]
        for i in range(len(simplified_path)-1):
            path += simplified_graph[simplified_path[i]][simplified_path[i+1]]["path"][1:]

        #sort the geocode in the same order as the path
        nodesgeocode = [nodesgeocode[nodes.index(node)] for node in simplified_path]
    elif algorithm2 == "christofides":
        print("christofides")
        dic_path = simplified_graph[1]
        simplified_graph = simplified_graph[0]
        undirected_path = christofides.christofides(simplified_graph, test="weight")
        path = []
        for start_node, end_node in pairwise(undirected_path):
            path.extend(dic_path[start_node][end_node][:-1])
        path.append(end_node)
    end = timestamp.time()
    print("Time to solve the TSP problem: ", end - start)
    
    #return the solution
    return graph, path#, time
