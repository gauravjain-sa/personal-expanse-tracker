"""
Account Service
Business logic for account management
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from models import Account
from repositories import AccountRepository
from config import Config


class AccountService:
    """Service for account business logic"""

    def __init__(self):
        """Initialize AccountService"""
        self.repository = AccountRepository()

    def create_account(
        self,
        name: str,
        initial_balance: float = 0.0,
        account_type: str = None,
        currency: str = None,
        notes: str = None
    ) -> Optional[Account]:
        """
        Create new account

        Args:
            name: Account name
            account_type: Account type
            initial_balance: Starting balance
            currency: Currency code (default from Config)
            notes: Optional notes

        Returns:
            Created account or None if failed
        """
        try:
            # Check if account with same name exists
            existing = self.repository.get_by_name(name)
            if existing:
                print(f"Account with name '{name}' already exists")
                return None

            # Create account
            account = Account(
                name=name,
                account_type=account_type,
                initial_balance=initial_balance,
                currency=currency or Config.CURRENCY_CODE,
                notes=notes
            )

            return self.repository.create(account)

        except Exception as e:
            print(f"Error creating account: {e}")
            return None

    def update_account(
        self,
        account_id: int,
        name: Optional[str] = None,
        account_type: Optional[str] = None,
        notes: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> bool:
        """
        Update account details (not balance)

        Args:
            account_id: Account ID
            name: New name (optional)
            account_type: New type (optional)
            notes: New notes (optional)
            is_active: New active status (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            account = self.repository.get_by_id(account_id)
            if not account:
                print(f"Account not found: {account_id}")
                return False

            # Update fields
            if name:
                # Check name uniqueness
                existing = self.repository.get_by_name(name)
                if existing and existing.id != account_id:
                    print(f"Account with name '{name}' already exists")
                    return False
                account.name = name

            if account_type is not None:
                account.account_type = account_type

            if notes is not None:
                account.notes = notes

            if is_active is not None:
                account.is_active = is_active

            return self.repository.update(account)

        except Exception as e:
            print(f"Error updating account: {e}")
            return False

    def delete_account(self, account_id: int, force: bool = False) -> bool:
        """
        Delete account (soft delete by default)

        Args:
            account_id: Account ID
            force: If True, hard delete; otherwise soft delete

        Returns:
            True if successful, False otherwise
        """
        try:
            account = self.repository.get_by_id(account_id)
            if not account:
                return False

            # Check if account has transactions
            if len(account.transactions) > 0 and not force:
                # Soft delete to preserve transaction history
                return self.repository.soft_delete(account_id)
            else:
                # Hard delete
                return self.repository.delete(account_id)

        except Exception as e:
            print(f"Error deleting account: {e}")
            return False

    def get_account(self, account_id: int) -> Optional[Account]:
        """Get account by ID"""
        return self.repository.get_by_id(account_id)

    def get_all_accounts(self, include_inactive: bool = False) -> List[Account]:
        """Get all accounts"""
        return self.repository.get_all(include_inactive)

    def get_accounts_by_type(self, account_type: str) -> List[Account]:
        """Get accounts by type"""
        return self.repository.get_by_type(account_type)

    def get_account_summary(self, account_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed account summary

        Args:
            account_id: Account ID

        Returns:
            Dictionary with account details and statistics
        """
        try:
            account = self.repository.get_by_id(account_id)
            if not account:
                return None

            return {
                'id': account.id,
                'name': account.name,
                'type': account.account_type,
                'initial_balance': account.initial_balance,
                'current_balance': account.current_balance,
                'balance_formatted': account.balance_formatted,
                'currency': account.currency,
                'is_active': account.is_active,
                'transaction_count': len(account.transactions),
                'created_at': account.created_at,
                'notes': account.notes
            }

        except Exception as e:
            print(f"Error getting account summary: {e}")
            return None

    def get_total_net_worth(self) -> float:
        """
        Calculate total net worth across all active accounts

        Returns:
            Total balance
        """
        return self.repository.get_total_balance(include_inactive=False)

    def get_accounts_overview(self) -> List[Dict[str, Any]]:
        """
        Get overview of all accounts with balances

        Returns:
            List of account summaries
        """
        return self.repository.get_accounts_summary()

    def search_accounts(self, search_term: str) -> List[Account]:
        """Search accounts by name"""
        return self.repository.search_accounts(search_term)

    def recalculate_balance(self, account_id: int) -> bool:
        """
        Recalculate account balance from transactions
        (useful for fixing discrepancies)

        Args:
            account_id: Account ID

        Returns:
            True if successful, False otherwise
        """
        try:
            account = self.repository.get_by_id(account_id)
            if not account:
                return False

            # Calculate balance from initial balance + all transactions
            balance = account.initial_balance

            for transaction in account.transactions:
                if transaction.direction == 'credit':
                    balance += transaction.amount
                else:  # debit
                    balance -= transaction.amount

            # Update balance
            account.current_balance = balance
            return self.repository.update(account)

        except Exception as e:
            print(f"Error recalculating balance: {e}")
            return False
