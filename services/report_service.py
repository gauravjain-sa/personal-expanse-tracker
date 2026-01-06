"""
Report Service
Business logic for reporting and analytics
"""
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
from calendar import monthrange

from repositories import TransactionRepository, AccountRepository, CategoryRepository
from config import Config


class ReportService:
    """Service for reports and analytics"""

    def __init__(self):
        """Initialize ReportService"""
        self.transaction_repo = TransactionRepository()
        self.account_repo = AccountRepository()
        self.category_repo = CategoryRepository()

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get dashboard summary with key metrics

        Returns:
            Dictionary with dashboard data
        """
        try:
            today = date.today()

            # Current month dates
            month_start = date(today.year, today.month, 1)
            month_end = today

            # Last month dates
            if today.month == 1:
                last_month_start = date(today.year - 1, 12, 1)
                last_month_end = date(today.year - 1, 12, 31)
            else:
                last_month_start = date(today.year, today.month - 1, 1)
                last_month_days = monthrange(today.year, today.month - 1)[1]
                last_month_end = date(today.year, today.month - 1, last_month_days)

            # Get summaries
            current_month = self.transaction_repo.get_income_expense_summary(
                month_start,
                month_end
            )

            last_month = self.transaction_repo.get_income_expense_summary(
                last_month_start,
                last_month_end
            )

            # Total net worth
            total_balance = self.account_repo.get_total_balance()

            # Recent transactions
            recent = self.transaction_repo.get_recent(limit=5)

            return {
                'total_balance': total_balance,
                'current_month': {
                    'income': current_month['income'],
                    'expense': current_month['expense'],
                    'balance': current_month['balance']
                },
                'last_month': {
                    'income': last_month['income'],
                    'expense': last_month['expense'],
                    'balance': last_month['balance']
                },
                'recent_transactions': [
                    {
                        'id': t.id,
                        'date': t.date_formatted,
                        'description': t.description or t.category.name if t.category else 'Unknown',
                        'amount': t.amount_formatted,
                        'type': t.transaction_type
                    }
                    for t in recent
                ]
            }

        except Exception as e:
            print(f"Error getting dashboard summary: {e}")
            return {}

    def get_monthly_report(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get detailed monthly report

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary with monthly report data
        """
        try:
            # Get monthly summary
            summary = self.transaction_repo.get_monthly_summary(year, month)

            # Get date range
            start_date = date(year, month, 1)
            days_in_month = monthrange(year, month)[1]
            end_date = date(year, month, days_in_month)

            # Category breakdown for expenses
            expense_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'expense'
            )

            # Category breakdown for income
            income_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'income'
            )

            # Daily totals
            daily_totals = self.transaction_repo.get_daily_totals(
                start_date,
                end_date
            )

            return {
                'year': year,
                'month': month,
                'summary': summary,
                'expense_by_category': expense_breakdown,
                'income_by_category': income_breakdown,
                'daily_totals': daily_totals
            }

        except Exception as e:
            print(f"Error getting monthly report: {e}")
            return {}

    def get_yearly_report(self, year: int) -> Dict[str, Any]:
        """
        Get yearly report

        Args:
            year: Year

        Returns:
            Dictionary with yearly report data
        """
        try:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

            # Overall summary
            summary = self.transaction_repo.get_income_expense_summary(
                start_date,
                end_date
            )

            # Monthly breakdown
            monthly_data = []
            for month in range(1, 13):
                month_summary = self.transaction_repo.get_monthly_summary(year, month)
                monthly_data.append({
                    'month': month,
                    'month_name': date(year, month, 1).strftime('%B'),
                    'income': month_summary.get('income', 0.0),
                    'expense': month_summary.get('expense', 0.0),
                    'balance': month_summary.get('balance', 0.0)
                })

            # Category breakdown
            expense_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'expense'
            )

            income_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'income'
            )

            return {
                'year': year,
                'summary': summary,
                'monthly_breakdown': monthly_data,
                'expense_by_category': expense_breakdown,
                'income_by_category': income_breakdown
            }

        except Exception as e:
            print(f"Error getting yearly report: {e}")
            return {}

    def get_date_range_report(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get report for custom date range

        Args:
            start_date: Start date
            end_date: End date
            account_id: Optional account filter

        Returns:
            Dictionary with report data
        """
        try:
            # Summary
            summary = self.transaction_repo.get_income_expense_summary(
                start_date,
                end_date,
                account_id
            )

            # Category breakdowns
            expense_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'expense'
            )

            income_breakdown = self.transaction_repo.get_category_breakdown(
                start_date,
                end_date,
                'income'
            )

            # Daily totals
            daily_totals = self.transaction_repo.get_daily_totals(
                start_date,
                end_date
            )

            # Transactions
            transactions = self.transaction_repo.get_by_date_range(
                start_date,
                end_date,
                account_id
            )

            return {
                'start_date': start_date,
                'end_date': end_date,
                'summary': summary,
                'expense_by_category': expense_breakdown,
                'income_by_category': income_breakdown,
                'daily_totals': daily_totals,
                'transaction_count': len(transactions)
            }

        except Exception as e:
            print(f"Error getting date range report: {e}")
            return {}

    def get_category_report(
        self,
        category_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Get detailed report for specific category

        Args:
            category_id: Category ID
            start_date: Optional start date
            end_date: Optional end date

        Returns:
            Dictionary with category report
        """
        try:
            category = self.category_repo.get_by_id(category_id)
            if not category:
                return {}

            # Get transactions
            if start_date and end_date:
                transactions = self.transaction_repo.get_by_date_range(
                    start_date,
                    end_date,
                    category_id=category_id
                )
            else:
                transactions = self.transaction_repo.get_by_category(category_id)

            # Calculate totals
            total_amount = sum(t.amount for t in transactions)
            avg_amount = total_amount / len(transactions) if transactions else 0.0

            return {
                'category_id': category.id,
                'category_name': category.full_name,
                'category_type': category.type,
                'transaction_count': len(transactions),
                'total_amount': total_amount,
                'average_amount': avg_amount,
                'transactions': [
                    {
                        'id': t.id,
                        'date': t.date_formatted,
                        'amount': t.amount,
                        'description': t.description,
                        'account': t.account.name if t.account else None
                    }
                    for t in transactions
                ]
            }

        except Exception as e:
            print(f"Error getting category report: {e}")
            return {}

    def get_account_report(
        self,
        account_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Get detailed report for specific account

        Args:
            account_id: Account ID
            start_date: Optional start date
            end_date: Optional end date

        Returns:
            Dictionary with account report
        """
        try:
            account = self.account_repo.get_by_id(account_id)
            if not account:
                return {}

            # Get transactions
            if start_date and end_date:
                transactions = self.transaction_repo.get_by_date_range(
                    start_date,
                    end_date,
                    account_id=account_id
                )
            else:
                transactions = self.transaction_repo.get_by_account(account_id)

            # Calculate credits/debits (income/expense)
            income = sum(t.amount for t in transactions if t.transaction_type == 'credit')
            expense = sum(t.amount for t in transactions if t.transaction_type == 'debit')

            return {
                'account_id': account.id,
                'account_name': account.name,
                'account_type': account.account_type,
                'current_balance': account.current_balance,
                'transaction_count': len(transactions),
                'total_income': income,
                'total_expense': expense,
                'net_change': income - expense
            }

        except Exception as e:
            print(f"Error getting account report: {e}")
            return {}

    def get_spending_trends(self, months: int = 6) -> List[Dict[str, Any]]:
        """
        Get spending trends for last N months

        Args:
            months: Number of months to analyze

        Returns:
            List of monthly spending data
        """
        try:
            today = date.today()
            trends = []

            for i in range(months - 1, -1, -1):
                # Calculate month and year
                target_month = today.month - i
                target_year = today.year

                while target_month <= 0:
                    target_month += 12
                    target_year -= 1

                # Get monthly summary
                summary = self.transaction_repo.get_monthly_summary(
                    target_year,
                    target_month
                )

                trends.append({
                    'year': target_year,
                    'month': target_month,
                    'month_name': date(target_year, target_month, 1).strftime('%b %Y'),
                    'income': summary.get('income', 0.0),
                    'expense': summary.get('expense', 0.0),
                    'balance': summary.get('balance', 0.0)
                })

            return trends

        except Exception as e:
            print(f"Error getting spending trends: {e}")
            return []

    def get_top_expenses(
        self,
        start_date: date,
        end_date: date,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get top expenses for date range

        Args:
            start_date: Start date
            end_date: End date
            limit: Number of results

        Returns:
            List of top expense transactions
        """
        try:
            transactions = self.transaction_repo.get_by_date_range(
                start_date,
                end_date
            )

            # Filter debits (expenses) and sort by amount
            expenses = [t for t in transactions if t.transaction_type == 'debit']
            expenses.sort(key=lambda t: t.amount, reverse=True)

            return [
                {
                    'id': t.id,
                    'date': t.date_formatted,
                    'amount': t.amount,
                    'description': t.description,
                    'category': t.category.name if t.category else 'Uncategorized',
                    'account': t.account.name if t.account else None
                }
                for t in expenses[:limit]
            ]

        except Exception as e:
            print(f"Error getting top expenses: {e}")
            return []
