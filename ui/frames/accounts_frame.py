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
                ("Account Name", 200, "w"),
                ("Type", 120, "w"),
                ("Balance", 120, "e"),
                ("Currency", 80, "center"),
                ("Notes", None, "w"),  # Expandable
                ("Actions", 90, "center")
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

            # Display accounts as list rows
            for account in accounts:
                self._create_account_row(account)

        except Exception as e:
            print(f"Error loading accounts: {e}")
            self.show_error("Failed to load accounts")

    def _create_account_row(self, account):
        """
        Create account row in list view

        Args:
            account: Account object
        """
        row = ctk.CTkFrame(
            self.accounts_container,
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
        name_label.pack(side="left", padx=15, pady=12)
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
            text=notes[:30] + "..." if len(notes) > 30 else notes,
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            anchor="w"
        )
        notes_label.pack(side="left", padx=15, pady=12, fill="x", expand=True)

        # Action buttons
        button_frame = ctk.CTkFrame(row, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=8)

        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️",
            command=lambda a=account: self._edit_account(a),
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover'],
            font=Config.get_font('body'),
            width=40,
            height=32
        )
        edit_btn.pack(side="left", padx=2)

        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️",
            command=lambda a=account: self._delete_account(a),
            fg_color=Config.COLORS['error'],
            hover_color=Config.COLORS['error'],
            font=Config.get_font('body'),
            width=40,
            height=32
        )
        delete_btn.pack(side="left", padx=2)

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
