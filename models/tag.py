"""
Tag Model
Represents tags for flexible transaction categorization
"""
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base, ModelMixin

# Association table for many-to-many relationship
transaction_tags = Table(
    'transaction_tags',
    Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Tag(Base, ModelMixin):
    """Tag model - flexible labels for transactions"""

    __tablename__ = 'tags'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7))  # Hex color code

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # Relationships
    transactions = relationship("Transaction", secondary=transaction_tags, back_populates="tags")

    def __init__(self, name: str, color: str = None):
        """
        Initialize Tag

        Args:
            name: Tag name
            color: Hex color code (optional)
        """
        self.name = name
        self.color = color or '#95A5A6'  # Default gray

    @property
    def transaction_count(self) -> int:
        """Get number of transactions with this tag"""
        return len(self.transactions)
