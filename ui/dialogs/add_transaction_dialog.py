"""
Add Transaction Dialog
Dialog for adding new transactions
"""
import customtkinter as ctk
from datetime import date
from typing import Optional, Callable
from tkcalendar import DateEntry

from ui.dialogs.transaction_dialog import TransactionDialog
from services import TransactionService, AccountService, CategoryService
from repositories import TagRepository
from config import Config


class AddTransactionDialog(TransactionDialog):
    """Dialog for adding new transactions"""

    def __init__(
        self,
        parent,
        transaction_service: TransactionService,
        account_service: AccountService,
        category_service: CategoryService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize AddTransactionDialog

        Args:
            parent: Parent widget
            transaction_service: Transaction service instance
            account_service: Account service instance
            category_service: Category service instance
            on_success: Callback function on successful creation
        """
        self.transaction_service = transaction_service
        self.account_service = account_service
        self.category_service = category_service
        self.tag_repo = TagRepository()
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Add Transaction", width=600, height=750)

        self._create_form()
        self._load_data()

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

        # Transaction Type field
        type_label = self.create_label(main_container, "Type *")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.type_combobox = self.create_combobox(
            main_container,
            values=["Debit", "Credit"],
            command=self._on_type_changed
        )
        self.type_combobox.set("Debit")
        self.type_combobox.grid(row=current_row, column=1, sticky="ew", padx=10, pady=5)
        current_row += 1

        # Account field
        account_label = self.create_label(main_container, "Account *")
        account_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)

        self.account_combobox = self.create_combobox(main_container, values=[])
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
            "Save",
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
                self.account_combobox.set(account_names[0])
                self.accounts_dict = {acc.name: acc.id for acc in accounts}
            else:
                self.accounts_dict = {}

            # Load categories based on default type (Debit)
            self._load_categories('debit')

            # Load tags
            tags = self.tag_repo.get_all()
            for tag in tags:
                var = ctk.BooleanVar()
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

    def _load_categories(self, transaction_type: str):
        """
        Load categories filtered by type

        Args:
            transaction_type: 'credit' or 'debit'
        """
        try:
            if transaction_type == 'credit':
                categories = self.category_service.get_credit_categories()
            else:
                categories = self.category_service.get_debit_categories()

            if categories:
                category_names = [cat.name for cat in categories]
                self.category_combobox.configure(values=category_names)
                if category_names:
                    self.category_combobox.set(category_names[0])
                self.categories_dict = {cat.name: cat.id for cat in categories}
            else:
                self.category_combobox.configure(values=[])
                self.categories_dict = {}

        except Exception as e:
            print(f"Error loading categories: {e}")

    def _on_type_changed(self, choice):
        """Handle transaction type change"""
        # UI labels now match internal types directly
        transaction_type = choice.lower()  # "Credit" -> "credit", "Debit" -> "debit"
        self._load_categories(transaction_type)

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

        # Account validation
        account_name = self.account_combobox.get()
        if not account_name:
            return False, "Please select an account"

        # Check if account exists
        if not hasattr(self, 'accounts_dict') or not self.accounts_dict:
            return False, "No accounts available. Please create an account first."

        if account_name not in self.accounts_dict:
            return False, "Selected account is invalid"

        return True, ""

    def _save_transaction(self):
        """Save the transaction"""
        print("Save button clicked!")  # Debug

        # Validate form
        is_valid, error_msg = self._validate_form()
        if not is_valid:
            print(f"Validation failed: {error_msg}")  # Debug
            self.show_error(error_msg)
            return

        print("Validation passed, creating transaction...")  # Debug
        try:
            # Get form data
            selected_date = self.date_entry.get_date()
            amount = float(self.amount_entry.get().strip())
            # UI labels now match internal types directly
            transaction_type = self.type_combobox.get().lower()  # "Credit" -> "credit", "Debit" -> "debit"
            account_name = self.account_combobox.get()
            account_id = self.accounts_dict.get(account_name)

            # Double-check account_id (safety check)
            if account_id is None:
                self.show_error("Invalid account selected. Please try again.")
                return

            # Get optional category
            category_name = self.category_combobox.get()
            category_id = self.categories_dict.get(category_name) if category_name else None

            # Get description, merchant, notes
            description = self.description_entry.get().strip() or None
            merchant = self.merchant_entry.get().strip() or None
            notes = self.notes_textbox.get("1.0", "end-1c").strip() or None

            # Get selected tags
            selected_tag_ids = [
                tag_id for tag_id, (var, _) in self.tag_checkboxes.items()
                if var.get()
            ]

            # Create transaction
            result = self.transaction_service.create_transaction(
                date=selected_date,
                amount=amount,
                transaction_type=transaction_type,
                account_id=account_id,
                category_id=category_id,
                description=description,
                notes=notes,
                merchant=merchant,
                tag_ids=selected_tag_ids if selected_tag_ids else None
            )

            if result:
                self.show_success("Transaction created successfully")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to create transaction. Please try again.")

        except Exception as e:
            print(f"Error saving transaction: {e}")
            self.show_error(f"An error occurred: {str(e)}")
