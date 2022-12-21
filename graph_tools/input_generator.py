import pandas as pd
import numpy as np
import random, re
import osmnx as ox

def open_communes():
    communes_df = pd.read_csv('testtools/dataset/communes-departement-region.csv')
    communes_df = communes_df[['latitude', 'longitude', 'nom_commune','nom_departement', 'nom_region']]
    return communes_df

# 'Territoire de Belfort' 
def get_communes_in_departement(nom_departement, range="\w"):
    regex = '^' + range + '.*'
    communes_df = open_communes()
    communes_df = communes_df[communes_df.nom_departement == nom_departement]
    communes_df = communes_df[communes_df.nom_commune.str.match(regex)]
    return np.array(communes_df[['latitude', 'longitude']])

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
    graph  = ox.graph_from_bbox(north,south,east,west, simplify=simplify, network_type=network_type, truncate_by_edge=True)
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    return ox.utils_graph.get_largest_component(graph, strongly=True)