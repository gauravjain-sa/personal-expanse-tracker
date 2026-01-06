"""
Filter Panel Component
Reusable filter UI for transaction filtering with period selection and search
"""
import customtkinter as ctk
from typing import List, Dict, Optional, Callable
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from tkcalendar import DateEntry

from models import Account, Category
from config import Config


class FilterPanel(ctk.CTkFrame):
    """Reusable filter panel component for transactions"""

    PERIOD_OPTIONS = [
        "All Time",
        "Current Month",
        "Current Financial Year",
        "Last Month",
        "Last 3 Months",
        "Last 6 Months",
        "Last Year",
        "Custom Date Range"
    ]

    def __init__(
        self,
        parent,
        accounts: List[Account],
        categories: List[Category],
        on_filter_apply: Callable,
        on_filter_clear: Optional[Callable] = None
    ):
        """
        Initialize Filter Panel

        Args:
            parent: Parent widget
            accounts: List of accounts for filtering
            categories: List of categories for filtering
            on_filter_apply: Callback function when filters are applied
            on_filter_clear: Optional callback when filters are cleared
        """
        super().__init__(parent, fg_color="transparent")

        self.accounts = accounts
        self.categories = categories
        self.on_filter_apply = on_filter_apply
        self.on_filter_clear = on_filter_clear or (lambda: None)

        self._create_ui()

    def _create_ui(self):
        """Create filter panel UI"""
        # Container
        container = ctk.CTkFrame(self, fg_color=Config.COLORS['card'])
        container.pack(fill="x", padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Filters",
            font=Config.get_font('heading'),
            text_color=Config.COLORS['text']
        )
        title_label.grid(row=0, column=0, columnspan=6, padx=10, pady=(10, 5), sticky="w")

        # Row 1: Period and Date Range
        period_label = ctk.CTkLabel(
            container,
            text="Period:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        period_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.period_var = ctk.StringVar(value="All Time")
        self.period_dropdown = ctk.CTkComboBox(
            container,
            variable=self.period_var,
            values=self.PERIOD_OPTIONS,
            command=self._on_period_changed,
            width=180,
            font=Config.get_font('body')
        )
        self.period_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # From Date
        from_label = ctk.CTkLabel(
            container,
            text="From:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        from_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.from_date_entry = DateEntry(
            container,
            width=12,
            background=Config.COLORS['primary'],
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            font=Config.get_font('body'),
            state='disabled'  # Initially disabled
        )
        self.from_date_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # To Date
        to_label = ctk.CTkLabel(
            container,
            text="To:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        to_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        self.to_date_entry = DateEntry(
            container,
            width=12,
            background=Config.COLORS['primary'],
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            font=Config.get_font('body'),
            state='disabled'  # Initially disabled
        )
        self.to_date_entry.grid(row=1, column=5, padx=10, pady=10, sticky="w")

        # Row 2: Account, Category, Type Filters
        account_label = ctk.CTkLabel(
            container,
            text="Account:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        account_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        account_names = ["All Accounts"] + [acc.name for acc in self.accounts]
        self.account_var = ctk.StringVar(value="All Accounts")
        self.account_dropdown = ctk.CTkComboBox(
            container,
            variable=self.account_var,
            values=account_names,
            width=180,
            font=Config.get_font('body')
        )
        self.account_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Category
        category_label = ctk.CTkLabel(
            container,
            text="Category:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        category_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        category_names = ["All Categories"] + [cat.name for cat in self.categories]
        self.category_var = ctk.StringVar(value="All Categories")
        self.category_dropdown = ctk.CTkComboBox(
            container,
            variable=self.category_var,
            values=category_names,
            width=180,
            font=Config.get_font('body')
        )
        self.category_dropdown.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        # Type
        type_label = ctk.CTkLabel(
            container,
            text="Type:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        type_label.grid(row=2, column=4, padx=10, pady=10, sticky="w")

        self.type_var = ctk.StringVar(value="All")
        self.type_dropdown = ctk.CTkComboBox(
            container,
            variable=self.type_var,
            values=["All", "Credit", "Debit"],
            width=120,
            font=Config.get_font('body')
        )
        self.type_dropdown.grid(row=2, column=5, padx=10, pady=10, sticky="w")

        # Row 3: Search and Action Buttons
        search_label = ctk.CTkLabel(
            container,
            text="Search:",
            font=Config.get_font('body'),
            text_color=Config.COLORS['text']
        )
        search_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(
            container,
            placeholder_text="Search description, merchant, notes...",
            width=300,
            font=Config.get_font('body')
        )
        self.search_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        # Action buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.grid(row=3, column=4, columnspan=2, padx=10, pady=10, sticky="e")

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear All",
            command=self._on_clear_clicked,
            width=100,
            font=Config.get_font('button'),
            fg_color=Config.COLORS['secondary'],
            hover_color=Config.COLORS['secondary_hover']
        )
        self.clear_btn.pack(side="left", padx=5)

        self.apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply Filters",
            command=self._on_apply_clicked,
            width=120,
            font=Config.get_font('button'),
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover']
        )
        self.apply_btn.pack(side="left", padx=5)

        # Configure grid weights for responsive design
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(3, weight=1)

    def _on_period_changed(self, choice: str):
        """Handle period dropdown change"""
        if choice == "Custom Date Range":
            # Enable date pickers
            self.from_date_entry.configure(state='normal')
            self.to_date_entry.configure(state='normal')
        else:
            # Disable date pickers and set dates based on period
            self.from_date_entry.configure(state='disabled')
            self.to_date_entry.configure(state='disabled')

            # Calculate dates based on period
            start_date, end_date = self._calculate_period_dates(choice)
            if start_date:
                self.from_date_entry.set_date(start_date)
            if end_date:
                self.to_date_entry.set_date(end_date)

    def _calculate_period_dates(self, period: str) -> tuple:
        """
        Calculate start and end dates based on period selection

        Args:
            period: Selected period string

        Returns:
            Tuple of (start_date, end_date) or (None, None) for All Time
        """
        today = date.today()

        if period == "All Time":
            return None, None

        elif period == "Current Month":
            start_date = today.replace(day=1)
            # Last day of current month
            next_month = start_date + relativedelta(months=1)
            end_date = next_month - timedelta(days=1)
            return start_date, end_date

        elif period == "Current Financial Year":
            # Indian FY: April to March
            from services.transaction_service import TransactionService
            fy_year = TransactionService.get_current_financial_year()
            start_date, end_date = TransactionService.get_financial_year_dates(fy_year)
            return start_date, end_date

        elif period == "Last Month":
            # First day of last month
            first_of_this_month = today.replace(day=1)
            first_of_last_month = first_of_this_month - relativedelta(months=1)
            # Last day of last month
            last_of_last_month = first_of_this_month - timedelta(days=1)
            return first_of_last_month, last_of_last_month

        elif period == "Last 3 Months":
            start_date = today - relativedelta(months=3)
            return start_date, today

        elif period == "Last 6 Months":
            start_date = today - relativedelta(months=6)
            return start_date, today

        elif period == "Last Year":
            start_date = today - relativedelta(years=1)
            return start_date, today

        elif period == "Custom Date Range":
            # Return current values in date pickers
            return self.from_date_entry.get_date(), self.to_date_entry.get_date()

        return None, None

    def _on_apply_clicked(self):
        """Handle Apply Filters button click"""
        filters = self.get_filters()
        self.on_filter_apply(filters)

    def _on_clear_clicked(self):
        """Handle Clear All button click"""
        self.reset_filters()
        self.on_filter_clear()
        # Also apply empty filters
        self.on_filter_apply(self.get_filters())

    def get_filters(self) -> Dict:
        """
        Get current filter values

        Returns:
            Dictionary with filter values:
                - start_date: date or None
                - end_date: date or None
                - account_id: int or None
                - category_id: int or None
                - transaction_type: str or None ('credit' or 'debit')
                - search_term: str or None
        """
        filters = {}

        # Date range
        period = self.period_var.get()
        if period == "Custom Date Range":
            filters['start_date'] = self.from_date_entry.get_date()
            filters['end_date'] = self.to_date_entry.get_date()
        elif period != "All Time":
            start_date, end_date = self._calculate_period_dates(period)
            filters['start_date'] = start_date
            filters['end_date'] = end_date
        else:
            filters['start_date'] = None
            filters['end_date'] = None

        # Account
        account_name = self.account_var.get()
        if account_name != "All Accounts":
            account = next((acc for acc in self.accounts if acc.name == account_name), None)
            filters['account_id'] = account.id if account else None
        else:
            filters['account_id'] = None

        # Category
        category_name = self.category_var.get()
        if category_name != "All Categories":
            category = next((cat for cat in self.categories if cat.name == category_name), None)
            filters['category_id'] = category.id if category else None
        else:
            filters['category_id'] = None

        # Type
        type_value = self.type_var.get()
        if type_value == "Credit":
            filters['transaction_type'] = 'credit'
        elif type_value == "Debit":
            filters['transaction_type'] = 'debit'
        else:
            filters['transaction_type'] = None

        # Search term
        search_text = self.search_entry.get().strip()
        filters['search_term'] = search_text if search_text else None

        return filters

    def reset_filters(self):
        """Reset all filters to default values"""
        self.period_var.set("All Time")
        self.account_var.set("All Accounts")
        self.category_var.set("All Categories")
        self.type_var.set("All")
        self.search_entry.delete(0, 'end')

        # Reset date pickers
        self.from_date_entry.configure(state='disabled')
        self.to_date_entry.configure(state='disabled')
        self.from_date_entry.set_date(date.today())
        self.to_date_entry.set_date(date.today())

    def update_accounts(self, accounts: List[Account]):
        """
        Update account list

        Args:
            accounts: New list of accounts
        """
        self.accounts = accounts
        account_names = ["All Accounts"] + [acc.name for acc in accounts]
        self.account_dropdown.configure(values=account_names)

    def update_categories(self, categories: List[Category]):
        """
        Update category list

        Args:
            categories: New list of categories
        """
        self.categories = categories
        category_names = ["All Categories"] + [cat.name for cat in categories]
        self.category_dropdown.configure(values=category_names)
