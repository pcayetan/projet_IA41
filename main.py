import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import osmnx as ox
import algorithms.dijkstra as dijkstra
import algorithms.ant_colony as ant_colony

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

    def findShortestRoute(self, start_latlng, end_latlng):
        # Create the graph from OSM within the boundaries of some
        # geocodable place(s)
        graph = ox.graph_from_place(self.place, simplify=True, network_type=self.mode)
        # impute speed on all edges missing data
        graph = ox.add_edge_speeds(graph)
        # calculate travel time (seconds) for all edges
        graph = ox.add_edge_travel_times(graph)
        # find the nearest node to the start location
        origin = ox.nearest_nodes(graph, start_latlng[0], start_latlng[1])
        # find the nearest node to the end location
        destination = ox.nearest_nodes(graph, end_latlng[0], end_latlng[1])
        # find the shortest path between origin and destination
        distance, route = dijkstra.dijkstra(graph, origin, destination)
        # return the route
        return graph, distance, route

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set the window size
        self.setFixedSize(800, 800)
        self.setWindowTitle("Map Viewer")
        # Create the input fields
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Start location")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("End location")
        
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

        # Create the layout and add the widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        layout.addWidget(self.button)
        layout.addWidget(self.preview)
        self.setLayout(layout)
        
    def handleButtonClick(self):
        # Get the input from the fields
        input1 = self.input1.text()
        input2 = self.input2.text()

        input1 = ox.geocode(input1)
        input2 = ox.geocode(input2)
        
        # Convert the input to float values
        start_latlng = (float(input1[1]), float(input1[0]))
        end_latlng = (float(input2[1]), float(input2[0]))
        
        # Create an instance of the MainClass
        main_class = MainClass()
        
        # Call the findShortestRoute() method, passing the start and end locations as arguments
        graph, distance, route = main_class.findShortestRoute(start_latlng, end_latlng)
        
        # Plot the route on a map and save it as an HTML file
        route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', route_color='red', route_width=6)
        route_map.save('route.html')
        
        # Convert the Map object to an HTML string
        route_html = route_map.render()

        # Load the HTML string in the preview widget
        self.preview.setHtml(route_html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())