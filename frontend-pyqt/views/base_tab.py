from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class BaseTab(QWidget):
    """Base class for all tab widgets with common functionality"""
    
    status_message = pyqtSignal(str)  # Signal to update status bar
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Override in subclasses to setup UI"""
        raise NotImplementedError
        
    def connect_signals(self):
        """Override in subclasses to connect signals"""
        pass
        
    def refresh_data(self):
        """Override in subclasses to refresh data"""
        pass