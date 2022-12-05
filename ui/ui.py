# Import the necessary modules from PyQt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextBrowser

# Import the necessary modules for handling signals and slots
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

# Create a class that will be used to handle the button click event
class ButtonHandler(QObject):
    # Define a custom signal that will be emitted when the button is clicked
    button_clicked = pyqtSignal()

    # Define the event handler for the button click
    @pyqtSlot()
    def on_click(self):
        # Emit the custom signal when the button is clicked
        self.button_clicked.emit()

# Create an instance of QApplication, which manages the main event loop
# and overall control flow of the GUI application
app = QApplication([])

# Create a QWidget, which will be the main window of our application
window = QWidget()

# Set the window title and size
window.setWindowTitle('My UI')
window.resize(600, 400)

# Create the two text fields and set their placeholder text
text_field1 = QLineEdit()
text_field1.setPlaceholderText('Enter text here')

text_field2 = QLineEdit()
text_field2.setPlaceholderText('Enter more text here')

# Create the button and set its text
button = QPushButton('Click me')

# Create an instance of ButtonHandler and connect its button_clicked signal
# to the on_click() slot
button_handler = ButtonHandler()
button.clicked.connect(button_handler.on_click)

# Create the HTML view
html_view = QTextBrowser()

# Add the text fields, button, and HTML view to the window
window.addWidget(text_field1)
window.addWidget(text_field2)
window.addWidget(button)
window.addWidget(html_view)

# Show the window
window.show()

# Run the main event loop of the application
app.exec_()
