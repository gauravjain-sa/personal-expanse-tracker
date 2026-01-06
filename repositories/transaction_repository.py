"""
Transaction Repository
Data access layer for Transaction operations with advanced filtering
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy import func, and_, or_, extract
from sqlalchemy.exc import SQLAlchemyError

from models import Transaction, Category, Account, Tag
from .base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction entity with advanced query methods"""

    def __init__(self):
        """Initialize TransactionRepository"""
        super().__init__(Transaction)

    def get_by_date_range(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None
    ) -> List[Transaction]:
        """
        Get transactions within date range with optional filters

        Args:
            start_date: Start date
            end_date: End date
            account_id: Optional account filter
            category_id: Optional category filter

        Returns:
            List of transactions
        """
        try:
            query = self.session.query(Transaction).filter(
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )

            if account_id:
                query = query.filter(Transaction.account_id == account_id)

            if category_id:
                query = query.filter(Transaction.category_id == category_id)

            return query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error getting transactions by date range: {e}")
            return []

    def get_by_type(self, transaction_type: str) -> List[Transaction]:
        """
        Get all transactions of specific type

        Args:
            transaction_type: Transaction type ('credit', 'debit', 'transfer')

        Returns:
            List of transactions
        """
        return self.find_by_field('transaction_type', transaction_type)

    def get_by_account(self, account_id: int, limit: Optional[int] = None) -> List[Transaction]:
        """
        Get all transactions for specific account

        Args:
            account_id: Account ID
            limit: Optional limit on number of results

        Returns:
            List of transactions
        """
        try:
            query = self.session.query(Transaction).filter(
                Transaction.account_id == account_id
            ).order_by(Transaction.date.desc(), Transaction.created_at.desc())

            if limit:
                query = query.limit(limit)

            return query.all()
        except SQLAlchemyError as e:
            print(f"Error getting transactions by account: {e}")
            return []

    def get_by_category(self, category_id: int, limit: Optional[int] = None) -> List[Transaction]:
        """
        Get all transactions for specific category

        Args:
            category_id: Category ID
            limit: Optional limit on number of results

        Returns:
            List of transactions
        """
        try:
            query = self.session.query(Transaction).filter(
                Transaction.category_id == category_id
            ).order_by(Transaction.date.desc(), Transaction.created_at.desc())

            if limit:
                query = query.limit(limit)

            return query.all()
        except SQLAlchemyError as e:
            print(f"Error getting transactions by category: {e}")
            return []

    def get_recent(self, limit: int = 10, account_id: Optional[int] = None) -> List[Transaction]:
        """
        Get most recent transactions

        Args:
            limit: Number of transactions to return
            account_id: Optional account filter

        Returns:
            List of recent transactions
        """
        try:
            query = self.session.query(Transaction)

            if account_id:
                query = query.filter(Transaction.account_id == account_id)

            return query.order_by(
                Transaction.date.desc(),
                Transaction.created_at.desc()
            ).limit(limit).all()
        except SQLAlchemyError as e:
            print(f"Error getting recent transactions: {e}")
            return []

    def search(
        self,
        search_term: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Transaction]:
        """
        Search transactions by description, notes, or merchant

        Args:
            search_term: Search term
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of matching transactions
        """
        try:
            query = self.session.query(Transaction).filter(
                or_(
                    Transaction.description.ilike(f'%{search_term}%'),
                    Transaction.notes.ilike(f'%{search_term}%'),
                    Transaction.merchant.ilike(f'%{search_term}%')
                )
            )

            if start_date:
                query = query.filter(Transaction.date >= start_date)

            if end_date:
                query = query.filter(Transaction.date <= end_date)

            return query.order_by(Transaction.date.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error searching transactions: {e}")
            return []

    def get_total_by_type(
        self,
        transaction_type: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[int] = None
    ) -> float:
        """
        Calculate total amount for specific transaction type

        Args:
            transaction_type: Transaction type
            start_date: Optional start date
            end_date: Optional end date
            account_id: Optional account filter

        Returns:
            Total amount
        """
        try:
            query = self.session.query(func.sum(Transaction.amount)).filter(
                Transaction.transaction_type == transaction_type
            )

            if start_date:
                query = query.filter(Transaction.date >= start_date)

            if end_date:
                query = query.filter(Transaction.date <= end_date)

            if account_id:
                query = query.filter(Transaction.account_id == account_id)

            result = query.scalar()
            return result if result else 0.0
        except SQLAlchemyError as e:
            print(f"Error calculating total: {e}")
            return 0.0

    def get_income_expense_summary(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Get credit and debit summary for date range

        Args:
            start_date: Start date
            end_date: End date
            account_id: Optional account filter

        Returns:
            Dictionary with income (credit), expense (debit), and balance
        """
        try:
            income = self.get_total_by_type('credit', start_date, end_date, account_id)
            expense = self.get_total_by_type('debit', start_date, end_date, account_id)

            return {
                'income': income,
                'expense': expense,
                'balance': income - expense,
                'start_date': start_date,
                'end_date': end_date
            }
        except Exception as e:
            print(f"Error getting credit/debit summary: {e}")
            return {'income': 0.0, 'expense': 0.0, 'balance': 0.0}

    def get_category_breakdown(
        self,
        start_date: date,
        end_date: date,
        transaction_type: str = 'debit'
    ) -> List[Dict[str, Any]]:
        """
        Get spending/income breakdown by category

        Args:
            start_date: Start date
            end_date: End date
            transaction_type: Transaction type ('credit' or 'debit')

        Returns:
            List of dictionaries with category totals
        """
        try:
            results = self.session.query(
                Category.name,
                Category.color,
                Category.icon,
                func.sum(Transaction.amount).label('total'),
                func.count(Transaction.id).label('count')
            ).join(
                Category, Transaction.category_id == Category.id
            ).filter(
                Transaction.date >= start_date,
                Transaction.date <= end_date,
                Transaction.transaction_type == transaction_type
            ).group_by(
                Category.id
            ).order_by(
                func.sum(Transaction.amount).desc()
            ).all()

            return [
                {
                    'category': row.name,
                    'color': row.color,
                    'icon': row.icon,
                    'total': row.total,
                    'count': row.count
                }
                for row in results
            ]
        except SQLAlchemyError as e:
            print(f"Error getting category breakdown: {e}")
            return []

    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get summary for specific month

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary with monthly statistics
        """
        try:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)

            summary = self.get_income_expense_summary(start_date, end_date)

            # Get transaction count
            count = self.session.query(func.count(Transaction.id)).filter(
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).scalar()

            summary['transaction_count'] = count
            summary['year'] = year
            summary['month'] = month

            return summary
        except Exception as e:
            print(f"Error getting monthly summary: {e}")
            return {}

    def get_daily_totals(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """
        Get daily credit and debit totals

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            List of dictionaries with daily totals (income=credits, expense=debits)
        """
        try:
            results = self.session.query(
                Transaction.date,
                Transaction.transaction_type,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).group_by(
                Transaction.date,
                Transaction.transaction_type
            ).order_by(
                Transaction.date
            ).all()

            # Organize by date
            daily_data = {}
            for row in results:
                date_str = row.date.isoformat()
                if date_str not in daily_data:
                    daily_data[date_str] = {'date': row.date, 'income': 0.0, 'expense': 0.0}

                if row.transaction_type == 'credit':
                    daily_data[date_str]['income'] = row.total
                elif row.transaction_type == 'debit':
                    daily_data[date_str]['expense'] = row.total

            return list(daily_data.values())
        except SQLAlchemyError as e:
            print(f"Error getting daily totals: {e}")
            return []
