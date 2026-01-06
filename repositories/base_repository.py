"""
Base Repository
Generic CRUD operations for all entities (reusable base class)
"""
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import get_session

# Generic type for model
T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository with generic CRUD operations
    All specific repositories inherit from this class
    """

    def __init__(self, model: Type[T]):
        """
        Initialize repository

        Args:
            model: SQLAlchemy model class
        """
        self.model = model
        self._session: Optional[Session] = None

    @property
    def session(self) -> Session:
        """Get database session (lazy loading)"""
        if self._session is None:
            self._session = get_session()
        return self._session

    def close_session(self):
        """Close current session"""
        if self._session:
            self._session.close()
            self._session = None

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Get entity by ID

        Args:
            id: Entity ID

        Returns:
            Entity if found, None otherwise
        """
        try:
            return self.session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            print(f"Error getting {self.model.__name__} by ID: {e}")
            return None

    def get_all(self, include_inactive: bool = False) -> List[T]:
        """
        Get all entities

        Args:
            include_inactive: If False, filter out inactive entities (if model has is_active field)

        Returns:
            List of entities
        """
        try:
            query = self.session.query(self.model)

            # Filter inactive if model has is_active field
            if not include_inactive and hasattr(self.model, 'is_active'):
                query = query.filter(self.model.is_active == True)

            return query.all()
        except SQLAlchemyError as e:
            print(f"Error getting all {self.model.__name__}: {e}")
            return []

    def create(self, entity: T) -> Optional[T]:
        """
        Create new entity

        Args:
            entity: Entity to create

        Returns:
            Created entity with ID, or None if failed
        """
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error creating {self.model.__name__}: {e}")
            return None

    def update(self, entity: T) -> bool:
        """
        Update existing entity

        Args:
            entity: Entity to update

        Returns:
            True if successful, False otherwise
        """
        try:
            self.session.merge(entity)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error updating {self.model.__name__}: {e}")
            return False

    def delete(self, id: int) -> bool:
        """
        Delete entity by ID

        Args:
            id: Entity ID

        Returns:
            True if successful, False otherwise
        """
        try:
            entity = self.get_by_id(id)
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting {self.model.__name__}: {e}")
            return False

    def soft_delete(self, id: int) -> bool:
        """
        Soft delete entity (set is_active = False)
        Only works if model has is_active field

        Args:
            id: Entity ID

        Returns:
            True if successful, False otherwise
        """
        if not hasattr(self.model, 'is_active'):
            return self.delete(id)

        try:
            entity = self.get_by_id(id)
            if entity:
                entity.is_active = False
                return self.update(entity)
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error soft deleting {self.model.__name__}: {e}")
            return False

    def count(self) -> int:
        """
        Count total entities

        Returns:
            Total count
        """
        try:
            return self.session.query(self.model).count()
        except SQLAlchemyError as e:
            print(f"Error counting {self.model.__name__}: {e}")
            return 0

    def exists(self, id: int) -> bool:
        """
        Check if entity exists

        Args:
            id: Entity ID

        Returns:
            True if exists, False otherwise
        """
        return self.get_by_id(id) is not None

    def find_by_field(self, field_name: str, value: Any) -> List[T]:
        """
        Find entities by field value

        Args:
            field_name: Name of the field
            value: Value to search for

        Returns:
            List of matching entities
        """
        try:
            field = getattr(self.model, field_name)
            return self.session.query(self.model).filter(field == value).all()
        except (AttributeError, SQLAlchemyError) as e:
            print(f"Error finding {self.model.__name__} by {field_name}: {e}")
            return []

    def find_one_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """
        Find single entity by field value

        Args:
            field_name: Name of the field
            value: Value to search for

        Returns:
            Entity if found, None otherwise
        """
        try:
            field = getattr(self.model, field_name)
            return self.session.query(self.model).filter(field == value).first()
        except (AttributeError, SQLAlchemyError) as e:
            print(f"Error finding {self.model.__name__} by {field_name}: {e}")
            return None
