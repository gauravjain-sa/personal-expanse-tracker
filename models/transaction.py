"""
Transaction Model
Represents financial transactions (credit, debit, transfer)
"""
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Optional

from .base import Base, ModelMixin


class Transaction(Base, ModelMixin):
    """Transaction model - represents a financial transaction"""

    __tablename__ = 'transactions'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Transaction Details
    date = Column(Date, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False, index=True)  # credit, debit, transfer
    direction = Column(String(10), nullable=False)  # debit, credit

    # References
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)

    # Description
    description = Column(String(255))
    notes = Column(Text)
    merchant = Column(String(100), index=True)

    # Attachments
    receipt_path = Column(String(500))

    # Transfer Specific
    is_transfer = Column(Boolean, nullable=False, default=False)
    transfer_to_account_id = Column(Integer, ForeignKey('accounts.id', ondelete='SET NULL'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    category = relationship("Category", back_populates="transactions")
    tags = relationship("Tag", secondary="transaction_tags", back_populates="transactions")

    def __init__(
        self,
        date: date,
        amount: float,
        transaction_type: str,
        account_id: int,
        **kwargs
    ):
        """
        Initialize Transaction

        Args:
            date: Transaction date
            amount: Transaction amount (always positive)
            transaction_type: 'credit', 'debit', or 'transfer'
            account_id: ID of the account
            **kwargs: Additional fields
        """
        self.date = date
        self.amount = abs(amount)  # Ensure positive
        self.transaction_type = transaction_type.lower()
        self.account_id = account_id

        # Validate type
        if self.transaction_type not in ['credit', 'debit', 'transfer']:
            raise ValueError("Type must be 'credit', 'debit', or 'transfer'")

        # Set direction based on type
        if self.transaction_type == 'credit':
            self.direction = 'credit'
        else:  # debit or transfer
            self.direction = 'debit'

        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def amount_formatted(self) -> str:
        """Get formatted amount with currency symbol and sign"""
        from config import Config
        sign = '+' if self.direction == 'credit' else '-'
        return f"{sign}{Config.format_currency(self.amount)}"

    @property
    def date_formatted(self) -> str:
        """Get formatted date"""
        from config import Config
        return self.date.strftime(Config.DISPLAY_DATE_FORMAT)

    @property
    def signed_amount(self) -> float:
        """Get amount with sign (positive for credit, negative for debit)"""
        return self.amount if self.direction == 'credit' else -self.amount

    def is_credit(self) -> bool:
        """Check if transaction is credit"""
        return self.transaction_type == 'credit'

    def is_debit(self) -> bool:
        """Check if transaction is debit"""
        return self.transaction_type == 'debit'
