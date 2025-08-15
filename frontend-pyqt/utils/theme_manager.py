from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict

class ThemeManager(QObject):
    """Manages application themes and styling"""
    
    theme_changed = pyqtSignal(str)  # Emits theme name when changed
    
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.themes = {
            "light": self._light_theme(),
            "dark": self._dark_theme()
        }
    
    def _light_theme(self) -> Dict[str, str]:
        """Light theme color palette"""
        return {
            "primary_bg": "#F2F2F7",
            "secondary_bg": "#FFFFFF",
            "card_bg": "#FFFFFF",
            "primary_text": "#1C1C1E",
            "secondary_text": "#636366",
            "tertiary_text": "#8E8E93",
            "accent_blue": "#007AFF",
            "accent_green": "#34C759",
            "accent_red": "#FF3B30",
            "accent_orange": "#FF9500",
            "border_light": "#E5E5EA",
            "border_medium": "#D1D1D6",
            "hover_bg": "#E8F0FE",
            "shadow": "rgba(0, 0, 0, 0.1)",
            "input_bg": "#FFFFFF",
            "button_bg": "#E5E5EA",
            "button_text": "#1C1C1E",
            # Table-specific colors
            "table_header_bg": "#F2F2F7",
            "table_header_text": "#636366",
            "table_selection": "#007AFF",
            "table_selection_text": "#FFFFFF",
            "table_hover": "#F8F8F8",
            "table_alternate": "#FAFAFA"
        }
    
    def _dark_theme(self) -> Dict[str, str]:
        """Dark theme color palette"""
        return {
            "primary_bg": "#1C1C1E",
            "secondary_bg": "#2C2C2E",
            "card_bg": "#2C2C2E",
            "primary_text": "#FFFFFF",
            "secondary_text": "#8E8E93",
            "tertiary_text": "#636366",
            "accent_blue": "#0A84FF",
            "accent_green": "#30D158",
            "accent_red": "#FF453A",
            "accent_orange": "#FF9F0A",
            "border_light": "#38383A",
            "border_medium": "#48484A",
            "hover_bg": "#3A3A3C",
            "shadow": "rgba(0, 0, 0, 0.3)",
            "input_bg": "#2C2C2E",
            "button_bg": "#3A3A3C",
            "button_text": "#FFFFFF",
            # Table-specific colors (Apple dark mode style)
            "table_header_bg": "#1C1C1E",
            "table_header_text": "#8E8E93",
            "table_selection": "#0A84FF",
            "table_selection_text": "#FFFFFF",
            "table_hover": "#3A3A3C",
            "table_alternate": "#2A2A2C"
        }
    
    def get_current_theme(self) -> Dict[str, str]:
        """Get current theme colors"""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.theme_changed.emit(theme_name)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(new_theme)
    
    def get_complete_stylesheet(self) -> str:
        """Get complete application stylesheet for current theme"""
        colors = self.get_current_theme()
        
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {colors['primary_bg']};
            color: {colors['primary_text']};
        }}
        
        /* General Widget Styling */
        QWidget {{
            background-color: {colors['primary_bg']};
            color: {colors['primary_text']};
        }}
        
        /* Labels */
        QLabel {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        /* Specific label styles */
        QLabel#main_title {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        QLabel#section_title {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        QLabel#cart_summary {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        QLabel#placeholder_text {{
            color: {colors['secondary_text']};
            background: transparent;
        }}
        
        QLabel#checkout_title {{
            color: {colors['accent_green']};
            background: transparent;
        }}
        
        QLabel#cart_total {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        /* Checkout Panel */
        QWidget#checkout_panel {{
            background-color: {colors['secondary_bg']};
            border: 1px solid {colors['border_light']};
            border-radius: 12px;
        }}
        
        /* Cart Item Styles */
        QLabel#cart_item_info {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        QLabel#cart_qty_label {{
            color: {colors['primary_text']};
            background: transparent;
            font-weight: bold;
        }}
        
        QPushButton#cart_qty_btn {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
            border: none;
            font-size: 15px;
            border-radius: 4px;
        }}
        
        QPushButton#cart_qty_btn:hover {{
            background-color: {colors['hover_bg']};
        }}
        
        /* Enhanced Cart Item Styles */
        QWidget#cart_item_card {{
            background-color: {colors['card_bg']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            margin: 2px;
        }}
        
        QLabel#cart_item_name {{
            color: {colors['primary_text']};
            font-weight: bold;
        }}
        
        QLabel#cart_item_price {{
            color: {colors['secondary_text']};
        }}
        
        QLabel#cart_item_total {{
            color: {colors['accent_green']};
            font-weight: bold;
        }}
        
        QLabel#qty_label {{
            color: {colors['secondary_text']};
        }}
        
        QLabel#cart_qty_display {{
            color: {colors['primary_text']};
            background-color: {colors['button_bg']};
            border: 1px solid {colors['border_light']};
            border-radius: 4px;
            padding: 2px;
        }}
        
        QPushButton#remove_btn {{
            background-color: transparent;
            border: none;
            color: {colors['accent_red']};
            border-radius: 12px;
        }}
        
        QPushButton#remove_btn:hover {{
            background-color: {colors['accent_red']};
            color: white;
        }}
        
        QPushButton#close_btn {{
            background-color: transparent;
            border: none;
            font-size: 16px;
            font-weight: bold;
            border-radius: 16px;
            color: {colors['secondary_text']};
        }}
        
        QPushButton#close_btn:hover {{
            background-color: {colors['accent_red']};
            color: white;
        }}
        
        /* Section Labels */
        QLabel#section_label {{
            color: {colors['primary_text']};
            font-weight: bold;
            margin-top: 8px;
        }}
        
        /* Summary Text */
        QLabel#summary_text {{
            color: {colors['secondary_text']};
        }}
        
        QLabel#discount_text {{
            color: {colors['accent_green']};
        }}
        
        QLabel#empty_cart_label {{
            color: {colors['tertiary_text']};
        }}
        
        /* Coupon Input */
        QLineEdit#coupon_input {{
            background-color: {colors['input_bg']};
            color: {colors['primary_text']};
            border: 1px solid {colors['border_light']};
            border-radius: 6px;
            padding: 8px;
        }}
        
        QLineEdit#coupon_input:focus {{
            border: 2px solid {colors['accent_blue']};
        }}
        
        QLabel#coupon_status {{
            font-style: italic;
        }}
        
        /* Separator */
        QFrame#separator {{
            color: {colors['border_light']};
        }}
        
        /* Scroll Area */
        QScrollArea#cart_scroll {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollArea#cart_scroll QScrollBar:vertical {{
            background-color: {colors['button_bg']};
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollArea#cart_scroll QScrollBar::handle:vertical {{
            background-color: {colors['border_medium']};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollArea#cart_scroll QScrollBar::handle:vertical:hover {{
            background-color: {colors['secondary_text']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {colors['border_light']};
            background: {colors['secondary_bg']};
            border-radius: 12px;
            padding: 10px;
        }}
        
        QTabBar::tab {{
            background: {colors['button_bg']};
            color: {colors['secondary_text']};
            padding: 10px 20px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            margin-right: 2px;
            font-family: "Inter";
            font-size: 14px;
            font-weight: 600;
        }}
        
        QTabBar::tab:selected {{
            background: {colors['secondary_bg']};
            color: {colors['accent_blue']};
        }}
        
        QTabBar::tab:hover {{
            background: {colors['hover_bg']};
        }}
        
        /* Apple-style Tables */
        QTableWidget {{
            background-color: {colors['secondary_bg']};
            color: {colors['primary_text']};
            gridline-color: {colors['border_light']};
            border: 1px solid {colors['border_light']};
            border-radius: 12px;
            selection-background-color: {colors['accent_blue']};
            alternate-background-color: {colors['table_alternate']};
        }}
        
        QTableWidget#data_table {{
            background-color: {colors['secondary_bg']};
            color: {colors['primary_text']};
            gridline-color: {colors['border_light']};
            border: 1px solid {colors['border_light']};
            border-radius: 12px;
            font-family: "Inter";
            font-size: 13px;
        }}
        
        QHeaderView::section {{
            background-color: {colors['table_header_bg']};
            color: {colors['table_header_text']};
            padding: 12px 10px;
            border: none;
            border-bottom: 1px solid {colors['border_light']};
            border-right: 1px solid {colors['border_light']};
            font-family: "Inter";
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QHeaderView::section:first {{
            border-top-left-radius: 12px;
        }}
        
        QHeaderView::section:last {{
            border-top-right-radius: 12px;
            border-right: none;
        }}
        
        QTableWidget::item {{
            padding: 12px 10px;
            font-family: "Inter";
            font-size: 13px;
            color: {colors['primary_text']};
            border-bottom: 1px solid {colors['border_light']};
            background-color: transparent;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['table_selection']};
            color: {colors['table_selection_text']};
        }}
        
        QTableWidget::item:hover {{
            background-color: {colors['table_hover']};
        }}
        
        QTableWidget::item:alternate {{
            background-color: {colors['table_alternate']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
        }}
        
        QPushButton:hover {{
            background-color: {colors['hover_bg']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['border_medium']};
        }}
        
        /* Primary Buttons */
        QPushButton[class="primary"] {{
            background-color: {colors['accent_blue']};
            color: white;
        }}
        
        QPushButton[class="primary"]:hover {{
            background-color: {colors['accent_blue']}CC;
        }}
        
        /* Success Buttons */
        QPushButton[class="success"] {{
            background-color: {colors['accent_green']};
            color: white;
        }}
        
        QPushButton[class="success"]:hover {{
            background-color: {colors['accent_green']}CC;
        }}
        
        /* Danger Buttons */
        QPushButton[class="danger"] {{
            background-color: {colors['accent_red']};
            color: white;
        }}
        
        QPushButton[class="danger"]:hover {{
            background-color: {colors['accent_red']}CC;
        }}
        
        /* Input Fields */
        QLineEdit {{
            background-color: {colors['input_bg']};
            color: {colors['primary_text']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            padding: 10px;
            font-family: "Inter";
            font-size: 13px;
        }}
        
        QLineEdit:focus {{
            border: 1px solid {colors['accent_blue']};
        }}
        
        /* Spin Boxes */
        QSpinBox, QDoubleSpinBox {{
            background-color: {colors['input_bg']};
            color: {colors['primary_text']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 1px solid {colors['accent_blue']};
        }}
        
        /* Scroll Areas */
        QScrollArea {{
            border: none;
            background-color: {colors['primary_bg']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {colors['button_bg']};
            border-top: 1px solid {colors['border_light']};
            color: {colors['secondary_text']};
        }}
        
        /* Frames */
        QFrame {{
            background-color: {colors['secondary_bg']};
            border: 1px solid {colors['border_light']};
            border-radius: 12px;
        }}
        
        /* Message Boxes */
        QMessageBox {{
            background-color: {colors['secondary_bg']};
            color: {colors['primary_text']};
        }}
        
        QMessageBox QLabel {{
            color: {colors['primary_text']};
        }}
        """
    
    def get_product_card_stylesheet(self) -> str:
        """Get stylesheet specifically for product cards"""
        colors = self.get_current_theme()
        
        return f"""
        QWidget {{
            background: {colors['card_bg']};
            border-radius: 16px;
            border: none;
        }}
        
        QWidget:hover {{
            background: {colors['card_bg']};
        }}
        
        QLabel {{
            color: {colors['primary_text']};
            background: transparent;
        }}
        
        QPushButton {{
            background-color: {colors['card_bg']};
            color: {colors['primary_text']};
            border: 1.5px solid {colors['primary_text']};
            border-radius: 8px;
            padding: 8px 20px;
            letter-spacing: 1px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {colors['hover_bg']};
        }}
        """

# Global theme manager instance
theme_manager = ThemeManager()