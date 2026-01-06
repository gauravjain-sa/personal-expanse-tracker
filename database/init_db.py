"""
Database Initialization
Handles database creation, table setup, and schema management
"""
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import os

from models import Base
from models import Account, Category, Transaction, Tag
from .connection import DatabaseConnection
from .seed_data import seed_default_data
from config import Config


def create_tables(drop_existing: bool = False) -> bool:
    """
    Create all database tables

    Args:
        drop_existing: If True, drop existing tables before creating

    Returns:
        True if successful, False otherwise
    """
    try:
        db = DatabaseConnection()
        engine = db.engine

        if drop_existing:
            print("Dropping existing tables...")
            Base.metadata.drop_all(engine)

        print("Creating database tables...")
        Base.metadata.create_all(engine)
        print("[OK] Tables created successfully")
        return True

    except SQLAlchemyError as e:
        print(f"[ERROR] Error creating tables: {e}")
        return False


def check_database_exists() -> bool:
    """
    Check if database file exists

    Returns:
        True if database exists, False otherwise
    """
    return os.path.exists(Config.DB_PATH)


def initialize_database(force_recreate: bool = False, seed_data: bool = True) -> bool:
    """
    Initialize database with tables and optional seed data

    Args:
        force_recreate: If True, drop and recreate all tables
        seed_data: If True, populate with default categories

    Returns:
        True if successful, False otherwise
    """
    try:
        db_exists = check_database_exists()

        if db_exists and not force_recreate:
            print(f"Database already exists at: {Config.DB_PATH}")
            print("Use force_recreate=True to reset database")
            return True

        if force_recreate or not db_exists:
            print("Initializing expense tracker database...")
            print(f"Location: {Config.DB_PATH}")

            # Create tables
            if not create_tables(drop_existing=force_recreate):
                return False

            # Seed default data
            if seed_data:
                print("\nSeeding default data...")
                if seed_default_data():
                    print("[OK] Default data seeded successfully")
                else:
                    print("[WARN] Warning: Could not seed default data")
                    return False

            print("\n[OK] Database initialized successfully!")
            return True

    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")
        return False


def reset_database() -> bool:
    """
    Reset database (drop all tables and recreate with seed data)

    Returns:
        True if successful, False otherwise
    """
    print("WARNING: This will delete all data!")
    return initialize_database(force_recreate=True, seed_data=True)


def verify_database() -> dict:
    """
    Verify database integrity and return statistics

    Returns:
        Dictionary with database statistics
    """
    try:
        db = DatabaseConnection()
        session = db.get_session()

        stats = {
            'accounts': session.query(Account).count(),
            'categories': session.query(Category).count(),
            'transactions': session.query(Transaction).count(),
            'tags': session.query(Tag).count()
        }

        session.close()
        return stats

    except SQLAlchemyError as e:
        print(f"Error verifying database: {e}")
        return {}


if __name__ == "__main__":
    """Run database initialization when executed directly"""
    print("=" * 50)
    print("Expense Tracker - Database Initialization")
    print("=" * 50)

    # Initialize database
    if initialize_database(force_recreate=False, seed_data=True):
        # Verify
        print("\nDatabase Statistics:")
        stats = verify_database()
        for table, count in stats.items():
            print(f"  {table.capitalize()}: {count} records")
    else:
        print("\n[ERROR] Database initialization failed!")
