import math
import osmnx as ox

ox.settings.log_console = True
ox.settings.use_cache = True

def get_midpoint(lat1, lon1, lat2, lon2):
    """Return the midpoint between two lat/long coordinates.
    """
    lat1_radians = math.radians(lat1)
    lon1_radians = math.radians(lon1)
    lat2_radians = math.radians(lat2)
    lon2_radians = math.radians(lon2)

    bx = math.cos(lat2_radians) * math.cos(lon2_radians - lon1_radians)
    by = math.cos(lat2_radians) * math.sin(lon2_radians - lon1_radians)
    lat_midpoint = math.atan2(math.sin(lat1_radians) + math.sin(lat2_radians), math.sqrt((math.cos(lat1_radians) + bx) ** 2 + by ** 2))
    lon_midpoint = lon1_radians + math.atan2(by, math.cos(lat1_radians) + bx)

    return math.degrees(lat_midpoint), math.degrees(lon_midpoint)

def get_distance(lat1, lon1, lat2, lon2):
    """Return the distance between two lat/long coordinates.
    """
    lat1_radians = math.radians(lat1)
    lon1_radians = math.radians(lon1)
    lat2_radians = math.radians(lat2)
    lon2_radians = math.radians(lon2)

    dlon = lon2_radians - lon1_radians
    dlat = lat2_radians - lat1_radians
    a = (math.sin(dlat / 2) ** 2) + math.cos(lat1_radians) * math.cos(lat2_radians) * (math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371000 * c

    return distance

def main():
    lat1 = 37.73004866666667
    lon1 = -122.39446533333333
    lat2 = 37.779444028651405
    lon2 = -122.42601701484655

    midpoint = get_midpoint(lat1, lon1, lat2, lon2)
    distance = get_distance(lat1, lon1, lat2, lon2)

    print("Midpoint:", midpoint)
    print("Distance:", distance, "meters")

    # Create a graph from the OpenStreetMap data
    graph = ox.graph_from_point(midpoint, dist=distance/2, network_type='drive')
    #graph = ox.graph_from_place('San Francisco, California, United States', simplify=True, network_type='drive')
    # impute speed on all edges missing data
    graph = ox.add_edge_speeds(graph)
    # calculate travel time (seconds) for all edges
    graph = ox.add_edge_travel_times(graph)

    # find the nearest node to the start location
    origin = ox.nearest_nodes(graph, lat1, lon1)
    # find the nearest node to the end location
    destination = ox.nearest_nodes(graph, lat2, lon2)

    # find the shortest path between origin and destination
    shortest_path  = ox.shortest_path(graph, origin, destination, weight='travel_time')

    route = shortest_path

    # plot the route
    fig = ox.plot_graph_route(graph, route, node_size=0)

    fig.show()
    
if __name__ == '__main__':
    main()
