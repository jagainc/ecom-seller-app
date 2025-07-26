import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# We import the MainWindow class from your main UI file.
# For this to work, the file containing the MainWindow class
# should be saved as 'main_window.py' in the same directory.
from main_window import MainWindow

def main():
    """
    The main function that initializes and runs the PyQt application.
    """
    # Create the application instance
    app = QApplication(sys.argv)

    # Set a default font substitution for a more modern look.
    # This attempts to use 'Inter', and falls back to 'Arial' if not found.
    QFont.insertSubstitution("Inter", "Arial")

    # Set global stylesheet for QMessageBox text color to black
    app.setStyleSheet("QMessageBox QLabel { color: black; }")

    # Create an instance of our main window
    window = MainWindow()
    
    # Show the main window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    # This ensures the main function is called only when the script is executed directly
    main()
# This is the entry point of the PyQt application.