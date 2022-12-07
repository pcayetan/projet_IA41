# Import the required modules
from PyQt5 import QtWidgets

# Create a QWidget-based class
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Create a QVBoxLayout
        self.layout = QtWidgets.QVBoxLayout()

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Create an empty list to store the inputs
        self.inputs = []

        # Create a QLineEdit widget
        input1 = QtWidgets.QLineEdit()

        # Set the placeholder text for the widget
        input1.setPlaceholderText("Start location")

        # Add the widget to the list of inputs
        self.inputs.append(input1)

        # Add the widget to the layout
        self.layout.addWidget(input1)

        # Create a second QLineEdit widget
        input2 = QtWidgets.QLineEdit()

        # Set the placeholder text for the widget
        input2.setPlaceholderText("End location")

        # Add the widget to the list of inputs
        self.inputs.append(input2)

        # Add the widget to the layout
        self.layout.addWidget(input2)

        # Create a QPushButton widget
        button1 = QtWidgets.QPushButton("+")

        # Connect the clicked signal of the button to a slot
        button1.clicked.connect(self.add_input)

        # Add the button to the layout
        self.layout.addWidget(button1)

        # Create a second QPushButton widget
        button2 = QtWidgets.QPushButton("Print inputs")

        # Connect the clicked signal of the button to a slot
        button2.clicked.connect(self.print_inputs)

        # Add the button to the layout
        self.layout.addWidget(button2)

    def add_input(self):
        # Create a new QLineEdit widget
        input = QtWidgets.QLineEdit()

        # Set the placeholder text for the widget
        input.setPlaceholderText("New input")

        # Add the widget to the list of inputs
        self.inputs.append(input)

        # Add the widget to the layout
        self.layout.addWidget(input)
         
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

# Create a QApplication
app = QtWidgets.QApplication([])

# Create an instance of MyWidget
widget = MyWidget()

# Show the widget
widget.show()

# Run the application
app.exec_()