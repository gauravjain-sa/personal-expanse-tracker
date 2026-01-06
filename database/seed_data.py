"""
Seed Data
Populates database with default categories and sample data
"""
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional

from models import Category, Account, Tag
from .connection import DatabaseConnection
from config import Config


def seed_default_categories() -> bool:
    """
    Seed default debit and credit categories

    Returns:
        True if successful, False otherwise
    """
    db = DatabaseConnection()
    session = db.get_session()

    try:
        # Check if categories already exist
        existing_count = session.query(Category).count()
        if existing_count > 0:
            print(f"  Categories already exist ({existing_count} found), skipping...")
            return True

        print("  Creating default categories...")

        # Default debit categories (generic high-level)
        debit_categories = [
            {'name': 'Food & Dining', 'type': 'debit', 'icon': '🍽️'},
            {'name': 'Transportation', 'type': 'debit', 'icon': '🚗'},
            {'name': 'Shopping', 'type': 'debit', 'icon': '🛒'},
            {'name': 'Bills & Utilities', 'type': 'debit', 'icon': '💡'},
            {'name': 'Healthcare', 'type': 'debit', 'icon': '🏥'},
            {'name': 'Entertainment', 'type': 'debit', 'icon': '🎬'},
            {'name': 'Education', 'type': 'debit', 'icon': '🎓'},
            {'name': 'Other Debits', 'type': 'debit', 'icon': '📝'},
        ]

        # Default credit categories (generic high-level)
        credit_categories = [
            {'name': 'Salary/Wages', 'type': 'credit', 'icon': '💼'},
            {'name': 'Business Income', 'type': 'credit', 'icon': '🏢'},
            {'name': 'Investment Returns', 'type': 'credit', 'icon': '📊'},
            {'name': 'Other Credits', 'type': 'credit', 'icon': '💰'},
        ]

        # Combine all categories
        all_categories = debit_categories + credit_categories

        # Create category objects
        for cat_data in all_categories:
            category = Category(
                name=cat_data['name'],
                type=cat_data['type'],
                icon=cat_data.get('icon')
            )
            session.add(category)

        session.commit()
        print(f"  [OK] Created {len(all_categories)} default categories")
        return True

    except IntegrityError as e:
        session.rollback()
        print(f"  [WARN] Some categories already exist: {e}")
        return True  # Not a critical error

    except SQLAlchemyError as e:
        session.rollback()
        print(f"  [ERROR] Error seeding categories: {e}")
        return False

    finally:
        session.close()


def seed_sample_account() -> bool:
    """
    Create a sample account for initial use

    Returns:
        True if successful, False otherwise
    """
    db = DatabaseConnection()
    session = db.get_session()

    try:
        # Check if accounts already exist
        existing_count = session.query(Account).count()
        if existing_count > 0:
            print(f"  Accounts already exist ({existing_count} found), skipping...")
            return True

        print("  Creating sample account...")

        # Create default cash account
        cash_account = Account(
            name="Cash",
            account_type="cash",
            initial_balance=0.0,
            currency=Config.CURRENCY_CODE
        )
        session.add(cash_account)
        session.commit()

        print("  [OK] Created sample account: Cash")
        return True

    except IntegrityError:
        session.rollback()
        print("  [WARN] Sample account already exists")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        print(f"  [ERROR] Error creating sample account: {e}")
        return False

    finally:
        session.close()


def seed_default_tags() -> bool:
    """
    Create default tags for flexible transaction categorization

    Returns:
        True if successful, False otherwise
    """
    db = DatabaseConnection()
    session = db.get_session()

    try:
        # Check if tags already exist
        existing_count = session.query(Tag).count()
        if existing_count > 0:
            print(f"  Tags already exist ({existing_count} found), skipping...")
            return True

        print("  Creating default tags...")

        default_tags = [
            {'name': 'Urgent', 'color': '#E74C3C'},
            {'name': 'Recurring', 'color': '#3498DB'},
            {'name': 'Business', 'color': '#2ECC71'},
            {'name': 'Personal', 'color': '#9B59B6'},
            {'name': 'Tax Deductible', 'color': '#F39C12'},
            {'name': 'Reimbursable', 'color': '#1ABC9C'},
        ]

        for tag_data in default_tags:
            tag = Tag(name=tag_data['name'], color=tag_data['color'])
            session.add(tag)

        session.commit()
        print(f"  [OK] Created {len(default_tags)} default tags")
        return True

    except IntegrityError:
        session.rollback()
        print("  [WARN] Some tags already exist")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        print(f"  [ERROR] Error seeding tags: {e}")
        return False

    finally:
        session.close()


def seed_default_data() -> bool:
    """
    Seed all default data (categories, sample account, tags)

    Returns:
        True if all successful, False otherwise
    """
    success = True

    # Seed categories
    if not seed_default_categories():
        success = False

    # Seed sample account
    if not seed_sample_account():
        success = False

    # Seed tags
    if not seed_default_tags():
        success = False

    return success


if __name__ == "__main__":
    """Run seed data when executed directly"""
    print("Seeding default data...")
    if seed_default_data():
        print("[OK] All default data seeded successfully!")
    else:
        print("[ERROR] Some data seeding failed!")
