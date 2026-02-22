"""
Configuration Module
Centralized configuration for the application - NO HARDCODING
Reads application settings from config.ini and UI/theme settings from theme.ini.
This file acts as a wrapper — all consuming code uses the Config class unchanged.
"""
import os
import configparser
from pathlib import Path
from typing import Dict, Tuple

_CONFIG_DIR = Path(__file__).parent


def _load_ini(filename):
    """Load an .ini file using RawConfigParser (no interpolation issues with % in date formats)"""
    parser = configparser.RawConfigParser()
    parser.optionxform = str  # Preserve key case for category names etc.
    parser.read(str(_CONFIG_DIR / filename), encoding='utf-8')
    return parser


_app = _load_ini('config.ini')
_theme = _load_ini('theme.ini')


# --- helpers for _app (application config) ---

def _get(section, key, fallback=None):
    return _app.get(section, key, fallback=fallback)


def _get_int(section, key, fallback=0):
    return _app.getint(section, key, fallback=fallback)


def _get_float(section, key, fallback=0.0):
    return _app.getfloat(section, key, fallback=fallback)


def _get_bool(section, key, fallback=False):
    return _app.getboolean(section, key, fallback=fallback)


def _get_list(section, key, fallback=None):
    val = _app.get(section, key, fallback=None)
    if val is None:
        return fallback or []
    return [item.strip() for item in val.split(',')]


# --- helpers for _theme (UI/theme config) ---

def _tget(section, key, fallback=None):
    return _theme.get(section, key, fallback=fallback)


def _tget_int(section, key, fallback=0):
    return _theme.getint(section, key, fallback=fallback)


def _tget_section_dict(section, fallback=None):
    if _theme.has_section(section):
        return dict(_theme.items(section))
    return fallback or {}


