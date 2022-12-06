# Description: This script uses the GeoIP2 database to get the user's IP address and then uses OSMnx to get the nearest network to the user's location.

# Import the necessary libraries
import osmnx as ox
import geoip2.database
import requests

ox.settings.log_console = True
ox.settings.use_cache = True

# Make an HTTP request to the httpbin.org website
response = requests.get('http://httpbin.org/ip')

# Get the user's IP address from the response
user_ip = response.json()['origin']

# Open the GeoIP2 database file

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# Look up the user's IP address
response = reader.city(user_ip)

# Get the user's latitude and longitude coordinates
latitude = response.location.latitude
longitude = response.location.longitude

# Use OSMnx to get the nearest network to the user's location
G = ox.graph_from_point((latitude, longitude), dist=500, network_type='drive')

G = ox.add_edge_speeds(G)
# calculate travel time (seconds) for all edges
G = ox.add_edge_travel_times(G)

fig = ox.plot_graph(G, node_size=0.5)

fig.show()