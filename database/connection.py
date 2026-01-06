"""
Database Connection
Manages SQLAlchemy engine and session with singleton pattern
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from typing import Optional
import os

from config import Config


class DatabaseConnection:
    """Singleton database connection manager"""

    _instance: Optional['DatabaseConnection'] = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize database connection (only once)"""
        if self._engine is None:
            self._initialize_connection()

    def _initialize_connection(self):
        """Create database engine and session factory"""
        # Ensure database directory exists
        os.makedirs(Config.DB_DIR, exist_ok=True)

        # Create engine
        self._engine = create_engine(
            Config.DATABASE_URL,
            echo=Config.DEBUG_MODE,  # Log SQL queries in debug mode
            connect_args={'check_same_thread': False}  # Needed for SQLite
        )

        # Create session factory
        self._session_factory = scoped_session(
            sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False
            )
        )

    @property
    def engine(self):
        """Get database engine"""
        return self._engine

    @property
    def session_factory(self):
        """Get session factory"""
        return self._session_factory

    def get_session(self) -> Session:
        """
        Get database session

        Returns:
            Session object for database operations
        """
        return self._session_factory()

    def close_session(self):
        """Close current session"""
        if self._session_factory:
            self._session_factory.remove()

    def dispose(self):
        """Dispose engine and close all connections"""
        if self._session_factory:
            self._session_factory.remove()
        if self._engine:
            self._engine.dispose()


# Global function for easy session access
def get_session() -> Session:
    """
    Get database session (convenience function)

    Returns:
        Session object for database operations

    Usage:
        with get_session() as session:
            # perform database operations
            session.commit()
    """
    db = DatabaseConnection()
    return db.get_session()
