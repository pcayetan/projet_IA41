import osmnx as ox
import algorithms.dijkstra as dijkstra
import algorithms.ant_colony as ant_colony

ox.settings.log_console=True
ox.settings.use_cache=True
# define the start and end locations in latlng
start_latlng = (-122.43327,37.78497)
end_latlng = (-122.41445,37.78071)
# location where you want to find your route
place     = 'San Francisco, California, United States'
# find shortest route based on the mode of travel
mode      = 'drive'        # 'drive', 'bike', 'walk'
# find shortest path based on distance or time
optimizer = 'time'        # 'length','time'
# create graph from OSM within the boundaries of some 
# geocodable place(s)
graph = ox.graph_from_place(place, simplify=True, network_type = mode)
# find the nearest node to the start location
print(graph.graph)
origin = ox.nearest_nodes(graph, start_latlng[0], start_latlng[1])
# find the nearest node to the end location
destination = ox.nearest_nodes(graph, end_latlng[0], end_latlng[1])

# find the shortest path between origin and destination
route = dijkstra.bidirectional_dijkstra(graph, origin, destination, weight=optimizer)

route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', route_color = 'red', route_width = 6)

# save the map as an html file
route_map.save('route.html')


