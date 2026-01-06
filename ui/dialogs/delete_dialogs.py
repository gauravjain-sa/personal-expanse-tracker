"""
Delete Confirmation Dialogs
Dialogs for confirming deletion of various entities
"""
import customtkinter as ctk
from typing import Optional, Callable

from ui.dialogs.transaction_dialog import TransactionDialog
from services import AccountService, CategoryService
from models import Account, Category
from config import Config


class DeleteAccountDialog(TransactionDialog):
    """Dialog for confirming account deletion"""

    def __init__(
        self,
        parent,
        account: Account,
        account_service: AccountService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize DeleteAccountDialog

        Args:
            parent: Parent widget
            account: Account object to delete
            account_service: Account service instance
            on_success: Callback function on successful deletion
        """
        self.account = account
        self.account_service = account_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Delete Account", width=450, height=300)

        self._create_content()

    def _create_content(self):
        """Create dialog content"""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        container.grid_columnconfigure(0, weight=1)

        # Warning icon and title
        warning_label = self.create_label(
            container,
            "WARNING: Delete Account",
            font_type='heading'
        )
        warning_label.grid(row=0, column=0, pady=(0, 20))

        # Confirmation message
        message_label = self.create_label(
            container,
            "Are you sure you want to delete this account?",
            font_type='body'
        )
        message_label.grid(row=1, column=0, pady=(0, 20))

        # Account details card
        details_frame = ctk.CTkFrame(
            container,
            fg_color=Config.COLORS['surface'],
            border_width=1,
            border_color=Config.COLORS['border'],
            corner_radius=8
        )
        details_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Name
        name_label = self.create_label(
            details_frame,
            f"Account: {self.account.name}",
            font_type='subtitle'
        )
        name_label.pack(anchor="w", padx=15, pady=(15, 5))

        # Account type (if provided)
        if self.account.account_type:
            type_label = self.create_label(
                details_frame,
                self.account.account_type,
                font_type='body',
                text_color=Config.COLORS['text_secondary']
            )
            type_label.pack(anchor="w", padx=15, pady=5)

        # Balance
        balance_label = self.create_label(
            details_frame,
            f"Balance: {self.account.balance_formatted}",
            font_type='subtitle',
            text_color=Config.COLORS['primary']
        )
        balance_label.pack(anchor="w", padx=15, pady=(5, 15))

        # Warning text
        warning_text = self.create_label(
            container,
            "WARNING: This action cannot be undone.\nAll transactions in this account will also be deleted.",
            font_type='small',
            text_color=Config.COLORS['error']
        )
        warning_text.grid(row=3, column=0, pady=(10, 20))

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(0, 20))

        cancel_btn = self.create_button(
            button_frame,
            "Cancel",
            command=self.close,
            style='secondary',
            width=120
        )
        cancel_btn.grid(row=0, column=0, padx=10)

        delete_btn = self.create_button(
            button_frame,
            "Delete",
            command=self._delete_account,
            style='danger',
            width=120
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def _delete_account(self):
        """Delete the account"""
        try:
            result = self.account_service.delete_account(self.account.id)

            if result:
                self.show_success("Account deleted successfully")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to delete account. It may have associated transactions.")

        except Exception as e:
            print(f"Error deleting account: {e}")
            self.show_error(f"An error occurred: {str(e)}")


class DeleteCategoryDialog(TransactionDialog):
    """Dialog for confirming category deletion"""

    def __init__(
        self,
        parent,
        category: Category,
        category_service: CategoryService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize DeleteCategoryDialog

        Args:
            parent: Parent widget
            category: Category object to delete
            category_service: Category service instance
            on_success: Callback function on successful deletion
        """
        self.category = category
        self.category_service = category_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Delete Category", width=450, height=300)

        self._create_content()

    def _create_content(self):
        """Create dialog content"""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        container.grid_columnconfigure(0, weight=1)

        # Warning icon and title
        warning_label = self.create_label(
            container,
            "WARNING: Delete Category",
            font_type='heading'
        )
        warning_label.grid(row=0, column=0, pady=(0, 20))

        # Confirmation message
        message_label = self.create_label(
            container,
            "Are you sure you want to delete this category?",
            font_type='body'
        )
        message_label.grid(row=1, column=0, pady=(0, 20))

        # Category details card
        details_frame = ctk.CTkFrame(
            container,
            fg_color=Config.COLORS['surface'],
            border_width=1,
            border_color=Config.COLORS['border'],
            corner_radius=8
        )
        details_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Name
        name_label = self.create_label(
            details_frame,
            f"Category: {self.category.name}",
            font_type='subtitle'
        )
        name_label.pack(anchor="w", padx=15, pady=(15, 5))

        # Category type (if provided)
        if self.category.type:
            type_label = self.create_label(
                details_frame,
                self.category.type.capitalize(),
                font_type='body',
                text_color=Config.COLORS['text_secondary']
            )
            type_label.pack(anchor="w", padx=15, pady=(5, 15))

        # Warning text
        warning_text = self.create_label(
            container,
            "WARNING: This action cannot be undone.\nTransactions using this category will become uncategorized.",
            font_type='small',
            text_color=Config.COLORS['error']
        )
        warning_text.grid(row=3, column=0, pady=(10, 20))

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, pady=(0, 20))

        cancel_btn = self.create_button(
            button_frame,
            "Cancel",
            command=self.close,
            style='secondary',
            width=120
        )
        cancel_btn.grid(row=0, column=0, padx=10)

        delete_btn = self.create_button(
            button_frame,
            "Delete",
            command=self._delete_category,
            style='danger',
            width=120
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def _delete_category(self):
        """Delete the category"""
        try:
            result = self.category_service.delete_category(self.category.id)

            if result:
                self.show_success("Category deleted successfully")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to delete category. It may be in use.")

        except Exception as e:
            print(f"Error deleting category: {e}")
            self.show_error(f"An error occurred: {str(e)}")
