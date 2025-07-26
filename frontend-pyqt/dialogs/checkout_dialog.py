from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class CheckoutDialog(QDialog):
    """
    A dialog window to simulate a checkout process.
    It collects customer name and total amount.
    """
    def __init__(self, parent=None):
        """
        Initializes the CheckoutDialog.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Simulate Checkout")
        self.setFixedSize(400, 250) # Fixed size for the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
                border-radius: 10px;
            }
            QLabel {
                font-family: "Inter";
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: "Inter";
                font-size: 14px;
            }
            QLineEdit:focus, QDoubleSpinBox:focus {
                border: 1px solid #6200EE;
            }
            QPushButton {
                background-color: #6200EE;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                font-family: "Inter";
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
            QPushButton#cancelButton {
                background-color: #B0BEC5; /* Blue Grey */
            }
            QPushButton#cancelButton:hover {
                background-color: #78909C;
            }
        """)

        self._create_ui()

    def _create_ui(self):
        """
        Sets up the UI elements within the dialog.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("Enter Order Details")
        title_label.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Customer Name Input
        customer_layout = QHBoxLayout()
        customer_label = QLabel("Customer Name:")
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("e.g., John Doe")
        customer_layout.addWidget(customer_label)
        customer_layout.addWidget(self.customer_name_input)
        main_layout.addLayout(customer_layout)

        # Total Amount Input
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Total Amount:")
        self.total_amount_spinbox = QDoubleSpinBox()
        self.total_amount_spinbox.setPrefix("$")
        self.total_amount_spinbox.setRange(0.00, 99999.99)
        self.total_amount_spinbox.setSingleStep(10.00)
        self.total_amount_spinbox.setValue(100.00) # Default value
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.total_amount_spinbox)
        main_layout.addLayout(amount_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelButton") # For specific styling
        self.cancel_button.clicked.connect(self.reject) # Reject the dialog
        button_layout.addWidget(self.cancel_button)

        self.process_button = QPushButton("Process Order")
        self.process_button.clicked.connect(self._process_order)
        button_layout.addWidget(self.process_button)
        main_layout.addLayout(button_layout)

    def _process_order(self):
        """
        Validates input and accepts the dialog.
        In a real scenario, this would send data to the API client.
        """
        customer_name = self.customer_name_input.text().strip()
        total_amount = self.total_amount_spinbox.value()

        if not customer_name:
            QMessageBox.warning(self, "Input Error", "Customer name cannot be empty.")
            return
        if total_amount <= 0:
            QMessageBox.warning(self, "Input Error", "Total amount must be greater than zero.")
            return

        # In a real app, you would pass this data to your ApiClient
        # api_client = ApiClient()
        # response = api_client.process_checkout({"customer_name": customer_name, "total_amount": total_amount})
        # if response['status'] == 'success':
        #     self.accept() # Accept the dialog if successful
        # else:
        #     QMessageBox.critical(self, "Error", f"Failed to process order: {response.get('message', 'Unknown error')}")

        # For simulation, just accept the dialog
        self.accept()

    def get_order_details(self):
        """
        Returns the entered order details.
        """
        return {
            "customer_name": self.customer_name_input.text().strip(),
            "total_amount": self.total_amount_spinbox.value()
        }
