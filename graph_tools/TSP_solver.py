from graph_tools import ConstructGraph, input_generator
from algorithms import ant_colony, christofides, pairwise_exchange, astar, dijkstra
import osmnx as ox
import time as timestamp

def main_solver(nodes_to_visit, name_algorithm1 = "Dijkstra", name_algorithm2="Christofides"):

    #select the algorithm to use
    algorithm1 = choose_algorithm(name_algorithm1)

    #Get the coordinates of the nodes
    nodesgeocode = NodesToCoordinates(nodes_to_visit)


    #Download the graph to run the algorithm on
    start = timestamp.time()
    nodes_to_visit, graph = graph_from_coordinates_array(nodesgeocode)
    end = timestamp.time()
    print("Time to download the graph: ", end - start)
    
    #Mesure the time to run the first algorithm
    start = timestamp.time()
    print("Start to create the graph with the algorithm: ", name_algorithm1, "")
    #Create a fully connected graph with only the nodes to visit with the algorithm1
    ConnectedSimplifiedGraph = ConstructGraph.construct_graph(graph, nodes_to_visit, algorithm1)
    end = timestamp.time()
    print("Time to create a  the graph: ", end - start)

    #If there is only two nodes, we don't need to run the TSP solver
    if len(nodesgeocode) == 2:
        path = ConnectedSimplifiedGraph[nodes_to_visit[0]][nodes_to_visit[1]]["path"]
        time = ConnectedSimplifiedGraph[nodes_to_visit[0]][nodes_to_visit[1]]["time"]
        return graph, path, time, [nodesgeocode[0],nodesgeocode[1]]

    else:
        
        solution_simplified_path = tsp_solver(graph, nodes_to_visit, ConnectedSimplifiedGraph, name_algorithm2)
        path, time = get_path_time(nodes_to_visit, ConnectedSimplifiedGraph, solution_simplified_path)
        nodesgeocode = [nodesgeocode[nodes_to_visit.index(node)] for node in solution_simplified_path]
        return graph, path, time, nodesgeocode

def tsp_solver(graph, nodes, dictionnary, algorithm_name="Christofides"):
    """Solve the TSP problem with the algorithm chosen.
    :param graph: the graph of the network
    :param nodes: the list of nodes to visit
    :param dictionnary: the graph representation
    :param algorithm_name: the name of the algorithm to use
    :return: the path to take
    """

    #Solve the TSP problem with the algorithm2
    start = timestamp.time()
    if(algorithm_name == "Ant Algorithm"):        
        colony = ant_colony.ant_colony(dictionnary, nodes[0],n_ants=25)
        simplified_solution_path = colony.run()
    elif algorithm_name == "Christofides":
        simplified_solution_path = christofides.christofides(dictionnary)
    elif algorithm_name == "Pairwise exchange":
        simplified_solution_path = pairwise_exchange.pairwise_exchange(graph, nodes, len(nodes))
    else:
        raise NameError("Unknown algorithm")
    end = timestamp.time()

    print("Time to solve the TSP problem: ", end - start)

    return simplified_solution_path

def choose_algorithm(algorithm="Dijkstra"):
    """Choose the algorithm 1 to use
    :param algorithm: the name of the algorithm to use
    :return: the function of the algorithm"""
    algorithm_dictionary = {
        "Dijkstra": dijkstra.dijkstra,
        "A*": astar.astar
    }
    function = algorithm_dictionary.get(algorithm)
    if function is None:
        raise NameError("Unknown algorithm")
    print("TSP algorithm:", algorithm)
    return function

def get_path_time(nodes, dictionnary, simplified_path):
    """
    This function takes a list of nodes and returns the path and the time to go through it
    :param nodes: list of nodes
    :param dictionnary: dictionnary of the graph
    :param simplified_path: list of nodes
    :return: path and time"""
    time = 0
    path = [nodes[0]]
    for i in range(len(simplified_path)-1):
        path += dictionnary[simplified_path[i]][simplified_path[i+1]]["path"][1:]
        time +=  dictionnary[simplified_path[i]][simplified_path[i+1]]["time"]
    return path, time

def NodesToCoordinates(NodesName):
    """
    This function takes a list of nodes and returns a list of coordinates
    :param NodesName: list of nodes
    :return: list of coordinates
    """

    geocode_list = []

    for NodeName in NodesName:
        geocode_list.append(ox.geocode(NodeName))
    
    return geocode_list

def graph_from_coordinates_array(coordinates_array, simplify=True, network_type='drive'):
    """Create a where the list of coordiante is in the graph
    :param coordinates_array: list of coordinates
    :param simplify: boolean to simplify the graph
    :param network_type: type of network
    :return: list of nodes and graph
    """
    #If there is the same adress, we remove the duplicates
    coordinates_array = list(dict.fromkeys(coordinates_array))

    if len(coordinates_array) == 0:
        raise ValueError("The list of coordinates is empty")
    if len(coordinates_array) == 1:
        raise ValueError("The list of coordinates contains only one element")
    

    minlat, maxlat, minlon, maxlon = coordinates_to_bounds(coordinates_array)    

    graph  = ox.graph_from_bbox(maxlat,minlat,maxlon,minlon, simplify=simplify, network_type=network_type, truncate_by_edge=True)
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    graph = ox.utils_graph.get_largest_component(graph, strongly=True)

    nodes = []
    for latitude, longitude in coordinates_array:
        nodes.append(ox.nearest_nodes(graph, float(longitude), float(latitude)))

    return nodes, graph

def coordinates_to_bounds(nodesgeocode):
    """Get the bounds of the coordinates and add a margin
    :param coordinates_array: list of coordinates
    :return: bounds
    """
    minlat = min([float(latitude) for latitude, _ in nodesgeocode])
    maxlat = max([float(latitude) for latitude, _ in nodesgeocode])
    minlon = min([float(longitude) for _, longitude in nodesgeocode])
    maxlon = max([float(longitude) for _, longitude in nodesgeocode])
    print(minlat, maxlat, minlon, maxlon)
    #Padding to get a bigger area
    padding = 0.05 * (maxlat - minlat)
    minlat -= padding
    maxlat += padding
    padding = 0.05 * (maxlon - minlon)
    minlon -= padding
    maxlon += padding
    #if the area is to linear, add padding to the other axis. This is to avoid the problem of the graph being a line
    if maxlat - minlat < 0.5 * (maxlon - minlon):
        padding = 0.5 * (maxlon - minlon) - (maxlat - minlat)
        minlat -= padding / 2
        maxlat += padding / 2
    elif maxlon - minlon < 0.5 * (maxlat - minlat):
        padding = 0.5 * (maxlat - minlat) - (maxlon - minlon)
        minlon -= padding / 2
        maxlon += padding / 2
    
    return minlat, maxlat, minlon, maxlon