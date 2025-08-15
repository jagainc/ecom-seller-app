import logging
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal

class ErrorHandler(QObject):
    """Centralized error handling for the application"""
    
    error_occurred = pyqtSignal(str, str)  # title, message
    
    def __init__(self):
        super().__init__()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_api_error(self, error: Exception, operation: str = "API operation"):
        """Handle API-related errors"""
        error_msg = f"Failed to {operation}: {str(error)}"
        self.logger.error(error_msg)
        self.error_occurred.emit("API Error", error_msg)
    
    def handle_validation_error(self, error: str, field: str = ""):
        """Handle validation errors"""
        error_msg = f"Validation error{f' in {field}' if field else ''}: {error}"
        self.logger.warning(error_msg)
        self.error_occurred.emit("Validation Error", error_msg)
    
    def handle_unexpected_error(self, error: Exception, context: str = ""):
        """Handle unexpected errors"""
        error_msg = f"Unexpected error{f' in {context}' if context else ''}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)
        self.error_occurred.emit("Unexpected Error", error_msg)
    
    def show_error_dialog(self, title: str, message: str, parent=None):
        """Show error dialog to user"""
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("QLabel{color: black;}")
        msg_box.exec()