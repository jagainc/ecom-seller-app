from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QDoubleSpinBox, QSpinBox, QTextEdit, QFormLayout,
    QMessageBox, QFileDialog
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from utils.validators import Validators, ValidationError

class ProductDialog(QDialog):
    """Dialog for adding/editing products"""
    
    product_saved = pyqtSignal(dict)  # Emits product data when saved
    
    def __init__(self, product_data=None, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.is_edit_mode = product_data is not None
        self.image_path = product_data.get('image_path', '') if product_data else ''
        
        self.setup_ui()
        self.setup_validation()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        title = "Edit Product" if self.is_edit_mode else "Add New Product"
        self.setWindowTitle(title)
        self.setFixedSize(500, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Product name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name...")
        form_layout.addRow("Product Name*:", self.name_input)
        
        # Price
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("$")
        self.price_input.setRange(0.01, 999999.99)
        self.price_input.setSingleStep(1.00)
        self.price_input.setDecimals(2)
        form_layout.addRow("Price*:", self.price_input)
        
        # Stock
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        self.stock_input.setSingleStep(1)
        form_layout.addRow("Stock Quantity*:", self.stock_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter product description...")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_input)
        
        # Image selection
        image_layout = QHBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                color: #666;
            }
        """)
        self.image_label.setMinimumHeight(80)
        
        self.select_image_btn = QPushButton("Select Image")
        self.select_image_btn.clicked.connect(self.select_image)
        
        image_layout.addWidget(self.image_label, 1)
        image_layout.addWidget(self.select_image_btn)
        form_layout.addRow("Product Image:", image_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Save Product")
        self.save_btn.clicked.connect(self.save_product)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #34C759;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #28A745;
            }
        """)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox, QTextEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
            }
            QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QTextEdit:focus {
                border: 2px solid #007AFF;
            }
            QLabel {
                font-weight: 500;
                color: #333;
            }
        """)
    
    def setup_validation(self):
        """Setup input validation"""
        self.name_input.textChanged.connect(self.validate_form)
        self.price_input.valueChanged.connect(self.validate_form)
        self.stock_input.valueChanged.connect(self.validate_form)
    
    def validate_form(self):
        """Validate form inputs and enable/disable save button"""
        name_valid, _ = Validators.validate_product_name(self.name_input.text())
        price_valid = self.price_input.value() > 0
        stock_valid = self.stock_input.value() >= 0
        
        self.save_btn.setEnabled(name_valid and price_valid and stock_valid)
    
    def populate_fields(self):
        """Populate fields with existing product data"""
        if self.product_data:
            self.name_input.setText(self.product_data.get('name', ''))
            self.price_input.setValue(self.product_data.get('price', 0.0))
            self.stock_input.setValue(self.product_data.get('stock', 0))
            self.description_input.setPlainText(self.product_data.get('description', ''))
            
            if self.image_path:
                self.update_image_preview()
    
    def select_image(self):
        """Open file dialog to select product image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Product Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_path:
            self.image_path = file_path
            self.update_image_preview()
    
    def update_image_preview(self):
        """Update image preview label"""
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                # Scale pixmap to fit label
                scaled_pixmap = pixmap.scaled(
                    60, 60,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")
            else:
                self.image_label.setText("Invalid image file")
        else:
            self.image_label.clear()
            self.image_label.setText("No image selected")
    
    def save_product(self):
        """Validate and save product data"""
        try:
            # Validate inputs
            name = self.name_input.text().strip()
            name_valid, error_msg = Validators.validate_product_name(name)
            if not name_valid:
                raise ValidationError(error_msg)
            
            price = self.price_input.value()
            if price <= 0:
                raise ValidationError("Price must be greater than 0")
            
            stock = self.stock_input.value()
            if stock < 0:
                raise ValidationError("Stock cannot be negative")
            
            # Create product data
            product_data = {
                'name': name,
                'price': price,
                'stock': stock,
                'description': self.description_input.toPlainText().strip(),
                'image_path': self.image_path
            }
            
            # Add ID if editing
            if self.is_edit_mode and self.product_data:
                product_data['id'] = self.product_data['id']
            
            # Emit signal and close dialog
            self.product_saved.emit(product_data)
            self.accept()
            
        except ValidationError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save product: {str(e)}")