import sys  # System utilities for application exit
import math  # Mathematical functions for calculating square roots
import numpy as np  # Numerical computing library
import matplotlib.pyplot as plt  # Plotting library
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Matplotlib canvas for PySide6
from matplotlib.figure import Figure  # Matplotlib figure object

# Import PySide6 core and GUI components
from PySide6.QtCore import Qt, QSize  # Core Qt functionality
from PySide6.QtGui import QPalette, QColor, QFont  # GUI styling components
from PySide6.QtWidgets import (
    QApplication,  # Main application object
    QMainWindow,  # Main window container
    QLabel,  # Text labels for display
    QPushButton,  # Clickable buttons
    QLineEdit,  # Text input fields
    QVBoxLayout,  # Vertical box layout manager
    QHBoxLayout,  # Horizontal box layout manager
    QWidget,  # Base widget class
)
 
# Calculator logic
def reelle_loesninger_til_andengradsligning(a, b, c):
    """Denne funktion modtager a, b og c-koefficienterne til en andengradsligning sat op på standardform som argumenter og returnerer de reelle løsninger."""
    # Calculate the discriminant (b² - 4ac) to determine the number of real solutions
    d = b**2 - 4*a*c
    
    # Case 1: Discriminant > 0 means two distinct real solutions
    if d > 0:
        # Calculate both solutions using the quadratic formula
        x_1 = (-b + math.sqrt(d)) / (2*a)
        x_2 = (-b - math.sqrt(d)) / (2*a)
        return f"There are two solutions\nx_1 = {x_1}   x_2 = {x_2}"
    
    # Case 2: Discriminant = 0 means one repeated real solution
    elif d == 0:
        x = (-b + math.sqrt(d)) / (2*a)
        return f"There is only one solution:\nx = {x}"
    
    # Case 3: Discriminant < 0 means no real solutions (only complex solutions)
    else:
        return f"There are no real solutions"

# GUI
class HovedVindue(QMainWindow):
    def __init__(self):
        """Initialize the main window and call setup method."""
        super().__init__()
        self.opsaetning()

    def opsaetning(self):
        """Set up the GUI layout and components."""
        self.setWindowTitle("Andengradsligningsløser") # window title

        # Create a matplotlib figure and canvas for graphing
        self.figure = Figure(figsize=(8, 4), dpi=100)  # Create a figure with specific dimensions
        self.canvas = FigureCanvas(self.figure)  # Create canvas to display the figure
        self.ax = self.figure.add_subplot(111)  # Add a subplot to the figure
        self.ax.set_title("Quadratic Function Graph")  # Set graph title
        self.ax.set_xlabel("x")  # Label x-axis
        self.ax.set_ylabel("y")  # Label y-axis
        self.ax.grid(True)  # Enable grid on the graph
        
        # Create three input fields for coefficients a, b, and c
        self.input1 = QLineEdit()  # Input field for coefficient 'a'
        self.input2 = QLineEdit()  # Input field for coefficient 'b'
        self.input3 = QLineEdit()  # Input field for coefficient 'c'

        # Create labels for each coefficient
        a = QLabel("a =")
        b = QLabel("b =")
        c = QLabel("c =")

        # Create horizontal layout for inputs (labels and text fields in a row)
        input_layout = QHBoxLayout()
        input_layout.addWidget(a)
        input_layout.addWidget(self.input1)
        input_layout.addWidget(b)
        input_layout.addWidget(self.input2)
        input_layout.addWidget(c)
        input_layout.addWidget(self.input3)

        # Create the Calculate button with fixed size
        button = QPushButton("Calculate")
        button.setFixedSize(80, 40)
        button.clicked.connect(self.beregn)  # Connect button click to calculation method
        
        # Create a horizontal layout to center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add space before button
        button_layout.addWidget(button)  # Add centered button
        button_layout.addStretch()  # Add space after button

        # Create a label to display the calculation results
        self.result_label = QLabel("")

        # Create main vertical layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)  # Add graph at the top
        layout.addLayout(input_layout)  # Add input fields row
        layout.addLayout(button_layout)  # Add centered button
        layout.addWidget(self.result_label)  # Add result display

        # Set up central widget with the main layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def beregn(self):
        """Handle Calculate button click - get inputs, calculate results, and display them."""
        try:
            # Read and convert input values to integers
            a = int(self.input1.text())
            b = int(self.input2.text())
            c = int(self.input3.text())
            # Call the quadratic equation solver function
            result = reelle_loesninger_til_andengradsligning(a, b, c)
            
            # Plot the quadratic function
            self.plot_quadratic(a, b, c)
        except ValueError:
            # Handle case where inputs are not valid integers
            result = "Please enter valid integers for a, b, and c."
            # Clear the graph if invalid input
            self.ax.clear()
            self.canvas.draw()
        # Update the result label with the calculation result
        self.result_label.setText(result)
    
    def plot_quadratic(self, a, b, c):
        """Plot the quadratic function y = ax² + bx + c on the graph."""
        # Generate x values from -10 to 10
        x = np.linspace(-10, 10, 400)
        # Calculate corresponding y values using the quadratic formula
        y = a * x**2 + b * x + c
        
        # Clear previous plot
        self.ax.clear()
        # Plot the quadratic function
        self.ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a}x² + {b}x + {c}')
        
        # Find and plot the roots (x-intercepts) if they exist
        d = b**2 - 4*a*c  # Calculate discriminant
        if d > 0:
            # Plot two roots
            x_1 = (-b + math.sqrt(d)) / (2*a)
            x_2 = (-b - math.sqrt(d)) / (2*a)
            self.ax.plot([x_1, x_2], [0, 0], 'ro', markersize=8, label='Roots')  # Plot roots as red dots
        elif d == 0:
            # Plot single root
            x_root = (-b) / (2*a)
            self.ax.plot(x_root, 0, 'ro', markersize=8, label='Root')  # Plot root as red dot
        
        # Add axis lines
        self.ax.axhline(y=0, color='k', linewidth=0.5)  # Horizontal line at y=0
        self.ax.axvline(x=0, color='k', linewidth=0.5)  # Vertical line at x=0
        
        # Update graph labels and grid
        self.ax.set_title(f"Graph: y = {a}x² + {b}x + {c}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend()  # Show legend with function and roots
        
        # Redraw the canvas to display the updated graph
        self.canvas.draw()


# Application startup code
if __name__ == "__main__":
    # Create the main application object with command-line arguments
    andengradsligningsloeser = QApplication(sys.argv)
    
    # Create an instance of the main window
    vindue = HovedVindue()
    # Display the main window
    vindue.show()
    
    # Start the application event loop (runs until the window is closed)
    andengradsligningsloeser.exec()
