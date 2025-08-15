import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppSettings:
    """Application settings configuration"""
    
    # API Configuration
    api_base_url: str = "http://localhost:8080/api"
    api_timeout: int = 30
    api_retry_attempts: int = 3
    
    # UI Configuration
    window_width: int = 1200
    window_height: int = 800
    theme: str = "light"  # light or dark
    font_family: str = "Inter"
    font_size: int = 10
    
    # Product Grid Configuration
    products_per_row: int = 4
    product_card_width: int = 320
    product_card_height: int = 600
    
    # Cart Configuration
    max_cart_items: int = 100
    currency_symbol: str = "$"
    
    # File Paths
    assets_dir: str = "assets"
    icons_dir: str = "assets/icons"
    images_dir: str = "assets/images"
    logs_dir: str = "logs"
    
    # Validation Rules
    min_product_name_length: int = 2
    max_product_name_length: int = 100
    min_price: float = 0.01
    max_price: float = 999999.99
    
    @classmethod
    def load_from_env(cls) -> 'AppSettings':
        """Load settings from environment variables"""
        return cls(
            api_base_url=os.getenv('API_BASE_URL', cls.api_base_url),
            api_timeout=int(os.getenv('API_TIMEOUT', cls.api_timeout)),
            window_width=int(os.getenv('WINDOW_WIDTH', cls.window_width)),
            window_height=int(os.getenv('WINDOW_HEIGHT', cls.window_height)),
            theme=os.getenv('THEME', cls.theme),
            font_family=os.getenv('FONT_FAMILY', cls.font_family),
            font_size=int(os.getenv('FONT_SIZE', cls.font_size)),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            'api_base_url': self.api_base_url,
            'api_timeout': self.api_timeout,
            'window_width': self.window_width,
            'window_height': self.window_height,
            'theme': self.theme,
            'font_family': self.font_family,
            'font_size': self.font_size,
        }

# Global settings instance
settings = AppSettings.load_from_env()