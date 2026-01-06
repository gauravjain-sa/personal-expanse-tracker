"""
Management Frame
Central location to view all data and manage types
"""
import customtkinter as ctk
from typing import Dict, List
from collections import Counter

from ui.components import BaseFrame, CardWidget
from services import TransactionService, AccountService, CategoryService
from config import Config


class ManagementFrame(BaseFrame):
    """Frame for managing and viewing all application data"""

    def __init__(
        self,
        parent,
        transaction_service: TransactionService,
        account_service: AccountService,
        category_service: CategoryService
    ):
        """
        Initialize ManagementFrame

        Args:
            parent: Parent widget
            transaction_service: Transaction service instance
            account_service: Account service instance
            category_service: Category service instance
        """
        super().__init__(parent, title="Data Management")

        self.transaction_service = transaction_service
        self.account_service = account_service
        self.category_service = category_service

        self._create_content()
        self._load_all_data()

    def _create_content(self):
        """Create frame content"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Create tabview
        self.tabview = ctk.CTkTabview(self, fg_color=Config.COLORS['card'])
        self.tabview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        # Add tabs
        self.tabview.add("All Accounts")
        self.tabview.add("All Categories")
        self.tabview.add("Types Management")

        # Configure tabs
        for tab_name in ["All Accounts", "All Categories", "Types Management"]:
            self.tabview.tab(tab_name).grid_columnconfigure(0, weight=1)
            self.tabview.tab(tab_name).grid_rowconfigure(0, weight=1)

    def _load_all_data(self):
        """Load all data into tabs"""
        self._load_accounts_tab()
        self._load_categories_tab()
        self._load_types_tab()

    def _load_accounts_tab(self):
        """Load All Accounts tab"""
        tab = self.tabview.tab("All Accounts")

        # Clear existing
        for widget in tab.winfo_children():
            widget.destroy()

        # Title and count
        accounts = self.account_service.get_all_accounts()

        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text=f"All Accounts ({len(accounts)})",
            font=Config.get_font('heading'),
            text_color=Config.COLORS['text']
        )
        title_label.pack(side="left")

        # Scrollable list
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not accounts:
            no_data = ctk.CTkLabel(
                scroll_frame,
                text="No accounts found",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text_secondary']
            )
            no_data.pack(pady=40)
            return

        # Create header
        header = ctk.CTkFrame(
            scroll_frame,
            fg_color=Config.COLORS['primary'],
            corner_radius=8,
            height=40
        )
        header.pack(fill="x", pady=(0, 5))

        headers_data = [
            ("Account Name", 200, "w"),
            ("Type", 120, "w"),
            ("Balance", 120, "e"),
            ("Currency", 80, "center"),
            ("Notes", None, "w")  # Expandable
        ]

        for text, width, anchor in headers_data:
            label = ctk.CTkLabel(
                header,
                text=text,
                font=Config.get_font('subtitle'),
                text_color="white",
                anchor=anchor
            )
            if width:
                label.configure(width=width)
                label.pack(side="left", padx=15, pady=10)
            else:
                # Expandable column (Notes)
                label.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        # Display accounts
        for account in accounts:
            self._create_account_row(scroll_frame, account)

    def _create_account_row(self, parent, account):
        """Create account row"""
        row = ctk.CTkFrame(
            parent,
            fg_color=Config.COLORS['surface'],
            corner_radius=8,
            border_width=1,
            border_color=Config.COLORS['border']
        )
        row.pack(fill="x", pady=2)

        # Account Name
        name_label = ctk.CTkLabel(
            row,
            text=account.name,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text'],
            anchor="w"
        )
        name_label.pack(side="left", padx=15, pady=12, fill="x", expand=False)
        name_label.configure(width=200)

        # Type
        account_type = account.account_type or "-"
        type_label = ctk.CTkLabel(
            row,
            text=account_type,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="w"
        )
        type_label.pack(side="left", padx=15, pady=12)
        type_label.configure(width=120)

        # Balance
        balance_color = Config.COLORS['success'] if account.current_balance >= 0 else Config.COLORS['error']
        balance_label = ctk.CTkLabel(
            row,
            text=f"{Config.CURRENCY_SYMBOL}{account.current_balance:,.2f}",
            font=Config.get_font('body'),
            text_color=balance_color,
            anchor="e"
        )
        balance_label.pack(side="left", padx=15, pady=12)
        balance_label.configure(width=120)

        # Currency
        currency_label = ctk.CTkLabel(
            row,
            text=account.currency or Config.DEFAULT_CURRENCY,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="center"
        )
        currency_label.pack(side="left", padx=15, pady=12)
        currency_label.configure(width=80)

        # Notes
        notes = account.notes or "-"
        notes_label = ctk.CTkLabel(
            row,
            text=notes[:40] + "..." if len(notes) > 40 else notes,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="w"
        )
        notes_label.pack(side="left", padx=15, pady=12, fill="x", expand=True)

    def _load_categories_tab(self):
        """Load All Categories tab"""
        tab = self.tabview.tab("All Categories")

        # Clear existing
        for widget in tab.winfo_children():
            widget.destroy()

        # Title and count
        categories = self.category_service.get_all_categories()

        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text=f"All Categories ({len(categories)})",
            font=Config.get_font('heading'),
            text_color=Config.COLORS['text']
        )
        title_label.pack(side="left")

        # Scrollable list
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not categories:
            no_data = ctk.CTkLabel(
                scroll_frame,
                text="No categories found",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text_secondary']
            )
            no_data.pack(pady=40)
            return

        # Create header
        header = ctk.CTkFrame(
            scroll_frame,
            fg_color=Config.COLORS['primary'],
            corner_radius=8,
            height=40
        )
        header.pack(fill="x", pady=(0, 5))

        headers_data = [
            ("Icon", 40),
            ("Category Name", 200),
            ("Type", 100),
            ("Description", None),  # Expandable
            ("Created", 90)
        ]

        for text, width in headers_data:
            label = ctk.CTkLabel(
                header,
                text=text,
                font=Config.get_font('subtitle'),
                text_color="white",
                anchor="center" if width and width < 100 else "w"
            )
            if width:
                label.configure(width=width)
                label.pack(side="left", padx=15, pady=10)
            else:
                # Expandable column
                label.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        # Display categories
        for category in categories:
            self._create_category_row(scroll_frame, category)

    def _create_category_row(self, parent, category):
        """Create category row"""
        row = ctk.CTkFrame(
            parent,
            fg_color=Config.COLORS['surface'],
            corner_radius=8,
            border_width=1,
            border_color=Config.COLORS['border']
        )
        row.pack(fill="x", pady=2)

        # Icon
        icon_label = ctk.CTkLabel(
            row,
            text=category.icon or "📁",
            font=Config.get_font('subtitle'),
            anchor="center"
        )
        icon_label.pack(side="left", padx=15, pady=12)
        icon_label.configure(width=40)

        # Name
        name_label = ctk.CTkLabel(
            row,
            text=category.name,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text'],
            anchor="w"
        )
        name_label.pack(side="left", padx=15, pady=12)
        name_label.configure(width=200)

        # Type
        category_type = category.type or "-"
        type_color = Config.COLORS['success'] if category_type == 'credit' else (
            Config.COLORS['error'] if category_type == 'debit' else Config.COLORS['text_secondary']
        )
        type_label = ctk.CTkLabel(
            row,
            text=category_type.capitalize() if category_type != "-" else "-",
            font=Config.get_font('small'),
            text_color=type_color,
            anchor="w"
        )
        type_label.pack(side="left", padx=15, pady=12)
        type_label.configure(width=100)

        # Description
        desc = category.description or "-"
        desc_label = ctk.CTkLabel(
            row,
            text=desc[:50] + "..." if len(desc) > 50 else desc,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="w"
        )
        desc_label.pack(side="left", padx=15, pady=12, fill="x", expand=True)

        # Created date
        created = category.created_at.strftime('%d-%m-%Y') if hasattr(category, 'created_at') and category.created_at else "-"
        created_label = ctk.CTkLabel(
            row,
            text=created,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="center"
        )
        created_label.pack(side="left", padx=15, pady=12)
        created_label.configure(width=90)

    def _load_types_tab(self):
        """Load Types Management tab"""
        tab = self.tabview.tab("Types Management")

        # Clear existing
        for widget in tab.winfo_children():
            widget.destroy()

        # Main container
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Account Types Section
        account_types_card = CardWidget(container, title="Account Types in Use")
        account_types_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        account_types_list = ctk.CTkScrollableFrame(
            account_types_card,
            fg_color="transparent",
            height=300
        )
        account_types_card.add_content(account_types_list)

        self._display_account_types(account_types_list)

        # Category Types Section
        category_types_card = CardWidget(container, title="Category Types in Use")
        category_types_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        category_types_list = ctk.CTkScrollableFrame(
            category_types_card,
            fg_color="transparent",
            height=300
        )
        category_types_card.add_content(category_types_list)

        self._display_category_types(category_types_list)

        # Info label
        info_label = ctk.CTkLabel(
            container,
            text="Types are user-defined and flexible. This view shows what types are currently in use.",
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            wraplength=600
        )
        info_label.grid(row=1, column=0, columnspan=2, pady=20)

    def _display_account_types(self, parent):
        """Display account types with counts"""
        accounts = self.account_service.get_all_accounts()

        # Count types
        type_counts = Counter()
        for account in accounts:
            account_type = account.account_type or "(No Type)"
            type_counts[account_type] += 1

        if not type_counts:
            no_data = ctk.CTkLabel(
                parent,
                text="No account types found",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Display types
        for account_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            self._create_type_row(parent, account_type, count)

    def _display_category_types(self, parent):
        """Display category types with counts"""
        categories = self.category_service.get_all_categories()

        # Count types
        type_counts = Counter()
        for category in categories:
            category_type = category.type or "(No Type)"
            type_counts[category_type] += 1

        if not type_counts:
            no_data = ctk.CTkLabel(
                parent,
                text="No category types found",
                font=Config.get_font('body'),
                text_color=Config.COLORS['text_secondary']
            )
            no_data.pack(pady=20)
            return

        # Display types
        for category_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            self._create_type_row(parent, category_type, count)

    def _create_type_row(self, parent, type_name: str, count: int):
        """Create type row with count"""
        row = ctk.CTkFrame(
            parent,
            fg_color=Config.COLORS['surface'],
            corner_radius=8,
            border_width=1,
            border_color=Config.COLORS['border'],
            height=50
        )
        row.pack(fill="x", pady=5, padx=5)

        # Type name
        name_label = ctk.CTkLabel(
            row,
            text=type_name,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text'],
            anchor="w"
        )
        name_label.pack(side="left", padx=20, pady=15, fill="x", expand=True)

        # Count badge
        count_frame = ctk.CTkFrame(
            row,
            fg_color=Config.COLORS['primary'],
            corner_radius=15,
            width=60,
            height=30
        )
        count_frame.pack(side="right", padx=20, pady=10)

        count_label = ctk.CTkLabel(
            count_frame,
            text=str(count),
            font=Config.get_font('subtitle'),
            text_color="white"
        )
        count_label.place(relx=0.5, rely=0.5, anchor="center")
