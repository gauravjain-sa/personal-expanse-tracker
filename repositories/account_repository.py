"""
Account Repository
Data access layer for Account operations
"""
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from models import Account
from .base_repository import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Repository for Account entity with specific query methods"""

    def __init__(self):
        """Initialize AccountRepository"""
        super().__init__(Account)

    def get_by_name(self, name: str) -> Optional[Account]:
        """
        Get account by name

        Args:
            name: Account name

        Returns:
            Account if found, None otherwise
        """
        return self.find_one_by_field('name', name)

    def get_by_type(self, account_type: str, include_inactive: bool = False) -> List[Account]:
        """
        Get all accounts of specific type

        Args:
            account_type: Account type (bank, credit_card, cash, etc.)
            include_inactive: Include inactive accounts

        Returns:
            List of accounts
        """
        try:
            query = self.session.query(Account).filter(Account.account_type == account_type)

            if not include_inactive:
                query = query.filter(Account.is_active == True)

            return query.all()
        except SQLAlchemyError as e:
            print(f"Error getting accounts by type: {e}")
            return []

    def get_active_accounts(self) -> List[Account]:
        """
        Get all active accounts

        Returns:
            List of active accounts
        """
        return self.get_all(include_inactive=False)

    def get_total_balance(self, include_inactive: bool = False) -> float:
        """
        Calculate total balance across all accounts

        Args:
            include_inactive: Include inactive accounts in calculation

        Returns:
            Total balance
        """
        try:
            accounts = self.get_all(include_inactive=include_inactive)
            return sum(account.current_balance for account in accounts)
        except Exception as e:
            print(f"Error calculating total balance: {e}")
            return 0.0

    def update_balance(self, account_id: int, amount: float, operation: str = 'add') -> bool:
        """
        Update account balance

        Args:
            account_id: Account ID
            amount: Amount to add or subtract
            operation: 'add' or 'subtract'

        Returns:
            True if successful, False otherwise
        """
        try:
            account = self.get_by_id(account_id)
            if account:
                account.update_balance(amount, operation)
                return self.update(account)
            return False
        except Exception as e:
            print(f"Error updating account balance: {e}")
            return False

    def get_accounts_summary(self) -> List[dict]:
        """
        Get summary of all accounts with balances

        Returns:
            List of dictionaries with account summaries
        """
        try:
            accounts = self.get_active_accounts()
            return [
                {
                    'id': account.id,
                    'name': account.name,
                    'type': account.account_type,
                    'balance': account.current_balance,
                    'balance_formatted': account.balance_formatted,
                    'currency': account.currency
                }
                for account in accounts
            ]
        except Exception as e:
            print(f"Error getting accounts summary: {e}")
            return []

    def search_accounts(self, search_term: str) -> List[Account]:
        """
        Search accounts by name

        Args:
            search_term: Search term

        Returns:
            List of matching accounts
        """
        try:
            return self.session.query(Account).filter(
                Account.name.ilike(f'%{search_term}%')
            ).all()
        except SQLAlchemyError as e:
            print(f"Error searching accounts: {e}")
            return []
