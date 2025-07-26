from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPixmap, QColor

class ProductCard(QWidget):
    """
    A reusable PyQt widget to display a single product with its image, name,
    price, and an "Add to Cart" button, styled to resemble an e-commerce product listing.
    """
    # Define a signal that emits the product data and quantity when "Add to Cart" is clicked
    add_to_cart_requested = pyqtSignal(dict, int)

    def __init__(self, product_data):
        """
        Initializes the ProductCard.

        Args:
            product_data (dict): A dictionary containing product details
                                 (e.g., 'id', 'name', 'price', 'image_url' or 'image_path').
        """
        super().__init__()
        self.product_data = product_data
        self.quantity = 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Product Image - This is where the product image is attached to the card
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(260, 200)  # Increased size for bigger product image
        # Styling for image container: light background with rounded corners to match design
        self.image_label.setStyleSheet("""
            border: none; 
            background: #F8F8F8; 
            border-radius: 16px;
        """)
        # Load product image from product_data or default path
        pixmap = QPixmap(product_data.get('image_path', f"assets/images/product_{product_data['id']}.jpg"))
        if pixmap.isNull():
            self.image_label.setText("")
        else:
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Product Name (centered, smaller)
        self.name_label = QLabel(product_data.get('name', 'Unknown Product'))
        self.name_label.setFont(QFont("Inter", 11, QFont.Weight.DemiBold))  # Slightly larger and lighter weight for modern look
        self.name_label.setStyleSheet("color: #1C1C1E;")  # Darker text color for better contrast
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Brand (if available)
        brand = product_data.get('brand', '')
        if brand:
            self.brand_label = QLabel(brand)
            self.brand_label.setFont(QFont("Inter", 9))
            self.brand_label.setStyleSheet("color: #444;")  # Slightly darker for better readability
            self.brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.brand_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Product Price (centered, green)
        self.price_label = QLabel(f"Rs {product_data.get('price', 0.00):.0f}")
        self.price_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))  # Slightly larger font for emphasis
        self.price_label.setStyleSheet("color: #1BA94C; margin-top: 4px;")  # Green color with margin for spacing
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.price_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Quantity controls
        qty_layout = QHBoxLayout()
        qty_layout.setSpacing(8)  # More spacing for better balance
        self.minus_btn = QPushButton("−")
        self.minus_btn.setFixedWidth(30)
        self.minus_btn.setStyleSheet("""
            background: #F2F2F2; 
            border: none; 
            font-size: 18px; 
            color: black;
            border-radius: 4px;
            min-height: 28px;
            min-width: 28px;
            """)  # Rounded buttons with subtle styling
        self.minus_btn.clicked.connect(self.decrease_qty)
        qty_layout.addWidget(self.minus_btn)

        self.qty_label = QLabel(str(self.quantity))
        self.qty_label.setFixedWidth(28)
        self.qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qty_label.setStyleSheet("color: black; font-weight: 700; font-size: 16px;")  # Bolder and larger for emphasis
        qty_layout.addWidget(self.qty_label)

        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedWidth(30)
        self.plus_btn.setStyleSheet("""
            background: #F2F2F2; 
            border: none; 
            font-size: 18px; 
            color: black;
            border-radius: 4px;
            min-height: 28px;
            min-width: 28px;
            """)  # Rounded buttons with subtle styling
        self.plus_btn.clicked.connect(self.increase_qty)
        qty_layout.addWidget(self.plus_btn)

        layout.addLayout(qty_layout)

        # Add to Cart Button
        self.add_to_cart_button = QPushButton("Add to Cart")
        self.add_to_cart_button.setFont(QFont("Inter", 9, QFont.Weight.DemiBold))  # Smaller font size
        self.add_to_cart_button.setFixedHeight(28)  # Smaller height for compact button
        self.add_to_cart_button.setStyleSheet("""
            QPushButton {
                background-color: #1BA94C;
                color: white;
                padding: 4px 12px;
                border-radius: 6px;
                border: none;
                min-width: 100px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #168C3B;
            }
        """)
        layout.addWidget(self.add_to_cart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.add_to_cart_button.clicked.connect(self.emit_add_to_cart)

        layout.addStretch(1)

        # Card shadow and rounded corners
        self.setMouseTracking(True)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(18)
        self._shadow.setOffset(0, 2)
        self._shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(self._shadow)
        self._shadow.setEnabled(False)
        self._scale_anim = QPropertyAnimation(self, b"geometry")
        self._scale_anim.setDuration(160)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Set the initial style (no blue border, subtle box look)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border-radius: 0;
                border: none;
            }
            QWidget:hover {
                background: transparent;
            }
        """)

    def increase_qty(self):
        """
        Increases the quantity by 1 and updates the quantity label.
        """
        self.quantity += 1
        self.qty_label.setText(str(self.quantity))

    def decrease_qty(self):
        """
        Decreases the quantity by 1 (minimum 1) and updates the quantity label.
        """
        if self.quantity > 1:
            self.quantity -= 1
            self.qty_label.setText(str(self.quantity))

    def emit_add_to_cart(self):
        """
        Emits the add_to_cart_requested signal with the product data and current quantity.
        """
        self.add_to_cart_requested.emit(self.product_data, self.quantity)

    def enterEvent(self, event):
        # Enable shadow and animate scale up
        self._shadow.setEnabled(True)
        rect = self.geometry()
        self._scale_anim.stop()
        self._scale_anim.setStartValue(rect)
        self._scale_anim.setEndValue(QRect(rect.x()-4, rect.y()-4, rect.width()+8, rect.height()+8))
        self._scale_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Disable shadow and animate scale down
        rect = self.geometry()
        self._scale_anim.stop()
        self._scale_anim.setStartValue(rect)
        self._scale_anim.setEndValue(QRect(rect.x()+4, rect.y()+4, rect.width()-8, rect.height()-8))
        self._scale_anim.start()
        self._shadow.setEnabled(False)
        super().leaveEvent(event)

