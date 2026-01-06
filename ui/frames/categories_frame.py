"""
Categories Frame
View and manage categories
"""
import customtkinter as ctk
from typing import Optional

from ui.components import BaseFrame, CardWidget
from ui.dialogs import AddCategoryDialog, EditCategoryDialog, DeleteCategoryDialog
from services import CategoryService
from config import Config


class CategoriesFrame(BaseFrame):
    """Frame for managing categories"""

    def __init__(
        self,
        parent,
        category_service: CategoryService
    ):
        """
        Initialize CategoriesFrame

        Args:
            parent: Parent widget
            category_service: Category service instance
        """
        super().__init__(parent, title="Categories")

        self.category_service = category_service

        self._create_content()
        self._load_categories()

    def _create_content(self):
        """Create frame content"""
        # Configure grid
        self.grid_columnconfigure((0, 1), weight=1)

        # Action buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        add_btn = self.create_button(
            "+ Add Category",
            command=self._add_category,
            style='primary'
        )
        add_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Debit categories card
        expense_card = CardWidget(self, title="Debit Categories")
        expense_card.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        self.expense_list = ctk.CTkScrollableFrame(
            expense_card,
            fg_color="transparent"
        )
        expense_card.add_content(self.expense_list)

        # Credit categories card
        income_card = CardWidget(self, title="Credit Categories")
        income_card.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.income_list = ctk.CTkScrollableFrame(
            income_card,
            fg_color="transparent"
        )
        income_card.add_content(self.income_list)

    def _load_categories(self):
        """Load and display categories"""
        try:
            # Get categories with usage counts
            expense_categories = self.category_service.get_categories_with_usage('debit')
            income_categories = self.category_service.get_categories_with_usage('credit')

            # Clear existing
            for widget in self.expense_list.winfo_children():
                widget.destroy()
            for widget in self.income_list.winfo_children():
                widget.destroy()

            # Display expense categories
            if expense_categories:
                for cat in expense_categories:
                    self._create_category_row(cat, self.expense_list)
            else:
                no_data = ctk.CTkLabel(
                    self.expense_list,
                    text="No debit categories",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text_secondary']
                )
                no_data.pack(pady=20)

            # Display credit categories
            if income_categories:
                for cat in income_categories:
                    self._create_category_row(cat, self.income_list)
            else:
                no_data = ctk.CTkLabel(
                    self.income_list,
                    text="No credit categories",
                    font=Config.get_font('body'),
                    text_color=Config.COLORS['text_secondary']
                )
                no_data.pack(pady=20)

        except Exception as e:
            print(f"Error loading categories: {e}")
            self.show_error("Failed to load categories")

    def _create_category_row(self, category: dict, parent):
        """
        Create category row

        Args:
            category: Category dictionary
            parent: Parent widget
        """
        row = ctk.CTkFrame(
            parent,
            fg_color=Config.COLORS['surface'],
            corner_radius=8,
            border_width=1,
            border_color=Config.COLORS['border']
        )
        row.pack(fill="x", padx=5, pady=5)
        row.grid_columnconfigure(1, weight=1)

        # Icon
        icon = category.get('icon', '📁')
        icon_label = ctk.CTkLabel(
            row,
            text=icon,
            font=('', 20),
            width=40
        )
        icon_label.grid(row=0, column=0, padx=(15, 10), pady=12)

        # Name
        name = category.get('name', 'Unknown')
        name_label = ctk.CTkLabel(
            row,
            text=name,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text_primary']
        )
        name_label.grid(row=0, column=1, padx=10, pady=12, sticky="w")

        # Transaction count
        count = category.get('transaction_count', 0)
        count_label = ctk.CTkLabel(
            row,
            text=f"{count} transactions",
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary'],
            width=120
        )
        count_label.grid(row=0, column=2, padx=(10, 15), pady=12, sticky="e")

        # Edit button
        edit_btn = ctk.CTkButton(
            row,
            text="Edit",
            command=lambda c_id=category.get('id'): self._edit_category(c_id),
            fg_color=Config.COLORS['primary'],
            hover_color=Config.COLORS['primary_hover'],
            font=Config.get_font('body'),
            width=60,
            height=32
        )
        edit_btn.grid(row=0, column=3, padx=5, pady=12)

        # Delete button
        delete_btn = ctk.CTkButton(
            row,
            text="Delete",
            command=lambda c_id=category.get('id'): self._delete_category(c_id),
            fg_color=Config.COLORS['error'],
            hover_color=Config.COLORS['error'],
            font=Config.get_font('body'),
            width=60,
            height=32
        )
        delete_btn.grid(row=0, column=4, padx=5, pady=12)

    def _add_category(self):
        """Add new category"""
        dialog = AddCategoryDialog(
            self,
            self.category_service,
            on_success=self._load_categories
        )

    def _edit_category(self, category_id: int):
        """
        Edit existing category

        Args:
            category_id: Category ID to edit
        """
        # Get full category object
        category = self.category_service.get_category(category_id)
        if category:
            dialog = EditCategoryDialog(
                self,
                category,
                self.category_service,
                on_success=self._load_categories
            )

    def _delete_category(self, category_id: int):
        """
        Delete category with confirmation

        Args:
            category_id: Category ID to delete
        """
        # Get full category object
        category = self.category_service.get_category(category_id)
        if category:
            dialog = DeleteCategoryDialog(
                self,
                category,
                self.category_service,
                on_success=self._load_categories
            )
