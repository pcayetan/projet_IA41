import math
import osmnx as ox
import networkx as nx
#from algorithms import christofides
import numpy as np
import random, re
import matplotlib.pyplot as plt

ox.settings.log_console = False
ox.settings.use_cache = True

 # input: bounds of the area in which the coordinates are generated
    # input: number of generated coordinates
    # output: array of nb_coordinates coordinates inside a rectangle bounded by the input 
def coordinates_array_generator(north,south,east,west, nb_coordinates):
    coordinates_array = [
        [
            random.uniform(south, north),
            random.uniform(east, west) 
        ] for _ in range(nb_coordinates)
    ]
    return np.array(coordinates_array)

#   input: string like "3.16458,-46.6876"
#   output: array of two floats [3.16458,-46.6876]
#   if regex fails to get the two floats, outputs -1
def string_to_coordinates(string):
    regex_float_pattern = "[-]?[0-9]*\.?[0-9]+"
    string_coordinates = re.findall(regex_float_pattern, string)
    float_coordinates = [float(ele) for ele in string_coordinates]
    if float_coordinates is None:
        print("Error: string_to_coordinates: no coordinates found!")
        return -1
    else:
        return float_coordinates

#   input: list of coordinates
#   output: a graph in which all of the coordinates fit
#   the graph construction fails, returns -1
def graph_from_coordinates_array(coordinates_array, simplify=True, network_type='drive'):
    north, west = np.max(coordinates_array, axis=0)
    south, east = np.min(coordinates_array, axis=0)
    graph  = ox.graph_from_bbox(48.86802,48.85323,2.40142,2.37008, simplify=simplify, network_type=network_type, clean_periphery=True)
    graph_strongly_connected = ox.utils_graph.get_largest_component(graph, strongly=True)
    return ox.utils_graph.get_undirected(graph_strongly_connected), graph

def main():
    south = 48.85323
    west = 2.37008
    north = 48.86802
    east = 2.40142
    coordinates_array = coordinates_array_generator(north,south,east,west, 5)
    #coordinates_array = [[48.85494919,2.38073608],
    #                    [48.86175313,2.37965958],
    #                    [48.86635282,2.39309527]]
    #coordinates_array = np.array(coordinates_array)
    # Create a graph from the OpenStreetMap data
    graph_strong, graph = graph_from_coordinates_array(coordinates_array, simplify=True, network_type='drive')
    latitudes_array, longitudes_array = coordinates_array.T
    
    # impute speed on all edges missing data
    graph_strong = ox.add_edge_speeds(graph_strong)
    # calculate travel time (seconds) for all edges
    graph_strong = ox.add_edge_travel_times(graph_strong)
    nodes_array = ox.nearest_nodes(graph_strong, longitudes_array, latitudes_array)
    route = nx.algorithms.approximation.traveling_salesman_problem(graph_strong, weight='travel_time', nodes=nodes_array, cycle=False)
    # find the shortest path between origin and destination
    
    # Plot the route on a map and save it as an HTML file
    route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', route_color="red" , route_width=10)
    route_map.save('route.html')
    fig = ox.plot_graph_route(graph_strong, route, node_size=0)    
    fig.show()
    
if __name__ == '__main__':
    main()
