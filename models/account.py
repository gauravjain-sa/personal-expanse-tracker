"""
Account Model
Represents financial accounts (bank, credit card, cash, etc.)
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from .base import Base, ModelMixin


class Account(Base, ModelMixin):
    """Account model - represents a financial account"""

    __tablename__ = 'accounts'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = Column(String(100), nullable=False, unique=True)
    account_type = Column(String(50), nullable=True)  # Optional: user-defined type

    # Financial Information
    initial_balance = Column(Float, nullable=False, default=0.0)
    current_balance = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default='USD')

    # Status
    is_active = Column(Boolean, nullable=False, default=True)

    # Additional Information
    notes = Column(String(500))

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    transactions = relationship(
        "Transaction",
        back_populates="account",
        foreign_keys="Transaction.account_id",
        cascade="all, delete-orphan"
    )

    def __init__(self, name: str, initial_balance: float = 0.0, account_type: str = None, **kwargs):
        """
        Initialize Account

        Args:
            name: Account name (required)
            initial_balance: Starting balance (default: 0.0)
            account_type: Type of account (optional, user-defined)
            **kwargs: Additional fields
        """
        self.name = name
        self.account_type = account_type
        self.initial_balance = initial_balance
        self.current_balance = initial_balance  # Start with initial balance

        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def balance_formatted(self) -> str:
        """Get formatted balance with currency symbol"""
        from config import Config
        return Config.format_currency(self.current_balance)

    def update_balance(self, amount: float, operation: str = 'add') -> None:
        """
        Update account balance

        Args:
            amount: Amount to add or subtract
            operation: 'add' or 'subtract'
        """
        if operation == 'add':
            self.current_balance += amount
        elif operation == 'subtract':
            self.current_balance -= amount
        else:
            raise ValueError(f"Invalid operation: {operation}")

    def get_transaction_count(self, session) -> int:
        """Get total number of transactions for this account"""
        return len(self.transactions)
