"""
Delete Confirmation Dialog
Dialog for confirming transaction deletion
"""
import customtkinter as ctk
from typing import Optional, Callable

from ui.dialogs.transaction_dialog import TransactionDialog
from services import TransactionService
from models import Transaction
from config import Config


class DeleteConfirmationDialog(TransactionDialog):
    """Dialog for confirming transaction deletion"""

    def __init__(
        self,
        parent,
        transaction: Transaction,
        transaction_service: TransactionService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize DeleteConfirmationDialog

        Args:
            parent: Parent widget
            transaction: Transaction object to delete
            transaction_service: Transaction service instance
            on_success: Callback function on successful deletion
        """
        self.transaction = transaction
        self.transaction_service = transaction_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Delete Transaction", width=450, height=300)

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
            "WARNING: Delete Transaction",
            font_type='heading'
        )
        warning_label.grid(row=0, column=0, pady=(0, 20))

        # Confirmation message
        message_label = self.create_label(
            container,
            "Are you sure you want to delete this transaction?",
            font_type='body'
        )
        message_label.grid(row=1, column=0, pady=(0, 20))

        # Transaction details card
        details_frame = ctk.CTkFrame(
            container,
            fg_color=Config.COLORS['surface'],
            border_width=1,
            border_color=Config.COLORS['border'],
            corner_radius=8
        )
        details_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # Date
        date_text = self.transaction.date_formatted
        date_label = self.create_label(
            details_frame,
            f"Date: {date_text}",
            font_type='body'
        )
        date_label.pack(anchor="w", padx=15, pady=(15, 5))

        # Description or Category
        desc = self.transaction.description or (
            self.transaction.category.name if self.transaction.category else "Uncategorized"
        )
        desc_label = self.create_label(
            details_frame,
            f"Description: {desc}",
            font_type='body'
        )
        desc_label.pack(anchor="w", padx=15, pady=5)

        # Amount
        amount_color = Config.COLORS['success'] if self.transaction.is_income() else Config.COLORS['error']
        amount_label = self.create_label(
            details_frame,
            f"Amount: {self.transaction.amount_formatted}",
            font_type='subtitle',
            text_color=amount_color
        )
        amount_label.pack(anchor="w", padx=15, pady=(5, 15))

        # Warning text
        warning_text = self.create_label(
            container,
            "WARNING: This action cannot be undone.",
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
            command=self._delete_transaction,
            style='danger',
            width=120
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def _delete_transaction(self):
        """Delete the transaction"""
        try:
            result = self.transaction_service.delete_transaction(self.transaction.id)

            if result:
                self.show_success("Transaction deleted successfully")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to delete transaction. Please try again.")

        except Exception as e:
            print(f"Error deleting transaction: {e}")
            self.show_error(f"An error occurred: {str(e)}")
