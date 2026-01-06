"""
Expense Tracker Application
Main entry point
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import ExpenseTrackerApp


def main():
    """Main function - entry point for the application"""
    try:
        # Create and run application
        app = ExpenseTrackerApp()
        app.run()

    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
