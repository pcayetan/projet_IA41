import ConstructGraph,input_generator
from algorithms import ant_colony, christofides, dijkstra
import osmnx as ox
import time as timestamp
from itertools import pairwise
def tsp_solver(nodesgeocode, algorithm1 = "Dijkstra", algorithm2="ant_colony"):
    """Construct a graph with only the nodes latitude and longitude to visit with the algorithm1 and solve the TSP problem with the algorithm2

    Args:
        places: A list of duos of latitude and longitude of the nodes to visit: (latitude, longitude)
        algorithm1: The algorithm to use to construct the new graph
        algorithm2: The algorithm to use to solve the TSP problem

    Returns:
        The path to visit the nodes in the order given by the algorithm2
    """
    nodes = []
    graph = input_generator.graph_from_coordinates_array(nodesgeocode)
    
    # c'est moche de faire ça alors que pas besoin pour ant
    graph_strongly_connected = ox.utils_graph.get_largest_component(graph, strongly=True)
    undirected_graph = ox.get_undirected(graph_strongly_connected)

    for latitude, longitude in nodesgeocode:
        nodes.append(ox.nearest_nodes(graph_strongly_connected, float(longitude), float(latitude)))

    #If there is only two nodes, return the path between them
    if len(nodesgeocode) == 2:
        path = simplified_graph[nodes[0]][nodes[1]]["path"]
        return graph, path, simplified_graph[nodes[0]][nodes[1]]["time"]
    end = timestamp.time()
    
    
    #Mesure the time to run the first algorithm
    start = timestamp.time()
    #Create a graph with only the nodes to visit with the algorithm1
    # c'est moche de faire ça alors que pas besoin pour ant
    simplified_graph = ConstructGraph.construct_graph(graph, undirected_graph, nodes, algorithm1, algorithm2)
    end = timestamp.time()
    print("Time to simplify the graph: ", end - start)


    #Mesure the time to run the second algorithm
    start = timestamp.time()
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


if __name__ == '__main__':
    input_list = ['Belfort, France', 'Botans, France', 'andelnans, France', 'Danjoutin, France','Moval, France','Urcerey, France','Essert, France, Territoire de Belfort', 'Bavilliers','Cravanche','Vezelois','Meroux','Dorans','Bessoncourt','Denney','Valdoie']
    geocode_list = []
    
    geocode_to_place = {}
    for input in input_list:
        try:
            geocode = ox.geocode(input)
            geocode_list.append(geocode)
            geocode_to_place[geocode] = input
        except:
            print("Please enter a valid location")
    graph, best_path = tsp_solver(geocode_list, algorithm2="christofides")
    route_map = ox.plot_route_folium(graph, best_path, tiles='openstreetmap', route_color="red" , route_width=10)   
    route_map.save('route.html')