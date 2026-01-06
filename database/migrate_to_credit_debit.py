"""
Database Migration: Change 'income'/'expense' to 'credit'/'debit'
This script updates all transaction_type and category type values in the database
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from database.connection import get_session
from models import Transaction, Category


def migrate_transaction_types():
    """Migrate transaction types from income/expense to credit/debit"""
    session = get_session()

    try:
        print("Starting migration of transaction types...")

        # Update transactions table
        print("Updating transactions...")
        result = session.execute(
            text("UPDATE transactions SET transaction_type = 'credit' WHERE transaction_type = 'income'")
        )
        credit_count = result.rowcount

        result = session.execute(
            text("UPDATE transactions SET transaction_type = 'debit' WHERE transaction_type = 'expense'")
        )
        debit_count = result.rowcount

        print(f"  - Updated {credit_count} transactions to 'credit'")
        print(f"  - Updated {debit_count} transactions to 'debit'")

        # Update categories table
        print("Updating categories...")
        result = session.execute(
            text("UPDATE categories SET type = 'credit' WHERE type = 'income'")
        )
        credit_cat_count = result.rowcount

        result = session.execute(
            text("UPDATE categories SET type = 'debit' WHERE type = 'expense'")
        )
        debit_cat_count = result.rowcount

        print(f"  - Updated {credit_cat_count} categories to 'credit'")
        print(f"  - Updated {debit_cat_count} categories to 'debit'")

        # Commit changes
        session.commit()
        print("\nMigration completed successfully!")

        # Verify
        print("\nVerifying migration...")
        credit_transactions = session.query(Transaction).filter_by(transaction_type='credit').count()
        debit_transactions = session.query(Transaction).filter_by(transaction_type='debit').count()
        print(f"  - Found {credit_transactions} credit transactions")
        print(f"  - Found {debit_transactions} debit transactions")

        credit_categories = session.query(Category).filter_by(type='credit').count()
        debit_categories = session.query(Category).filter_by(type='debit').count()
        print(f"  - Found {credit_categories} credit categories")
        print(f"  - Found {debit_categories} debit categories")

    except Exception as e:
        print(f"Error during migration: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def rollback_migration():
    """Rollback migration (change credit/debit back to income/expense)"""
    session = get_session()

    try:
        print("Starting rollback of transaction types...")

        # Rollback transactions table
        print("Rolling back transactions...")
        result = session.execute(
            text("UPDATE transactions SET transaction_type = 'income' WHERE transaction_type = 'credit'")
        )
        income_count = result.rowcount

        result = session.execute(
            text("UPDATE transactions SET transaction_type = 'expense' WHERE transaction_type = 'debit'")
        )
        expense_count = result.rowcount

        print(f"  - Updated {income_count} transactions to 'income'")
        print(f"  - Updated {expense_count} transactions to 'expense'")

        # Rollback categories table
        print("Rolling back categories...")
        result = session.execute(
            text("UPDATE categories SET type = 'income' WHERE type = 'credit'")
        )
        income_cat_count = result.rowcount

        result = session.execute(
            text("UPDATE categories SET type = 'expense' WHERE type = 'debit'")
        )
        expense_cat_count = result.rowcount

        print(f"  - Updated {income_cat_count} categories to 'income'")
        print(f"  - Updated {expense_cat_count} categories to 'expense'")

        # Commit changes
        session.commit()
        print("\nRollback completed successfully!")

    except Exception as e:
        print(f"Error during rollback: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        print("=" * 60)
        print("ROLLBACK MODE: Changing credit/debit back to income/expense")
        print("=" * 60)
        rollback_migration()
    else:
        print("=" * 60)
        print("MIGRATION: Changing income/expense to credit/debit")
        print("=" * 60)
        migrate_transaction_types()
