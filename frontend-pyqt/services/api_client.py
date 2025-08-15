import time
import random
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class ApiResponse:
    """Standardized API response structure"""
    success: bool
    data: Any = None
    error: str = ""
    status_code: int = 200

class ApiException(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code

class ApiClient:
    """
    Simulates an API client for the ECOM Seller App frontend.
    In a real application, this class would handle HTTP requests
    to the Spring Boot backend (e.g., using 'requests' library).
    For demonstration purposes, it returns static/simulated data.
    """
    def __init__(self, base_url="http://localhost:8080/api", timeout=30):
        """
        Initializes the ApiClient.

        Args:
            base_url (str): The base URL of the Spring Boot backend API.
            timeout (int): Request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self._products_data = self._generate_simulated_products()
        self._orders_data = self._generate_simulated_orders()

    def _simulate_delay(self, min_delay=0.1, max_delay=0.5):
        """Simulates network delay."""
        time.sleep(random.uniform(min_delay, max_delay))

    def _generate_simulated_products(self):
        """Generates a list of simulated product data."""
        products = []
        for i in range(1, 11):
            products.append({
                "id": 100 + i,
                "name": f"Product {i}",
                "price": round(random.uniform(10.0, 500.0), 2),
                "stock": random.randint(0, 200),
                "description": f"Description for product {i}.",
                "image_path": f"assets/icons/product_{100 + i}.png"
            })
        return products

    def _generate_simulated_orders(self):
        """Generates a list of simulated order data."""
        orders = []
        statuses = ["Pending", "Shipped", "Delivered", "Cancelled"]
        customer_names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Eve Adams"]
        for i in range(1, 16):
            orders.append({
                "id": 1000 + i,
                "customer_name": random.choice(customer_names),
                "total_amount": round(random.uniform(50.0, 1500.0), 2),
                "status": random.choice(statuses),
                "order_date": f"2025-07-{random.randint(1, 25):02d}"
            })
        return orders

    def get_dashboard_summary(self):
        """
        Simulates fetching dashboard summary data (KPIs).
        Corresponds to DashboardController in backend.
        """
        self._simulate_delay()
        total_sales = sum(order['total_amount'] for order in self._orders_data if order['status'] != 'Cancelled')
        total_orders = len([order for order in self._orders_data if order['status'] != 'Cancelled'])
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0
        pending_orders = len([order for order in self._orders_data if order['status'] == 'Pending'])

        return {
            "total_sales": total_sales,
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "pending_orders": pending_orders,
            "chart_data": [random.randint(100, 1000) for _ in range(7)] # Placeholder for chart data
        }

    def get_products(self):
        """
        Simulates fetching a list of products.
        Corresponds to ProductController in backend.
        
        Returns the products list directly for backward compatibility.
        In a real implementation, this would return ApiResponse.
        """
        try:
            self._simulate_delay()
            self.logger.info("Fetching products")
            return self._products_data
        except Exception as e:
            self.logger.error(f"Error fetching products: {e}")
            raise ApiException(f"Failed to fetch products: {e}")
    
    def get_products_response(self) -> ApiResponse:
        """
        Returns products with full ApiResponse structure.
        Use this for new code that handles ApiResponse properly.
        """
        try:
            self._simulate_delay()
            self.logger.info("Fetching products")
            return ApiResponse(success=True, data=self._products_data)
        except Exception as e:
            self.logger.error(f"Error fetching products: {e}")
            return ApiResponse(success=False, error=str(e))

    def get_product_by_id(self, product_id):
        """
        Simulates fetching a single product by ID.
        """
        self._simulate_delay()
        for product in self._products_data:
            if product['id'] == product_id:
                return product
        return None

    def add_product(self, product_data):
        """
        Simulates adding a new product.
        """
        self._simulate_delay()
        new_id = max(p['id'] for p in self._products_data) + 1 if self._products_data else 101
        product_data['id'] = new_id
        self._products_data.append(product_data)
        return {"status": "success", "id": new_id}

    def update_product(self, product_id, product_data):
        """
        Simulates updating an existing product.
        """
        self._simulate_delay()
        for i, product in enumerate(self._products_data):
            if product['id'] == product_id:
                self._products_data[i].update(product_data)
                return {"status": "success"}
        return {"status": "error", "message": "Product not found"}

    def delete_product(self, product_id):
        """
        Simulates deleting a product.
        """
        self._simulate_delay()
        initial_len = len(self._products_data)
        self._products_data = [p for p in self._products_data if p['id'] != product_id]
        if len(self._products_data) < initial_len:
            return {"status": "success"}
        return {"status": "error", "message": "Product not found"}

    def get_orders(self):
        """
        Simulates fetching a list of orders.
        Corresponds to OrderController in backend.
        """
        self._simulate_delay()
        return self._orders_data

    def get_order_by_id(self, order_id):
        """
        Simulates fetching a single order by ID.
        """
        self._simulate_delay()
        for order in self._orders_data:
            if order['id'] == order_id:
                return order
        return None

    def process_checkout(self, checkout_data):
        """
        Simulates processing a checkout.
        Corresponds to OrderController in backend.
        """
        self._simulate_delay()
        new_order_id = max(o['id'] for o in self._orders_data) + 1 if self._orders_data else 1001
        new_order = {
            "id": new_order_id,
            "customer_name": checkout_data.get("customer_name", "Guest"),
            "total_amount": checkout_data.get("total_amount", 0.0),
            "status": "Pending",
            "order_date": time.strftime("%Y-%m-%d")
        }
        self._orders_data.append(new_order)
        return {"status": "success", "order_id": new_order_id}

