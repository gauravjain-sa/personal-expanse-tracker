"""
Category Model
Represents debit/credit categories with hierarchical support
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List

from .base import Base, ModelMixin


class Category(Base, ModelMixin):
    """Category model - hierarchical debit/credit categories"""

    __tablename__ = 'categories'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=True)  # Optional: user-defined type (e.g., 'credit', 'debit', or custom)

    # Hierarchy
    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)

    # Visual
    color = Column(String(7))  # Hex color code #RRGGBB
    icon = Column(String(10))  # Emoji or icon identifier

    # Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Additional
    description = Column(String(255))

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    transactions = relationship("Transaction", back_populates="category")

    def __init__(self, name: str, type: str = None, **kwargs):
        """
        Initialize Category

        Args:
            name: Category name
            type: Optional user-defined type (e.g., 'credit', 'debit', or custom)
            **kwargs: Additional fields (parent_id, color, icon, etc.)
        """
        self.name = name
        self.type = type.lower() if type else None

        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # Set default color and icon from config
        if not self.color:
            from config import Config
            self.color = Config.get_category_color(name)

        if not self.icon:
            from config import Config
            self.icon = Config.get_category_icon(name)

    @property
    def full_name(self) -> str:
        """Get full name including parent (e.g., 'Housing > Rent')"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    @property
    def is_parent(self) -> bool:
        """Check if this category has children"""
        return len(self.children) > 0

    def get_all_children(self) -> List['Category']:
        """
        Get all children recursively

        Returns:
            List of all descendant categories
        """
        result = []
        for child in self.children:
            result.append(child)
            result.extend(child.get_all_children())
        return result
