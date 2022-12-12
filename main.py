import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import osmnx as ox
import algorithms.dijkstra as dijkstra
import algorithms.astar as astar
import algorithms.ant_colony as ant_colony
import math
from folium import Marker, Icon
import matplotlib.pyplot as plt
from graph_tools import TSP_solver

class MainClass:
    # Define class attributes
    global_var = "Hello, World!"
    
    def __init__(self):
        # Set configuration settings for osmnx
        ox.settings.log_console = True
        ox.settings.use_cache = True
        # location where you want to find your route
        self.place = 'San Francisco, California, United States'
        # find shortest route based on the mode of travel
        self.mode = 'drive'        # 'drive', 'bike', 'walk'
        # find shortest path based on distance or time
        self.optimizer = 'time'        # 'length', 'time'
        
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

    def findShortestRoute(self, start_latlng, end_latlng, algorithm):
        # Create the graph from OSM within the boundaries of some
        # geocodable place(s)
        lat1 = start_latlng[1]
        lon1 = start_latlng[0]
        lat2 = end_latlng[1]
        lon2 = end_latlng[0]

        midpoint = MainClass.get_midpoint(lat1, lon1, lat2, lon2)
        distance = MainClass.get_distance(lat1, lon1, lat2, lon2)

        print("Midpoint:", midpoint)
        print("Distance:", distance, "meters")

        # Create a graph from the OpenStreetMap data
        graph = ox.graph_from_point(midpoint, dist=distance/2, network_type='drive', simplify=False)
        #graph = ox.graph_from_place(self.place, simplify=True, network_type=self.mode)


        # impute speed on all edges missing data
        graph = ox.add_edge_speeds(graph)
        # calculate travel time (seconds) for all edges
        graph = ox.add_edge_travel_times(graph)
        # find the nearest node to the start location
        origin = ox.nearest_nodes(graph, start_latlng[0], start_latlng[1])
        # find the nearest node to the end location
        destination = ox.nearest_nodes(graph, end_latlng[0], end_latlng[1])
        # find the shortest path between origin and destination
        if algorithm == "A*":
            distance, route = astar.astar(graph, origin, destination)
        elif algorithm == "Dijkstra":
            distance, route = dijkstra.dijkstra(graph, origin, destination)
        #distance, route = dijkstra.dijkstra(graph, origin, destination)
        # return the route
        return graph, distance, route

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowTitle("Map Viewer")
        # Create the input fields
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Start location")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("End location")

        # Create the drop-down menu
        self.algorithmComboBox = QComboBox()
        self.algorithmComboBox.addItem("A*")
        self.algorithmComboBox.addItem("Dijkstra")
        
        # Create the button and connect it to the handleButtonClick() method
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.handleButtonClick)
        
        # Create the HTML preview widget
        self.preview = QWebEngineView()
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'route.html')
        url = QUrl.fromLocalFile(filename)
        print(os.path.exists(filename))
        self.preview.load(url)

        self.inputs = []
        # Add the widget to the list of inputs
        self.inputs.append(self.input1)     

        # Add the widget to the list of inputs
        self.inputs.append(self.input2)

        # Create a QPushButton widget
        self.button1 = QPushButton("+")  

        # Connect the clicked signal of the button to a slot
        self.button1.clicked.connect(self.add_input)

        # Create a second QPushButton widget
        self.button2 = QPushButton("Print inputs")

        # Connect the clicked signal of the button to a slot
        self.button2.clicked.connect(self.print_inputs)

        # Create the layout and add the widgets to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.input2)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.algorithmComboBox)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)
        
    def add_input(self):
        # Create a new QLineEdit widget
        self.input = QLineEdit()

        # Set the placeholder text for the widget
        self.input.setPlaceholderText("New input")

        # Add the widget to the list of inputs
        self.inputs.append(self.input)

        # Add the widget to the layout
        self.layout.addWidget(self.input)

    def print_inputs(self):
        # Create an empty list to store the text entered in the inputs
        inputs_list = []
        # Use a for loop to add the text entered in each input to the list
        for input in self.inputs:
            # Check if the input is empty
            if input.text():
                # Add the text entered in the input to the list
                inputs_list.append(input.text())
        # Move the second input to the end of the list
        inputs_list.append(inputs_list.pop(1))
        # Print the list
        print(inputs_list)
        # Return the list
        return inputs_list

    def handleButtonClick(self):
        # Get the input from the fields

        input_list = self.print_inputs()
        #Line used to debug quickly
        #input_list = ['Belfort, France', 'Botans, France', 'andelnans, France', 'Danjoutin, France', 'Sevenans, France','Bourgogne-Franche-Comté, Perouse','Moval, France','Urcerey, France','Essert, France, Territoire de Belfort', 'Bavilliers','Cravanche','Vezelois','Meroux','Dorans','Bessoncourt','Denney','Valdoie']
        geocode_list = []
        
        for input in input_list:
            try:
                geocode_list.append(ox.geocode(input))
            except:
                print("Please enter a valid location")
                return
        
        # Create an instance of the MainClass
        main_class = MainClass()
        
        # Call the construct_graph method, passing the start and end locations as arguments
        try:
            graph, route, time = TSP_solver.construct_graph(geocode_list, algorithm1=self.algorithmComboBox.currentText())
        except:
            return "No route found between the given locations. Please select two different locations"
        # Plot the route on a map and save it as an HTML file
        route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', route_color="red" , route_width=10)
        #route_map.save('route.html')

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

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'route.html')
        url = QUrl.fromLocalFile(filename)
        print(os.path.exists(filename))
        self.preview.load(url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())