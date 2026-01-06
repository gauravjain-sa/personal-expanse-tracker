"""
Account Dialog
Dialog for adding/editing accounts
"""
import customtkinter as ctk
from typing import Optional, Callable

from ui.dialogs.transaction_dialog import TransactionDialog
from services import AccountService
from models import Account
from config import Config


class AddAccountDialog(TransactionDialog):
    """Dialog for adding new accounts"""

    def __init__(
        self,
        parent,
        account_service: AccountService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize AddAccountDialog

        Args:
            parent: Parent widget
            account_service: Account service instance
            on_success: Callback function on successful creation
        """
        self.account_service = account_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Add Account", width=500, height=450)

        self._create_form()

    def _create_form(self):
        """Create form layout"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_container.grid_columnconfigure(1, weight=1)

        current_row = 0

        # Account Name
        name_label = self.create_label(main_container, "Account Name *")
        name_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.name_entry = self.create_entry(main_container, placeholder="e.g., Bank of India")
        self.name_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Account Type (Optional)
        type_label = self.create_label(main_container, "Account Type")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.type_entry = self.create_entry(main_container, placeholder="Optional (e.g., Bank, Person, Factory)")
        self.type_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Initial Balance
        balance_label = self.create_label(main_container, "Initial Balance *")
        balance_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.balance_entry = self.create_entry(main_container, placeholder="0.00")
        self.balance_entry.insert(0, "0.00")
        self.balance_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Description
        desc_label = self.create_label(main_container, "Description")
        desc_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.description_entry = self.create_entry(main_container, placeholder="Optional")
        self.description_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=20)

        cancel_btn = self.create_button(
            button_frame,
            "Cancel",
            command=self.close,
            style='secondary',
            width=120
        )
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = self.create_button(
            button_frame,
            "Save",
            command=self._save_account,
            style='primary',
            width=120
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _save_account(self):
        """Save the account"""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Account name is required")
            return

        account_type = self.type_entry.get().strip() or None

        balance_str = self.balance_entry.get().strip()
        try:
            balance = float(balance_str)
        except ValueError:
            self.show_error("Balance must be a valid number")
            return

        notes = self.description_entry.get().strip() or None

        # Create account
        try:
            result = self.account_service.create_account(
                name=name,
                account_type=account_type,
                initial_balance=balance,
                notes=notes
            )

            if result:
                self.show_success("Account created successfully!")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to create account")

        except Exception as e:
            print(f"Error creating account: {e}")
            self.show_error(f"An error occurred: {str(e)}")


class EditAccountDialog(TransactionDialog):
    """Dialog for editing existing accounts"""

    def __init__(
        self,
        parent,
        account: Account,
        account_service: AccountService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize EditAccountDialog

        Args:
            parent: Parent widget
            account: Account object to edit
            account_service: Account service instance
            on_success: Callback function on successful update
        """
        self.account = account
        self.account_service = account_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Edit Account", width=500, height=400)

        self._create_form()
        self._populate_fields()

    def _create_form(self):
        """Create form layout"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_container.grid_columnconfigure(1, weight=1)

        current_row = 0

        # Account Name
        name_label = self.create_label(main_container, "Account Name *")
        name_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.name_entry = self.create_entry(main_container)
        self.name_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Account Type (editable)
        type_label = self.create_label(main_container, "Account Type")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.type_entry = self.create_entry(main_container, placeholder="Optional")
        self.type_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Description
        desc_label = self.create_label(main_container, "Description")
        desc_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.description_entry = self.create_entry(main_container, placeholder="Optional")
        self.description_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=20)

        cancel_btn = self.create_button(
            button_frame,
            "Cancel",
            command=self.close,
            style='secondary',
            width=120
        )
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = self.create_button(
            button_frame,
            "Save Changes",
            command=self._save_account,
            style='primary',
            width=120
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _populate_fields(self):
        """Populate form with account data"""
        self.name_entry.insert(0, self.account.name)

        if self.account.account_type:
            self.type_entry.insert(0, self.account.account_type)

        if self.account.notes:
            self.description_entry.insert(0, self.account.notes)

    def _save_account(self):
        """Save account updates"""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Account name is required")
            return

        account_type = self.type_entry.get().strip() or None
        notes = self.description_entry.get().strip() or None

        # Update account
        try:
            result = self.account_service.update_account(
                account_id=self.account.id,
                name=name,
                account_type=account_type,
                notes=notes
            )

            if result:
                self.show_success("Account updated successfully!")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to update account")

        except Exception as e:
            print(f"Error updating account: {e}")
            self.show_error(f"An error occurred: {str(e)}")
