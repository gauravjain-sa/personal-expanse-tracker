"""
Transactions Frame
View and manage all transactions with accounting-style display, filters, and pagination
"""
import customtkinter as ctk
from datetime import date
from typing import Optional, Dict, List
from pathlib import Path

from ui.components import BaseFrame, CardWidget, FilterPanel
from ui.dialogs import AddTransactionDialog, EditTransactionDialog, DeleteConfirmationDialog
from services import TransactionService, AccountService, CategoryService, ExportService
from models import Transaction
from config import Config


class TransactionsFrame(BaseFrame):
    """Frame for managing transactions with accounting view"""

    def __init__(
        self,
        parent,
        transaction_service: TransactionService,
        account_service: AccountService,
        category_service: CategoryService,
        export_service: ExportService
    ):
        """
        Initialize TransactionsFrame

        Args:
            parent: Parent widget
            transaction_service: Transaction service instance
            account_service: Account service instance
            category_service: Category service instance
            export_service: Export service instance
        """
        super().__init__(parent, title="Transactions")

        self.transaction_service = transaction_service
        self.account_service = account_service
        self.category_service = category_service
        self.export_service = export_service

        # State management
        self.current_page = 1
        self.page_size = 50
        self.total_pages = 1
        self.total_transactions = 0
        self.current_filters = {}
        self.current_view = ctk.StringVar(value='combined')  # 'combined', 'credits', 'debits'
        self.all_transactions = []  # Current page transactions

        self._create_content()
        self._load_page(page=1)

    def _create_content(self):
        """Create frame content"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Row 1: Filter Panel
        accounts = self.account_service.get_all_accounts()
        categories = self.category_service.get_all_categories()

        self.filter_panel = FilterPanel(
            self,
            accounts=accounts,
            categories=categories,
            on_filter_apply=self._apply_filters,
            on_filter_clear=self._clear_filters
        )
        self.filter_panel.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # Row 2: Summary Bar
        self.summary_frame = ctk.CTkFrame(self, fg_color=Config.COLORS['card'])
        self.summary_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)

        self.summary_label = ctk.CTkLabel(
            self.summary_frame,
            text="Loading...",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        self.summary_label.pack(padx=15, pady=10)

        # Row 3: View Toggle and Action Buttons
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        # View Toggle (Left side)
        view_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        view_frame.grid(row=0, column=0, sticky="w")

        view_label = ctk.CTkLabel(
            view_frame,
            text="View:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        view_label.pack(side="left", padx=(0, 10))

        combined_radio = ctk.CTkRadioButton(
            view_frame,
            text="Combined",
            variable=self.current_view,
            value='combined',
            command=self._on_view_changed,
            font=Config.get_font('body')
        )
        combined_radio.pack(side="left", padx=5)

        credits_radio = ctk.CTkRadioButton(
            view_frame,
            text="Credits Only",
            variable=self.current_view,
            value='credits',
            command=self._on_view_changed,
            font=Config.get_font('body')
        )
        credits_radio.pack(side="left", padx=5)

        debits_radio = ctk.CTkRadioButton(
            view_frame,
            text="Debits Only",
            variable=self.current_view,
            value='debits',
            command=self._on_view_changed,
            font=Config.get_font('body')
        )
        debits_radio.pack(side="left", padx=5)

        # Action Buttons (Right side)
        actions_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")

        add_btn = ctk.CTkButton(
            actions_frame,
            text="Add Transaction",
            command=self._add_transaction,
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover'],
            font=Config.get_font('body'),
            width=140
        )
        add_btn.pack(side="left", padx=5)

        export_excel_btn = ctk.CTkButton(
            actions_frame,
            text="Export Excel",
            command=self._export_excel,
            fg_color=Config.COLORS['secondary'],
            hover_color=Config.COLORS['secondary_hover'],
            font=Config.get_font('body'),
            width=120
        )
        export_excel_btn.pack(side="left", padx=5)

        export_csv_btn = ctk.CTkButton(
            actions_frame,
            text="Export CSV",
            command=self._export_csv,
            fg_color=Config.COLORS['secondary'],
            hover_color=Config.COLORS['secondary_hover'],
            font=Config.get_font('body'),
            width=110
        )
        export_csv_btn.pack(side="left", padx=5)

        # Row 4: Transactions List (Accounting Style)
        list_card = CardWidget(self, title="Transaction History")
        list_card.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        # Scrollable list with accounting columns
        self.transactions_list = ctk.CTkScrollableFrame(
            list_card,
            fg_color="transparent"
        )
        list_card.add_content(self.transactions_list)

        # Row 5: Pagination Controls
        self.pagination_frame = ctk.CTkFrame(self, fg_color=Config.COLORS['card'])
        self.pagination_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.pagination_label = ctk.CTkLabel(
            self.pagination_frame,
            text="Page 1 of 1",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        self.pagination_label.pack(pady=10)

    def _load_page(self, page: int = 1):
        """
        Load transactions for specific page

        Args:
            page: Page number to load
        """
        try:
            # Get paginated transactions with current filters
            result = self.transaction_service.get_transactions_paginated(
                page=page,
                page_size=self.page_size,
                **self.current_filters
            )

            self.all_transactions = result['transactions']
            self.total_transactions = result['total']
            self.current_page = result['page']
            self.total_pages = result['pages']

            # Update summary
            self._update_summary()

            # Update transaction list
            self._update_transaction_list()

            # Update pagination controls
            self._update_pagination_controls()

        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.show_error("Failed to load transactions")

    def _update_summary(self):
        """Update summary bar with credits/debits totals"""
        try:
            summary = self.transaction_service.get_credits_debits_summary(
                self.all_transactions
            )

            credits = summary['total_credits']
            debits = summary['total_debits']
            balance = summary['net_balance']
            credit_count = summary['credit_count']
            debit_count = summary['debit_count']

            # Format summary text
            balance_symbol = "+" if balance >= 0 else ""
            summary_text = (
                f"Credits: {Config.CURRENCY_SYMBOL}{credits:,.2f} ({credit_count}) | "
                f"Debits: {Config.CURRENCY_SYMBOL}{debits:,.2f} ({debit_count}) | "
                f"Balance: {balance_symbol}{Config.CURRENCY_SYMBOL}{balance:,.2f} | "
                f"Showing {len(self.all_transactions)} of {self.total_transactions} transactions"
            )

            self.summary_label.configure(text=summary_text)

        except Exception as e:
            print(f"Error updating summary: {e}")
            self.summary_label.configure(text="Error calculating summary")

    def _update_transaction_list(self):
        """Update transaction list based on current view"""
        try:
            # Clear existing
            for widget in self.transactions_list.winfo_children():
                widget.destroy()

            if not self.all_transactions:
                no_data = ctk.CTkLabel(
                    self.transactions_list,
                    text="No transactions found. Try adjusting your filters.",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text_secondary']
                )
                no_data.pack(pady=40)
                return

            # Filter transactions by view
            view = self.current_view.get()
            if view == 'credits':
                transactions = [t for t in self.all_transactions if t.transaction_type == 'credit']
            elif view == 'debits':
                transactions = [t for t in self.all_transactions if t.transaction_type == 'debit']
            else:  # combined
                transactions = self.all_transactions

            if not transactions:
                no_data = ctk.CTkLabel(
                    self.transactions_list,
                    text=f"No {view} to display.",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text_secondary']
                )
                no_data.pack(pady=40)
                return

            # Create header row
            self._create_header_row()

            # Display transaction rows
            for transaction in transactions:
                self._create_accounting_row(transaction)

        except Exception as e:
            print(f"Error updating transaction list: {e}")
            self.show_error("Failed to update transaction list")

    def _create_header_row(self):
        """Create header row for accounting columns"""
        header = ctk.CTkFrame(
            self.transactions_list,
            fg_color=Config.COLORS['primary'],
            corner_radius=0,
            height=40
        )
        header.pack(fill="x", padx=0, pady=0)
        header.grid_columnconfigure(1, weight=1)

        headers = [
            ("Date", 0, 80),
            ("Description", 1, 200),
            ("Account", 2, 120),
            ("Category", 3, 120),
            ("Debit", 4, 100),
            ("Credit", 5, 100),
            ("Actions", 6, 150)
        ]

        for text, col, width in headers:
            # Determine alignment based on column
            if col <= 3:  # Date, Description, Account, Category - left align
                sticky = "w"
                anchor = "w"
            elif col <= 5:  # Debit, Credit - right align
                sticky = "e"
                anchor = "e"
            else:  # Actions - right align
                sticky = "e"
                anchor = "e"

            label = ctk.CTkLabel(
                header,
                text=text,
                font=Config.get_font('subtitle'),
                text_color="white",
                width=width,
                anchor=anchor
            )
            label.grid(row=0, column=col, padx=10, pady=10, sticky=sticky)

    def _create_accounting_row(self, transaction: Transaction):
        """
        Create accounting-style transaction row

        Args:
            transaction: Transaction object
        """
        row = ctk.CTkFrame(
            self.transactions_list,
            fg_color=Config.COLORS['surface'],
            corner_radius=0,
            border_width=0,
            border_color=Config.COLORS['border'],
            height=45
        )
        row.pack(fill="x", padx=0, pady=1)
        row.grid_columnconfigure(1, weight=1)

        # Date
        date_label = ctk.CTkLabel(
            row,
            text=transaction.date.strftime('%d %b'),
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            width=80,
            anchor="w"
        )
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Description
        desc = transaction.description or (
            transaction.category.name if transaction.category else "Uncategorized"
        )
        desc_label = ctk.CTkLabel(
            row,
            text=desc[:30] + "..." if len(desc) > 30 else desc,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text'],
            width=200,
            anchor="w"
        )
        desc_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Account
        account_name = transaction.account.name if transaction.account else "Unknown"
        account_label = ctk.CTkLabel(
            row,
            text=account_name[:15] + "..." if len(account_name) > 15 else account_name,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            width=120,
            anchor="w"
        )
        account_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Category
        category_name = transaction.category.name if transaction.category else "-"
        category_label = ctk.CTkLabel(
            row,
            text=category_name[:15] + "..." if len(category_name) > 15 else category_name,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            width=120,
            anchor="w"
        )
        category_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Debit column
        if transaction.transaction_type == 'debit':
            debit_text = f"{Config.CURRENCY_SYMBOL}{transaction.amount:,.2f}"
            debit_color = Config.COLORS['error']
        else:
            debit_text = "-"
            debit_color = Config.COLORS['text_secondary']

        debit_label = ctk.CTkLabel(
            row,
            text=debit_text,
            font=Config.get_font('body'),
            text_color=debit_color,
            width=100,
            anchor="e"
        )
        debit_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        # Credit column
        if transaction.transaction_type == 'credit':
            credit_text = f"{Config.CURRENCY_SYMBOL}{transaction.amount:,.2f}"
            credit_color = Config.COLORS['success']
        else:
            credit_text = "-"
            credit_color = Config.COLORS['text_secondary']

        credit_label = ctk.CTkLabel(
            row,
            text=credit_text,
            font=Config.get_font('body'),
            text_color=credit_color,
            width=100,
            anchor="e"
        )
        credit_label.grid(row=0, column=5, padx=10, pady=10, sticky="e")

        # Actions
        actions_frame = ctk.CTkFrame(row, fg_color="transparent")
        actions_frame.grid(row=0, column=6, padx=10, pady=5, sticky="e")

        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda t=transaction: self._edit_transaction(t),
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover'],
            font=Config.get_font('body'),
            width=60,
            height=28
        )
        edit_btn.pack(side="left", padx=2)

        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda t=transaction: self._delete_transaction(t),
            fg_color=Config.COLORS['error'],
            hover_color=Config.COLORS['error'],
            font=Config.get_font('body'),
            width=70,
            height=28
        )
        delete_btn.pack(side="left", padx=2)

    def _update_pagination_controls(self):
        """Update pagination controls"""
        try:
            # Clear existing
            for widget in self.pagination_frame.winfo_children():
                widget.destroy()

            if self.total_pages <= 1:
                # No pagination needed
                label = ctk.CTkLabel(
                    self.pagination_frame,
                    text=f"Total: {self.total_transactions} transactions",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text']
                )
                label.pack(pady=10)
                return

            # Create pagination controls
            controls = ctk.CTkFrame(self.pagination_frame, fg_color="transparent")
            controls.pack(pady=10)

            # First button
            first_btn = ctk.CTkButton(
                controls,
                text="<< First",
                command=lambda: self._load_page(1),
                fg_color=Config.COLORS['secondary'],
                hover_color=Config.COLORS['secondary_hover'],
                font=Config.get_font('body'),
                width=80,
                height=30
            )
            first_btn.pack(side="left", padx=5)
            if self.current_page == 1:
                first_btn.configure(state="disabled")

            # Previous button
            prev_btn = ctk.CTkButton(
                controls,
                text="< Previous",
                command=lambda: self._load_page(self.current_page - 1),
                fg_color=Config.COLORS['secondary'],
                hover_color=Config.COLORS['secondary_hover'],
                font=Config.get_font('body'),
                width=90,
                height=30
            )
            prev_btn.pack(side="left", padx=5)
            if self.current_page == 1:
                prev_btn.configure(state="disabled")

            # Page indicator
            page_label = ctk.CTkLabel(
                controls,
                text=f"Page {self.current_page} of {self.total_pages}",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text'],
                width=120
            )
            page_label.pack(side="left", padx=10)

            # Next button
            next_btn = ctk.CTkButton(
                controls,
                text="Next >",
                command=lambda: self._load_page(self.current_page + 1),
                fg_color=Config.COLORS['secondary'],
                hover_color=Config.COLORS['secondary_hover'],
                font=Config.get_font('body'),
                width=80,
                height=30
            )
            next_btn.pack(side="left", padx=5)
            if self.current_page == self.total_pages:
                next_btn.configure(state="disabled")

            # Last button
            last_btn = ctk.CTkButton(
                controls,
                text="Last >>",
                command=lambda: self._load_page(self.total_pages),
                fg_color=Config.COLORS['secondary'],
                hover_color=Config.COLORS['secondary_hover'],
                font=Config.get_font('body'),
                width=80,
                height=30
            )
            last_btn.pack(side="left", padx=5)
            if self.current_page == self.total_pages:
                last_btn.configure(state="disabled")

        except Exception as e:
            print(f"Error updating pagination: {e}")

    def _apply_filters(self, filters: Dict):
        """
        Apply filters and reload first page

        Args:
            filters: Dictionary of filter values
        """
        self.current_filters = filters
        self._load_page(page=1)

    def _clear_filters(self):
        """Clear all filters"""
        self.current_filters = {}

    def _on_view_changed(self):
        """Handle view toggle change"""
        self._update_transaction_list()

    def _export_excel(self):
        """Export filtered transactions to Excel"""
        try:
            # Get ALL transactions matching current filters (not just current page)
            all_filtered = self.transaction_service.get_transactions_paginated(
                page=1,
                page_size=10000,  # Large number to get all
                **self.current_filters
            )

            transactions = all_filtered['transactions']

            if not transactions:
                self.show_error("No transactions to export")
                return

            # Generate filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transactions_{timestamp}.xlsx"

            # Export
            start_date = self.current_filters.get('start_date')
            end_date = self.current_filters.get('end_date')

            filepath = self.export_service.export_to_excel(
                transactions,
                filename=filename,
                start_date=start_date,
                end_date=end_date
            )

            # Check if user cancelled
            if filepath is None:
                return

            self.show_success(f"Exported to: {filepath}")

        except ImportError:
            self.show_error("openpyxl not installed. Install with: pip install openpyxl")
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            self.show_error(f"Failed to export: {str(e)}")

    def _export_csv(self):
        """Export filtered transactions to CSV"""
        try:
            # Get ALL transactions matching current filters
            all_filtered = self.transaction_service.get_transactions_paginated(
                page=1,
                page_size=10000,
                **self.current_filters
            )

            transactions = all_filtered['transactions']

            if not transactions:
                self.show_error("No transactions to export")
                return

            # Generate filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transactions_{timestamp}.csv"

            # Export
            filepath = self.export_service.export_to_csv(
                transactions,
                filename=filename
            )

            # Check if user cancelled
            if filepath is None:
                return

            self.show_success(f"Exported to: {filepath}")

        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            self.show_error(f"Failed to export: {str(e)}")

    def _add_transaction(self):
        """Add new transaction"""
        dialog = AddTransactionDialog(
            self,
            self.transaction_service,
            self.account_service,
            self.category_service,
            on_success=lambda: self._load_page(self.current_page)
        )

    def _edit_transaction(self, transaction: Transaction):
        """
        Edit existing transaction

        Args:
            transaction: Transaction object to edit
        """
        dialog = EditTransactionDialog(
            self,
            transaction,
            self.transaction_service,
            self.account_service,
            self.category_service,
            on_success=lambda: self._load_page(self.current_page)
        )

    def _delete_transaction(self, transaction: Transaction):
        """
        Delete transaction with confirmation

        Args:
            transaction: Transaction object to delete
        """
        dialog = DeleteConfirmationDialog(
            self,
            transaction,
            self.transaction_service,
            on_success=lambda: self._load_page(self.current_page)
        )
