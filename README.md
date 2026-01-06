# Expense Tracker

A lightweight desktop application for tracking personal expenses, income, and managing accounts.

## Features

- **Dashboard**: Overview of your financial status with summary statistics
- **Transactions**: Track income and expenses with detailed categorization
- **Accounts**: Manage multiple accounts (bank, credit card, cash, etc.)
- **Categories**: Organize transactions with customizable categories
- **Reports**: View spending patterns and financial insights

## Technology Stack

- **Python 3.11+**
- **CustomTkinter**: Modern UI framework for desktop applications
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight embedded database

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Project Structure

```
expanse-tracker/
├── config.py                 # Application configuration
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
│
├── models/                   # Database models
│   ├── base.py
│   ├── account.py
│   ├── category.py
│   ├── transaction.py
│   └── tag.py
│
├── database/                 # Database management
│   ├── connection.py         # Database connection
│   ├── init_db.py           # Database initialization
│   └── seed_data.py         # Default data seeding
│
├── repositories/             # Data access layer
│   ├── base_repository.py
│   ├── account_repository.py
│   ├── category_repository.py
│   ├── transaction_repository.py
│   └── tag_repository.py
│
├── services/                 # Business logic layer
│   ├── account_service.py
│   ├── category_service.py
│   ├── transaction_service.py
│   └── report_service.py
│
└── ui/                       # User interface
    ├── app.py               # Main application window
    ├── components/          # Reusable UI components
    │   ├── base_frame.py
    │   ├── card_widget.py
    │   └── stat_card.py
    └── frames/              # Application screens
        ├── dashboard_frame.py
        ├── transactions_frame.py
        ├── accounts_frame.py
        └── categories_frame.py
```

## Architecture

The application follows a layered architecture:

1. **UI Layer**: CustomTkinter-based interface
2. **Service Layer**: Business logic and orchestration
3. **Repository Layer**: Data access abstraction
4. **Database Layer**: SQLAlchemy ORM with SQLite

### Key Design Principles

- **Object-Oriented**: All components use OOP principles
- **Modular**: Clear separation of concerns
- **Reusable**: Base classes and shared components
- **No Hardcoding**: Configuration centralized in config.py
- **Type-Safe**: Type hints throughout the codebase

## Database

The application uses SQLite for data storage. The database file is created automatically at:
- `data/expense_tracker.db`

### Default Data

On first run, the application seeds the database with:
- Default expense and income categories
- A sample "Cash" account
- Default tags for categorization

## Usage

### First Run

1. Launch the application
2. The database will be initialized automatically
3. Default categories and a sample account will be created

### Adding Transactions

*(Coming soon - dialog implementation pending)*

### Managing Accounts

1. Navigate to "Accounts" section
2. View all your accounts with current balances
3. Click "Add Account" to create new accounts *(dialog pending)*

### Managing Categories

1. Navigate to "Categories" section
2. View expense and income categories
3. Click "Add Category" to create custom categories *(dialog pending)*

## Future Enhancements

- Transaction add/edit/delete dialogs
- Advanced filtering and search
- Visual charts and graphs
- Budget tracking
- Data export (Excel, CSV, PDF)
- Recurring transactions
- Receipt attachments
- Multi-currency support
- Web version (migration path ready)

## Development

### Adding New Features

The modular architecture makes it easy to extend:

1. **New Model**: Add to `models/` and create migration
2. **New Repository**: Extend `BaseRepository` in `repositories/`
3. **New Service**: Add business logic in `services/`
4. **New UI Frame**: Extend `BaseFrame` in `ui/frames/`

### Testing

```bash
# Run database initialization test
python database/init_db.py

# Run individual modules
python -m models.account
python -m services.transaction_service
```

## License

This is a personal project for expense tracking.

## Contact

For issues or questions, please refer to the project documentation.
