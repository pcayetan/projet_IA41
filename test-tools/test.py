import math
import osmnx as ox
import networkx as nx
#from algorithms import christofides
import numpy as np
import random, re
import matplotlib.pyplot as plt
import sys
import input_generator

sys.path.insert(1, '/home/pierre_olivier/Documents/IA41/projet_IA41/algorithms')
import christofides


ox.settings.log_console = True
ox.settings.use_cache = True



def main():
    
    coordinates_array = input_generator.get_communes_in_departement("Bas-Rhin", "U")

    print(coordinates_array)


    latitudes_array, longitudes_array = coordinates_array.T
    # Create a graph from the OpenStreetMap data
    graph, graph_strong = input_generator.graph_from_coordinates_array(coordinates_array, simplify=True, network_type='drive')
    print("CREATED GRAPH")
    
    # impute speed on all edges missing data
    graph_strong = ox.add_edge_speeds(graph_strong)
    # calculate travel time (seconds) for all edges
    graph_strong = ox.add_edge_travel_times(graph_strong)
    nodes_array = ox.nearest_nodes(graph_strong, longitudes_array, latitudes_array)
    print("ADDED NODES AND EDGES")
    #route = nx.algorithms.approximation.traveling_salesman_problem(graph_strong, weight='travel_time', nodes=nodes_array, cycle=True)
    route = christofides.traveling_salesman_problem(graph_strong, weight='travel_time', nodes=nodes_array, cycle=True)
    print("CALCULATED ROUTE")
    # find the shortest path between origin and destination
    
    # Plot the route on a map and save it as an HTML file
    route_map = ox.plot_route_folium(graph_strong, route, tiles='openstreetmap', route_color="red" , route_width=10, )
    route_map.save('route.html')
    print("FINISHED")

if __name__ == '__main__':
    main()
