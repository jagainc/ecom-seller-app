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
from components.product_card import ProductCard
from dialogs.checkout_dialog import CheckoutDialog
from services.api_client import ApiClient
from utils.theme_manager import theme_manager

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
        self.setGeometry(100, 100, 1200, 800)
        
        self.api_client = ApiClient()
        self.cart_items = {}
        self.checkout_panel = None
        
        # Connect to theme changes
        theme_manager.theme_changed.connect(self.apply_theme)
        
        self._create_ui()
        self._load_dashboard_data()
        
        # Apply initial theme
        self.apply_theme()

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        
        # Reposition checkout panel if it's visible
        if hasattr(self, 'checkout_panel') and self.checkout_panel and self.checkout_panel.isVisible():
            # Stop any running animation first
            if hasattr(self, '_checkout_anim') and self._checkout_anim:
                self._checkout_anim.stop()
            
            # Recalculate position for new window size
            panel_height = self.height() - 100
            end_x = self.width() - self.panel_width - 20
            new_rect = QRect(end_x, 50, self.panel_width, panel_height)
            self.checkout_panel.setGeometry(new_rect)

    def apply_theme(self):
        """Apply the current theme to the main window"""
        self.setStyleSheet(theme_manager.get_complete_stylesheet())
        
        # Update dark mode toggle button
        if theme_manager.current_theme == "dark":
            self.dark_mode_toggle.setText("🌙")
            self.dark_mode_toggle.setChecked(True)
        else:
            self.dark_mode_toggle.setText("☀️")
            self.dark_mode_toggle.setChecked(False)
        
        # Update toggle button style
        colors = theme_manager.get_current_theme()
        self.dark_mode_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['button_bg']};
                border-radius: 20px;
                font-weight: bold;
                font-size: 20px;
                color: {colors['button_text']};
            }}
            QPushButton:checked {{
                background-color: {colors['primary_text']};
                color: {colors['primary_bg']};
            }}
        """)

    def _create_ui(self):
        """
        Sets up the main user interface components of the window.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Application Title and Dark Mode Toggle
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("ECOM Seller Dashboard")
        self.title_label.setFont(QFont("Inter", 26, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setObjectName("main_title")
        header_layout.addWidget(self.title_label)

        # Dark Mode Toggle Button
        self.dark_mode_toggle = QPushButton("☀️")
        self.dark_mode_toggle.setCheckable(True)
        self.dark_mode_toggle.setFixedSize(40, 40)
        self.dark_mode_toggle.clicked.connect(self._toggle_dark_mode)
        header_layout.addStretch(1)
        header_layout.addWidget(self.dark_mode_toggle)

        main_layout.addLayout(header_layout)

        # Tab Widget for different sections
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Setup tabs
        self._setup_shop_tab()
        self._setup_dashboard_tab()
        self._setup_products_tab()
        self._setup_orders_tab()

        # Status Bar
        self.statusBar().showMessage("Ready")

    def _toggle_dark_mode(self):
        """Toggle between light and dark themes"""
        theme_manager.toggle_theme()

    def _setup_shop_tab(self):
        """Sets up the 'Shop' tab for browsing products and adding to cart."""
        shop_widget = QWidget()
        shop_layout = QVBoxLayout(shop_widget)
        shop_layout.setContentsMargins(25, 25, 25, 25)
        shop_layout.setSpacing(20)

        shop_header_layout = QHBoxLayout()
        
        self.shop_label = QLabel("Product Catalog")
        self.shop_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        self.shop_label.setObjectName("section_title")
        shop_header_layout.addWidget(self.shop_label)
        shop_header_layout.addStretch(1)

        # Cart Summary and Checkout Button
        self.cart_summary_label = QLabel("Cart: 0 items ($0.00)")
        self.cart_summary_label.setFont(QFont("Inter", 14, QFont.Weight.DemiBold))
        self.cart_summary_label.setObjectName("cart_summary")
        shop_header_layout.addWidget(self.cart_summary_label)

        self.go_to_checkout_button = QPushButton("Go to Checkout")
        self.go_to_checkout_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        self.go_to_checkout_button.setProperty("class", "success")
        self.go_to_checkout_button.clicked.connect(self._toggle_checkout_panel)
        shop_header_layout.addWidget(self.go_to_checkout_button)
        
        shop_layout.addLayout(shop_header_layout)

        # Product Grid
        self.product_grid_layout = QGridLayout()
        self.product_grid_layout.setSpacing(40)

        self.product_scroll_area = QScrollArea()
        self.product_scroll_area.setWidgetResizable(True)
        
        products_container = QWidget()
        products_container.setLayout(self.product_grid_layout)
        self.product_scroll_area.setWidget(products_container)
        
        shop_layout.addWidget(self.product_scroll_area)
        
        self.tab_widget.addTab(shop_widget, "Shop")
        self._load_shop_products()

    def _setup_dashboard_tab(self):
        """Sets up the 'Dashboard' tab with analytics."""
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.setContentsMargins(25, 25, 25, 25)
        dashboard_layout.setSpacing(25)

        # Chart Section
        chart_label = QLabel("Sales Trends & Analytics")
        chart_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        chart_label.setObjectName("section_title")
        dashboard_layout.addWidget(chart_label)

        chart_frame = QFrame()
        chart_frame.setFrameShape(QFrame.Shape.StyledPanel)
        chart_frame.setFrameShadow(QFrame.Shadow.Raised)
        chart_layout = QVBoxLayout(chart_frame)
        
        chart_placeholder = QLabel("Sales charts and analytics would be displayed here. This data would be fetched from the backend's ChartGenerationService.")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setWordWrap(True)
        chart_placeholder.setFont(QFont("Inter", 12))
        chart_placeholder.setObjectName("placeholder_text")
        chart_layout.addWidget(chart_placeholder)
        
        dashboard_layout.addWidget(chart_frame)
        dashboard_layout.addStretch(1)

        self.tab_widget.addTab(dashboard_widget, "Dashboard")

    def _setup_products_tab(self):
        """Sets up the 'Products' tab for product management."""
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        products_layout.setContentsMargins(25, 25, 25, 25)
        products_layout.setSpacing(20)

        products_label = QLabel("Product Management")
        products_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        products_label.setObjectName("section_title")
        products_layout.addWidget(products_label)

        # Product search and add section
        search_add_layout = QHBoxLayout()
        
        self.product_search_input = QLineEdit()
        self.product_search_input.setPlaceholderText("Search products...")
        self.product_search_input.setFont(QFont("Inter", 13))
        self.product_search_input.returnPressed.connect(self._search_products)
        search_add_layout.addWidget(self.product_search_input)

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        search_button.setProperty("class", "primary")
        search_button.clicked.connect(self._search_products)
        search_add_layout.addWidget(search_button)

        add_product_button = QPushButton("Add New Product")
        add_product_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        add_product_button.setProperty("class", "success")
        add_product_button.clicked.connect(self._add_product)
        search_add_layout.addWidget(add_product_button)
        
        products_layout.addLayout(search_add_layout)

        # Product table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Stock", "Actions"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        products_layout.addWidget(self.product_table)

        self.tab_widget.addTab(products_widget, "Products")
        self._load_products()

    def _setup_orders_tab(self):
        """Sets up the 'Orders' tab for order management."""
        orders_widget = QWidget()
        orders_layout = QVBoxLayout(orders_widget)
        orders_layout.setContentsMargins(25, 25, 25, 25)
        orders_layout.setSpacing(20)

        orders_label = QLabel("Order Management")
        orders_label.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        orders_label.setObjectName("section_title")
        orders_layout.addWidget(orders_label)

        # Order controls
        order_controls_layout = QHBoxLayout()
        
        self.order_search_input = QLineEdit()
        self.order_search_input.setPlaceholderText("Search orders...")
        self.order_search_input.setFont(QFont("Inter", 13))
        self.order_search_input.returnPressed.connect(self._search_orders)
        order_controls_layout.addWidget(self.order_search_input)

        search_order_button = QPushButton("Search")
        search_order_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        search_order_button.setProperty("class", "primary")
        search_order_button.clicked.connect(self._search_orders)
        order_controls_layout.addWidget(search_order_button)

        open_checkout_button = QPushButton("Simulate Checkout")
        open_checkout_button.setFont(QFont("Inter", 13, QFont.Weight.DemiBold))
        open_checkout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9500;
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
        orders_layout.addWidget(self.order_table)

        self.tab_widget.addTab(orders_widget, "Orders")
        self._load_orders()

    # Data loading methods
    def _load_dashboard_data(self):
        """Load dashboard data"""
        self.statusBar().showMessage("Dashboard data loaded.")

    def _load_products(self):
        """Load products into the table"""
        self.statusBar().showMessage("Loading products...")
        try:
            products = self.api_client.get_products()
            self._populate_product_table(products)
            self.statusBar().showMessage(f"Loaded {len(products)} products.")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading products: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load products: {e}")

    def _load_shop_products(self):
        """Load products for the shop tab"""
        self.statusBar().showMessage("Loading shop products...")
        try:
            products = self.api_client.get_products()

            # Clear existing products
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

    def _load_orders(self):
        """Load orders into the table"""
        self.statusBar().showMessage("Loading orders...")
        try:
            orders = self.api_client.get_orders()
            self._populate_order_table(orders)
            self.statusBar().showMessage(f"Loaded {len(orders)} orders.")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading orders: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load orders: {e}")

    # Cart and checkout methods
    def _add_product_to_cart_with_qty(self, product_data, quantity):
        """Add product to cart with specified quantity"""
        product_id = product_data['id']
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] += quantity
        else:
            self.cart_items[product_id] = {'product': product_data, 'quantity': quantity}
        
        self._update_cart_summary()
        if self.checkout_panel and self.checkout_panel.isVisible():
            self._refresh_checkout_panel()
        
        self.statusBar().showMessage(f"Added {product_data['name']} to cart. Quantity: {self.cart_items[product_id]['quantity']}")

    def _update_cart_summary(self):
        """Update cart summary display"""
        total_items = sum(item['quantity'] for item in self.cart_items.values())
        total_amount = sum(item['product']['price'] * item['quantity'] for item in self.cart_items.values())
        self.cart_summary_label.setText(f"Cart: {total_items} items (${total_amount:.2f})")

    def _toggle_checkout_panel(self):
        """Toggle checkout panel visibility"""
        if self.checkout_panel and self.checkout_panel.isVisible():
            self.checkout_panel.hide()
        else:
            self._show_checkout_panel()

    def _show_checkout_panel(self):
        """Show checkout panel with sliding animation"""
        if not self.cart_items:
            QMessageBox.information(self, "Empty Cart", "Your cart is empty. Add some products first!")
            return
        
        if not self.checkout_panel:
            self._create_checkout_panel()
        
        # Position panel off-screen initially
        self.panel_width = 400
        panel_height = self.height() - 100
        start_x = self.width()
        end_x = self.width() - self.panel_width - 20
        
        self.checkout_panel.setGeometry(start_x, 50, self.panel_width, panel_height)
        self.checkout_panel.show()
        
        # Animate panel sliding in
        self._checkout_anim = QPropertyAnimation(self.checkout_panel, b"geometry")
        self._checkout_anim.setDuration(300)
        self._checkout_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._checkout_anim.setStartValue(QRect(start_x, 50, self.panel_width, panel_height))
        self._checkout_anim.setEndValue(QRect(end_x, 50, self.panel_width, panel_height))
        self._checkout_anim.start()
        
        # Refresh panel content
        self._refresh_checkout_panel()
    
    def _create_checkout_panel(self):
        """Create the checkout panel widget"""
        from PyQt6.QtWidgets import QScrollArea, QFrame
        
        self.checkout_panel = QWidget(self)
        self.checkout_panel.setObjectName("checkout_panel")
        
        # Main layout
        panel_layout = QVBoxLayout(self.checkout_panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(15)
        
        # Header with title and close button
        header_layout = QHBoxLayout()
        title = QLabel("🛒 Shopping Cart")
        title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        title.setObjectName("checkout_title")
        header_layout.addWidget(title)
        
        close_btn = QPushButton("✕")
        close_btn.setObjectName("close_btn")
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self._hide_checkout_panel)
        header_layout.addWidget(close_btn)
        
        panel_layout.addLayout(header_layout)
        
        # Scroll area for cart items
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setObjectName("cart_scroll")
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.cart_content = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_content)
        self.cart_layout.setSpacing(10)
        self.cart_scroll.setWidget(self.cart_content)
        
        panel_layout.addWidget(self.cart_scroll, 1)
        
        # Coupon section
        coupon_frame = QFrame()
        coupon_layout = QVBoxLayout(coupon_frame)
        coupon_layout.setContentsMargins(10, 10, 10, 10)
        
        coupon_label = QLabel("Coupon Code:")
        coupon_label.setObjectName("section_label")
        coupon_layout.addWidget(coupon_label)
        
        coupon_input_layout = QHBoxLayout()
        self.coupon_input = QLineEdit()
        self.coupon_input.setObjectName("coupon_input")
        self.coupon_input.setPlaceholderText("Enter coupon code...")
        coupon_input_layout.addWidget(self.coupon_input)
        
        apply_coupon_btn = QPushButton("Apply")
        apply_coupon_btn.setProperty("class", "primary")
        apply_coupon_btn.clicked.connect(self._apply_coupon)
        coupon_input_layout.addWidget(apply_coupon_btn)
        
        coupon_layout.addLayout(coupon_input_layout)
        
        self.coupon_status = QLabel("")
        self.coupon_status.setObjectName("coupon_status")
        coupon_layout.addWidget(self.coupon_status)
        
        panel_layout.addWidget(coupon_frame)
        
        # Summary section
        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(10, 10, 10, 10)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        summary_layout.addWidget(separator)
        
        self.subtotal_label = QLabel("Subtotal: $0.00")
        self.subtotal_label.setObjectName("summary_text")
        summary_layout.addWidget(self.subtotal_label)
        
        self.discount_label = QLabel("")
        self.discount_label.setObjectName("discount_text")
        summary_layout.addWidget(self.discount_label)
        
        self.tax_label = QLabel("Tax (8%): $0.00")
        self.tax_label.setObjectName("summary_text")
        summary_layout.addWidget(self.tax_label)
        
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.total_label.setObjectName("cart_total")
        summary_layout.addWidget(self.total_label)
        
        panel_layout.addWidget(summary_frame)
        
        # Checkout button
        checkout_btn = QPushButton("Proceed to Checkout")
        checkout_btn.setProperty("class", "success")
        checkout_btn.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        checkout_btn.clicked.connect(self._proceed_to_checkout)
        panel_layout.addWidget(checkout_btn)
        
        # Initialize coupon system
        self.applied_coupon = None
        self.discount_amount = 0.0
        self.tax_rate = 0.08
    
    def _hide_checkout_panel(self):
        """Hide checkout panel with sliding animation"""
        if not self.checkout_panel or not self.checkout_panel.isVisible():
            return
        
        current_rect = self.checkout_panel.geometry()
        end_x = self.width()
        
        self._checkout_anim = QPropertyAnimation(self.checkout_panel, b"geometry")
        self._checkout_anim.setDuration(300)
        self._checkout_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._checkout_anim.setStartValue(current_rect)
        self._checkout_anim.setEndValue(QRect(end_x, current_rect.y(), current_rect.width(), current_rect.height()))
        self._checkout_anim.finished.connect(self.checkout_panel.hide)
        self._checkout_anim.start()
    
    def _refresh_checkout_panel(self):
        """Refresh checkout panel contents"""
        if not self.checkout_panel or not hasattr(self, 'cart_layout'):
            return
        
        # Clear existing cart items
        for i in reversed(range(self.cart_layout.count())):
            child = self.cart_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                child.deleteLater()
        
        if not self.cart_items:
            empty_label = QLabel("Your cart is empty")
            empty_label.setObjectName("empty_cart_label")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_layout.addWidget(empty_label)
        else:
            # Add cart items
            for product_id, item_data in self.cart_items.items():
                cart_item = self._create_cart_item_widget(item_data)
                self.cart_layout.addWidget(cart_item)
        
        self.cart_layout.addStretch()
        self._update_checkout_summary()
    
    def _create_cart_item_widget(self, item_data):
        """Create a widget for a single cart item"""
        product = item_data['product']
        quantity = item_data['quantity']
        
        item_widget = QWidget()
        item_widget.setObjectName("cart_item_card")
        item_layout = QVBoxLayout(item_widget)
        item_layout.setContentsMargins(10, 10, 10, 10)
        item_layout.setSpacing(8)
        
        # Product info
        info_layout = QHBoxLayout()
        
        name_price_layout = QVBoxLayout()
        name_label = QLabel(product['name'])
        name_label.setObjectName("cart_item_name")
        name_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        name_price_layout.addWidget(name_label)
        
        price_label = QLabel(f"${product['price']:.2f} each")
        price_label.setObjectName("cart_item_price")
        name_price_layout.addWidget(price_label)
        
        info_layout.addLayout(name_price_layout, 1)
        
        # Remove button
        remove_btn = QPushButton("🗑")
        remove_btn.setObjectName("remove_btn")
        remove_btn.setFixedSize(24, 24)
        remove_btn.clicked.connect(lambda: self._remove_from_cart(product['id']))
        info_layout.addWidget(remove_btn)
        
        item_layout.addLayout(info_layout)
        
        # Quantity controls and total
        qty_total_layout = QHBoxLayout()
        
        # Quantity controls
        qty_layout = QHBoxLayout()
        qty_label = QLabel("Qty:")
        qty_label.setObjectName("qty_label")
        qty_layout.addWidget(qty_label)
        
        minus_btn = QPushButton("-")
        minus_btn.setObjectName("cart_qty_btn")
        minus_btn.setFixedSize(24, 24)
        minus_btn.clicked.connect(lambda: self._update_cart_quantity(product['id'], -1))
        qty_layout.addWidget(minus_btn)
        
        qty_display = QLabel(str(quantity))
        qty_display.setObjectName("cart_qty_display")
        qty_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qty_display.setFixedWidth(30)
        qty_layout.addWidget(qty_display)
        
        plus_btn = QPushButton("+")
        plus_btn.setObjectName("cart_qty_btn")
        plus_btn.setFixedSize(24, 24)
        plus_btn.clicked.connect(lambda: self._update_cart_quantity(product['id'], 1))
        qty_layout.addWidget(plus_btn)
        
        qty_total_layout.addLayout(qty_layout)
        qty_total_layout.addStretch()
        
        # Item total
        total_label = QLabel(f"${product['price'] * quantity:.2f}")
        total_label.setObjectName("cart_item_total")
        total_label.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        qty_total_layout.addWidget(total_label)
        
        item_layout.addLayout(qty_total_layout)
        
        return item_widget
    
    def _update_cart_quantity(self, product_id, change):
        """Update quantity of item in cart"""
        if product_id in self.cart_items:
            new_qty = self.cart_items[product_id]['quantity'] + change
            if new_qty <= 0:
                self._remove_from_cart(product_id)
            else:
                self.cart_items[product_id]['quantity'] = new_qty
                self._update_cart_summary()
                self._refresh_checkout_panel()
    
    def _remove_from_cart(self, product_id):
        """Remove item from cart"""
        if product_id in self.cart_items:
            del self.cart_items[product_id]
            self._update_cart_summary()
            self._refresh_checkout_panel()
    
    def _apply_coupon(self):
        """Apply coupon code"""
        from utils.validators import Validators
        
        code = self.coupon_input.text().strip()
        valid, error = Validators.validate_coupon_code(code)
        
        if not valid:
            self.coupon_status.setText(f"❌ {error}")
            self.coupon_status.setStyleSheet("color: #FF3B30;")
            return
        
        # Simulate coupon validation (in real app, this would call API)
        valid_coupons = {
            "SAVE10": 0.10,
            "WELCOME20": 0.20,
            "STUDENT15": 0.15,
            "NEWUSER": 0.25
        }
        
        if code.upper() in valid_coupons:
            self.applied_coupon = code.upper()
            discount_percent = valid_coupons[code.upper()]
            self.discount_amount = self._calculate_subtotal() * discount_percent
            self.coupon_status.setText(f"✅ Coupon applied! {discount_percent*100:.0f}% off")
            self.coupon_status.setStyleSheet("color: #34C759;")
            self._update_checkout_summary()
        else:
            self.coupon_status.setText("❌ Invalid coupon code")
            self.coupon_status.setStyleSheet("color: #FF3B30;")
    
    def _calculate_subtotal(self):
        """Calculate cart subtotal"""
        return sum(item['product']['price'] * item['quantity'] for item in self.cart_items.values())
    
    def _update_checkout_summary(self):
        """Update checkout summary labels"""
        if not hasattr(self, 'subtotal_label'):
            return
        
        subtotal = self._calculate_subtotal()
        discount = self.discount_amount if self.applied_coupon else 0
        discounted_subtotal = subtotal - discount
        tax = discounted_subtotal * self.tax_rate
        total = discounted_subtotal + tax
        
        self.subtotal_label.setText(f"Subtotal: ${subtotal:.2f}")
        
        if discount > 0:
            self.discount_label.setText(f"Discount ({self.applied_coupon}): -${discount:.2f}")
            self.discount_label.show()
        else:
            self.discount_label.hide()
        
        self.tax_label.setText(f"Tax ({self.tax_rate*100:.0f}%): ${tax:.2f}")
        self.total_label.setText(f"Total: ${total:.2f}")
    
    def _proceed_to_checkout(self):
        """Proceed to checkout process"""
        if not self.cart_items:
            QMessageBox.information(self, "Empty Cart", "Your cart is empty!")
            return
        
        total = self._calculate_subtotal() - self.discount_amount
        total += total * self.tax_rate
        
        dialog = CheckoutDialog(self)
        # Pre-fill total amount
        if hasattr(dialog, 'total_amount_spinbox'):
            dialog.total_amount_spinbox.setValue(total)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            order_details = dialog.get_order_details()
            
            # Process checkout via API
            try:
                checkout_data = {
                    "customer_name": order_details["customer_name"],
                    "total_amount": total,
                    "items": [
                        {
                            "product_id": pid,
                            "quantity": item['quantity'],
                            "price": item['product']['price']
                        }
                        for pid, item in self.cart_items.items()
                    ],
                    "coupon_code": self.applied_coupon,
                    "discount_amount": self.discount_amount
                }
                
                result = self.api_client.process_checkout(checkout_data)
                
                if result.get("status") == "success":
                    QMessageBox.information(
                        self, 
                        "Order Successful", 
                        f"Order #{result.get('order_id')} has been placed successfully!\n"
                        f"Total: ${total:.2f}"
                    )
                    
                    # Clear cart and refresh
                    self.cart_items = {}
                    self.applied_coupon = None
                    self.discount_amount = 0.0
                    self._update_cart_summary()
                    self._refresh_checkout_panel()
                    self._load_orders()  # Refresh orders tab
                    self._hide_checkout_panel()
                else:
                    QMessageBox.critical(self, "Checkout Failed", "Failed to process order. Please try again.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Checkout error: {str(e)}")
        else:
            QMessageBox.information(self, "Checkout Cancelled", "Checkout process was cancelled.")

    # Search methods
    def _search_products(self):
        """Search products based on name or ID"""
        from utils.validators import Validators
        
        search_text = self.product_search_input.text().strip()
        
        # Validate search query
        valid, error = Validators.validate_search_query(search_text)
        if not valid:
            QMessageBox.warning(self, "Invalid Search", error)
            return
        
        if not search_text:
            # If empty, reload all products
            self._load_products()
            return
        
        self.statusBar().showMessage(f"Searching for products: '{search_text}'...")
        
        try:
            # Get all products from API
            all_products = self.api_client.get_products()
            
            # Filter products based on search text
            search_lower = search_text.lower()
            filtered_products = []
            
            for product in all_products:
                # Search in product name, ID, and description
                if (search_lower in product['name'].lower() or 
                    search_lower in str(product['id']) or
                    search_lower in product.get('description', '').lower()):
                    filtered_products.append(product)
            
            # Update table with filtered results
            self._populate_product_table(filtered_products)
            
            self.statusBar().showMessage(f"Found {len(filtered_products)} products matching '{search_text}'")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error searching products: {e}")
            QMessageBox.critical(self, "Search Error", f"Failed to search products: {e}")
    
    def _populate_product_table(self, products):
        """Populate product table with given products list"""
        self.product_table.setRowCount(len(products))
        
        for row_idx, product in enumerate(products):
            self.product_table.setItem(row_idx, 0, QTableWidgetItem(str(product['id'])))
            self.product_table.setItem(row_idx, 1, QTableWidgetItem(product['name']))
            self.product_table.setItem(row_idx, 2, QTableWidgetItem(f"${product['price']:.2f}"))
            self.product_table.setItem(row_idx, 3, QTableWidgetItem(str(product['stock'])))
            
            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_button = QPushButton("Edit")
            edit_button.setFont(QFont("Inter", 11))
            edit_button.setProperty("class", "success")
            edit_button.clicked.connect(lambda _, p_id=product['id']: self._edit_product(p_id))
            
            delete_button = QPushButton("Delete")
            delete_button.setFont(QFont("Inter", 11))
            delete_button.setProperty("class", "danger")
            delete_button.clicked.connect(lambda _, p_id=product['id']: self._delete_product(p_id))
            
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)
            action_layout.addStretch(1)
            
            self.product_table.setCellWidget(row_idx, 4, action_widget)

    def _search_orders(self):
        """Search orders based on customer name, order ID, or status"""
        from utils.validators import Validators
        
        search_text = self.order_search_input.text().strip()
        
        # Validate search query
        valid, error = Validators.validate_search_query(search_text)
        if not valid:
            QMessageBox.warning(self, "Invalid Search", error)
            return
        
        if not search_text:
            # If empty, reload all orders
            self._load_orders()
            return
        
        self.statusBar().showMessage(f"Searching for orders: '{search_text}'...")
        
        try:
            # Get all orders from API
            all_orders = self.api_client.get_orders()
            
            # Filter orders based on search text
            search_lower = search_text.lower()
            filtered_orders = []
            
            for order in all_orders:
                # Search in customer name, order ID, and status
                if (search_lower in order['customer_name'].lower() or 
                    search_lower in str(order['id']) or
                    search_lower in order['status'].lower()):
                    filtered_orders.append(order)
            
            # Update table with filtered results
            self._populate_order_table(filtered_orders)
            
            self.statusBar().showMessage(f"Found {len(filtered_orders)} orders matching '{search_text}'")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error searching orders: {e}")
            QMessageBox.critical(self, "Search Error", f"Failed to search orders: {e}")
    
    def _populate_order_table(self, orders):
        """Populate order table with given orders list"""
        self.order_table.setRowCount(len(orders))
        
        for row_idx, order in enumerate(orders):
            self.order_table.setItem(row_idx, 0, QTableWidgetItem(str(order['id'])))
            self.order_table.setItem(row_idx, 1, QTableWidgetItem(order['customer_name']))
            self.order_table.setItem(row_idx, 2, QTableWidgetItem(f"${order['total_amount']:.2f}"))
            self.order_table.setItem(row_idx, 3, QTableWidgetItem(order['status']))
            self.order_table.setItem(row_idx, 4, QTableWidgetItem(order['order_date']))

    # Product management methods
    def _add_product(self):
        """Add new product"""
        QMessageBox.information(self, "Add Product", "This would open a dialog to add a new product.")
        self._load_products()

    def _edit_product(self, product_id):
        """Edit existing product"""
        QMessageBox.information(self, "Edit Product", f"This would open a dialog to edit product ID: {product_id}")
        self._load_products()

    def _delete_product(self, product_id):
        """Delete product"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Delete Product')
        msg_box.setText(f"Are you sure you want to delete product ID: {product_id}?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.statusBar().showMessage(f"Deleting product ID: {product_id}...")
            try:
                QMessageBox.information(self, "Delete Product", f"Product ID {product_id} deleted (simulated).")
                self.statusBar().showMessage(f"Product ID {product_id} deleted.")
                self._load_products()
            except Exception as e:
                self.statusBar().showMessage(f"Error deleting product: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete product: {e}")

    def _open_checkout_dialog(self):
        """Open checkout dialog"""
        dialog = CheckoutDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Checkout", "Checkout process completed (simulated).")
            self._load_orders()
            self.cart_items = {}
            self._update_cart_summary()
        else:
            QMessageBox.information(self, "Checkout", "Checkout process cancelled.")