class Config:
    """Application configuration - all settings in one place"""

    # ==================== APPLICATION INFO ====================
    APP_NAME: str = _get('application', 'name', 'Expense Tracker')
    VERSION: str = _get('application', 'version', '1.0.0')
    AUTHOR: str = _get('application', 'author', 'Your Name')

    # ==================== PATHS ====================
    BASE_DIR: Path = _CONFIG_DIR
    DATA_DIR: Path = Path(os.getenv('APPDATA', '.')) / APP_NAME
    DB_DIR: Path = DATA_DIR
    DB_PATH: Path = DATA_DIR / "expense_tracker.db"
    BACKUP_DIR: Path = DATA_DIR / "backups"
    EXPORT_DIR: Path = DATA_DIR / "exports"
    LOG_DIR: Path = DATA_DIR / "logs"

    # ==================== DATABASE ====================
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    DB_ECHO: bool = _get_bool('database', 'echo', False)
    DEBUG_MODE: bool = _get_bool('database', 'debug_mode', False)

    # ==================== UI SETTINGS (from theme.ini) ====================
    # Window
    WINDOW_WIDTH: int = _tget_int('window', 'width', 1200)
    WINDOW_HEIGHT: int = _tget_int('window', 'height', 700)
    MIN_WIDTH: int = _tget_int('window', 'min_width', 1000)
    MIN_HEIGHT: int = _tget_int('window', 'min_height', 600)

    # Sidebar
    SIDEBAR_WIDTH: int = _tget_int('window', 'sidebar_width', 200)

    # Theme
    APPEARANCE_MODE: str = _tget('theme', 'appearance_mode', 'dark')
    COLOR_THEME: str = _tget('theme', 'color_theme', 'blue')

    # ==================== COLORS (from theme.ini) ====================
    # Primary colors
    PRIMARY: str = _tget('colors', 'primary', '#1f538d')
    SECONDARY: str = _tget('colors', 'secondary', '#14375e')

    # Status colors
    SUCCESS: str = _tget('colors', 'success', '#2fa572')
    DANGER: str = _tget('colors', 'danger', '#e74c3c')
    WARNING: str = _tget('colors', 'warning', '#f39c12')
    INFO: str = _tget('colors', 'info', '#3498db')

    # UI colors
    BG_DARK: str = _tget('colors', 'bg_dark', '#1a1a1a')
    BG_LIGHT: str = _tget('colors', 'bg_light', '#f5f5f5')
    CARD_DARK: str = _tget('colors', 'card_dark', '#2b2b2b')
    CARD_LIGHT: str = _tget('colors', 'card_light', '#ffffff')
    TEXT_DARK: str = _tget('colors', 'text_dark', '#ffffff')
    TEXT_LIGHT: str = _tget('colors', 'text_light', '#000000')

    # Color dictionary for easy access
    COLORS: Dict[str, str] = _tget_section_dict('color_palette', {
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
        'card': "#2b2b2b",
        'border': "#404040",
        'text': "#ffffff",
        'text_primary': "#ffffff",
        'text_secondary': "#b0b0b0"
    })

    # ==================== FONTS (from theme.ini) ====================
    FONT_FAMILY: str = _tget('fonts', 'family', 'Segoe UI')

    FONT_SIZES: Dict[str, int] = {
        k: int(v) for k, v in _tget_section_dict('font_sizes', {
            'title': '24', 'heading': '18', 'subheading': '16',
            'body': '14', 'small': '12', 'tiny': '10'
        }).items()
    }

    FONT_WEIGHTS: Dict[str, str] = _tget_section_dict('font_weights', {
        'normal': 'normal',
        'bold': 'bold'
    })

    # ==================== BUSINESS RULES (from config.ini) ====================
    # Currencies
    CURRENCIES: list = _get_list('currency', 'currencies',
                                 ['INR', 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'])
    DEFAULT_CURRENCY: str = _get('currency', 'default', 'INR')
    CURRENCY_CODE: str = _get('currency', 'code', 'INR')

    # Transaction types
    TRANSACTION_TYPES: list = _get_list('transactions', 'types',
                                        ['Credit', 'Debit', 'Transfer'])

    # Transaction directions
    DIRECTIONS: list = _get_list('transactions', 'directions', ['Debit', 'Credit'])

    # Date formats
    DATE_FORMAT: str = _get('date_formats', 'date', '%d-%m-%Y')
    DISPLAY_DATE_FORMAT: str = _get('date_formats', 'display_date', '%d %b %Y')
    DATETIME_FORMAT: str = _get('date_formats', 'datetime', '%d-%m-%Y %H:%M:%S')

    # Currency format
    CURRENCY_SYMBOL: str = _get('currency', 'symbol', '₹')
    DECIMAL_PLACES: int = _get_int('currency', 'decimal_places', 2)

    # Pagination
    DEFAULT_PAGE_SIZE: int = _get_int('pagination', 'default_page_size', 50)
    MAX_PAGE_SIZE: int = _get_int('pagination', 'max_page_size', 100)

    # Validation
    MAX_DESCRIPTION_LENGTH: int = _get_int('validation', 'max_description_length', 255)
    MAX_NOTES_LENGTH: int = _get_int('validation', 'max_notes_length', 1000)
    MAX_NAME_LENGTH: int = _get_int('validation', 'max_name_length', 100)
    MIN_AMOUNT: float = _get_float('validation', 'min_amount', 0.01)
    MAX_AMOUNT: float = _get_float('validation', 'max_amount', 999999999.99)

    # ==================== CATEGORY COLORS (from theme.ini) ====================
    CATEGORY_COLORS: Dict[str, str] = _tget_section_dict('category_colors', {
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
    })

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
        """Get icon for category - returns 2-letter code based on first two letters"""
        if not category_name:
            return "IC"
        return category_name[:2].upper()

    @classmethod
    def get_category_color(cls, category_name: str) -> str:
        """Get color for category, or default"""
        return cls.CATEGORY_COLORS.get(category_name, '#95A5A6')


# Initialize directories on import
Config.ensure_directories()
