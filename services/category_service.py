"""
Category Service
Business logic for category management
"""
from typing import List, Optional, Dict, Any

from models import Category
from repositories import CategoryRepository
from config import Config


class CategoryService:
    """Service for category business logic"""

    def __init__(self):
        """Initialize CategoryService"""
        self.repository = CategoryRepository()

    def create_category(
        self,
        name: str,
        type: str = None,
        parent_id: Optional[int] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Category]:
        """
        Create new category

        Args:
            name: Category name
            type: Optional user-defined type (e.g., 'credit', 'debit', or custom)
            parent_id: Optional parent category ID
            color: Optional color hex code
            icon: Optional icon
            description: Optional description

        Returns:
            Created category or None if failed
        """
        try:
            # Check for duplicate name (if type provided, check within type)
            existing = self.repository.get_by_name(name, type)
            if existing:
                type_msg = f"{type.capitalize()} " if type else ""
                print(f"{type_msg}category '{name}' already exists")
                return None

            # Validate parent if provided
            if parent_id:
                parent = self.repository.get_by_id(parent_id)
                if not parent:
                    print(f"Parent category not found: {parent_id}")
                    return None

                # Parent should have compatible type (if both have types)
                if parent.type and type and parent.type != type:
                    print(f"Parent category has different type ({parent.type} vs {type})")
                    return None

            # Create category
            category = Category(
                name=name,
                type=type,
                parent_id=parent_id,
                color=color,
                icon=icon,
                description=description
            )

            return self.repository.create(category)

        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    def update_category(
        self,
        category_id: int,
        name: Optional[str] = None,
        type: Optional[str] = None,
        parent_id: Optional[int] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> bool:
        """
        Update category details

        Args:
            category_id: Category ID
            name: New name (optional)
            type: New type (optional)
            parent_id: New parent ID (optional)
            color: New color (optional)
            icon: New icon (optional)
            description: New description (optional)
            is_active: New active status (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            category = self.repository.get_by_id(category_id)
            if not category:
                print(f"Category not found: {category_id}")
                return False

            # Update fields
            if name:
                # Check name uniqueness within type
                existing = self.repository.get_by_name(name, category.type)
                if existing and existing.id != category_id:
                    print(f"Category '{name}' already exists")
                    return False
                category.name = name

            if type is not None:
                category.type = type

            if parent_id is not None:
                # Validate parent
                if parent_id != 0:  # 0 means remove parent
                    parent = self.repository.get_by_id(parent_id)
                    if not parent:
                        print(f"Parent category not found: {parent_id}")
                        return False

                    # Prevent circular reference
                    if parent_id == category_id:
                        print("Category cannot be its own parent")
                        return False

                    # Check if parent would create circular reference
                    if self._would_create_circular_reference(category_id, parent_id):
                        print("Cannot set parent: would create circular reference")
                        return False

                    category.parent_id = parent_id
                else:
                    category.parent_id = None

            if color:
                category.color = color

            if icon:
                category.icon = icon

            if description is not None:
                category.description = description

            if is_active is not None:
                category.is_active = is_active

            return self.repository.update(category)

        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    def delete_category(self, category_id: int, force: bool = False) -> bool:
        """
        Delete category (soft delete by default)

        Args:
            category_id: Category ID
            force: If True, hard delete; otherwise soft delete

        Returns:
            True if successful, False otherwise
        """
        try:
            category = self.repository.get_by_id(category_id)
            if not category:
                return False

            # Check if has children - must delete or reassign children first
            if len(category.children) > 0:
                print("Cannot delete category with subcategories")
                return False

            # Check if has transactions
            if len(category.transactions) > 0 and not force:
                # Soft delete to preserve transaction history
                return self.repository.soft_delete(category_id)
            else:
                # Hard delete
                return self.repository.delete(category_id)

        except Exception as e:
            print(f"Error deleting category: {e}")
            return False

    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.repository.get_by_id(category_id)

    def get_all_categories(self, type: Optional[str] = None) -> List[Category]:
        """
        Get all categories

        Args:
            type: Optional type filter ('credit' or 'debit')

        Returns:
            List of categories
        """
        if type:
            return self.repository.get_by_type(type)
        return self.repository.get_all()

    def get_credit_categories(self) -> List[Category]:
        """Get all credit categories (including categories with no type)"""
        credit_cats = self.repository.get_credit_categories()
        untyped_cats = self.repository.get_by_type(None)
        return credit_cats + untyped_cats

    def get_debit_categories(self) -> List[Category]:
        """Get all debit categories (including categories with no type)"""
        debit_cats = self.repository.get_debit_categories()
        untyped_cats = self.repository.get_by_type(None)
        return debit_cats + untyped_cats

    def get_root_categories(self, type: Optional[str] = None) -> List[Category]:
        """Get root categories (no parent)"""
        return self.repository.get_root_categories(type)

    def get_category_hierarchy(self, type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get categories in hierarchical structure"""
        return self.repository.get_category_hierarchy(type)

    def search_categories(self, search_term: str, type: Optional[str] = None) -> List[Category]:
        """Search categories by name"""
        return self.repository.search_categories(search_term, type)

    def get_category_statistics(self, category_id: int) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a category

        Args:
            category_id: Category ID

        Returns:
            Dictionary with category statistics
        """
        try:
            category = self.repository.get_by_id(category_id)
            if not category:
                return None

            # Calculate total amount from transactions
            total_amount = sum(
                transaction.amount for transaction in category.transactions
            )

            return {
                'id': category.id,
                'name': category.full_name,
                'type': category.type,
                'color': category.color,
                'icon': category.icon,
                'transaction_count': len(category.transactions),
                'total_amount': total_amount,
                'has_children': category.is_parent,
                'is_active': category.is_active
            }

        except Exception as e:
            print(f"Error getting category statistics: {e}")
            return None

    def get_categories_with_usage(self, type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get categories with transaction counts

        Args:
            type: Optional type filter

        Returns:
            List of category data with usage counts
        """
        return self.repository.get_categories_with_transaction_count(type)

    def _would_create_circular_reference(self, category_id: int, new_parent_id: int) -> bool:
        """
        Check if setting new parent would create circular reference

        Args:
            category_id: Category being modified
            new_parent_id: Proposed new parent ID

        Returns:
            True if would create circular reference
        """
        # Trace up from new parent to see if we encounter category_id
        current_id = new_parent_id
        while current_id:
            if current_id == category_id:
                return True

            parent = self.repository.get_by_id(current_id)
            if not parent:
                break

            current_id = parent.parent_id

        return False
