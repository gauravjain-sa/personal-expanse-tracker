"""
Configuration Module
Centralized configuration for the application - NO HARDCODING
"""
import os
from pathlib import Path
from typing import Dict, Tuple

class Config:
    """Application configuration - all settings in one place"""

    # ==================== APPLICATION INFO ====================
    APP_NAME: str = "Expense Tracker"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Your Name"

    # ==================== PATHS ====================
    BASE_DIR: Path = Path(__file__).parent
    DATA_DIR: Path = Path(os.getenv('APPDATA', '.')) / APP_NAME
    DB_DIR: Path = DATA_DIR  # Alias for backward compatibility
    DB_PATH: Path = DATA_DIR / "expense_tracker.db"
    BACKUP_DIR: Path = DATA_DIR / "backups"
    EXPORT_DIR: Path = DATA_DIR / "exports"
    LOG_DIR: Path = DATA_DIR / "logs"

    # ==================== DATABASE ====================
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    DB_ECHO: bool = False  # Set to True for SQL debugging
    DEBUG_MODE: bool = False  # Enable debug mode for development

    # ==================== UI SETTINGS ====================
    # Window
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 700
    MIN_WIDTH: int = 1000
    MIN_HEIGHT: int = 600

    # Sidebar
    SIDEBAR_WIDTH: int = 200

    # Theme
    APPEARANCE_MODE: str = "dark"  # "dark" or "light"
    COLOR_THEME: str = "blue"  # "blue", "green", "dark-blue"

    # ==================== COLORS ====================
    # Primary colors
    PRIMARY: str = "#1f538d"
    SECONDARY: str = "#14375e"

    # Status colors
    SUCCESS: str = "#2fa572"    # Green (credits)
    DANGER: str = "#e74c3c"     # Red (debits)
    WARNING: str = "#f39c12"    # Orange
    INFO: str = "#3498db"       # Blue

    # UI colors
    BG_DARK: str = "#1a1a1a"
    BG_LIGHT: str = "#f5f5f5"
    CARD_DARK: str = "#2b2b2b"
    CARD_LIGHT: str = "#ffffff"
    TEXT_DARK: str = "#ffffff"
    TEXT_LIGHT: str = "#000000"

    # Color dictionary for easy access
    COLORS: Dict[str, str] = {
        'primary': "#1f538d",
        'primary_hover': "#16406f",
        'secondary': "#14375e",
        'secondary_hover': "#0f2840",
        'success': "#2fa572",
        'error': "#e74c3c",
        'warning': "#f39c12",
        'info': "#3498db",
        'background': "#1a1a1a",
        'surface': "#2b2b2b",
        'card': "#2b2b2b",  # Alias for surface
        'border': "#404040",
        'text': "#ffffff",  # Alias for text_primary
        'text_primary': "#ffffff",
        'text_secondary': "#b0b0b0"
    }

    # ==================== FONTS ====================
    FONT_FAMILY: str = "Segoe UI"

    FONT_SIZES: Dict[str, int] = {
        'title': 24,
        'heading': 18,
        'subheading': 16,
        'body': 14,
        'small': 12,
        'tiny': 10
    }

    FONT_WEIGHTS: Dict[str, str] = {
        'normal': 'normal',
        'bold': 'bold'
    }

    # ==================== BUSINESS RULES ====================
    # Currencies
    CURRENCIES: list = ["INR", "USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    DEFAULT_CURRENCY: str = "INR"
    CURRENCY_CODE: str = "INR"  # Alias for backward compatibility

    # Account types - removed hardcoding, users manage these from UI

    # Transaction types
    TRANSACTION_TYPES: list = ["Credit", "Debit", "Transfer"]

    # Transaction directions
    DIRECTIONS: list = ["Debit", "Credit"]

    # Date formats (Indian format)
    DATE_FORMAT: str = "%d-%m-%Y"  # DD-MM-YYYY
    DISPLAY_DATE_FORMAT: str = "%d %b %Y"  # 03 Jan 2026
    DATETIME_FORMAT: str = "%d-%m-%Y %H:%M:%S"

    # Currency format (Indian Rupee)
    CURRENCY_SYMBOL: str = "₹"
    DECIMAL_PLACES: int = 2

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    # Validation
    MAX_DESCRIPTION_LENGTH: int = 255
    MAX_NOTES_LENGTH: int = 1000
    MAX_NAME_LENGTH: int = 100
    MIN_AMOUNT: float = 0.01
    MAX_AMOUNT: float = 999999999.99

    # ==================== CATEGORY ICONS ====================
    CATEGORY_ICONS: Dict[str, str] = {
        'Housing': '🏠',
        'Utilities': '⚡',
        'Groceries': '🛒',
        'Dining': '🍔',
        'Transportation': '🚗',
        'Healthcare': '🏥',
        'Insurance': '🛡️',
        'Personal Care': '💆',
        'Entertainment': '🎬',
        'Shopping': '🛍️',
        'Education': '📚',
        'Travel': '✈️',
        'Subscriptions': '🔄',
        'Gifts': '🎁',
        'Fees': '💳',
        'Other': '📌',
        'Salary': '💰',
        'Business': '💼',
        'Investments': '📈',
        'Rental': '🏠',
        'Freelance': '💻',
        'Interest': '💵',
        'Refunds': '↩️',
    }

    # Default category colors
    CATEGORY_COLORS: Dict[str, str] = {
        'Housing': '#FF6B6B',
        'Utilities': '#4ECDC4',
        'Groceries': '#45B7D1',
        'Dining': '#FFA07A',
        'Transportation': '#98D8C8',
        'Healthcare': '#FF69B4',
        'Insurance': '#87CEEB',
        'Personal Care': '#DDA0DD',
        'Entertainment': '#F7DC6F',
        'Shopping': '#BB8FCE',
        'Education': '#85C1E2',
        'Travel': '#52BE80',
        'Subscriptions': '#EC7063',
        'Gifts': '#F8B500',
        'Fees': '#E74C3C',
        'Other': '#95A5A6',
        'Salary': '#2ECC71',
        'Business': '#3498DB',
        'Investments': '#9B59B6',
        'Rental': '#1ABC9C',
        'Freelance': '#F39C12',
        'Interest': '#27AE60',
        'Refunds': '#16A085',
    }

    # ==================== METHODS ====================
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist"""
        for directory in [cls.DATA_DIR, cls.BACKUP_DIR, cls.EXPORT_DIR, cls.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_font(cls, size_key: str = 'body', weight: str = 'normal') -> Tuple[str, int, str]:
        """
        Get font configuration

        Args:
            size_key: Key from FONT_SIZES dict
            weight: 'normal' or 'bold'

        Returns:
            Tuple of (family, size, weight)
        """
        size = cls.FONT_SIZES.get(size_key, cls.FONT_SIZES['body'])
        return (cls.FONT_FAMILY, size, weight)

    @classmethod
    def format_currency(cls, amount: float) -> str:
        """Format amount as currency string"""
        return f"{cls.CURRENCY_SYMBOL}{amount:,.{cls.DECIMAL_PLACES}f}"

    @classmethod
    def get_category_icon(cls, category_name: str) -> str:
        """Get icon for category, or default"""
        return cls.CATEGORY_ICONS.get(category_name, '📌')

    @classmethod
    def get_category_color(cls, category_name: str) -> str:
        """Get color for category, or default"""
        return cls.CATEGORY_COLORS.get(category_name, '#95A5A6')


# Initialize directories on import
Config.ensure_directories()
