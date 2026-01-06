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
    Seed default expense and income categories

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

        # Default expense categories (from Config)
        expense_categories = [
            # Food & Dining
            {'name': 'Groceries', 'type': 'expense', 'icon': '🛒'},
            {'name': 'Restaurants', 'type': 'expense', 'icon': '🍽️'},
            {'name': 'Cafes', 'type': 'expense', 'icon': '☕'},

            # Transportation
            {'name': 'Public Transport', 'type': 'expense', 'icon': '🚇'},
            {'name': 'Fuel', 'type': 'expense', 'icon': '⛽'},
            {'name': 'Vehicle Maintenance', 'type': 'expense', 'icon': '🔧'},
            {'name': 'Taxi/Ride Share', 'type': 'expense', 'icon': '🚕'},

            # Housing
            {'name': 'Rent', 'type': 'expense', 'icon': '🏠'},
            {'name': 'Utilities', 'type': 'expense', 'icon': '💡'},
            {'name': 'Internet', 'type': 'expense', 'icon': '🌐'},
            {'name': 'Phone', 'type': 'expense', 'icon': '📱'},
            {'name': 'Home Maintenance', 'type': 'expense', 'icon': '🔨'},

            # Shopping
            {'name': 'Clothing', 'type': 'expense', 'icon': '👕'},
            {'name': 'Electronics', 'type': 'expense', 'icon': '💻'},
            {'name': 'Books', 'type': 'expense', 'icon': '📚'},
            {'name': 'General Shopping', 'type': 'expense', 'icon': '🛍️'},

            # Health & Fitness
            {'name': 'Medical', 'type': 'expense', 'icon': '🏥'},
            {'name': 'Pharmacy', 'type': 'expense', 'icon': '💊'},
            {'name': 'Gym', 'type': 'expense', 'icon': '💪'},
            {'name': 'Sports', 'type': 'expense', 'icon': '⚽'},

            # Entertainment
            {'name': 'Movies', 'type': 'expense', 'icon': '🎬'},
            {'name': 'Streaming Services', 'type': 'expense', 'icon': '📺'},
            {'name': 'Games', 'type': 'expense', 'icon': '🎮'},
            {'name': 'Hobbies', 'type': 'expense', 'icon': '🎨'},

            # Financial
            {'name': 'Insurance', 'type': 'expense', 'icon': '🛡️'},
            {'name': 'Taxes', 'type': 'expense', 'icon': '📋'},
            {'name': 'Bank Fees', 'type': 'expense', 'icon': '🏦'},
            {'name': 'Investments', 'type': 'expense', 'icon': '📈'},

            # Personal
            {'name': 'Personal Care', 'type': 'expense', 'icon': '💇'},
            {'name': 'Education', 'type': 'expense', 'icon': '🎓'},
            {'name': 'Gifts', 'type': 'expense', 'icon': '🎁'},
            {'name': 'Charity', 'type': 'expense', 'icon': '❤️'},

            # Other
            {'name': 'Other Expenses', 'type': 'expense', 'icon': '📝'},
        ]

        # Default income categories
        income_categories = [
            {'name': 'Salary', 'type': 'income', 'icon': '💼'},
            {'name': 'Freelance', 'type': 'income', 'icon': '💻'},
            {'name': 'Business', 'type': 'income', 'icon': '🏢'},
            {'name': 'Investment Returns', 'type': 'income', 'icon': '📊'},
            {'name': 'Rental Income', 'type': 'income', 'icon': '🏘️'},
            {'name': 'Gifts Received', 'type': 'income', 'icon': '🎁'},
            {'name': 'Refunds', 'type': 'income', 'icon': '💵'},
            {'name': 'Other Income', 'type': 'income', 'icon': '💰'},
        ]

        # Combine all categories
        all_categories = expense_categories + income_categories

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
