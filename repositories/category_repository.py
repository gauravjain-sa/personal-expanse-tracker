"""
Category Repository
Data access layer for Category operations with hierarchical support
"""
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from models import Category
from .base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entity with hierarchical query methods"""

    def __init__(self):
        """Initialize CategoryRepository"""
        super().__init__(Category)

    def get_by_name(self, name: str, type: Optional[str] = None) -> Optional[Category]:
        """
        Get category by name and optional type

        Args:
            name: Category name
            type: Category type ('credit' or 'debit')

        Returns:
            Category if found, None otherwise
        """
        try:
            query = self.session.query(Category).filter(Category.name == name)
            if type:
                query = query.filter(Category.type == type)
            return query.first()
        except SQLAlchemyError as e:
            print(f"Error getting category by name: {e}")
            return None

    def get_by_type(self, type: str, include_inactive: bool = False) -> List[Category]:
        """
        Get all categories of specific type

        Args:
            type: Category type ('credit' or 'debit')
            include_inactive: Include inactive categories

        Returns:
            List of categories
        """
        try:
            query = self.session.query(Category).filter(Category.type == type)

            if not include_inactive:
                query = query.filter(Category.is_active == True)

            return query.order_by(Category.name).all()
        except SQLAlchemyError as e:
            print(f"Error getting categories by type: {e}")
            return []

    def get_credit_categories(self, include_inactive: bool = False) -> List[Category]:
        """
        Get all credit categories

        Returns:
            List of credit categories
        """
        return self.get_by_type('credit', include_inactive)

    def get_debit_categories(self, include_inactive: bool = False) -> List[Category]:
        """
        Get all debit categories

        Returns:
            List of debit categories
        """
        return self.get_by_type('debit', include_inactive)

    def get_root_categories(self, type: Optional[str] = None) -> List[Category]:
        """
        Get all root categories (no parent)

        Args:
            type: Optional category type filter

        Returns:
            List of root categories
        """
        try:
            query = self.session.query(Category).filter(Category.parent_id == None)

            if type:
                query = query.filter(Category.type == type)

            query = query.filter(Category.is_active == True)
            return query.order_by(Category.name).all()
        except SQLAlchemyError as e:
            print(f"Error getting root categories: {e}")
            return []

    def get_children(self, parent_id: int) -> List[Category]:
        """
        Get all child categories of a parent

        Args:
            parent_id: Parent category ID

        Returns:
            List of child categories
        """
        try:
            return self.session.query(Category).filter(
                Category.parent_id == parent_id,
                Category.is_active == True
            ).order_by(Category.name).all()
        except SQLAlchemyError as e:
            print(f"Error getting child categories: {e}")
            return []

    def get_category_hierarchy(self, type: Optional[str] = None) -> List[dict]:
        """
        Get categories in hierarchical structure

        Args:
            type: Optional category type filter

        Returns:
            List of dictionaries with category hierarchy
        """
        try:
            root_categories = self.get_root_categories(type)

            hierarchy = []
            for root in root_categories:
                hierarchy.append({
                    'category': root,
                    'children': self._get_children_recursive(root.id)
                })

            return hierarchy
        except Exception as e:
            print(f"Error getting category hierarchy: {e}")
            return []

    def _get_children_recursive(self, parent_id: int) -> List[dict]:
        """
        Recursively get children with their children

        Args:
            parent_id: Parent category ID

        Returns:
            List of dictionaries with nested children
        """
        children = self.get_children(parent_id)
        result = []

        for child in children:
            result.append({
                'category': child,
                'children': self._get_children_recursive(child.id)
            })

        return result

    def search_categories(self, search_term: str, type: Optional[str] = None) -> List[Category]:
        """
        Search categories by name

        Args:
            search_term: Search term
            type: Optional category type filter

        Returns:
            List of matching categories
        """
        try:
            query = self.session.query(Category).filter(
                Category.name.ilike(f'%{search_term}%'),
                Category.is_active == True
            )

            if type:
                query = query.filter(Category.type == type)

            return query.order_by(Category.name).all()
        except SQLAlchemyError as e:
            print(f"Error searching categories: {e}")
            return []

    def get_categories_with_transaction_count(self, type: Optional[str] = None) -> List[dict]:
        """
        Get categories with their transaction counts

        Args:
            type: Optional category type filter

        Returns:
            List of dictionaries with category and transaction count
        """
        try:
            query = self.session.query(Category).filter(Category.is_active == True)

            if type:
                query = query.filter(Category.type == type)

            categories = query.all()

            return [
                {
                    'id': cat.id,
                    'name': cat.full_name,
                    'type': cat.type,
                    'color': cat.color,
                    'icon': cat.icon,
                    'transaction_count': len(cat.transactions)
                }
                for cat in categories
            ]
        except Exception as e:
            print(f"Error getting categories with counts: {e}")
            return []
