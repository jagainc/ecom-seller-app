import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from main_window import MainWindow
from utils.error_handler import ErrorHandler

class Application:
    """Main application class with proper initialization and error handling"""
    
    def __init__(self):
        self.app = None
        self.window = None
        self.error_handler = ErrorHandler()
        
    def setup_application(self):
        """Setup the QApplication with proper configuration"""
        self.app = QApplication(sys.argv)
        
        # Set application metadata
        self.app.setApplicationName("ECOM Seller Dashboard")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Your Company")
        
        # Enable high DPI scaling (Qt 6 handles this automatically)
        # These attributes are deprecated in Qt 6 and handled automatically
        # self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        # self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Set application icon if available
        icon_path = "assets/icons/app_icon.png"
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        
        # Font configuration
        self.setup_fonts()
        
        # Global stylesheet
        self.setup_global_styles()
        
    def setup_fonts(self):
        """Configure application fonts"""
        # Set font substitutions for better cross-platform compatibility
        QFont.insertSubstitution("Inter", "Segoe UI")  # Windows fallback
        QFont.insertSubstitution("Inter", "San Francisco")  # macOS fallback
        QFont.insertSubstitution("Inter", "Ubuntu")  # Linux fallback
        QFont.insertSubstitution("Inter", "Arial")  # Universal fallback
        
        # Set default application font
        default_font = QFont("Inter", 10)
        self.app.setFont(default_font)
        
    def setup_global_styles(self):
        """Setup global application styles"""
        global_style = """
        QMessageBox QLabel { 
            color: black; 
        }
        QToolTip {
            background-color: #2b2b2b;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px;
            font-size: 11px;
        }
        """
        self.app.setStyleSheet(global_style)
        
    def create_main_window(self):
        """Create and configure the main window"""
        try:
            self.window = MainWindow()
            
            # Connect error handler
            self.error_handler.error_occurred.connect(
                lambda title, msg: self.error_handler.show_error_dialog(title, msg, self.window)
            )
            
            # Center window on screen
            self.center_window()
            
            return True
        except Exception as e:
            self.error_handler.handle_unexpected_error(e, "main window creation")
            return False
            
    def center_window(self):
        """Center the main window on the screen"""
        if self.window:
            screen = self.app.primaryScreen().geometry()
            window_geometry = self.window.geometry()
            x = (screen.width() - window_geometry.width()) // 2
            y = (screen.height() - window_geometry.height()) // 2
            self.window.move(x, y)
    
    def run(self):
        """Run the application"""
        try:
            self.setup_application()
            
            if not self.create_main_window():
                return 1
                
            self.window.show()
            return self.app.exec()
            
        except Exception as e:
            logging.error(f"Critical error during application startup: {e}", exc_info=True)
            
            # Show critical error dialog
            if self.app:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Critical Error")
                msg.setText("A critical error occurred during application startup.")
                msg.setDetailedText(str(e))
                msg.exec()
            
            return 1

def main():
    """Main entry point"""
    app = Application()
    sys.exit(app.run())

if __name__ == "__main__":
    main()