"""
Edit Transaction Dialog
Dialog for editing existing transactions
"""
import customtkinter as ctk
from datetime import date
from typing import Optional, Callable
from tkcalendar import DateEntry

from ui.dialogs.transaction_dialog import TransactionDialog
from services import TransactionService, AccountService, CategoryService
from repositories import TagRepository
from models import Transaction
from config import Config


class EditTransactionDialog(TransactionDialog):
    """Dialog for editing existing transactions"""

    def __init__(
        self,
        parent,
        transaction: Transaction,
        transaction_service: TransactionService,
        account_service: AccountService,
        category_service: CategoryService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize EditTransactionDialog

        Args:
            parent: Parent widget
            transaction: Transaction object to edit
            transaction_service: Transaction service instance
            account_service: Account service instance
            category_service: Category service instance
            on_success: Callback function on successful update
        """
        self.transaction = transaction
        self.transaction_service = transaction_service
        self.account_service = account_service
        self.category_service = category_service
        self.tag_repo = TagRepository()
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Edit Transaction", width=600, height=750)

        self._create_form()
        self._load_data()
        self._populate_fields()

    def _create_form(self):
        """Create form layout"""
        # Main container with scrolling
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)

        current_row = 0

        # Date field
        date_label = self.create_label(main_container, "Date *")
        date_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=(10, 5))

        self.date_entry = DateEntry(
            main_container,
            width=20,
            background=Config.COLORS['primary'],
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            font=Config.get_font('body')
        )
        self.date_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=(10, 5))
        current_row += 1

        # Amount field
        amount_label = self.create_label(main_container, "Amount *")
        amount_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.amount_entry = self.create_entry(main_container, placeholder="0.00")
        self.amount_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Transaction Type field (read-only)
        type_label = self.create_label(main_container, "Type *")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.type_combobox = self.create_combobox(
            main_container,
            values=["Debit", "Credit"]
        )
        self.type_combobox.configure(state="disabled")
        self.type_combobox.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Account field (read-only)
        account_label = self.create_label(main_container, "Account *")
        account_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.account_combobox = self.create_combobox(main_container, values=[])
        self.account_combobox.configure(state="disabled")
        self.account_combobox.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Category field
        category_label = self.create_label(main_container, "Category")
        category_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.category_combobox = self.create_combobox(main_container, values=[])
        self.category_combobox.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Tags field
        tags_label = self.create_label(main_container, "Tags")
        tags_label.grid(row=current_row, column=0, sticky="nw", padx=10, pady=5)

        self.tags_frame = ctk.CTkScrollableFrame(
            main_container,
            height=100,
            fg_color=Config.COLORS['surface'],
            border_width=1,
            border_color=Config.COLORS['border']
        )
        self.tags_frame.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        self.tag_checkboxes = {}
        current_row += 1

        # Description field
        desc_label = self.create_label(main_container, "Description")
        desc_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.description_entry = self.create_entry(main_container, placeholder="Optional")
        self.description_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Merchant field
        merchant_label = self.create_label(main_container, "Merchant")
        merchant_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.merchant_entry = self.create_entry(main_container, placeholder="Optional")
        self.merchant_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Notes field
        notes_label = self.create_label(main_container, "Notes")
        notes_label.grid(row=current_row, column=0, sticky="nw", padx=10, pady=5)

        self.notes_textbox = self.create_textbox(main_container, height=80)
        self.notes_textbox.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

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

        save_btn = self.create_button(
            button_frame,
            "Save Changes",
            command=self._save_transaction,
            style='primary',
            width=120
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _load_data(self):
        """Load accounts, categories, and tags"""
        try:
            # Load accounts
            accounts = self.account_service.get_all_accounts(include_inactive=False)
            if accounts:
                account_names = [acc.name for acc in accounts]
                self.account_combobox.configure(values=account_names)
                self.accounts_dict = {acc.name: acc.id for acc in accounts}
            else:
                self.accounts_dict = {}

            # Load categories based on transaction type
            transaction_type = self.transaction.transaction_type
            if transaction_type == 'credit':
                categories = self.category_service.get_credit_categories()
            else:
                categories = self.category_service.get_debit_categories()

            if categories:
                category_names = [cat.name for cat in categories]
                self.category_combobox.configure(values=category_names)
                self.categories_dict = {cat.name: cat.id for cat in categories}
            else:
                self.category_combobox.configure(values=[])
                self.categories_dict = {}

            # Load tags
            tags = self.tag_repo.get_all()
            existing_tag_ids = [tag.id for tag in self.transaction.tags]

            for tag in tags:
                var = ctk.BooleanVar(value=(tag.id in existing_tag_ids))
                cb = ctk.CTkCheckBox(
                    self.tags_frame,
                    text=tag.name,
                    variable=var,
                    font=Config.get_font('body'),
                    fg_color=Config.COLORS['primary']
                )
                cb.pack(anchor="w", padx=5, pady=2)
                self.tag_checkboxes[tag.id] = (var, tag.name)

        except Exception as e:
            print(f"Error loading data: {e}")
            self.show_error("Failed to load form data")

    def _populate_fields(self):
        """Populate form fields with transaction data"""
        try:
            # Set date
            self.date_entry.set_date(self.transaction.date)

            # Set amount
            self.amount_entry.insert(0, str(self.transaction.amount))

            # Set type (capitalize for display)
            transaction_type = self.transaction.transaction_type.capitalize()
            self.type_combobox.set(transaction_type)

            # Set account
            if self.transaction.account:
                self.account_combobox.set(self.transaction.account.name)

            # Set category
            if self.transaction.category:
                self.category_combobox.set(self.transaction.category.name)

            # Set description
            if self.transaction.description:
                self.description_entry.insert(0, self.transaction.description)

            # Set merchant
            if self.transaction.merchant:
                self.merchant_entry.insert(0, self.transaction.merchant)

            # Set notes
            if self.transaction.notes:
                self.notes_textbox.insert("1.0", self.transaction.notes)

        except Exception as e:
            print(f"Error populating fields: {e}")
            self.show_error("Failed to populate form fields")

    def _validate_form(self) -> tuple[bool, str]:
        """
        Validate form data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Date validation (from date picker, always valid)
        try:
            selected_date = self.date_entry.get_date()
        except Exception:
            return False, "Please select a valid date"

        # Amount validation
        amount_str = self.amount_entry.get().strip()
        if not amount_str:
            return False, "Amount is required"

        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Amount must be a valid number"

        return True, ""

    def _save_transaction(self):
        """Save the transaction updates"""
        # Validate form
        is_valid, error_msg = self._validate_form()
        if not is_valid:
            self.show_error(error_msg)
            return

        try:
            # Get form data
            selected_date = self.date_entry.get_date()
            amount = float(self.amount_entry.get().strip())

            # Get optional category
            category_name = self.category_combobox.get()
            category_id = self.categories_dict.get(category_name) if category_name else None

            # Get description, merchant, notes
            description = self.description_entry.get().strip() or None
            merchant = self.merchant_entry.get().strip() or None
            notes = self.notes_textbox.get("1.0", "end-1c").strip() or None

            # Update transaction
            result = self.transaction_service.update_transaction(
                transaction_id=self.transaction.id,
                date=selected_date,
                amount=amount,
                category_id=category_id,
                description=description,
                notes=notes,
                merchant=merchant
            )

            if result:
                # Update tags
                # Get currently selected tags
                selected_tag_ids = [
                    tag_id for tag_id, (var, _) in self.tag_checkboxes.items()
                    if var.get()
                ]

                # Get existing tags
                existing_tag_ids = [tag.id for tag in self.transaction.tags]

                # Remove tags that are no longer selected
                for tag_id in existing_tag_ids:
                    if tag_id not in selected_tag_ids:
                        self.tag_repo.remove_tag_from_transaction(self.transaction.id, tag_id)

                # Add newly selected tags
                for tag_id in selected_tag_ids:
                    if tag_id not in existing_tag_ids:
                        self.tag_repo.add_tag_to_transaction(self.transaction.id, tag_id)

                self.show_success("Transaction updated successfully")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to update transaction. Please try again.")

        except Exception as e:
            print(f"Error saving transaction: {e}")
            self.show_error(f"An error occurred: {str(e)}")
