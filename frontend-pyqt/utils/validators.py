import re
from typing import Optional, Tuple

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validators:
    """Collection of input validation methods"""
    
    @staticmethod
    def validate_price(price_str: str) -> Tuple[bool, Optional[float]]:
        """Validate price input"""
        try:
            price = float(price_str.replace('$', '').replace(',', ''))
            if price < 0:
                return False, None
            return True, price
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_stock(stock_str: str) -> Tuple[bool, Optional[int]]:
        """Validate stock quantity"""
        try:
            stock = int(stock_str)
            if stock < 0:
                return False, None
            return True, stock
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_product_name(name: str) -> Tuple[bool, str]:
        """Validate product name"""
        name = name.strip()
        if not name:
            return False, "Product name cannot be empty"
        if len(name) < 2:
            return False, "Product name must be at least 2 characters"
        if len(name) > 100:
            return False, "Product name cannot exceed 100 characters"
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 10:
            return False, "Phone number must have at least 10 digits"
        return True, ""
    
    @staticmethod
    def validate_customer_name(name: str) -> Tuple[bool, str]:
        """Validate customer name"""
        name = name.strip()
        if not name:
            return False, "Customer name cannot be empty"
        if len(name) < 2:
            return False, "Customer name must be at least 2 characters"
        if len(name) > 50:
            return False, "Customer name cannot exceed 50 characters"
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return False, "Customer name contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_quantity(qty_str: str) -> Tuple[bool, Optional[int]]:
        """Validate quantity input"""
        try:
            qty = int(qty_str)
            if qty <= 0:
                return False, None
            if qty > 1000:  # Reasonable upper limit
                return False, None
            return True, qty
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_coupon_code(code: str) -> Tuple[bool, str]:
        """Validate coupon code format"""
        code = code.strip().upper()
        if not code:
            return False, "Coupon code cannot be empty"
        if len(code) < 3:
            return False, "Coupon code must be at least 3 characters"
        if len(code) > 20:
            return False, "Coupon code cannot exceed 20 characters"
        # Allow alphanumeric characters and hyphens
        if not re.match(r'^[A-Z0-9\-]+$', code):
            return False, "Coupon code contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_search_query(query: str) -> Tuple[bool, str]:
        """Validate search query"""
        query = query.strip()
        if len(query) > 100:
            return False, "Search query too long"
        # Basic sanitization - remove potentially harmful characters
        if re.search(r'[<>"\';]', query):
            return False, "Search query contains invalid characters"
        return True, ""
    
    @staticmethod
    def validate_order_id(order_id: str) -> Tuple[bool, Optional[int]]:
        """Validate order ID"""
        try:
            oid = int(order_id.strip())
            if oid <= 0:
                return False, None
            return True, oid
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_product_id(product_id: str) -> Tuple[bool, Optional[int]]:
        """Validate product ID"""
        try:
            pid = int(product_id.strip())
            if pid <= 0:
                return False, None
            return True, pid
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_description(description: str) -> Tuple[bool, str]:
        """Validate product description"""
        description = description.strip()
        if len(description) > 1000:
            return False, "Description cannot exceed 1000 characters"
        return True, ""
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input by removing potentially harmful characters"""
        if not input_str:
            return ""
        # Remove HTML tags and script content
        input_str = re.sub(r'<[^>]+>', '', input_str)
        # Remove potentially harmful characters
        input_str = re.sub(r'[<>"\';]', '', input_str)
        return input_str.strip()