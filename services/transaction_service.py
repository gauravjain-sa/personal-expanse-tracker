"""
Transaction Service
Business logic for transaction management
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime

from models import Transaction
from repositories import TransactionRepository, AccountRepository, TagRepository
from config import Config


class TransactionService:
    """Service for transaction business logic"""

    def __init__(self):
        """Initialize TransactionService"""
        self.transaction_repo = TransactionRepository()
        self.account_repo = AccountRepository()
        self.tag_repo = TagRepository()

    def create_transaction(
        self,
        date: date,
        amount: float,
        transaction_type: str,
        account_id: int,
        category_id: Optional[int] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        merchant: Optional[str] = None,
        tag_ids: Optional[List[int]] = None
    ) -> Optional[Transaction]:
        """
        Create new transaction and update account balance

        Args:
            date: Transaction date
            amount: Amount (positive)
            transaction_type: 'income' or 'expense'
            account_id: Account ID
            category_id: Category ID (optional)
            description: Description (optional)
            notes: Notes (optional)
            merchant: Merchant name (optional)
            tag_ids: List of tag IDs (optional)

        Returns:
            Created transaction or None if failed
        """
        try:
            # Validate transaction type
            if transaction_type not in ['credit', 'debit', 'transfer']:
                print(f"Invalid transaction type: {transaction_type}")
                return None

            # Validate account
            account = self.account_repo.get_by_id(account_id)
            if not account:
                print(f"Account not found: {account_id}")
                return None

            # Create transaction
            transaction = Transaction(
                date=date,
                amount=amount,
                transaction_type=transaction_type,
                account_id=account_id,
                category_id=category_id,
                description=description,
                notes=notes,
                merchant=merchant
            )

            # Save transaction
            created_transaction = self.transaction_repo.create(transaction)
            if not created_transaction:
                return None

            # Update account balance
            if transaction_type == 'credit':
                self.account_repo.update_balance(account_id, amount, 'add')
            elif transaction_type == 'debit':
                self.account_repo.update_balance(account_id, amount, 'subtract')

            # Add tags if provided
            if tag_ids:
                for tag_id in tag_ids:
                    self.tag_repo.add_tag_to_transaction(created_transaction.id, tag_id)

            return created_transaction

        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None

    def create_transfer(
        self,
        date: date,
        amount: float,
        from_account_id: int,
        to_account_id: int,
        description: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[Transaction]:
        """
        Create transfer between accounts

        Args:
            date: Transfer date
            amount: Transfer amount
            from_account_id: Source account ID
            to_account_id: Destination account ID
            description: Description (optional)
            notes: Notes (optional)

        Returns:
            Created transaction or None if failed
        """
        try:
            # Validate accounts
            from_account = self.account_repo.get_by_id(from_account_id)
            to_account = self.account_repo.get_by_id(to_account_id)

            if not from_account or not to_account:
                print("One or both accounts not found")
                return None

            if from_account_id == to_account_id:
                print("Cannot transfer to same account")
                return None

            # Create transfer transaction
            transaction = Transaction(
                date=date,
                amount=amount,
                transaction_type='transfer',
                account_id=from_account_id,
                is_transfer=True,
                transfer_to_account_id=to_account_id,
                description=description or f"Transfer to {to_account.name}",
                notes=notes
            )

            # Save transaction
            created_transaction = self.transaction_repo.create(transaction)
            if not created_transaction:
                return None

            # Update account balances
            self.account_repo.update_balance(from_account_id, amount, 'subtract')
            self.account_repo.update_balance(to_account_id, amount, 'add')

            return created_transaction

        except Exception as e:
            print(f"Error creating transfer: {e}")
            return None

    def update_transaction(
        self,
        transaction_id: int,
        date: Optional[date] = None,
        amount: Optional[float] = None,
        category_id: Optional[int] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        merchant: Optional[str] = None
    ) -> bool:
        """
        Update transaction (handles balance adjustments)

        Args:
            transaction_id: Transaction ID
            date: New date (optional)
            amount: New amount (optional)
            category_id: New category ID (optional)
            description: New description (optional)
            notes: New notes (optional)
            merchant: New merchant (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            transaction = self.transaction_repo.get_by_id(transaction_id)
            if not transaction:
                print(f"Transaction not found: {transaction_id}")
                return False

            # If amount changed, adjust account balance
            if amount and amount != transaction.amount:
                old_amount = transaction.amount
                difference = amount - old_amount

                # Reverse old transaction effect
                if transaction.transaction_type == 'credit':
                    self.account_repo.update_balance(
                        transaction.account_id,
                        old_amount,
                        'subtract'
                    )
                    # Apply new amount
                    self.account_repo.update_balance(
                        transaction.account_id,
                        amount,
                        'add'
                    )
                elif transaction.transaction_type == 'debit':
                    self.account_repo.update_balance(
                        transaction.account_id,
                        old_amount,
                        'add'
                    )
                    # Apply new amount
                    self.account_repo.update_balance(
                        transaction.account_id,
                        amount,
                        'subtract'
                    )

                transaction.amount = amount

            # Update other fields
            if date:
                transaction.date = date

            if category_id is not None:
                transaction.category_id = category_id

            if description is not None:
                transaction.description = description

            if notes is not None:
                transaction.notes = notes

            if merchant is not None:
                transaction.merchant = merchant

            return self.transaction_repo.update(transaction)

        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete transaction and adjust account balance

        Args:
            transaction_id: Transaction ID

        Returns:
            True if successful, False otherwise
        """
        try:
            transaction = self.transaction_repo.get_by_id(transaction_id)
            if not transaction:
                return False

            # Reverse transaction effect on account balance
            if transaction.transaction_type == 'credit':
                self.account_repo.update_balance(
                    transaction.account_id,
                    transaction.amount,
                    'subtract'
                )
            elif transaction.transaction_type == 'debit':
                self.account_repo.update_balance(
                    transaction.account_id,
                    transaction.amount,
                    'add'
                )
            elif transaction.is_transfer and transaction.transfer_to_account_id:
                # Reverse both sides of transfer
                self.account_repo.update_balance(
                    transaction.account_id,
                    transaction.amount,
                    'add'
                )
                self.account_repo.update_balance(
                    transaction.transfer_to_account_id,
                    transaction.amount,
                    'subtract'
                )

            # Delete transaction
            return self.transaction_repo.delete(transaction_id)

        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID"""
        return self.transaction_repo.get_by_id(transaction_id)

    def get_transactions_by_date_range(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None
    ) -> List[Transaction]:
        """Get transactions within date range"""
        return self.transaction_repo.get_by_date_range(
            start_date,
            end_date,
            account_id,
            category_id
        )

    def get_recent_transactions(self, limit: int = 10, account_id: Optional[int] = None) -> List[Transaction]:
        """Get most recent transactions"""
        return self.transaction_repo.get_recent(limit, account_id)

    def search_transactions(
        self,
        search_term: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Transaction]:
        """Search transactions"""
        return self.transaction_repo.search(search_term, start_date, end_date)

    def get_income_expense_summary(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None
    ) -> Dict[str, float]:
        """Get income/expense summary for date range"""
        return self.transaction_repo.get_income_expense_summary(
            start_date,
            end_date,
            account_id
        )

    def add_tags_to_transaction(self, transaction_id: int, tag_ids: List[int]) -> bool:
        """
        Add multiple tags to transaction

        Args:
            transaction_id: Transaction ID
            tag_ids: List of tag IDs

        Returns:
            True if successful, False otherwise
        """
        try:
            for tag_id in tag_ids:
                self.tag_repo.add_tag_to_transaction(transaction_id, tag_id)
            return True
        except Exception as e:
            print(f"Error adding tags: {e}")
            return False

    def remove_tag_from_transaction(self, transaction_id: int, tag_id: int) -> bool:
        """Remove tag from transaction"""
        return self.tag_repo.remove_tag_from_transaction(transaction_id, tag_id)

    def get_transaction_details(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed transaction information

        Args:
            transaction_id: Transaction ID

        Returns:
            Dictionary with transaction details
        """
        try:
            transaction = self.transaction_repo.get_by_id(transaction_id)
            if not transaction:
                return None

            return {
                'id': transaction.id,
                'date': transaction.date,
                'date_formatted': transaction.date_formatted,
                'amount': transaction.amount,
                'amount_formatted': transaction.amount_formatted,
                'transaction_type': transaction.transaction_type,
                'direction': transaction.direction,
                'account': transaction.account.name if transaction.account else None,
                'category': transaction.category.full_name if transaction.category else None,
                'description': transaction.description,
                'notes': transaction.notes,
                'merchant': transaction.merchant,
                'tags': [tag.name for tag in transaction.tags],
                'is_transfer': transaction.is_transfer,
                'created_at': transaction.created_at
            }

        except Exception as e:
            print(f"Error getting transaction details: {e}")
            return None

    def get_transactions_paginated(
        self,
        page: int = 1,
        page_size: int = 50,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated transactions with filters

        Args:
            page: Page number (1-indexed)
            page_size: Number of transactions per page
            start_date: Start date filter (optional)
            end_date: End date filter (optional)
            account_id: Account ID filter (optional)
            category_id: Category ID filter (optional)
            transaction_type: Type filter ('income', 'expense', or None for all)
            search_term: Search term for description/merchant/notes (optional)

        Returns:
            Dictionary with:
                - transactions: List of Transaction objects
                - total: Total number of transactions matching filters
                - page: Current page number
                - pages: Total number of pages
                - page_size: Number of transactions per page
        """
        try:
            # Get filtered transactions from repository
            from sqlalchemy import and_, or_
            from models import Transaction

            query = self.transaction_repo.session.query(Transaction)

            # Apply filters
            filters = []

            if start_date:
                filters.append(Transaction.date >= start_date)

            if end_date:
                filters.append(Transaction.date <= end_date)

            if account_id:
                filters.append(Transaction.account_id == account_id)

            if category_id:
                filters.append(Transaction.category_id == category_id)

            if transaction_type:
                filters.append(Transaction.transaction_type == transaction_type.lower())

            if search_term:
                search_filter = or_(
                    Transaction.description.ilike(f'%{search_term}%'),
                    Transaction.notes.ilike(f'%{search_term}%'),
                    Transaction.merchant.ilike(f'%{search_term}%')
                )
                filters.append(search_filter)

            if filters:
                query = query.filter(and_(*filters))

            # Get total count
            total = query.count()

            # Calculate pagination
            total_pages = (total + page_size - 1) // page_size if total > 0 else 1
            offset = (page - 1) * page_size

            # Get paginated results
            transactions = query.order_by(Transaction.date.desc())\
                .limit(page_size)\
                .offset(offset)\
                .all()

            return {
                'transactions': transactions,
                'total': total,
                'page': page,
                'pages': total_pages,
                'page_size': page_size
            }

        except Exception as e:
            print(f"Error getting paginated transactions: {e}")
            return {
                'transactions': [],
                'total': 0,
                'page': page,
                'pages': 1,
                'page_size': page_size
            }

    @staticmethod
    def get_financial_year_dates(year: int) -> tuple:
        """
        Get start and end dates for Indian Financial Year

        Indian FY runs from April 1 to March 31
        FY 2025-26 means: April 1, 2025 to March 31, 2026

        Args:
            year: Starting year of FY (e.g., 2025 for FY 2025-26)

        Returns:
            Tuple of (start_date, end_date)
        """
        from datetime import date
        start_date = date(year, 4, 1)  # April 1
        end_date = date(year + 1, 3, 31)  # March 31 of next year
        return start_date, end_date

    @staticmethod
    def get_current_financial_year() -> int:
        """
        Get current Indian Financial Year starting year

        Examples:
            - If today is 2025-05-15, returns 2025 (FY 2025-26)
            - If today is 2026-02-10, returns 2025 (FY 2025-26)
            - If today is 2026-04-05, returns 2026 (FY 2026-27)

        Returns:
            Starting year of current FY
        """
        from datetime import date
        today = date.today()
        if today.month >= 4:  # April or later
            return today.year
        else:  # January-March (belongs to previous year's FY)
            return today.year - 1

    def get_credits_debits_summary(
        self,
        transactions: List[Transaction]
    ) -> Dict[str, Any]:
        """
        Calculate credits/debits summary for accounting view

        Args:
            transactions: List of transactions

        Returns:
            Dictionary with:
                - credits: List of income transactions
                - debits: List of expense transactions
                - total_credits: Sum of income amounts
                - total_debits: Sum of expense amounts
                - net_balance: Credits - Debits
                - credit_count: Number of income transactions
                - debit_count: Number of expense transactions
        """
        from decimal import Decimal

        credits = []
        debits = []
        total_credits = Decimal('0')
        total_debits = Decimal('0')

        for transaction in transactions:
            if transaction.transaction_type == 'credit':
                credits.append(transaction)
                total_credits += Decimal(str(transaction.amount))
            elif transaction.transaction_type == 'debit':
                debits.append(transaction)
                total_debits += Decimal(str(transaction.amount))

        net_balance = total_credits - total_debits

        return {
            'credits': credits,
            'debits': debits,
            'total_credits': float(total_credits),
            'total_debits': float(total_debits),
            'net_balance': float(net_balance),
            'credit_count': len(credits),
            'debit_count': len(debits)
        }
