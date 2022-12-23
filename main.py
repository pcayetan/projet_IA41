import sys, os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from folium import Marker, Icon
from folium.features import DivIcon
import osmnx as ox

import graph_tools.TSP_solver as tsp_solver

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
        layout = QVBoxLayout()
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        layout.addWidget(self.button1)
        layout.addWidget(self.algorithmComboBox1)
        layout.addWidget(self.algorithmComboBox2)
        layout.addWidget(self.button)
        layout.addWidget(self.preview)
        self.setLayout(layout)
        
    def add_input(self):
        # Create a new QLineEdit widget
        self.input = QLineEdit()

        # Set the placeholder text for the widget
        self.input.setPlaceholderText("New input")

        # Add the widget to the list of inputs
        self.inputs.append(self.input)

        # Add the widget to the layout
        self.layout.addWidget(self.input)

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
        #input_list = ['Belfort, France', 'Botans, France', 'andelnans, France', 'Danjoutin, France', 'Sevenans, France','Bourgogne-Franche-Comté, Perouse','Moval, France','Urcerey, France','Essert, France, Territoire de Belfort', 'Bavilliers','Cravanche','Vezelois','Meroux','Dorans','Bessoncourt','Denney','Valdoie']        
        
        ox.settings.log_console = True
        ox.settings.use_cache = True
        
        # Call the construct_graph method, passing the start and end locations as arguments
        try:
            graph, route, time, geocode_list = tsp_solver.main_solver(input_list, name_algorithm1=self.algorithmComboBox1.currentText(), name_algorithm2=self.algorithmComboBox2.currentText())
            print("The time to travel the route is: ", time, " seconds")

        except ValueError as err:
            #print an msgbox if the route is not possible
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(err.args[0])
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        except ConnectionError:
            #print an msgbox if the route is not possible
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
        route_map = ox.plot_route_folium(graph, route, tiles='openstreetmap', route_color="red" , route_width=10)

        # Create a Marker object for the start location
        start_latlng = (float(geocode_list[0][1]), float(geocode_list[0][0]))
        start_marker = Marker(location=(start_latlng[::-1]), popup='Start Location', icon=Icon(icon='glyphicon-flag', color='green'))

        # Add the start and end markers to the route_map
        start_marker.add_to(route_map)

        # Create a Marker object for each location in the route
        for i in range(1, len(geocode_list)-1):
            latlng = (float(geocode_list[i][1]), float(geocode_list[i][0]))
            # create a Marker object for the location containing a number icon
            marker = Marker(location=(latlng[::-1]), popup='Location', icon=Icon(icon='glyphicon-flag', color='blue'))
            marker = Marker(location=(latlng[::-1]), popup='Location', icon=DivIcon(icon_size=(150,36),icon_anchor=(7,20),html='<div style="font-size: 18pt; color : black">'+str(i)+'</div>'))
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