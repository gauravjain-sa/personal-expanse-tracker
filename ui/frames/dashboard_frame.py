"""
Dashboard Frame
Main dashboard with summary statistics and recent transactions
"""
import customtkinter as ctk
from datetime import date

from ui.components import BaseFrame, StatCard, CardWidget
from services import ReportService, TransactionService
from config import Config


class DashboardFrame(BaseFrame):
    """Dashboard frame showing overview"""

    def __init__(
        self,
        parent,
        report_service: ReportService,
        transaction_service: TransactionService
    ):
        """
        Initialize DashboardFrame

        Args:
            parent: Parent widget
            report_service: Report service instance
            transaction_service: Transaction service instance
        """
        super().__init__(parent, title="Dashboard")

        self.report_service = report_service
        self.transaction_service = transaction_service

        self._create_content()
        self._load_data()

    def _create_content(self):
        """Create dashboard content"""
        # Configure grid
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Stats row
        self.stat_cards = {}
        stat_titles = ['Total Balance', 'This Month Credits', 'This Month Debits']
        stat_colors = [Config.COLORS['primary'], Config.COLORS['success'], Config.COLORS['error']]

        for idx, (title, color) in enumerate(zip(stat_titles, stat_colors)):
            card = StatCard(
                self,
                title=title,
                value="Loading...",
                subtitle="",
                color=color
            )
            card.grid(row=1, column=idx, padx=10, pady=10, sticky="ew")
            self.stat_cards[title] = card

        # Recent transactions card
        self.transactions_card = CardWidget(
            self,
            title="Recent Transactions"
        )
        self.transactions_card.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Transactions list frame
        self.transactions_list = ctk.CTkScrollableFrame(
            self.transactions_card,
            fg_color="transparent",
            height=300
        )
        self.transactions_card.add_content(self.transactions_list)

    def _load_data(self):
        """Load dashboard data"""
        try:
            # Get dashboard summary
            summary = self.report_service.get_dashboard_summary()

            # Update stat cards
            if summary:
                # Total balance
                total_balance = summary.get('total_balance', 0.0)
                self.stat_cards['Total Balance'].update_value(
                    Config.format_currency(total_balance)
                )

                # Current month credits (income)
                current_month = summary.get('current_month', {})
                income = current_month.get('income', 0.0)
                self.stat_cards['This Month Credits'].update_value(
                    Config.format_currency(income)
                )

                # Current month debits (expenses)
                expense = current_month.get('expense', 0.0)
                self.stat_cards['This Month Debits'].update_value(
                    Config.format_currency(expense)
                )

                # Load recent transactions
                recent = summary.get('recent_transactions', [])
                self._display_recent_transactions(recent)

        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            self.show_error("Failed to load dashboard data")

    def _display_recent_transactions(self, transactions: list):
        """
        Display recent transactions

        Args:
            transactions: List of transaction dictionaries
        """
        # Clear existing
        for widget in self.transactions_list.winfo_children():
            widget.destroy()

        if not transactions:
            # No transactions message
            no_data_label = ctk.CTkLabel(
                self.transactions_list,
                text="No recent transactions",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text_secondary']
            )
            no_data_label.pack(pady=20)
            return

        # Display transactions
        for transaction in transactions:
            self._create_transaction_row(transaction)

    def _create_transaction_row(self, transaction: dict):
        """
        Create transaction row widget

        Args:
            transaction: Transaction dictionary
        """
        # Row container
        row = ctk.CTkFrame(
            self.transactions_list,
            fg_color="transparent",
            height=50
        )
        row.pack(fill="x", padx=5, pady=5)
        row.grid_columnconfigure(1, weight=1)

        # Date
        date_label = ctk.CTkLabel(
            row,
            text=transaction.get('date', ''),
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            width=100
        )
        date_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Description
        desc_label = ctk.CTkLabel(
            row,
            text=transaction.get('description', 'No description'),
            font=Config.get_font('body'),
            text_color=Config.COLORS['text_primary']
        )
        desc_label.grid(row=0, column=1, padx=10, sticky="w")

        # Amount
        amount = transaction.get('amount', '$0.00')
        trans_type = transaction.get('type', 'debit')

        amount_color = Config.COLORS['success'] if trans_type == 'credit' else Config.COLORS['error']

        amount_label = ctk.CTkLabel(
            row,
            text=amount,
            font=Config.get_font('body'),
            text_color=amount_color,
            width=100
        )
        amount_label.grid(row=0, column=2, padx=(10, 0), sticky="e")

    def refresh(self):
        """Refresh dashboard data"""
        self._load_data()
