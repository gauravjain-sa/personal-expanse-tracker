"""
Tag Repository
Data access layer for Tag operations
"""
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from models import Tag, Transaction
from .base_repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    """Repository for Tag entity with tag-specific query methods"""

    def __init__(self):
        """Initialize TagRepository"""
        super().__init__(Tag)

    def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Get tag by name

        Args:
            name: Tag name

        Returns:
            Tag if found, None otherwise
        """
        return self.find_one_by_field('name', name)

    def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """
        Get most used tags

        Args:
            limit: Number of tags to return

        Returns:
            List of popular tags
        """
        try:
            # Get all tags and sort by transaction count
            all_tags = self.get_all()
            sorted_tags = sorted(
                all_tags,
                key=lambda tag: tag.transaction_count,
                reverse=True
            )
            return sorted_tags[:limit]
        except Exception as e:
            print(f"Error getting popular tags: {e}")
            return []

    def search_tags(self, search_term: str) -> List[Tag]:
        """
        Search tags by name

        Args:
            search_term: Search term

        Returns:
            List of matching tags
        """
        try:
            return self.session.query(Tag).filter(
                Tag.name.ilike(f'%{search_term}%')
            ).order_by(Tag.name).all()
        except SQLAlchemyError as e:
            print(f"Error searching tags: {e}")
            return []

    def get_tags_for_transaction(self, transaction_id: int) -> List[Tag]:
        """
        Get all tags for a specific transaction

        Args:
            transaction_id: Transaction ID

        Returns:
            List of tags
        """
        try:
            transaction = self.session.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()

            if transaction:
                return transaction.tags
            return []
        except SQLAlchemyError as e:
            print(f"Error getting tags for transaction: {e}")
            return []

    def get_tags_with_counts(self) -> List[dict]:
        """
        Get all tags with their transaction counts

        Returns:
            List of dictionaries with tag info and counts
        """
        try:
            tags = self.get_all()
            return [
                {
                    'id': tag.id,
                    'name': tag.name,
                    'color': tag.color,
                    'transaction_count': tag.transaction_count
                }
                for tag in tags
            ]
        except Exception as e:
            print(f"Error getting tags with counts: {e}")
            return []

    def add_tag_to_transaction(self, transaction_id: int, tag_id: int) -> bool:
        """
        Add tag to transaction

        Args:
            transaction_id: Transaction ID
            tag_id: Tag ID

        Returns:
            True if successful, False otherwise
        """
        try:
            transaction = self.session.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()

            tag = self.get_by_id(tag_id)

            if transaction and tag:
                if tag not in transaction.tags:
                    transaction.tags.append(tag)
                    self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding tag to transaction: {e}")
            return False

    def remove_tag_from_transaction(self, transaction_id: int, tag_id: int) -> bool:
        """
        Remove tag from transaction

        Args:
            transaction_id: Transaction ID
            tag_id: Tag ID

        Returns:
            True if successful, False otherwise
        """
        try:
            transaction = self.session.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()

            tag = self.get_by_id(tag_id)

            if transaction and tag:
                if tag in transaction.tags:
                    transaction.tags.remove(tag)
                    self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error removing tag from transaction: {e}")
            return False

    def get_unused_tags(self) -> List[Tag]:
        """
        Get tags that are not used by any transaction

        Returns:
            List of unused tags
        """
        try:
            all_tags = self.get_all()
            return [tag for tag in all_tags if tag.transaction_count == 0]
        except Exception as e:
            print(f"Error getting unused tags: {e}")
            return []
