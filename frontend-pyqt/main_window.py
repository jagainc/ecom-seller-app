import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTabWidget, QScrollArea, QFrame, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QGridLayout, QDockWidget, QListWidget, QListWidgetItem, QSpinBox, QAbstractItemView
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QRect, QEasingCurve

# Import custom components and services
from components.stat_card import StatCard
from components.product_card import ProductCard # New import
from dialogs.checkout_dialog import CheckoutDialog
from services.api_client import ApiClient

class MainWindow(QMainWindow):
    """
    The main application window for the ECOM Seller App.
    This window displays a dashboard with various sections for products, orders,
    and sales analytics, fetching data from a backend API.
    """
    def __init__(self):
        """
        Initializes the MainWindow, sets up the UI, and connects to the API.
        """
        super().__init__()
        self.setWindowTitle("ECOM Seller Dashboard")
        self.setGeometry(100, 100, 1200, 800) # Initial window size and position
        self.setStyleSheet("background-color: #F2F2F7;") # Apple Light Theme background

        self.api_client = ApiClient() # Initialize API client
        self.cart_items = {} # In-memory cart: {product_id: {'product': product_data, 'quantity': count}}
        self.checkout_panel = None  # Add this line

        self._create_ui() # Setup the user interface
        self._load_dashboard_data() # Load initial data for the dashboard

    def _create_ui(self):
        """
        Sets up the main user interface components of the window.
        This includes a central widget, a tab widget for different sections,
        and a status bar.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25) # Increased margins
        main_layout.setSpacing(20) # Increased spacing

        # Application Title and Dark Mode Toggle
        header_layout = QHBoxLayout()
        title_label = QLabel("ECOM Seller Dashboard")
        title_label.setFont(QFont("Inter", 26, QFont.Weight.Bold)) # Slightly larger font
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft) # Align left for modern feel
        title_label.setStyleSheet("color: #1C1C1E; margin-bottom: 25px;") # Darker text for contrast
        header_layout.addWidget(title_label)

        # Dark Mode Toggle Button
        self.dark_mode_toggle = QPushButton("☀️")
        self.dark_mode_toggle.setCheckable(True)
        self.dark_mode_toggle.setFixedSize(40, 40)
        self.dark_mode_toggle.setStyleSheet("""
            QPushButton {
                background-color: #E5E5EA;
                border-radius: 20px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:checked {
                background-color: #1C1C1E;
            }
        """)
        self.dark_mode_toggle.clicked.connect(self._toggle_dark_mode)
        header_layout.addStretch(1)
        header_layout.addWidget(self.dark_mode_toggle)

        main_layout.addLayout(header_layout)

        # Tab Widget for different sections (Shop, Dashboard, Products, Orders)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self._light_mode_tab_style())
        main_layout.addWidget(self.tab_widget)

        # Shift Shop tab to be first
        self._setup_shop_tab()
        self._setup_dashboard_tab()
        self._setup_products_tab()
        self._setup_orders_tab()

        # Status Bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("background-color: #E5E5EA; border-top: 1px solid #D1D1D6; color: #636366;") # Lighter status bar

    def _setup_dashboard_tab(self):
        """
        Sets up the 'Dashboard' tab with only a chart section (no KPI blocks or icons).
        """
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.setContentsMargins(25, 25, 25, 25)
        dashboard_layout.setSpacing(25)

        # Chart Section Only
        chart_label = QLabel("Sales Trends & Analytics")
        chart_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        chart_label.setStyleSheet("color: #1C1C1E; margin-top: 30px;")
        dashboard_layout.addWidget(chart_label)

        chart_frame = QFrame()
        chart_frame.setFrameShape(QFrame.Shape.StyledPanel)
        chart_frame.setFrameShadow(QFrame.Shadow.Raised)
        chart_frame.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E5E5EA; border-radius: 12px; padding: 20px;")
        chart_layout = QVBoxLayout(chart_frame)
        chart_placeholder = QLabel("Imagine beautiful sales charts here (e.g., daily sales, product categories, customer demographics). This data would be fetched from the backend's ChartGenerationService.")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setWordWrap(True)
        chart_placeholder.setFont(QFont("Inter", 12))
        chart_placeholder.setStyleSheet("color: #8E8E93;")
        chart_layout.addWidget(chart_placeholder)
        dashboard_layout.addWidget(chart_frame)

        dashboard_layout.addStretch(1)

        self.tab_widget.addTab(dashboard_widget, "Dashboard")

    def _setup_products_tab(self):
        """
        Sets up the 'Products' tab, allowing sellers to view and manage products.
        """
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        products_layout.setContentsMargins(25, 25, 25, 25) # Increased margins
        products_layout.setSpacing(20) # Increased spacing

        products_label = QLabel("Product Management")
        products_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        products_label.setStyleSheet("color: #1C1C1E;")
        products_layout.addWidget(products_label)

        # Product search and add section
        search_add_layout = QHBoxLayout()
        self.product_search_input = QLineEdit()
        self.product_search_input.setPlaceholderText("Search products...")
        self.product_search_input.setFont(QFont("Inter", 13)) # Slightly larger font
        self.product_search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; /* More padding */
                border: 1px solid #D1D1D6; /* Lighter border */
                border-radius: 8px; /* More rounded */
                background-color: #FFFFFF;
                color: #1C1C1E;
            }
            QLineEdit:focus {
                border: 1px solid #007AFF; /* Apple Blue focus */
            }
        """)
        self.product_search_input.returnPressed.connect(self._search_products)
        search_add_layout.addWidget(self.product_search_input)

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF; /* Apple Blue */
                color: white;
                padding: 10px 20px; /* More padding */
                border-radius: 8px; /* More rounded */
                border: none;
            }
            QPushButton:hover {
                background-color: #005BBF; /* Darker blue on hover */
            }
        """)
        search_button.clicked.connect(self._search_products)
        search_add_layout.addWidget(search_button)

        add_product_button = QPushButton("Add New Product")
        add_product_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        add_product_button.setStyleSheet("""
            QPushButton {
                background-color: #34C759; /* Apple Green accent */
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #28A745;
            }
        """)
        add_product_button.clicked.connect(self._add_product)
        search_add_layout.addWidget(add_product_button)
        products_layout.addLayout(search_add_layout)

        # Product table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Actions"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.product_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E5EA; /* Lighter border */
                border-radius: 12px; /* More curved edges */
                gridline-color: #E5E5EA; /* Lighter grid lines */
                background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #F2F2F7; /* Light gray header background */
                padding: 10px; /* More padding */
                border-bottom: 1px solid #D1D1D6; /* Lighter border */
                font-family: "Inter";
                font-size: 14px; /* Slightly larger */
                font-weight: bold;
                color: #636366; /* Medium gray text */
            }
            QTableWidget::item {
                padding: 10px; /* More padding */
                font-family: "Inter";
                font-size: 13px; /* Slightly larger */
                color: #1C1C1E;
            }
            QTableWidget::item:selected {
                background-color: #E8F0FE; /* Very light blue for selection */
                color: #1C1C1E;
            }
        """)
        products_layout.addWidget(self.product_table)

        self.tab_widget.addTab(products_widget, "Products")

        self._load_products() # Load products when tab is set up

    def _setup_orders_tab(self):
        """
        Sets up the 'Orders' tab, allowing sellers to view and manage orders.
        """
        orders_widget = QWidget()
        orders_layout = QVBoxLayout(orders_widget)
        orders_layout.setContentsMargins(25, 25, 25, 25) # Increased margins
        orders_layout.setSpacing(20) # Increased spacing

        orders_label = QLabel("Order Management")
        orders_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        orders_label.setStyleSheet("color: #1C1C1E;")
        orders_layout.addWidget(orders_label)

        # Order search and checkout button
        order_controls_layout = QHBoxLayout()
        self.order_search_input = QLineEdit()
        self.order_search_input.setPlaceholderText("Search orders...")
        self.order_search_input.setFont(QFont("Inter", 13))
        self.order_search_input.setStyleSheet(self.product_search_input.styleSheet()) # Reuse style
        self.order_search_input.returnPressed.connect(self._search_orders)
        order_controls_layout.addWidget(self.order_search_input)

        search_order_button = QPushButton("Search")
        search_order_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        search_order_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF; /* Apple Blue */
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #005BBF;
            }
        """)
        search_order_button.clicked.connect(self._search_orders)
        order_controls_layout.addWidget(search_order_button)

        # Example button to open a checkout dialog
        open_checkout_button = QPushButton("Simulate Checkout")
        open_checkout_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        open_checkout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9500; /* Apple Orange accent */
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #CC7700;
            }
        """)
        open_checkout_button.clicked.connect(self._open_checkout_dialog)
        order_controls_layout.addWidget(open_checkout_button)
        orders_layout.addLayout(order_controls_layout)

        # Order table
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Order ID", "Customer", "Total", "Status", "Date"])
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.order_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E5E5EA; /* Lighter border */
                border-radius: 12px; /* More curved edges */
                gridline-color: #E5E5EA; /* Lighter grid lines */
                background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #F2F2F7; /* Light gray header background */
                padding: 10px; /* More padding */
                border-bottom: 1px solid #D1D1D6; /* Lighter border */
                font-family: "Inter";
                font-size: 14px; /* Slightly larger */
                font-weight: bold;
                color: #636366; /* Medium gray text */
            }
            QTableWidget::item {
                padding: 10px; /* More padding */
                font-family: "Inter";
                font-size: 13px; /* Slightly larger */
                color: #1C1C1E;
            }
            QTableWidget::item:selected {
                background-color: #E8F0FE; /* Very light blue for selection */
                color: #1C1C1E;
            }
        """)
        orders_layout.addWidget(self.order_table)

        self.tab_widget.addTab(orders_widget, "Orders")

        self._load_orders() # Load orders when tab is set up

    def _setup_shop_tab(self):
        """
        Sets up the new 'Shop' tab for browsing products and adding to cart.
        """
        shop_widget = QWidget()
        shop_layout = QVBoxLayout(shop_widget)
        shop_layout.setContentsMargins(25, 25, 25, 25)
        shop_layout.setSpacing(20)

        shop_header_layout = QHBoxLayout()
        shop_label = QLabel("Product Catalog")
        shop_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        shop_label.setStyleSheet("color: #1C1C1E;")
        shop_header_layout.addWidget(shop_label)
        shop_header_layout.addStretch(1)

        # Cart Summary and Checkout Button
        self.cart_summary_label = QLabel("Cart: 0 items (Rs 0.00)")
        self.cart_summary_label.setFont(QFont("Inter", 14, QFont.Weight.DemiBold))
        self.cart_summary_label.setStyleSheet("color: #1C1C1E;")
        shop_header_layout.addWidget(self.cart_summary_label)

        self.go_to_checkout_button = QPushButton("Go to Checkout")
        self.go_to_checkout_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        self.go_to_checkout_button.setStyleSheet("""
            QPushButton {
                background-color: #34C759; /* Apple Green */
                color: white;
                padding: 8px 15px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #28A745;
            }
        """)
        self.go_to_checkout_button.clicked.connect(self._toggle_checkout_panel)
        shop_header_layout.addWidget(self.go_to_checkout_button)
        shop_layout.addLayout(shop_header_layout)

        # Product Grid
        self.product_grid_layout = QGridLayout()
        self.product_grid_layout.setSpacing(40) # Increased spacing between product cards

        self.product_scroll_area = QScrollArea()
        self.product_scroll_area.setWidgetResizable(True)
        self.product_scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        products_container = QWidget()
        products_container.setLayout(self.product_grid_layout)
        self.product_scroll_area.setWidget(products_container)
        
        shop_layout.addWidget(self.product_scroll_area)
        
        self.tab_widget.addTab(shop_widget, "Shop")

        self._load_shop_products() # Load products for the shop tab

    def _load_dashboard_data(self):
        """
        Fetches dashboard data (KPIs) from the API and updates the StatCards.
        This function is now a no-op since KPI cards have been removed.
        """
        self.statusBar().showMessage("Dashboard data loaded (no KPIs to update).")
        # No KPI cards to update, so nothing else is needed.

    def _load_products(self):
        """
        Fetches product data from the API and populates the product table.
        """
        self.statusBar().showMessage("Loading products...")
        try:
            products = self.api_client.get_products()
            self.product_table.setRowCount(len(products))
            for row_idx, product in enumerate(products):
                self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product['id'])))
                self.product_table.setItem(row_idx, 1, QTableWidgetItem(product['name']))
                self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${product['price']:.2f}"))
                self.product_table.setItem(row_idx, 3, QTableWidgetItem(str(product['stock'])))
                # Add action buttons (e.g., Edit, Delete) - placeholder for now
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                edit_button = QPushButton("Edit")
                edit_button.setFont(QFont("Inter", 11)) # Slightly larger font
                edit_button.setStyleSheet("""
                    background-color: #34C759; /* Apple Green */
                    color: white;
                    border-radius: 5px;
                    padding: 5px 12px;
                """) # Green, more padding, rounded
                edit_button.clicked.connect(lambda _, p_id=product['id']: self._edit_product(p_id))
                delete_button = QPushButton("Delete")
                delete_button.setFont(QFont("Inter", 11)) # Slightly larger font
                delete_button.setStyleSheet("""
                    background-color: #FF3B30; /* Apple Red */
                    color: white;
                    border-radius: 5px;
                    padding: 5px 12px;
                """) # Red, more padding, rounded
                delete_button.clicked.connect(lambda _, p_id=product['id']: self._delete_product(p_id))
                action_layout.addWidget(edit_button)
                action_layout.addWidget(delete_button)
                action_layout.addStretch(1)
                self.product_table.setCellWidget(row_idx, 4, action_widget)
            self.statusBar().showMessage(f"Loaded {len(products)} products.")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")

    def _search_products(self):
        """
        Searches for products based on the input text.
        In a real app, this would call a backend API search endpoint.
        For now, it filters the simulated data.
        """
        search_text = self.product_search_input.text().lower()
        self.statusBar().showMessage(f"Searching for products: '{search_text}'...")
        try:
            all_products = self.api_client.get_products() # Get all simulated products
            filtered_products = [
                p for p in all_products
                if search_text in p['name'].lower() or search_text in str(p['id'])
            ]
            self.product_table.setRowCount(0) # Clear existing rows
            for row_idx, product in enumerate(filtered_products):
                self.product_table.insertRow(row_idx)
                self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product['id'])))
                self.product_table.setItem(row_idx, 1, QTableWidgetItem(product['name']))
                self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${product['price']:.2f}"))
                self.product_table.setItem(row_idx, 3, QTableWidgetItem(str(product['stock'])))
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                edit_button = QPushButton("Edit")
                edit_button.setFont(QFont("Inter", 11))
                edit_button.setStyleSheet("background-color: #007AFF; color: white; border-radius: 5px; padding: 5px 10px;")
                edit_button.clicked.connect(lambda _, p_id=product['id']: self._edit_product(p_id))
                delete_button = QPushButton("Delete")
                delete_button.setFont(QFont("Inter", 11))
                delete_button.setStyleSheet("background-color: #FF3B30; color: white; border-radius: 5px; padding: 5px 10px;")
                delete_button.clicked.connect(lambda _, p_id=product['id']: self._delete_product(p_id))
                action_layout.addWidget(edit_button)
                action_layout.addWidget(delete_button)
                action_layout.addStretch(1)
                self.product_table.setCellWidget(row_idx, 4, action_widget)
            self.statusBar().showMessage(f"Found {len(filtered_products)} products.")
        except Exception as e:
            self.statusBar().showMessage(f"Error searching products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to search products: {e}")

    def _add_product(self):
        """
        Simulates adding a new product. In a real app, this would open a form
        dialog and then call the API client to send data to the backend.
        """
        QMessageBox.information(self, "Add Product", "This would open a dialog to add a new product.")
        # After adding, reload products:
        self._load_products()

    def _edit_product(self, product_id):
        """
        Simulates editing an existing product.
        """
        QMessageBox.information(self, "Edit Product", f"This would open a dialog to edit product ID: {product_id}")
        # After editing, reload products:
        self._load_products()

    def _delete_product(self, product_id):
        """
        Simulates deleting a product.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Delete Product')
        msg_box.setText(f"Are you sure you want to delete product ID: {product_id}?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet("QLabel{color: black;} QPushButton{min-width: 80px;}")
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage(f"Deleting product ID: {product_id}...")
            try:
                # In a real app, call self.api_client.delete_product(product_id)
                QMessageBox.information(self, "Delete Product", f"Product ID {product_id} deleted (simulated).")
                self.statusBar().showMessage(f"Product ID {product_id} deleted.")
                self._load_products() # Refresh the list
            except Exception as e:
                self.statusBar().showMessage(f"Error deleting product: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete product: {e}")


    def _load_orders(self):
        """
        Fetches order data from the API and populates the order table.
        """
        self.statusBar().showMessage("Loading orders...")
        try:
            orders = self.api_client.get_orders()
            self.order_table.setRowCount(len(orders))
            for row_idx, order in enumerate(orders):
                self.order_table.setItem(row_idx, 0, QTableWidgetItem(str(order['id'])))
                self.order_table.setItem(row_idx, 1, QTableWidgetItem(order['customer_name']))
                self.order_table.setItem(row_idx, 2, QTableWidgetItem(f"${order['total_amount']:.2f}"))
                self.order_table.setItem(row_idx, 3, QTableWidgetItem(order['status']))
                self.order_table.setItem(row_idx, 4, QTableWidgetItem(order['order_date']))
            self.statusBar().showMessage(f"Loaded {len(orders)} orders.")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading orders: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load orders: {e}")

    def _search_orders(self):
        """
        Searches for orders based on the input text.
        In a real app, this would call a backend API search endpoint.
        For now, it filters the simulated data.
        """
        search_text = self.order_search_input.text().lower()
        self.statusBar().showMessage(f"Searching for orders: '{search_text}'...")
        try:
            all_orders = self.api_client.get_orders() # Get all simulated orders
            filtered_orders = [
                o for o in all_orders
                if search_text in o['customer_name'].lower() or search_text in str(o['id']) or search_text in o['status'].lower()
            ]
            self.order_table.setRowCount(0) # Clear existing rows
            for row_idx, order in enumerate(filtered_orders):
                self.order_table.insertRow(row_idx)
                self.order_table.setItem(row_idx, 0, QTableWidgetItem(str(order['id'])))
                self.order_table.setItem(row_idx, 1, QTableWidgetItem(order['customer_name']))
                self.order_table.setItem(row_idx, 2, QTableWidgetItem(f"${order['total_amount']:.2f}"))
                self.order_table.setItem(row_idx, 3, QTableWidgetItem(order['status']))
                self.order_table.setItem(row_idx, 4, QTableWidgetItem(order['order_date']))
            self.statusBar().showMessage(f"Found {len(filtered_orders)} orders.")
        except Exception as e:
            self.statusBar().showMessage(f"Error searching orders: {e}")
            QMessageBox.critical(self, "Error", f"Failed to search orders: {e}")

    def _open_checkout_dialog(self):
        """
        Opens a simulated checkout dialog.
        """
        dialog = CheckoutDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # In a real app, you'd get details from dialog and send to API
            # For now, just simulate success
            QMessageBox.information(self, "Checkout", "Checkout process completed (simulated).")
            self._load_orders() # Refresh orders after simulated checkout
            self.cart_items = {} # Clear cart after checkout
            self._update_cart_summary()
        else:
            QMessageBox.information(self, "Checkout", "Checkout process cancelled.")

    def _load_shop_products(self):
        """
        Loads products for the 'Shop' tab and displays them in a grid.
        """
        self.statusBar().showMessage("Loading shop products...")
        try:
            products = self.api_client.get_products() # Reuse existing product data

            # Clear existing products from the grid layout
            for i in reversed(range(self.product_grid_layout.count())):
                widget_to_remove = self.product_grid_layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.setParent(None)
                    widget_to_remove.deleteLater()

            self.product_cards = []

            col = 0
            row = 0
            for product in products:
                product_card = ProductCard(product)
                product_card.add_to_cart_requested.connect(self._add_product_to_cart_with_qty)
                self.product_grid_layout.addWidget(product_card, row, col)
                self.product_cards.append(product_card)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            self.statusBar().showMessage(f"Loaded {len(products)} products for shop.")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading shop products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load shop products: {e}")

    def _add_product_to_cart_with_qty(self, product_data, quantity):
        product_id = product_data['id']
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] += quantity
        else:
            self.cart_items[product_id] = {'product': product_data, 'quantity': quantity}
        self._update_cart_summary()
        if self.checkout_panel and self.checkout_panel.isVisible():
            self._refresh_checkout_panel()
        self.statusBar().showMessage(f"Added {product_data['name']} to cart. Quantity: {self.cart_items[product_id]['quantity']}")

    def _show_checkout_panel(self):
        if not self.checkout_panel:
            self.checkout_panel = QDockWidget("", self)
            self.checkout_panel.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
            self.checkout_panel.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

            # Responsive width for mobile vs desktop
            if self.width() <= 480:  # Mobile width threshold
                panel_width = self.width()  # Full width on mobile
            else:
                panel_width = 350  # Default width on desktop

            self.checkout_panel.setMinimumWidth(panel_width)
            self.checkout_panel.setMaximumWidth(panel_width)

            # Panel widget and layout
            panel_widget = QWidget()
            panel_layout = QVBoxLayout(panel_widget)
            panel_layout.setContentsMargins(16, 16, 16, 16)
            panel_layout.setSpacing(12)

            # Checkout Title
            checkout_title = QLabel("Checkout")
            checkout_title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
            checkout_title.setStyleSheet("color: #1BA94C; margin-bottom: 2px;")
            panel_layout.addWidget(checkout_title, alignment=Qt.AlignmentFlag.AlignLeft)

            # Cart List
            self.cart_list_widget = QWidget()
            self.cart_list_layout = QVBoxLayout(self.cart_list_widget)
            self.cart_list_layout.setSpacing(10)
            self.cart_list_layout.setContentsMargins(0, 0, 0, 0)  # Remove top margin to lift list closer to checkout text
            self.cart_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align items from top
            panel_layout.addWidget(self.cart_list_widget)

            # Footer (total and checkout button)
            footer = QWidget()
            footer_layout = QVBoxLayout(footer)
            footer_layout.setContentsMargins(0, 16, 0, 0)
            self.cart_total_label = QLabel()
            self.cart_total_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
            self.cart_total_label.setStyleSheet("color: #222;")
            footer_layout.addWidget(self.cart_total_label)
            checkout_btn = QPushButton("Complete Checkout")
            checkout_btn.setStyleSheet("background-color: #34C759; color: white; padding: 10px; border-radius: 8px;")
            checkout_btn.clicked.connect(self._complete_checkout)
            footer_layout.addWidget(checkout_btn)
            panel_layout.addWidget(footer)

            self.checkout_panel.setWidget(panel_widget)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.checkout_panel)

            # Setup slide animation for showing/hiding
            self._checkout_anim = QPropertyAnimation(self.checkout_panel, b"geometry")
            self._checkout_anim.setDuration(500)
            self._checkout_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self._refresh_checkout_panel()

        # Animate showing the panel
        start_rect = QRect(self.width(), 0, self.checkout_panel.width(), self.height())
        end_rect = QRect(self.width() - self.checkout_panel.width(), 0, self.checkout_panel.width(), self.height())
        self.checkout_panel.setGeometry(start_rect)
        self.checkout_panel.show()
        self._checkout_anim.stop()
        self._checkout_anim.setStartValue(start_rect)
        self._checkout_anim.setEndValue(end_rect)
        self._checkout_anim.start()

    def _toggle_checkout_panel(self):
        if self.checkout_panel and self.checkout_panel.isVisible():
            # Animate hiding the panel
            start_rect = self.checkout_panel.geometry()
            end_rect = QRect(self.width(), 0, self.checkout_panel.width(), self.height())
            self._checkout_anim.stop()
            self._checkout_anim.setStartValue(start_rect)
            self._checkout_anim.setEndValue(end_rect)
            self._checkout_anim.start()
            self._checkout_anim.finished.connect(self.checkout_panel.hide)
        else:
            self._show_checkout_panel()

    def _refresh_checkout_panel(self):
        # Clear previous items
        for i in reversed(range(self.cart_list_layout.count())):
            widget = self.cart_list_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        for product_id, item in self.cart_items.items():
            product = item['product']
            quantity = item['quantity']

            # Card for each cart item
            card = QWidget()
            card.setStyleSheet("""
                background: transparent;
                border: none;
                padding: 0;
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(8, 4, 8, 4)
            card_layout.setSpacing(8)

            # Product name and price
            info = QLabel(f"{product['name']} (Rs {product['price']:.2f})")
            info.setFont(QFont("Inter", 10, QFont.Weight.Bold))
            info.setStyleSheet("color: #222;")
            card_layout.addWidget(info, stretch=2)

            # Minus button
            minus_btn = QPushButton("−")
            minus_btn.setFixedWidth(26)
            minus_btn.setStyleSheet("background: #F2F2F2; border: none; font-size: 15px; color: black;")
            minus_btn.clicked.connect(lambda _, pid=product_id: self._change_cart_quantity(pid, -1))
            card_layout.addWidget(minus_btn)

            # Quantity label
            qty_label = QLabel(str(quantity))
            qty_label.setFixedWidth(22)
            qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_label.setStyleSheet("color: black; font-weight: bold;")
            card_layout.addWidget(qty_label)

            # Plus button
            plus_btn = QPushButton("+")
            plus_btn.setFixedWidth(26)
            plus_btn.setStyleSheet("background: #F2F2F2; border: none; font-size: 15px; color: black;")
            plus_btn.clicked.connect(lambda _, pid=product_id: self._change_cart_quantity(pid, 1))
            card_layout.addWidget(plus_btn)

            # Remove button
            remove_btn = QPushButton("Remove")
            remove_btn.setStyleSheet("background-color: #FF3B30; color: white; border-radius: 5px; padding: 4px 10px;")
            remove_btn.clicked.connect(lambda _, pid=product_id: self._remove_from_cart(pid))
            card_layout.addWidget(remove_btn)

            self.cart_list_layout.addWidget(card)

        # Removed stretch to align items from top
        # self.cart_list_layout.addStretch(1)
        total_amount = sum(item['product']['price'] * item['quantity'] for item in self.cart_items.values())
        self.cart_total_label.setText(f"Total: Rs {total_amount:.2f}")

    def _change_cart_quantity(self, product_id, delta):
        if product_id in self.cart_items:
            new_qty = self.cart_items[product_id]['quantity'] + delta
            if new_qty < 1:
                self._remove_from_cart(product_id)
            else:
                self.cart_items[product_id]['quantity'] = new_qty
            self._update_cart_summary()
            self._refresh_checkout_panel()

    def _remove_from_cart(self, product_id):
        if product_id in self.cart_items:
            del self.cart_items[product_id]
            self._update_cart_summary()
            self._refresh_checkout_panel()

    def _complete_checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Cart Empty", "Your cart is empty.")
            return
        # Simulate checkout
        QMessageBox.information(self, "Checkout", "Checkout process completed (simulated).")
        self.cart_items = {}
        self._update_cart_summary()
        self._refresh_checkout_panel()
        self._load_orders()
        self.checkout_panel.hide()

    def _add_product_to_cart(self, product_data):
        product_id = product_data['id']
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] += 1
        else:
            self.cart_items[product_id] = {'product': product_data, 'quantity': 1}
        self._update_cart_summary()
        if self.checkout_panel and self.checkout_panel.isVisible():
            self._refresh_checkout_panel()
        self.statusBar().showMessage(f"Added {product_data['name']} to cart. Quantity: {self.cart_items[product_id]['quantity']}")

    def _update_cart_summary(self):
        """
        Updates the cart summary label with current item count and total.
        """
        total_items = sum(item['quantity'] for item in self.cart_items.values())
        total_amount = sum(item['product']['price'] * item['quantity'] for item in self.cart_items.values())
        self.cart_summary_label.setText(f"Cart: {total_items} items (Rs {total_amount:.2f})")

    def _go_to_checkout(self):
        """
        Opens the checkout dialog with current cart items.
        """
        if not self.cart_items:
            QMessageBox.warning(self, "Cart Empty", "Your cart is empty. Please add products before checking out.")
            return

        total_amount = sum(item['product']['price'] * item['quantity'] for item in self.cart_items.values())
        
        # Pass cart details to the CheckoutDialog if it supported it.
        # For now, we'll just pass the total amount and a generic customer name.
        dialog = CheckoutDialog(self)
        dialog.total_amount_spinbox.setValue(total_amount)
        dialog.customer_name_input.setText("Walk-in Customer") # Default for POS

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # In a real app, you'd get details from dialog and send to API
            # For now, just simulate success
            QMessageBox.information(self, "Checkout", "Checkout process completed (simulated).")
            # After successful checkout, clear the cart and refresh orders
            self.cart_items = {}
            self._update_cart_summary()
            self._load_orders()
        else:
            QMessageBox.information(self, "Checkout", "Checkout process cancelled.")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_product_grid_columns()

    def _adjust_product_grid_columns(self):
        # Responsive columns: 4 for desktop, 2 for tablet, 1 for mobile
        width = self.width()
        if width > 1400:
            cols = 4
        elif width > 800:
            cols = 2
        else:
            cols = 1

        # Re-layout product cards
        for i in reversed(range(self.product_grid_layout.count())):
            widget = self.product_grid_layout.itemAt(i).widget()
            if widget:
                self.product_grid_layout.removeWidget(widget)

        for idx, card in enumerate(self.product_cards):
            row = idx // cols
            col = idx % cols
            self.product_grid_layout.addWidget(card, row, col)

    def _toggle_checkout_panel(self):
        if self.checkout_panel and self.checkout_panel.isVisible():
            self.checkout_panel.hide()
        else:
            self._show_checkout_panel()

    def _toggle_dark_mode(self):
        """
        Toggles the application between light and dark mode.
        """
        if self.dark_mode_toggle.isChecked():
            # Dark mode enabled
            self.dark_mode_toggle.setText("🌙")
            self.setStyleSheet("""
                QWidget {
                    background-color: #1C1C1E;
                    color: #FFFFFF;
                }
                QTabWidget::pane {
                    border: 1px solid #444444;
                    background: #2C2C2E;
                    border-radius: 12px;
                    padding: 10px;
                }
                QTabBar::tab {
                    background: #3A3A3C;
                    color: #FFFFFF;
                    padding: 10px 20px;
                    border-top-left-radius: 12px;
                    border-top-right-radius: 12px;
                    margin-right: 2px;
                    font-family: "Inter";
                    font-size: 14px;
                    font-weight: 600;
                }
                QTabBar::tab:selected {
                    background: #1C1C1E;
                    color: #34C759;
                }
                QTabBar::tab:hover {
                    background: #48484A;
                }
                QTableWidget {
                    background-color: #000000;
                    color: #FFFFFF;
                    gridline-color: #444444;
                    border: 1px solid #444444;
                }
                QHeaderView::section {
                    background-color: #2C2C2E;
                    color: #34C759;
                    padding: 10px;
                    border: 1px solid #444444;
                }
                QPushButton {
                    background-color: #3A3A3C;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #1C1C1E;
                }
                QPushButton:hover {
                    background-color: #48484A;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLineEdit {
                    background-color: #2C2C2E;
                    color: #FFFFFF;
                    border: 1px solid #444444;
                    border-radius: 8px;
                    padding: 8px;
                }
                QLineEdit:focus {
                    border: 1px solid #34C759;
                }
            """)
        else:
            # Light mode enabled
            self.dark_mode_toggle.setText("☀️")
            self.setStyleSheet("""
                QWidget {
                    background-color: #F2F2F7;
                    color: #1C1C1E;
                }
                QTabWidget::pane {
                    border: 1px solid #D1D1D6;
                    background: #FFFFFF;
                    border-radius: 12px;
                    padding: 10px;
                }
                QTabBar::tab {
                    background: #F2F2F7;
                    color: #636366;
                    padding: 10px 20px;
                    border-top-left-radius: 12px;
                    border-top-right-radius: 12px;
                    margin-right: 2px;
                    font-family: "Inter";
                    font-size: 14px;
                    font-weight: 600;
                }
                QTabBar::tab:selected {
                    background: #FFFFFF;
                    color: #007AFF;
                }
                QTabBar::tab:hover {
                    background: #E5E5EA;
                }
                QTableWidget {
                    background-color: #FFFFFF;
                    color: #1C1C1E;
                    gridline-color: #E5E5EA;
                    border: 1px solid #E5E5EA;
                }
                QHeaderView::section {
                    background-color: #F2F2F7;
                    color: #636366;
                    padding: 10px;
                    border: 1px solid #D1D1D6;
                }
                QPushButton {
                    background-color: #E5E5EA;
                    color: #1C1C1E;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #1C1C1E;
                    color: #E5E5EA;
                }
                QPushButton:hover {
                    background-color: #D1D1D6;
                }
                QLabel {
                    color: #1C1C1E;
                }
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #1C1C1E;
                    border: 1px solid #D1D1D6;
                    border-radius: 8px;
                    padding: 8px;
                }
                QLineEdit:focus {
                    border: 1px solid #007AFF;
                }
            """)

    def _dark_mode_tab_style(self):
        """
        Returns the stylesheet string for the tab widget in dark mode.
        """
        return """
        QTabWidget::pane {
            border: 1px solid #444444;
            background: #2C2C2E;
            border-radius: 12px;
            padding: 10px;
        }
        QTabBar::tab {
            background: #3A3A3C;
            color: #FFFFFF;
            padding: 10px 20px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            margin-right: 2px;
            font-family: "Inter";
            font-size: 14px;
            font-weight: 600;
        }
        QTabBar::tab:selected {
            background: #1C1C1E;
            color: #34C759;
        }
        QTabBar::tab:hover {
            background: #48484A;
        }
        """

    def _light_mode_tab_style(self):
        """
        Returns the stylesheet string for the tab widget in light mode.
        """
        return """
        QTabWidget::pane {
            border: 1px solid #D1D1D6;
            background: #FFFFFF;
            border-radius: 12px;
            padding: 10px;
        }
        QTabBar::tab {
            background: #F2F2F7;
            color: #636366;
            padding: 10px 20px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            margin-right: 2px;
            font-family: "Inter";
            font-size: 14px;
            font-weight: 600;
        }
        QTabBar::tab:selected {
            background: #FFFFFF;
            color: #007AFF;
        }
        QTabBar::tab:hover {
            background: #E5E5EA;
        }
        """

