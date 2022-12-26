import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import folium
from folium.features import DivIcon
from folium import Marker, Icon
import osmnx as ox
import geoip2.database
import requests
import time

import graph_tools.TSP_solver as tsp_solver


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.preload()
        self.initUI()

    def preload(self):
        start_time = time.time()

        ox.settings.log_console = False
        ox.settings.use_cache = True

        # Make an HTTP request to the httpbin.org website
        response = requests.get('http://httpbin.org/ip')

        # Get the user's IP address from the response
        user_ip = response.json()['origin']

        # Open the GeoIP2 database file
        reader = geoip2.database.Reader('testtools/dataset/GeoLite2-City.mmdb')

        # Look up the user's IP address
        response = reader.city(user_ip)

        # Get the user's latitude and longitude coordinates
        latitude = response.location.latitude
        longitude = response.location.longitude

        # Use OSMnx to get the nearest network to the user's location
        G = ox.graph_from_point((latitude, longitude),
                                dist=1000, network_type='drive')
        G = ox.add_edge_speeds(G)
        # calculate travel time (seconds) for all edges
        G = ox.add_edge_travel_times(G)
        end_time = time.time()

        # Use folium to plot the map
        m = folium.Map(location=[latitude, longitude], zoom_start=15)

        # Add the map to the web page
        m.save('route.html')

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        # Print the elapsed time
        print(f'Elapsed time: {elapsed_time:.2f} seconds')

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowTitle("Map Viewer")
        # Create a URL pointing to the CSS file
        css_url = QUrl.fromLocalFile("style.css")
        # Create a QFile object to read the CSS file
        css_file = QFile(css_url.toLocalFile())
        # Open the file
        css_file.open(QFile.ReadOnly | QFile.Text)
        # Read the file
        css = QTextStream(css_file).readAll()
        # Close the file
        css_file.close()        # Set the stylesheet for the form
        self.setStyleSheet(css)
        # Create the input fields
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Start location")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("End location")

        # Create the drop-down menu
        self.algorithmComboBox1 = QComboBox()
        self.algorithmComboBox1.addItem("A*")
        self.algorithmComboBox1.addItem("Dijkstra")

        self.algorithmComboBox2 = QComboBox()
        self.algorithmComboBox2.addItem("Ant Algorithm")
        self.algorithmComboBox2.addItem("Christofides")
        self.algorithmComboBox2.addItem("Pairwise exchange")

        # Create the button and connect it to the handleButtonClick() method
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.handleButtonClick)

        # Create the HTML preview widget
        self.preview = QWebEngineView()
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'route.html')
        url = QUrl.fromLocalFile(filename)
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

        # Create the layout and add the widgets to it
        self.playout = QVBoxLayout()
        self.playout2 = QVBoxLayout()
        # Add self.playout2 to the main layout
        self.playout.addLayout(self.playout2)
        self.playout2.addWidget(self.input1)
        self.playout2.addWidget(self.input2)
        self.playout.addWidget(self.button1)
        self.playout.addWidget(self.algorithmComboBox1)
        self.playout.addWidget(self.algorithmComboBox2)
        self.playout.addWidget(self.button)
        self.playout.addWidget(self.preview)
        self.setLayout(self.playout)

    def add_input(self):
        # Create a new QLineEdit widget
        self.input = QLineEdit()

        # Set the placeholder text for the widget
        self.input.setPlaceholderText("New input")

        # Add the widget to the list of inputs
        self.inputs.append(self.input)

        # Add the widget to the layout
        self.playout2.addWidget(self.input)

    def get_inputs(self):
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

    #The function that will be called when the button is clicked
    def handleButtonClick(self):
        # Get the input from the fields

        input_list = self.get_inputs()
        #Line used to debug quickly
        #input_list = ['Belfort, France', 'Botans, France', 'andelnans, France', 'Danjoutin, France', 'Sevenans, France','Territoire de Belfort, Perouse','Moval, France','Urcerey, France','Essert, France, Territoire de Belfort', 'Bavilliers','Cravanche','Vezelois','Meroux','Dorans','Bessoncourt','Denney','Valdoie',"Chèvremont, Territoire de Belfort, France","Fontenelle, Territoire de Belfort, France","Sermamagny, Territoire de Belfort, France","Eloie, Territoire de Belfort, France"]

        ox.settings.log_console = True
        ox.settings.use_cache = True

        # Call the construct_graph method, passing the start and end locations as arguments
        try:
            graph, route, time, geocode_list = tsp_solver.main_solver(
                input_list, name_algorithm1=self.algorithmComboBox1.currentText(), name_algorithm2=self.algorithmComboBox2.currentText())
            print("The time to travel the route is: ", time, " seconds")
            # Create a QLabel widget to display the time
            # divide time by 3600 to get the number of hours
            hours, seconds = divmod(time, 3600)
            # divide the remainder by 60 to get the number of minutes
            minutes, seconds = divmod(seconds, 60)

            # Convert the hours, minutes, and seconds to strings and add leading zeros if necessary
            hours_string = str(int(hours)).zfill(2)
            minutes_string = str(int(minutes)).zfill(2)
            seconds_string = str(int(seconds)).zfill(2)
            # Create a string in the format "hours:minutes:seconds"
            time_string = f"{hours_string}:{minutes_string}:{seconds_string} to drive"
            # Check if the time_label widget already exists
            if hasattr(self, 'time_label'):
                # If the time_label widget already exists, set the text of the widget to the updated time
                self.time_label.setText(time_string)
            else:
                # If the time_label widget does not exist, create a new QLabel widget to display the time
                self.time_label = QLabel()
                # Set the text of the time_label to the time string
                self.time_label.setText(time_string)
                # Add the time_label to the layout
                self.playout.addWidget(self.time_label, 0, Qt.AlignRight)

        except ValueError as err:
            #print an msgbox if there is a problem with the input
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(err.args[0])
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        except ConnectionError:
            #print an msgbox if there is a problem with the connection
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Connection error, please try again")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        except:
            #print an msgbox if the route is not possible
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unknow error, please try again")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        # Plot the route on a map and save it as an HTML file
        route_map = ox.plot_route_folium(
            graph, route, tiles='openstreetmap', route_color="red", route_width=10)

        # Create a Marker object for the start location
        start_latlng = (float(geocode_list[0][1]), float(geocode_list[0][0]))
        start_marker = Marker(location=(
            start_latlng[::-1]), popup='Start Location', icon=Icon(icon='glyphicon-flag', color='green'))

        # Add the start and end markers to the route_map
        start_marker.add_to(route_map)

        # Create a Marker object for each location in the route
        for i in range(1, len(geocode_list)-1):
            latlng = (float(geocode_list[i][1]), float(geocode_list[i][0]))
            # create a Marker object for the location containing a number icon
            marker = Marker(location=(
                latlng[::-1]), popup='Location', icon=Icon(icon='glyphicon-flag', color='blue'))
            marker = Marker(location=(latlng[::-1]), popup='Location', icon=DivIcon(icon_size=(
                150, 36), icon_anchor=(7, 20), html='<div style="font-size: 18pt; color : black">'+str(i)+'</div>'))
            marker.add_to(route_map)

        # Save the HTML file
        route_map.save('route.html')

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'route.html')
        url = QUrl.fromLocalFile(filename)
        print(os.path.exists(filename))
        self.preview.load(url)
        print("Route sent")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
