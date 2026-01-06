"""
Accounts Frame
View and manage accounts
"""
import customtkinter as ctk
from typing import Optional

from ui.components import BaseFrame, CardWidget
from ui.dialogs import AddAccountDialog, EditAccountDialog, DeleteAccountDialog
from services import AccountService
from config import Config


class AccountsFrame(BaseFrame):
    """Frame for managing accounts"""

    def __init__(
        self,
        parent,
        account_service: AccountService
    ):
        """
        Initialize AccountsFrame

        Args:
            parent: Parent widget
            account_service: Account service instance
        """
        super().__init__(parent, title="Accounts")

        self.account_service = account_service

        self._create_content()
        self._load_accounts()

    def _create_content(self):
        """Create frame content"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Action buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        add_btn = self.create_button(
            "➕ Add Account",
            command=self._add_account,
            style='primary'
        )
        add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Accounts list (scrollable)
        self.accounts_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.accounts_container.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

    def _load_accounts(self):
        """Load and display accounts"""
        try:
            # Get all active accounts
            accounts = self.account_service.get_all_accounts(include_inactive=False)

            # Clear existing
            for widget in self.accounts_container.winfo_children():
                widget.destroy()

            if not accounts:
                no_data = ctk.CTkLabel(
                    self.accounts_container,
                    text="No accounts yet. Add your first account!",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text_secondary']
                )
                no_data.pack(pady=40)
                return

            # Create header row
            header = ctk.CTkFrame(
                self.accounts_container,
                fg_color=Config.COLORS['primary'],
                corner_radius=8,
                height=40
            )
            header.pack(fill="x", pady=(0, 5))

            headers_data = [
                ("Account Name", 0.25),
                ("Type", 0.15),
                ("Balance", 0.15),
                ("Currency", 0.10),
                ("Notes", 0.25),
                ("Actions", 0.10)
            ]

            for text, weight in headers_data:
                label = ctk.CTkLabel(
                    header,
                    text=text,
                    font=Config.get_font('subtitle'),
                    text_color="white"
                )
                label.pack(side="left", padx=15, pady=10, fill="x",
                          expand=True if weight > 0.2 else False)

            # Display accounts as list rows
            for account in accounts:
                self._create_account_row(account)

        except Exception as e:
            print(f"Error loading accounts: {e}")
            self.show_error("Failed to load accounts")

    def _create_account_card(self, account, row: int, col: int):
        """
        Create account card

        Args:
            account: Account object
            row: Grid row
            col: Grid column
        """
        card = CardWidget(self.accounts_container)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # Account type icon
        type_icons = {
            'bank': '🏦',
            'credit_card': '💳',
            'cash': '💵',
            'wallet': '👛',
            'investment': '📈',
            'person': '👤',
            'loan': '💰',
            'factory': '🏭',
            'property': '🏠',
            'other': '📋'
        }
        icon = type_icons.get(account.account_type, '💼')

        # Icon and name
        header = ctk.CTkFrame(card, fg_color="transparent")
        card.add_content(header)
        header.grid_columnconfigure(1, weight=1)

        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=('', 32)
        )
        icon_label.grid(row=0, column=0, padx=(0, 10))

        name_label = ctk.CTkLabel(
            header,
            text=account.name,
            font=Config.get_font('subtitle'),
            text_color=Config.COLORS['text_primary']
        )
        name_label.grid(row=0, column=1, sticky="w")

        # Account type (if provided)
        if account.account_type:
            type_label = ctk.CTkLabel(
                card,
                text=account.account_type,
                font=Config.get_font('small'),
                text_color=Config.COLORS['text_secondary']
            )
            card.add_content(type_label)

        card.add_separator()

        # Balance
        balance_label = ctk.CTkLabel(
            card,
            text="Balance",
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary']
        )
        card.add_content(balance_label)

        balance_value = ctk.CTkLabel(
            card,
            text=account.balance_formatted,
            font=Config.get_font('heading'),
            text_color=Config.COLORS['primary']
        )
        card.add_content(balance_value)

        card.add_separator()

        # Buttons frame
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        card.add_content(button_frame)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            command=lambda a=account: self._edit_account(a),
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover'],
            font=Config.get_font('body'),
            height=32
        )
        edit_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            command=lambda a=account: self._delete_account(a),
            fg_color=Config.COLORS['error'],
            hover_color=Config.COLORS['error'],
            font=Config.get_font('body'),
            height=32
        )
        delete_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def _add_account(self):
        """Add new account"""
        dialog = AddAccountDialog(
            self,
            self.account_service,
            on_success=self._load_accounts
        )

    def _edit_account(self, account):
        """
        Edit existing account

        Args:
            account: Account object to edit
        """
        dialog = EditAccountDialog(
            self,
            account,
            self.account_service,
            on_success=self._load_accounts
        )

    def _delete_account(self, account):
        """
        Delete account with confirmation

        Args:
            account: Account object to delete
        """
        dialog = DeleteAccountDialog(
            self,
            account,
            self.account_service,
            on_success=self._load_accounts
        )
