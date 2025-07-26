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

        self.setFixedSize(320, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Product Image - This is where the product image is attached to the card
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(280, 350)  # Adjusted size for better fit in card
        self.image_label.setStyleSheet("""
            border: none;
            border-radius: 12px;
        """)
        
        pixmap = QPixmap(product_data.get('image_path', f"assets/images/product_{product_data['id']}.jpg"))
        if pixmap.isNull():
            self.image_label.setText("")
        else:
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Product Name (centered, bold)
        self.name_label = QLabel(product_data.get('name', 'Unknown Product'))
        self.name_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #3B1F1F; background: transparent;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Price and Add to Cart layout
        price_cart_layout = QHBoxLayout()
        price_cart_layout.setContentsMargins(0, 0, 0, 0)
        price_cart_layout.setSpacing(15)

        # Product Price (bold, dark)
        self.price_label = QLabel(f"${product_data.get('price', 0.00):.2f}")
        self.price_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.price_label.setStyleSheet("color: #3B1F1F; background: transparent;")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        price_cart_layout.addWidget(self.price_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add to Cart Button (white background, border, rounded corners)
        self.add_to_cart_button = QPushButton("ADD TO CART")
        self.add_to_cart_button.setFont(QFont("Inter", 10, QFont.Weight.DemiBold))
        self.add_to_cart_button.setFixedHeight(36)
        self.add_to_cart_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #3B1F1F;
                border: 1.5px solid #3B1F1F;
                border-radius: 8px;
                padding: 8px 20px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.add_to_cart_button.clicked.connect(self.emit_add_to_cart)
        price_cart_layout.addWidget(self.add_to_cart_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(price_cart_layout)

        layout.addStretch(1)

        # Card shadow and rounded corners
        self.setMouseTracking(True)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(20)
        self._shadow.setOffset(0, 4)
        self._shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(self._shadow)
        self._shadow.setEnabled(False)
        self._scale_anim = QPropertyAnimation(self, b"geometry")
        self._scale_anim.setDuration(200)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Set the initial style for the card background and rounded corners
        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: none;
            }
            QWidget:hover {
                background: white;
            }
        """)

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
        self.name_label.setStyleSheet("color: #3B1F1F; background: transparent;")
        self.price_label.setStyleSheet("color: #3B1F1F; background: transparent;")


