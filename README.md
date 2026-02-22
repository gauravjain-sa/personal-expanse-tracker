# Expense Tracker

A lightweight desktop application for tracking personal expenses, income, and managing accounts.

## Features

- **Dashboard**: Overview of your financial status with summary statistics
- **Transactions**: Track income and expenses with detailed categorization
- **Accounts**: Manage multiple accounts (bank, credit card, cash, etc.)
- **Categories**: Organize transactions with customizable categories
- **Reports**: View spending patterns and financial insights
- **Export**: Export data to Excel/CSV

## Technology Stack

- **Python 3.10+**
- **CustomTkinter**: Modern UI framework for desktop applications
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight embedded database
- **PyInstaller**: Build standalone executable
- **Inno Setup**: Windows installer creation

## Installation

### Prerequisites

- Python 3.10 or higher
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
├── README.md                 # This file
├── start.bat                 # Quick launcher (Windows)
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
│   ├── init_db.py            # Database initialization
│   └── seed_data.py          # Default data seeding
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
│   ├── report_service.py
│   └── export_service.py
│
├── ui/                       # User interface
│   ├── app.py                # Main application window
│   ├── components/           # Reusable UI components
│   ├── dialogs/              # Dialog windows
│   └── frames/               # Application screens
│
├── resources/                # Application resources (icon, etc.)
│
├── documents/                # Project documentation
│   ├── BUILD_QUICKSTART.md   # Quick build guide
│   ├── DEPLOYMENT_GUIDE.md   # Full deployment guide
│   └── ...                   # Design docs, specs, etc.
│
├── build.py                  # Build script (PyInstaller)
├── build_all.bat             # Automated build pipeline
└── installer.iss             # Inno Setup installer script
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
- `%APPDATA%\Expense Tracker\expense_tracker.db`

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

1. Navigate to "Transactions" section
2. Click "Add Transaction"
3. Fill in amount, category, account, date, and description
4. Choose Credit or Debit

### Managing Accounts

1. Navigate to "Accounts" section
2. View all your accounts with current balances
3. Click "Add Account" to create new accounts

### Managing Categories

1. Navigate to "Categories" section
2. View expense and income categories
3. Click "Add Category" to create custom categories

## Building & Distribution

For building the standalone executable and installer, see:
- **Quick guide**: `documents/BUILD_QUICKSTART.md`
- **Full guide**: `documents/DEPLOYMENT_GUIDE.md`

### Quick Build

```bash
build_all.bat
```

This builds the executable, lets you test it, and creates the installer.

## Development

### Adding New Features

The modular architecture makes it easy to extend:

1. **New Model**: Add to `models/`
2. **New Repository**: Extend `BaseRepository` in `repositories/`
3. **New Service**: Add business logic in `services/`
4. **New UI Frame**: Extend `BaseFrame` in `ui/frames/`

## License

This is a personal project for expense tracking.

## Contact

For issues or questions, please refer to the project documentation in `documents/`.
