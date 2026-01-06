# Expense Tracker - Windows Desktop Application Specification

**Version:** 1.0
**Target Platform:** Windows 10/11 (64-bit)
**Architecture:** Simple, Object-Oriented, Native Desktop
**Philosophy:** Lightweight, Easy to Maintain, No Over-Engineering

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Technology Stack](#technology-stack)
3. [Application Architecture](#application-architecture)
4. [Object-Oriented Design](#object-oriented-design)
5. [Database Design](#database-design)
6. [User Interface Design](#user-interface-design)
7. [Core Features](#core-features)
8. [Project Structure](#project-structure)
9. [Development Setup](#development-setup)
10. [Build & Distribution](#build--distribution)
11. [Implementation Guide](#implementation-guide)

---

## Executive Summary

### Goal
Build a **simple, lightweight Windows desktop application** for personal expense tracking with:
- ✅ Native Windows UI (no browser)
- ✅ Single executable (~30-50 MB)
- ✅ SQLite database (single file)
- ✅ Object-oriented, clean code
- ✅ Easy to maintain and extend
- ✅ Fast startup (<2 seconds)

### Technology Choice: Python + CustomTkinter

**Why This Stack?**
1. **Lightweight** - CustomTkinter is built on Tkinter (included with Python)
2. **Modern UI** - Looks professional, not dated
3. **Object-Oriented** - Natural fit for Python classes
4. **Simple** - No complex frameworks, no browser, no web server
5. **Easy Maintenance** - Small codebase, clear structure
6. **SQLite** - Zero-config database, single file
7. **PyInstaller** - Creates single Windows executable

**What We're NOT Using:**
- ❌ Web browser / localhost server (too complex)
- ❌ FastAPI / Flask (not needed for desktop)
- ❌ React / JavaScript (over-engineering)
- ❌ Electron / Tauri (too heavy)
- ❌ Multiple processes (keep it simple)

---

## Technology Stack

### Core Technologies

```yaml
Language: Python 3.11+
UI Framework: CustomTkinter 5.2+
Database: SQLite 3
ORM: SQLAlchemy 2.0+
Packaging: PyInstaller 6.0+
```

### Dependencies (Minimal)

```python
# requirements.txt
customtkinter==5.2.1      # Modern UI framework
Pillow==10.1.0            # Image handling
sqlalchemy==2.0.23        # Database ORM
pandas==2.1.4             # Data processing for reports
openpyxl==3.1.2           # Excel export
tkcalendar==1.6.1         # Date picker widget
```

**Total Dependencies:** 6 packages (plus their sub-dependencies)
**Approximate Size:** 30-50 MB when packaged

---

## Application Architecture

### Simple Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│         EXPENSE TRACKER.EXE                     │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │         PRESENTATION LAYER                │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  CustomTkinter UI (Native Windows)  │ │ │
│  │  │  - Main Window (CTk)                │ │ │
│  │  │  - Dashboard Frame                  │ │ │
│  │  │  - Transaction Frame                │ │ │
│  │  │  - Account Frame                    │ │ │
│  │  │  - Category Frame                   │ │ │
│  │  │  - Reports Frame                    │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
│                      ↓                          │
│  ┌───────────────────────────────────────────┐ │
│  │         BUSINESS LOGIC LAYER              │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  Service Classes (Python)           │ │ │
│  │  │  - TransactionService               │ │ │
│  │  │  - AccountService                   │ │ │
│  │  │  - CategoryService                  │ │ │
│  │  │  - ReportService                    │ │ │
│  │  │  - ExportService                    │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
│                      ↓                          │
│  ┌───────────────────────────────────────────┐ │
│  │         DATA ACCESS LAYER                 │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  Repository Classes (Python)        │ │ │
│  │  │  - TransactionRepository            │ │ │
│  │  │  - AccountRepository                │ │ │
│  │  │  - CategoryRepository               │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
│                      ↓                          │
│  ┌───────────────────────────────────────────┐ │
│  │         DATABASE LAYER                    │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  SQLite + SQLAlchemy ORM            │ │ │
│  │  │  - expense_tracker.db               │ │ │
│  │  │  Location: %APPDATA%/ExpenseTracker/│ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Layered Architecture Benefits

1. **Presentation Layer** - UI only, no business logic
2. **Business Logic Layer** - All rules, calculations, validations
3. **Data Access Layer** - Database operations only
4. **Clean Separation** - Easy to test and maintain

---

## Object-Oriented Design

### Class Hierarchy

```
Application (Main Entry Point)
│
├── UI Layer (CustomTkinter)
│   ├── MainWindow(ctk.CTk)
│   │   ├── Sidebar
│   │   ├── DashboardFrame(BaseFrame)
│   │   ├── TransactionsFrame(BaseFrame)
│   │   ├── AccountsFrame(BaseFrame)
│   │   ├── CategoriesFrame(BaseFrame)
│   │   └── ReportsFrame(BaseFrame)
│   │
│   └── Dialogs
│       ├── TransactionDialog(BaseDialog)
│       ├── AccountDialog(BaseDialog)
│       └── CategoryDialog(BaseDialog)
│
├── Service Layer
│   ├── TransactionService
│   ├── AccountService
│   ├── CategoryService
│   ├── ReportService
│   └── ExportService
│
├── Repository Layer
│   ├── BaseRepository
│   ├── TransactionRepository(BaseRepository)
│   ├── AccountRepository(BaseRepository)
│   └── CategoryRepository(BaseRepository)
│
└── Model Layer (SQLAlchemy)
    ├── Base
    ├── Transaction(Base)
    ├── Account(Base)
    ├── Category(Base)
    └── Tag(Base)
```

### Key Design Patterns

1. **Repository Pattern** - Abstracts database operations
2. **Service Pattern** - Encapsulates business logic
3. **MVC Pattern** - Model-View-Controller separation
4. **Singleton Pattern** - Database session management
5. **Factory Pattern** - Dialog/Frame creation

---

## Database Design

### SQLite Schema (Same as Before)

```sql
-- ACCOUNTS TABLE
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    account_type TEXT NOT NULL,  -- bank, credit_card, cash, wallet
    initial_balance REAL NOT NULL DEFAULT 0.0,
    current_balance REAL NOT NULL DEFAULT 0.0,
    currency TEXT NOT NULL DEFAULT 'USD',
    is_active INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORIES TABLE
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    type TEXT NOT NULL,  -- income, expense
    color TEXT,  -- Hex color
    icon TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,  -- income, expense, transfer
    direction TEXT NOT NULL,  -- debit, credit
    account_id INTEGER NOT NULL,
    category_id INTEGER,
    description TEXT,
    notes TEXT,
    merchant TEXT,
    receipt_path TEXT,
    is_transfer INTEGER NOT NULL DEFAULT 0,
    transfer_to_account_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (transfer_to_account_id) REFERENCES accounts(id) ON DELETE SET NULL
);

-- TAGS TABLE
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    color TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION_TAGS (Many-to-Many)
CREATE TABLE transaction_tags (
    transaction_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (transaction_id, tag_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- INDEXES
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
```

### SQLAlchemy Models (Object-Oriented)

**File: `models/account.py`**
```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    account_type = Column(String(50), nullable=False)
    initial_balance = Column(Float, nullable=False, default=0.0)
    current_balance = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), nullable=False, default='USD')
    is_active = Column(Boolean, nullable=False, default=True)
    notes = Column(String(500))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    transactions = relationship("Transaction", back_populates="account", foreign_keys="Transaction.account_id")

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.name}', balance={self.current_balance})>"

    def to_dict(self):
        """Convert to dictionary for easy serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'is_active': self.is_active,
            'notes': self.notes
        }
```

**File: `models/transaction.py`**
```python
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # income, expense, transfer
    direction = Column(String(10), nullable=False)  # debit, credit
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String(255))
    notes = Column(Text)
    merchant = Column(String(100))
    receipt_path = Column(String(500))
    is_transfer = Column(Boolean, nullable=False, default=False)
    transfer_to_account_id = Column(Integer, ForeignKey('accounts.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, date={self.date}, amount={self.amount}, type='{self.transaction_type}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'direction': self.direction,
            'account_id': self.account_id,
            'category_id': self.category_id,
            'description': self.description,
            'merchant': self.merchant,
            'is_transfer': self.is_transfer
        }
```

---

## User Interface Design

### CustomTkinter Modern Look

**Color Theme:**
```python
# Dark Blue Theme
PRIMARY_COLOR = "#1f538d"        # Dark blue
SECONDARY_COLOR = "#14375e"      # Darker blue
ACCENT_COLOR = "#2fa572"         # Green (for income)
DANGER_COLOR = "#e74c3c"         # Red (for expenses)
BG_COLOR = "#1a1a1a"             # Dark background
FG_COLOR = "#ffffff"             # White text
CARD_COLOR = "#2b2b2b"           # Card background
```

**Font Configuration:**
```python
FONT_FAMILY = "Segoe UI"
FONT_SIZES = {
    'title': 24,
    'heading': 18,
    'subheading': 14,
    'body': 12,
    'small': 10
}
```

### Main Window Layout

```
┌────────────────────────────────────────────────────────────────┐
│ EXPENSE TRACKER                                    [_] [□] [X] │
├──────────┬─────────────────────────────────────────────────────┤
│          │                                                     │
│ SIDEBAR  │  MAIN CONTENT AREA                                 │
│ (200px)  │  (Dynamic - Changes based on selection)            │
│          │                                                     │
│ ┌──────┐ │  ┌───────────────────────────────────────────────┐│
│ │  🏠  │ │  │                                               ││
│ │ Dash │ │  │                                               ││
│ └──────┘ │  │                                               ││
│          │  │                                               ││
│ ┌──────┐ │  │          Content Frame                        ││
│ │  💳  │ │  │          (Changes based on sidebar)           ││
│ │Trans │ │  │                                               ││
│ └──────┘ │  │                                               ││
│          │  │                                               ││
│ ┌──────┐ │  │                                               ││
│ │  🏦  │ │  │                                               ││
│ │Accts │ │  └───────────────────────────────────────────────┘│
│ └──────┘ │                                                     │
│          │  ┌───────────────────────────────────────────────┐│
│ ┌──────┐ │  │ STATUS BAR                                    ││
│ │  📁  │ │  │ Total Balance: $12,450.00 | Last Sync: Now    ││
│ │Categ │ │  └───────────────────────────────────────────────┘│
│ └──────┘ │                                                     │
│          │                                                     │
│ ┌──────┐ │                                                     │
│ │  📊  │ │                                                     │
│ │Repts │ │                                                     │
│ └──────┘ │                                                     │
│          │                                                     │
│ ┌──────┐ │                                                     │
│ │  ⚙️  │ │                                                     │
│ │Setts │ │                                                     │
│ └──────┘ │                                                     │
│          │                                                     │
│ ┌──────┐ │                                                     │
│ │  ➕  │ │                                                     │
│ │ Add  │ │                                                     │
│ └──────┘ │                                                     │
└──────────┴─────────────────────────────────────────────────────┘
```

### Sample UI Code (CustomTkinter)

**Main Window Class:**
```python
import customtkinter as ctk
from typing import Optional

class MainWindow(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Expense Tracker")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Set color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Current frame
        self.current_frame: Optional[ctk.CTkFrame] = None

        # Create UI components
        self.create_sidebar()
        self.create_status_bar()

        # Show dashboard by default
        self.show_dashboard()

    def create_sidebar(self):
        """Create sidebar navigation"""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(8, weight=1)  # Push buttons to top

        # App title
        title = ctk.CTkLabel(
            self.sidebar,
            text="Expense Tracker",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Navigation buttons
        self.btn_dashboard = self.create_nav_button("🏠 Dashboard", 1, self.show_dashboard)
        self.btn_transactions = self.create_nav_button("💳 Transactions", 2, self.show_transactions)
        self.btn_accounts = self.create_nav_button("🏦 Accounts", 3, self.show_accounts)
        self.btn_categories = self.create_nav_button("📁 Categories", 4, self.show_categories)
        self.btn_reports = self.create_nav_button("📊 Reports", 5, self.show_reports)
        self.btn_settings = self.create_nav_button("⚙️ Settings", 6, self.show_settings)

        # Add transaction button (prominent)
        self.btn_add = ctk.CTkButton(
            self.sidebar,
            text="➕ Add Transaction",
            command=self.add_transaction,
            height=40,
            fg_color="#2fa572",  # Green
            hover_color="#27a569"
        )
        self.btn_add.grid(row=7, column=0, padx=20, pady=20, sticky="ew")

    def create_nav_button(self, text: str, row: int, command):
        """Create a navigation button"""
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            height=40,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        btn.grid(row=row, column=0, padx=20, pady=(0, 10), sticky="ew")
        return btn

    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Total Balance: $0.00 | Last Updated: Never",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(side="left", padx=20, pady=5)

    def switch_frame(self, new_frame: ctk.CTkFrame):
        """Switch to a new content frame"""
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def show_dashboard(self):
        """Show dashboard frame"""
        from ui.frames.dashboard_frame import DashboardFrame
        self.switch_frame(DashboardFrame(self))

    def show_transactions(self):
        """Show transactions frame"""
        from ui.frames.transactions_frame import TransactionsFrame
        self.switch_frame(TransactionsFrame(self))

    def show_accounts(self):
        """Show accounts frame"""
        from ui.frames.accounts_frame import AccountsFrame
        self.switch_frame(AccountsFrame(self))

    def show_categories(self):
        """Show categories frame"""
        from ui.frames.categories_frame import CategoriesFrame
        self.switch_frame(CategoriesFrame(self))

    def show_reports(self):
        """Show reports frame"""
        from ui.frames.reports_frame import ReportsFrame
        self.switch_frame(ReportsFrame(self))

    def show_settings(self):
        """Show settings frame"""
        from ui.frames.settings_frame import SettingsFrame
        self.switch_frame(SettingsFrame(self))

    def add_transaction(self):
        """Open add transaction dialog"""
        from ui.dialogs.transaction_dialog import TransactionDialog
        dialog = TransactionDialog(self)
        dialog.wait_window()  # Wait for dialog to close

        # Refresh current frame if needed
        if isinstance(self.current_frame, TransactionsFrame):
            self.current_frame.refresh_data()

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.configure(text=message)
```

---

## Core Features

### Feature 1: Dashboard

**Dashboard Frame Content:**
- Summary cards (Income, Expenses, Savings)
- Recent transactions (last 10)
- Quick stats (top categories)
- Quick add button

**Implementation:**
```python
class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        title = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="w")

        # Summary cards
        self.create_summary_cards()

        # Recent transactions
        self.create_recent_transactions()

        # Load data
        self.load_data()

    def create_summary_cards(self):
        # Income card
        self.income_card = SummaryCard(self, "Income", "$0.00", "#2fa572")
        self.income_card.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Expense card
        self.expense_card = SummaryCard(self, "Expenses", "$0.00", "#e74c3c")
        self.expense_card.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Savings card
        self.savings_card = SummaryCard(self, "Savings", "$0.00", "#3498db")
        self.savings_card.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    def load_data(self):
        # Load data from service
        from services.report_service import ReportService
        report_service = ReportService()

        summary = report_service.get_monthly_summary()

        self.income_card.update_value(f"${summary['income']:.2f}")
        self.expense_card.update_value(f"${summary['expenses']:.2f}")
        self.savings_card.update_value(f"${summary['savings']:.2f}")
```

### Feature 2: Transaction Management

**Transaction Dialog (Add/Edit):**
```python
class TransactionDialog(ctk.CTkToplevel):
    def __init__(self, parent, transaction=None):
        super().__init__(parent)

        self.transaction = transaction
        self.is_edit = transaction is not None

        # Window setup
        self.title("Edit Transaction" if self.is_edit else "Add Transaction")
        self.geometry("500x600")
        self.transient(parent)
        self.grab_set()

        # Services
        from services.transaction_service import TransactionService
        from services.account_service import AccountService
        from services.category_service import CategoryService

        self.transaction_service = TransactionService()
        self.account_service = AccountService()
        self.category_service = CategoryService()

        # Create form
        self.create_form()

        # Load data if editing
        if self.is_edit:
            self.load_transaction_data()

    def create_form(self):
        # Date field
        ctk.CTkLabel(self, text="Date:").grid(row=0, column=0, padx=20, pady=(20,5), sticky="w")
        self.date_entry = DateEntry(self)
        self.date_entry.grid(row=0, column=1, padx=20, pady=(20,5), sticky="ew")

        # Amount field
        ctk.CTkLabel(self, text="Amount:").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="0.00")
        self.amount_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        # Type field (Income/Expense/Transfer)
        ctk.CTkLabel(self, text="Type:").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.type_var = ctk.StringVar(value="expense")
        self.type_menu = ctk.CTkSegmentedButton(
            self,
            values=["Income", "Expense", "Transfer"],
            variable=self.type_var,
            command=self.on_type_change
        )
        self.type_menu.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        # Account dropdown
        ctk.CTkLabel(self, text="Account:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        accounts = self.account_service.get_all_active()
        account_names = [acc.name for acc in accounts]
        self.account_menu = ctk.CTkOptionMenu(self, values=account_names)
        self.account_menu.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        # Category dropdown
        ctk.CTkLabel(self, text="Category:").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.category_menu = ctk.CTkOptionMenu(self, values=["Loading..."])
        self.category_menu.grid(row=4, column=1, padx=20, pady=5, sticky="ew")
        self.load_categories()

        # Description field
        ctk.CTkLabel(self, text="Description:").grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.desc_entry = ctk.CTkEntry(self, placeholder_text="Optional")
        self.desc_entry.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        # Merchant field
        ctk.CTkLabel(self, text="Merchant:").grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.merchant_entry = ctk.CTkEntry(self, placeholder_text="Optional")
        self.merchant_entry.grid(row=6, column=1, padx=20, pady=5, sticky="ew")

        # Notes field
        ctk.CTkLabel(self, text="Notes:").grid(row=7, column=0, padx=20, pady=5, sticky="nw")
        self.notes_text = ctk.CTkTextbox(self, height=100)
        self.notes_text.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.destroy)
        cancel_btn.pack(side="right", padx=(10, 0))

        save_btn = ctk.CTkButton(button_frame, text="Save", command=self.save_transaction)
        save_btn.pack(side="right")

    def save_transaction(self):
        # Validate
        if not self.validate():
            return

        # Collect data
        data = {
            'date': self.date_entry.get_date(),
            'amount': float(self.amount_entry.get()),
            'transaction_type': self.type_var.get().lower(),
            'account_id': self.get_selected_account_id(),
            'category_id': self.get_selected_category_id(),
            'description': self.desc_entry.get(),
            'merchant': self.merchant_entry.get(),
            'notes': self.notes_text.get("1.0", "end-1c")
        }

        try:
            if self.is_edit:
                self.transaction_service.update(self.transaction.id, data)
            else:
                self.transaction_service.create(data)

            # Show success message
            self.show_success()
            self.destroy()

        except Exception as e:
            self.show_error(str(e))
```

---

## Project Structure

```
expense-tracker/
│
├── main.py                      # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md
│
├── database/                    # Database layer
│   ├── __init__.py
│   ├── connection.py            # SQLAlchemy session management
│   ├── init_db.py               # Database initialization
│   └── seed_data.py             # Initial categories/data
│
├── models/                      # SQLAlchemy models
│   ├── __init__.py
│   ├── base.py                  # Base model
│   ├── account.py
│   ├── category.py
│   ├── transaction.py
│   └── tag.py
│
├── repositories/                # Data access layer
│   ├── __init__.py
│   ├── base_repository.py       # Base repository class
│   ├── account_repository.py
│   ├── category_repository.py
│   └── transaction_repository.py
│
├── services/                    # Business logic layer
│   ├── __init__.py
│   ├── transaction_service.py
│   ├── account_service.py
│   ├── category_service.py
│   ├── report_service.py
│   └── export_service.py
│
├── ui/                          # User interface layer
│   ├── __init__.py
│   ├── main_window.py           # Main application window
│   │
│   ├── frames/                  # Content frames
│   │   ├── __init__.py
│   │   ├── base_frame.py        # Base frame class
│   │   ├── dashboard_frame.py
│   │   ├── transactions_frame.py
│   │   ├── accounts_frame.py
│   │   ├── categories_frame.py
│   │   ├── reports_frame.py
│   │   └── settings_frame.py
│   │
│   ├── dialogs/                 # Dialog windows
│   │   ├── __init__.py
│   │   ├── base_dialog.py
│   │   ├── transaction_dialog.py
│   │   ├── account_dialog.py
│   │   └── category_dialog.py
│   │
│   └── components/              # Reusable UI components
│       ├── __init__.py
│       ├── summary_card.py
│       ├── transaction_table.py
│       ├── date_entry.py
│       └── chart_widget.py
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── formatters.py            # Currency, date formatting
│   ├── validators.py            # Input validation
│   └── constants.py             # Constants (colors, sizes, etc.)
│
├── assets/                      # Application assets
│   ├── icons/
│   └── images/
│
├── data/                        # Application data (created at runtime)
│   ├── expense_tracker.db       # SQLite database
│   ├── backups/                 # Database backups
│   └── exports/                 # Exported files
│
└── build/                       # Build output (created by PyInstaller)
    └── expense-tracker.exe
```

---

## Development Setup

### Step 1: Install Python

Download Python 3.11 or newer from [python.org](https://www.python.org/downloads/)

**During installation:**
- ✅ Check "Add Python to PATH"
- ✅ Check "Install pip"

### Step 2: Create Project Directory

```bash
mkdir expense-tracker
cd expense-tracker
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

**Activate virtual environment:**
```bash
# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

### Step 4: Install Dependencies

```bash
pip install customtkinter==5.2.1
pip install Pillow==10.1.0
pip install sqlalchemy==2.0.23
pip install pandas==2.1.4
pip install openpyxl==3.1.2
pip install tkcalendar==1.6.1
pip install pyinstaller==6.3.0
```

Or create `requirements.txt`:
```txt
customtkinter==5.2.1
Pillow==10.1.0
sqlalchemy==2.0.23
pandas==2.1.4
openpyxl==3.1.2
tkcalendar==1.6.1
pyinstaller==6.3.0
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 5: Create Project Structure

```bash
# Create directories
mkdir database models repositories services ui ui/frames ui/dialogs ui/components utils assets assets/icons data

# Create __init__.py files
type nul > database/__init__.py
type nul > models/__init__.py
type nul > repositories/__init__.py
type nul > services/__init__.py
type nul > ui/__init__.py
type nul > ui/frames/__init__.py
type nul > ui/dialogs/__init__.py
type nul > ui/components/__init__.py
type nul > utils/__init__.py
```

### Step 6: Create Main Entry Point

**File: `main.py`**
```python
"""
Expense Tracker - Main Entry Point
Simple, object-oriented Windows desktop application
"""
import customtkinter as ctk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from database.init_db import initialize_database
from config import Config

def main():
    """Main application entry point"""
    try:
        # Initialize database
        print("Initializing database...")
        initialize_database()

        # Create and run application
        print("Starting application...")
        app = MainWindow()
        app.mainloop()

    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Build & Distribution

### Build Single Executable with PyInstaller

**Step 1: Create Build Spec File**

**File: `expense-tracker.spec`**
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'sqlalchemy.sql.default_comparator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExpenseTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app_icon.ico'  # Optional: Add your icon
)
```

**Step 2: Build**

```bash
pyinstaller expense-tracker.spec
```

**Output:** `dist/ExpenseTracker.exe` (~30-50 MB)

### Distribution Options

**Option 1: Portable Executable**
- Just share the `ExpenseTracker.exe` file
- User can run from any location
- Data stored in `%APPDATA%/ExpenseTracker/`

**Option 2: Installer (Inno Setup)**

Download Inno Setup: [jrsoftware.org](https://jrsoftware.org/isdl.php)

**File: `installer_script.iss`**
```iss
[Setup]
AppName=Expense Tracker
AppVersion=1.0
DefaultDirName={autopf}\ExpenseTracker
DefaultGroupName=Expense Tracker
OutputDir=installer_output
OutputBaseFilename=ExpenseTracker_Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\ExpenseTracker.exe

[Files]
Source: "dist\ExpenseTracker.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Expense Tracker"; Filename: "{app}\ExpenseTracker.exe"
Name: "{autodesktop}\Expense Tracker"; Filename: "{app}\ExpenseTracker.exe"

[Run]
Filename: "{app}\ExpenseTracker.exe"; Description: "Launch Expense Tracker"; Flags: postinstall nowait skipifsilent
```

Compile installer:
```bash
iscc installer_script.iss
```

**Output:** `installer_output/ExpenseTracker_Setup.exe`

---

## Implementation Guide

### Week 1: Setup & Database

**Day 1-2: Project Setup**
1. Install Python and dependencies
2. Create project structure
3. Set up version control (Git)

**Day 3-5: Database Layer**
1. Create SQLAlchemy models
2. Implement database initialization
3. Create seed data for categories
4. Test database operations

### Week 2: Repositories & Services

**Day 1-3: Repository Layer**
1. Create `BaseRepository` class
2. Implement `AccountRepository`
3. Implement `CategoryRepository`
4. Implement `TransactionRepository`

**Day 4-5: Service Layer**
1. Create `AccountService`
2. Create `CategoryService`
3. Create `TransactionService`

### Week 3-4: User Interface

**Day 1-2: Main Window**
1. Create main window with sidebar
2. Implement navigation
3. Create status bar

**Day 3-5: Dashboard**
1. Create dashboard frame
2. Implement summary cards
3. Show recent transactions

**Day 6-10: Transaction Management**
1. Create transaction table
2. Implement add transaction dialog
3. Implement edit transaction
4. Implement delete transaction
5. Add filters and search

### Week 5: Accounts & Categories

**Day 1-3: Accounts**
1. Create accounts frame
2. Implement account management
3. Show account transactions

**Day 4-5: Categories**
1. Create categories frame
2. Implement category tree view
3. Category management (add/edit/delete)

### Week 6: Reports & Export

**Day 1-3: Reports**
1. Create reports frame
2. Implement monthly report
3. Implement category report

**Day 4-5: Export**
1. Implement Excel export
2. Implement CSV export
3. Test export functionality

### Week 7-8: Polish & Package

**Day 1-3: UI Polish**
1. Improve visual design
2. Add loading indicators
3. Error handling and messages

**Day 4-5: Testing**
1. Manual testing
2. Fix bugs
3. Performance optimization

**Day 6-7: Build & Package**
1. Test PyInstaller build
2. Create installer
3. Write user documentation

---

## Key Implementation Tips

### 1. Keep It Simple
```python
# ✅ GOOD: Simple and clear
def get_total_expenses(month: int, year: int) -> float:
    transactions = repository.get_by_month(month, year)
    return sum(t.amount for t in transactions if t.transaction_type == 'expense')

# ❌ BAD: Over-engineered
class ExpenseAggregator:
    def __init__(self, strategy: AggregationStrategy):
        self.strategy = strategy

    def aggregate(self, transactions, filters):
        # Too complex for a simple app
        pass
```

### 2. Use Object-Oriented Principles
```python
# ✅ GOOD: Clear class responsibilities
class TransactionService:
    """Handles all transaction business logic"""

    def __init__(self):
        self.repository = TransactionRepository()

    def create(self, data: dict) -> Transaction:
        # Validate
        self._validate_transaction(data)

        # Create
        transaction = self.repository.create(data)

        # Update account balance (handled by trigger)

        return transaction
```

### 3. Handle Errors Gracefully
```python
try:
    transaction = service.create(data)
    messagebox.showinfo("Success", "Transaction added successfully!")
except ValueError as e:
    messagebox.showerror("Validation Error", str(e))
except Exception as e:
    messagebox.showerror("Error", f"Failed to add transaction: {e}")
    logging.error(f"Error adding transaction: {e}", exc_info=True)
```

### 4. Use Type Hints
```python
from typing import List, Optional
from datetime import date

def get_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    account_id: Optional[int] = None
) -> List[Transaction]:
    """
    Get transactions with optional filters

    Args:
        start_date: Filter transactions from this date
        end_date: Filter transactions until this date
        account_id: Filter by account

    Returns:
        List of Transaction objects
    """
    return repository.get_filtered(start_date, end_date, account_id)
```

### 5. Separate Concerns
```python
# UI Layer - Only UI code
class TransactionDialog(ctk.CTkToplevel):
    def save(self):
        data = self.collect_form_data()
        self.service.create(data)  # Delegate to service

# Service Layer - Business logic
class TransactionService:
    def create(self, data: dict):
        # Validation, calculations, rules
        pass

# Repository Layer - Database only
class TransactionRepository:
    def create(self, data: dict):
        # SQLAlchemy operations only
        pass
```

---

## Configuration File

**File: `config.py`**
```python
import os
from pathlib import Path

class Config:
    """Application configuration"""

    # Application Info
    APP_NAME = "Expense Tracker"
    VERSION = "1.0.0"

    # Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = Path(os.getenv('APPDATA')) / APP_NAME  # %APPDATA%/Expense Tracker/
    DB_PATH = DATA_DIR / "expense_tracker.db"
    BACKUP_DIR = DATA_DIR / "backups"
    EXPORT_DIR = DATA_DIR / "exports"

    # Database
    DATABASE_URL = f"sqlite:///{DB_PATH}"

    # UI Settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    MIN_WIDTH = 1000
    MIN_HEIGHT = 600

    # Theme
    THEME = "dark"  # or "light"
    COLOR_THEME = "blue"

    # Colors
    PRIMARY_COLOR = "#1f538d"
    ACCENT_COLOR = "#2fa572"
    DANGER_COLOR = "#e74c3c"

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_DIR.mkdir(exist_ok=True)
        cls.EXPORT_DIR.mkdir(exist_ok=True)

# Initialize directories on import
Config.ensure_directories()
```

---

## Summary

### What You Get

✅ **Simple Windows Desktop App**
- Native UI with CustomTkinter
- Single executable (~30-50 MB)
- Fast startup (<2 seconds)

✅ **Object-Oriented Design**
- Clear layered architecture
- Separation of concerns
- Easy to test and maintain

✅ **Lightweight**
- Only 6 core dependencies
- No web browser/server
- SQLite single-file database

✅ **Easy to Maintain**
- Clear project structure
- Well-organized code
- Type hints throughout
- No over-engineering

### Next Steps

1. **Review Functional Specifications** - Understand what to build
2. **Follow Implementation Guide** - 8-week development plan
3. **Start with Week 1** - Database and models
4. **Iterate and refine** - Build feature by feature

### Need Help?

I can provide:
1. Complete code for any class/module
2. Detailed implementation of specific features
3. Help with CustomTkinter UI examples
4. Database query examples
5. PyInstaller configuration help

**Ready to start coding?** Let me know which part you'd like me to implement first!
