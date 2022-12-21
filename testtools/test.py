import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import osmnx as ox
import networkx as nx
import math
from folium import Marker, Icon
import matplotlib.pyplot as plt
import input_generator
import christofides
from networkx.utils import pairwise
import time as timestamp

ox.settings.log_console = True
ox.settings.use_cache = True



def main():
    input_list = ['Belfort, France', 'Botans, France', 'andelnans, France', 'Danjoutin, France', 'Sevenans, France','Bourgogne-Franche-Comté, Perouse','Moval, France','Urcerey, France','Essert, France, Territoire de Belfort', 'Bavilliers','Cravanche','Vezelois','Meroux','Dorans']#,'Bessoncourt','Denney','Valdoie']
    geocode_list = []
    
    geocode_to_place = {}
    for input in input_list:
        try:
            geocode = ox.geocode(input)
            geocode_list.append(geocode)
            geocode_to_place[geocode] = input
        except:
            print("Please enter a valid location")
            return

    graph = input_generator.graph_from_coordinates_array(geocode_list)
    graph_strongly_connected = ox.utils_graph.get_largest_component(graph, strongly=True)
    undirected_graph = ox.get_undirected(graph_strongly_connected)
    nodes = []
    undirected_nodes = []
    node_to_place = {}
    for latitude, longitude in geocode_list:
        n = ox.nearest_nodes(undirected_graph, float(longitude), float(latitude))
        undirected_nodes.append(n)
        node_to_place[n] = geocode_to_place[(latitude, longitude)]
    
    
    print("Calculating path in undirected graph")
    start = timestamp.time()
    # Gives the path between the main nodes in the undirectedly connected, undirected graph
    simplified_graph = christofides.traveling_salesman_problem(undirected_graph, "distance", undirected_nodes)
    end = timestamp.time()
    print("Calculated path in undirected graph. Time: ", end - start)

    undirected_path = christofides.christofides(simplified_graph, test="weight")
    print("Calculating full path")
    start = timestamp.time()
    # Calculate the full path between the nodes of the normal path
    best_path = []
    for u, v in pairwise(undirected_path):
        print(node_to_place[u],node_to_place[v])
        best_path.extend(nx.algorithms.dijkstra_path(graph, u, v)[:-1])
    best_path.append(v)
    end = timestamp.time()
    print("Translated. Time: ", end - start)
    

    route_map = ox.plot_route_folium(graph, best_path, tiles='openstreetmap', route_color="red" , route_width=10)

    # Create a Marker object for the start location
    start_latlng = (float(geocode_list[0][1]), float(geocode_list[0][0]))
    start_marker = Marker(location=(start_latlng[::-1]), popup='Start Location', icon=Icon(icon='glyphicon-flag', color='green'))

    # Add the start and end markers to the route_map
    start_marker.add_to(route_map)

    # Create a Marker object for each location in the route
    for i in range(1, len(geocode_list)):
        latlng = (float(geocode_list[i][1]), float(geocode_list[i][0]))
        marker = Marker(location=(latlng[::-1]), popup='Location', icon=Icon(icon='glyphicon-flag', color='blue'))
        marker.add_to(route_map)


    # Save the HTML file
    route_map.save('route.html')
    print("FINISHED")
    exit(1)

if __name__ == '__main__':
    main()
