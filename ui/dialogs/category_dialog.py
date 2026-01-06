"""
Category Dialog
Dialog for adding/editing categories
"""
import customtkinter as ctk
from typing import Optional, Callable

from ui.dialogs.transaction_dialog import TransactionDialog
from services import CategoryService
from models import Category
from config import Config


class AddCategoryDialog(TransactionDialog):
    """Dialog for adding new categories"""

    def __init__(
        self,
        parent,
        category_service: CategoryService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize AddCategoryDialog

        Args:
            parent: Parent widget
            category_service: Category service instance
            on_success: Callback function on successful creation
        """
        self.category_service = category_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Add Category", width=500, height=450)

        self._create_form()

    def _create_form(self):
        """Create form layout"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_container.grid_columnconfigure(1, weight=1)

        current_row = 0

        # Category Name
        name_label = self.create_label(main_container, "Category Name *")
        name_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.name_entry = self.create_entry(main_container, placeholder="e.g., Groceries")
        self.name_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Category Type
        type_label = self.create_label(main_container, "Category Type")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.type_entry = self.create_entry(main_container, placeholder="Optional (e.g., Credit, Debit, etc.)")
        self.type_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Icon
        icon_label = self.create_label(main_container, "Icon")
        icon_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.icon_entry = self.create_entry(main_container, placeholder="emoji (e.g., 🛒)")
        self.icon_entry.insert(0, "📁")
        self.icon_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
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
            command=self._save_category,
            style='primary',
            width=120
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _save_category(self):
        """Save the category"""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Category name is required")
            return

        category_type = self.type_entry.get().strip() or None

        icon = self.icon_entry.get().strip()
        if not icon:
            icon = "📁"

        description = self.description_entry.get().strip() or None

        # Create category
        try:
            result = self.category_service.create_category(
                name=name,
                type=category_type,
                icon=icon,
                description=description
            )

            if result:
                self.show_success("Category created successfully!")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to create category")

        except Exception as e:
            print(f"Error creating category: {e}")
            self.show_error(f"An error occurred: {str(e)}")


class EditCategoryDialog(TransactionDialog):
    """Dialog for editing existing categories"""

    def __init__(
        self,
        parent,
        category: Category,
        category_service: CategoryService,
        on_success: Optional[Callable] = None
    ):
        """
        Initialize EditCategoryDialog

        Args:
            parent: Parent widget
            category: Category object to edit
            category_service: Category service instance
            on_success: Callback function on successful update
        """
        self.category = category
        self.category_service = category_service
        self.on_success_callback = on_success or (lambda: None)

        super().__init__(parent, title="Edit Category", width=500, height=450)

        self._create_form()
        self._populate_fields()

    def _create_form(self):
        """Create form layout"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_container.grid_columnconfigure(1, weight=1)

        current_row = 0

        # Category Name
        name_label = self.create_label(main_container, "Category Name *")
        name_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.name_entry = self.create_entry(main_container)
        self.name_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Category Type (editable)
        type_label = self.create_label(main_container, "Category Type")
        type_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.type_entry = self.create_entry(main_container, placeholder="Optional")
        self.type_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
        current_row += 1

        # Icon
        icon_label = self.create_label(main_container, "Icon")
        icon_label.grid(row=current_row, column=0, sticky="w", padx=10, pady=10)

        self.icon_entry = self.create_entry(main_container)
        self.icon_entry.grid(row=current_row, column=1, sticky="ew", padx=10, pady=10)
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
            command=self._save_category,
            style='primary',
            width=120
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _populate_fields(self):
        """Populate form with category data"""
        self.name_entry.insert(0, self.category.name)

        if self.category.type:
            self.type_entry.insert(0, self.category.type)

        self.icon_entry.insert(0, self.category.icon or "📁")

        if self.category.description:
            self.description_entry.insert(0, self.category.description)

    def _save_category(self):
        """Save category updates"""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            self.show_error("Category name is required")
            return

        category_type = self.type_entry.get().strip() or None

        icon = self.icon_entry.get().strip()
        if not icon:
            icon = "📁"

        description = self.description_entry.get().strip() or None

        # Update category
        try:
            result = self.category_service.update_category(
                category_id=self.category.id,
                name=name,
                type=category_type,
                icon=icon,
                description=description
            )

            if result:
                self.show_success("Category updated successfully!")
                self.on_success_callback()
                self.close()
            else:
                self.show_error("Failed to update category")

        except Exception as e:
            print(f"Error updating category: {e}")
            self.show_error(f"An error occurred: {str(e)}")
