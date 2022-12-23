from graph_tools import ConstructGraph, input_generator
from algorithms import ant_colony, christofides, pairwise_exchange
import osmnx as ox
import time as timestamp
import networkx as nx

def main_solver(nodesgeocode, algorithm1 = "Dijkstra", algorithm2="Christofides"):

    #Create the graph to run the algorithm on
    start = timestamp.time()
    nodes, graph = input_generator.graph_from_coordinates_array(nodesgeocode)
    end = timestamp.time()
    print("Time to create the graph: ", end - start)
    
    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    dictionnary = ConstructGraph.construct_graph(graph, nodes, algorithm1)
    end = timestamp.time()
    print("Time to simplify the graph: ", end - start)

    if len(nodesgeocode) == 2:
        path, time = single_path_solver(nodes, dictionnary)
        return graph, path, time, [nodesgeocode[0],nodesgeocode[1]]
    else:
        simplified_path = tsp_solver(graph, nodes, dictionnary, algorithm2)
        path, time = get_path_time(nodes, dictionnary, simplified_path)
        nodesgeocode = [nodesgeocode[nodes.index(node)] for node in simplified_path]
        return graph, path, time, nodesgeocode


def single_path_solver(nodes, dictionnary):
    path = dictionnary[nodes[0]][nodes[1]]["path"]
    time = dictionnary[nodes[0]][nodes[1]]["time"]
    return path, time
    

def tsp_solver(graph, nodes, dictionnary, algorithm_name="Christofides"):
    algorithm = choose_algorithm(algorithm_name)
    #Solve the TSP problem with the algorithm2
    start = timestamp.time()
    if(algorithm == "ant_colony"):        
        colony = ant_colony.ant_colony(dictionnary, nodes[0],n_ants=25)
        simplified_path, time = colony.run()
    elif algorithm == "christofides":
        simplified_path = christofides.christofides(dictionnary)
    if algorithm == "pairwise_exchange":
        simplified_path = pairwise_exchange.pairwise_exchange(dictionnary, nodes, len(nodes))
    end = timestamp.time()
    print("Time to solve the TSP problem: ", end - start)
    return simplified_path

def choose_algorithm(algorithm):
    algorithm_dictionary = {
        "Pairwise exchange": "pairwise_exchange",
        "Christofides": "christofides",
        "Ant Algorithm": "ant_colony"
    }
    function = algorithm_dictionary.get(algorithm)
    if function is None:
        raise NameError("Unknown algorithm")
    print("TSP algorithm:", algorithm)
    return function

def get_path_time(nodes, dictionnary, simplified_path):
    #Recreate path
    time = 0
    path = [nodes[0]]
    for i in range(len(simplified_path)-1):
        path += dictionnary[simplified_path[i]][simplified_path[i+1]]["path"][1:]
        time +=  dictionnary[simplified_path[i]][simplified_path[i+1]]["time"]
    return path, time