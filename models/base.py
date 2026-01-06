"""
Base Model
SQLAlchemy declarative base and common functionality
"""
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class ModelMixin:
    """Mixin class for common model functionality"""

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary

        Returns:
            Dictionary representation of the model
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Convert date/datetime to string
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            result[column.name] = value
        return result

    def __repr__(self) -> str:
        """String representation of the model"""
        class_name = self.__class__.__name__
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.to_dict().items() if k != 'notes')
        return f"<{class_name}({attrs})>"
