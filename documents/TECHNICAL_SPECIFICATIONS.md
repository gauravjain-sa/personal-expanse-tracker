# Expense Tracker Application - Technical Specifications

**Document Version:** 1.0
**Date:** January 4, 2026
**Document Type:** Technical Architecture & Implementation Specifications
**Status:** Design Phase - Ready for Development

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Technology Stack Decision Matrix](#technology-stack-decision-matrix)
3. [Architecture Options](#architecture-options)
4. [Recommended Architecture](#recommended-architecture)
5. [Database Design](#database-design)
6. [API Specifications](#api-specifications)
7. [Frontend Architecture](#frontend-architecture)
8. [Backend Architecture](#backend-architecture)
9. [Security Specifications](#security-specifications)
10. [Performance Requirements](#performance-requirements)
11. [Deployment & Packaging](#deployment--packaging)
12. [Desktop to Web Migration Path](#desktop-to-web-migration-path)
13. [Development Environment Setup](#development-environment-setup)
14. [Testing Strategy](#testing-strategy)
15. [Implementation Roadmap](#implementation-roadmap)
16. [Risk Analysis & Mitigation](#risk-analysis--mitigation)

---

## Executive Summary

### Technical Vision
Build a modern, lightweight expense tracking application using a browser-based local architecture that can seamlessly transition to a web application when needed. The system will prioritize developer productivity, maintainability, and future scalability over absolute minimum file size.

### Technology Decision Summary
After comprehensive analysis of Go, Python, Node.js, Rust, and other options, the **recommended technology stack is:**

**Desktop Application (Version 1.0):**
- **Frontend:** React 18 + TypeScript + Tailwind CSS + Vite
- **Backend:** Python 3.11+ + FastAPI + Pydantic
- **Database:** SQLite 3
- **Packaging:** PyInstaller (single executable)
- **Distribution:** Single-click installer or portable executable

**Web Application (Version 2.0):**
- **Frontend:** Same React application
- **Backend:** Same FastAPI application (deployed on Linux)
- **Database:** PostgreSQL 15+
- **Deployment:** Docker containers on VPS or PaaS
- **Web Server:** Nginx as reverse proxy

### Key Technical Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Architecture Pattern** | Browser-based local app | Modern UI, easy web migration |
| **Backend Language** | Python + FastAPI | Rapid development, excellent libraries |
| **Frontend Framework** | React + TypeScript | Mature ecosystem, type safety |
| **Database (Desktop)** | SQLite | Zero-config, single file, ACID compliant |
| **Database (Web)** | PostgreSQL | Robust, scalable, open-source |
| **API Style** | REST | Simple, well-understood, HTTP-based |
| **Packaging Strategy** | PyInstaller | Python ecosystem standard |

### Why Not Other Options?

**Why not Go + Wails?**
- Smaller executable (10-20MB vs 50-100MB)
- Faster startup (<1s vs 2-4s)
- ✗ Longer development time
- ✗ Smaller ecosystem for reporting
- **Verdict:** Choose if file size is critical

**Why not Rust + Tauri?**
- Smallest possible (5-15MB)
- Maximum security and performance
- ✗ Steepest learning curve
- ✗ Slower development
- **Verdict:** Choose for long-term project with time to learn

**Why not Node.js + Tauri?**
- JavaScript everywhere
- Large ecosystem
- ✗ Native module packaging complexity
- ✗ More boilerplate than Python
- **Verdict:** Good alternative if team already knows Node

---

## Technology Stack Decision Matrix

### Complete Backend Comparison

| Criteria | Python + FastAPI | Go + Wails | Node.js + Tauri | Rust + Tauri |
|----------|------------------|------------|-----------------|--------------|
| **PACKAGING** |
| File Size | 50-100 MB | 10-20 MB | 20-40 MB | 5-15 MB |
| Startup Speed | 2-4 sec | <1 sec | 1-2 sec | <1 sec |
| Memory Usage | 80-150 MB | 20-50 MB | 50-100 MB | 15-40 MB |
| True Single Binary | ⚠️ Bundles runtime | ✅ Yes | ✅ Yes | ✅ Yes |
| **DEVELOPMENT** |
| Development Speed | ⭐⭐⭐⭐⭐ Fastest | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Fast | ⭐⭐ Slower |
| Learning Curve | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Easy | ⭐⭐ Steep |
| Code Readability | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Good |
| Debugging | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| Hot Reload | ✅ Built-in | ✅ Available | ✅ Built-in | ⚠️ Cargo watch |
| **ECOSYSTEM** |
| Community Size | ⭐⭐⭐⭐⭐ Huge | ⭐⭐⭐⭐ Growing | ⭐⭐⭐⭐⭐ Huge | ⭐⭐⭐ Growing |
| Stack Overflow | 2M+ questions | 100K+ questions | 2.5M+ questions | 150K+ questions |
| Package Ecosystem | ⭐⭐⭐⭐⭐ PyPI (450K+) | ⭐⭐⭐⭐ Go modules | ⭐⭐⭐⭐⭐ npm (2M+) | ⭐⭐⭐ Crates (120K+) |
| **FEATURES** |
| SQLite Support | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent |
| Excel Export | ⭐⭐⭐⭐⭐ openpyxl | ⭐⭐⭐⭐ excelize | ⭐⭐⭐⭐ exceljs | ⭐⭐⭐ rust_xlsxwriter |
| PDF Generation | ⭐⭐⭐⭐⭐ ReportLab | ⭐⭐⭐⭐ gofpdf | ⭐⭐⭐⭐ pdfkit | ⭐⭐⭐ printpdf |
| Data Processing | ⭐⭐⭐⭐⭐ pandas | ⭐⭐⭐ Manual | ⭐⭐⭐ lodash | ⭐⭐⭐ polars |
| Chart Libraries | ⭐⭐⭐⭐⭐ matplotlib | ⭐⭐⭐ Limited | ⭐⭐⭐⭐ Chart.js | ⭐⭐⭐ plotters |
| **SCALABILITY** |
| Web Migration | ✅ Seamless | ✅ Seamless | ✅ Seamless | ✅ Seamless |
| REST API | ⭐⭐⭐⭐⭐ FastAPI | ⭐⭐⭐⭐ Gin/Chi | ⭐⭐⭐⭐⭐ Express/Fastify | ⭐⭐⭐⭐ Axum/Actix |
| ORM Support | ⭐⭐⭐⭐⭐ SQLAlchemy | ⭐⭐⭐⭐ GORM | ⭐⭐⭐⭐⭐ Prisma/TypeORM | ⭐⭐⭐⭐ Diesel/SeaORM |
| Containerization | ⭐⭐⭐⭐⭐ Docker native | ⭐⭐⭐⭐⭐ Small images | ⭐⭐⭐⭐⭐ Standard | ⭐⭐⭐⭐⭐ Tiny images |
| **PERFORMANCE** |
| Runtime Speed | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐⭐ Excellent |
| Concurrency | ⭐⭐⭐⭐ Async/await | ⭐⭐⭐⭐⭐ Goroutines | ⭐⭐⭐⭐ Event loop | ⭐⭐⭐⭐⭐ Async/threads |
| Memory Safety | ⭐⭐⭐ Runtime checks | ⭐⭐⭐⭐ GC + type safe | ⭐⭐⭐ GC | ⭐⭐⭐⭐⭐ Compile-time |
| **SCORING** |
| Overall Score | **95/100** | **88/100** | **90/100** | **85/100** |

### Frontend Framework Comparison

| Criteria | React | Vue.js | Svelte | Solid.js |
|----------|-------|--------|--------|----------|
| Learning Curve | Moderate | Easy | Easy | Moderate |
| Ecosystem | ⭐⭐⭐⭐⭐ Huge | ⭐⭐⭐⭐ Large | ⭐⭐⭐ Growing | ⭐⭐ Small |
| Performance | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent |
| Bundle Size | Medium | Medium | Small | Small |
| TypeScript | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| Job Market | ⭐⭐⭐⭐⭐ Highest | ⭐⭐⭐⭐ High | ⭐⭐⭐ Medium | ⭐⭐ Low |
| Component Libraries | ⭐⭐⭐⭐⭐ Many | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Limited | ⭐⭐ Very Limited |
| **Recommendation** | **✅ Best** | ✅ Good | ✅ Performance | ⚠️ Cutting edge |

**Chosen:** React + TypeScript
- Most mature ecosystem
- Excellent TypeScript support
- Largest talent pool
- Most component libraries
- Best for long-term maintenance

---

## Architecture Options

### Option 1: Browser-Based Local App (RECOMMENDED)

**Overview:** Desktop application that runs a local backend server and automatically opens the UI in the default browser.

```
┌────────────────────────────────────────────────┐
│         DESKTOP APPLICATION                    │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │   User's Default Web Browser             │ │
│  │   ┌────────────────────────────────────┐ │ │
│  │   │  React Frontend (SPA)              │ │ │
│  │   │  - UI Components                   │ │ │
│  │   │  - State Management (React Query)  │ │ │
│  │   │  - API Client (Axios/Fetch)        │ │ │
│  │   └────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────┘ │
│                     ↕ HTTP (localhost:8000)    │
│  ┌──────────────────────────────────────────┐ │
│  │   FastAPI Backend (uvicorn)              │ │
│  │   - REST API Endpoints                   │ │
│  │   - Business Logic                       │ │
│  │   - Data Validation (Pydantic)           │ │
│  └──────────────────────────────────────────┘ │
│                     ↕ SQL                      │
│  ┌──────────────────────────────────────────┐ │
│  │   SQLite Database                        │ │
│  │   - expense_tracker.db                   │ │
│  │   - Stored in app data folder            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Packaged as: expense-tracker.exe              │
│  Startup: Launches backend → Opens browser    │
└────────────────────────────────────────────────┘
```

**Advantages:**
- ✅ Modern web UI (React, CSS frameworks work natively)
- ✅ Rapid development (separate frontend/backend)
- ✅ Hot reload during development
- ✅ Easy testing (API can be tested independently)
- ✅ Seamless web migration (same codebase)
- ✅ Large ecosystem (npm + PyPI)

**Disadvantages:**
- ⚠️ Requires browser (but always available on modern OS)
- ⚠️ Larger executable size (50-100 MB)
- ⚠️ Slower startup (2-4 seconds)

**Best For:**
- Rapid development timeline
- Plan to scale to web
- Need rich reporting features
- Modern UI requirements

---

### Option 2: Native Desktop Shell (Alternative)

**Overview:** Desktop application with embedded WebView using Wails (Go) or Tauri (Rust).

```
┌────────────────────────────────────────────────┐
│         NATIVE DESKTOP APPLICATION             │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │   Embedded WebView (System)              │ │
│  │   ┌────────────────────────────────────┐ │ │
│  │   │  React Frontend (Embedded)         │ │ │
│  │   └────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────┘ │
│                     ↕ IPC/Function Calls       │
│  ┌──────────────────────────────────────────┐ │
│  │   Go/Rust Backend                        │ │
│  │   - Wails Commands / Tauri Commands      │ │
│  │   - Business Logic                       │ │
│  └──────────────────────────────────────────┘ │
│                     ↕ SQL                      │
│  ┌──────────────────────────────────────────┐ │
│  │   SQLite Database                        │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Packaged as: expense-tracker.exe (10-20 MB)  │
│  Startup: <1 second, native window            │
└────────────────────────────────────────────────┘
```

**Advantages:**
- ✅ Smallest executable (10-20 MB with Go, 5-15 MB with Rust)
- ✅ Fastest startup (<1 second)
- ✅ Native window (not browser tab)
- ✅ Professional feel

**Disadvantages:**
- ⚠️ Learning curve (Go or Rust)
- ⚠️ Longer development time
- ⚠️ Smaller reporting library ecosystem

**Best For:**
- File size is critical
- Performance priority
- Time to learn Go/Rust
- Professional distribution

---

### Option 3: Electron (NOT RECOMMENDED)

**Why Not Electron?**
- ❌ Very large (150-200 MB)
- ❌ High memory usage (200-300 MB)
- ❌ Bundles entire Chromium
- ✅ Only advantage: Cross-platform consistency

**Verdict:** Overkill for a finance app. Use Tauri if need native shell.

---

## Recommended Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXPENSE TRACKER DESKTOP                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────── PRESENTATION LAYER ─────────────┐  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │            React Frontend (Browser)                   ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Pages/        Components/      Hooks/     Utils/    ││  │
│  │  │  - Dashboard   - TransactionForm  - useTransactions  ││  │
│  │  │  - Transactions- AccountCard      - useAccounts      ││  │
│  │  │  - Accounts    - CategoryTree     - useCategories    ││  │
│  │  │  - Categories  - ReportChart      - useReports       ││  │
│  │  │  - Reports     - FilterPanel                         ││  │
│  │  │  - Settings    - Modal                               ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  State Management: React Query (TanStack Query)      ││  │
│  │  │  - Server state caching                              ││  │
│  │  │  - Automatic refetching                              ││  │
│  │  │  - Optimistic updates                                ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  API Client: Axios                                   ││  │
│  │  │  - Base URL: http://localhost:8000                   ││  │
│  │  │  - Request/response interceptors                     ││  │
│  │  │  - Error handling                                    ││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                 │
│                        ↕ HTTP REST API                          │
│                                                                 │
│  ┌────────────────────── APPLICATION LAYER ──────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │          FastAPI Backend (Uvicorn)                    ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Routes/               Services/                      ││  │
│  │  │  - transaction_routes  - transaction_service         ││  │
│  │  │  - account_routes      - account_service             ││  │
│  │  │  - category_routes     - category_service            ││  │
│  │  │  - report_routes       - report_service              ││  │
│  │  │  - export_routes       - export_service              ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Models (Pydantic):                                  ││  │
│  │  │  - Request/Response schemas                          ││  │
│  │  │  - Data validation                                   ││  │
│  │  │  - Type safety                                       ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Middleware:                                         ││  │
│  │  │  - CORS (allow localhost origins)                   ││  │
│  │  │  - Error handling                                    ││  │
│  │  │  - Request logging                                   ││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                 │
│                           ↕ SQL (SQLAlchemy ORM)                │
│                                                                 │
│  ┌─────────────────────── DATA LAYER ───────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐│  │
│  │  │              SQLite Database                          ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Tables:                                             ││  │
│  │  │  - accounts                                          ││  │
│  │  │  - categories                                        ││  │
│  │  │  - transactions                                      ││  │
│  │  │  - tags                                              ││  │
│  │  │  - transaction_tags                                  ││  │
│  │  │  - recurring_transactions (future)                   ││  │
│  │  │  - budgets (future)                                  ││  │
│  │  ├──────────────────────────────────────────────────────┤│  │
│  │  │  Location: %APPDATA%/ExpenseTracker/data.db         ││  │
│  │  │  Backup: %APPDATA%/ExpenseTracker/backups/          ││  │
│  │  └──────────────────────────────────────────────────────┘│  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack Details

#### Frontend Stack

**Core Framework:**
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.3.0"
}
```

**Build Tool:**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.0"
}
```

**Routing:**
```json
{
  "react-router-dom": "^6.21.0"
}
```

**State Management:**
```json
{
  "@tanstack/react-query": "^5.17.0",
  "zustand": "^4.4.7" // For local UI state (optional)
}
```

**API Client:**
```json
{
  "axios": "^1.6.0"
}
```

**UI & Styling:**
```json
{
  "tailwindcss": "^3.4.0",
  "@headlessui/react": "^1.7.17",
  "@heroicons/react": "^2.1.1",
  "clsx": "^2.1.0"
}
```

**Forms:**
```json
{
  "react-hook-form": "^7.49.0",
  "zod": "^3.22.0"
}
```

**Charts:**
```json
{
  "recharts": "^2.10.0" // or "chart.js": "^4.4.1"
}
```

**Date Handling:**
```json
{
  "date-fns": "^3.0.0"
}
```

**Utilities:**
```json
{
  "lodash": "^4.17.21"
}
```

#### Backend Stack

**Core Framework:**
```python
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

**Database:**
```python
sqlalchemy==2.0.25
alembic==1.13.0  # Database migrations
aiosqlite==0.19.0  # Async SQLite driver
```

**Data Processing:**
```python
pandas==2.1.4  # Data analysis for reports
openpyxl==3.1.2  # Excel export
python-dateutil==2.8.2
```

**Utilities:**
```python
python-multipart==0.0.6  # File uploads (receipts)
python-jose[cryptography]==3.3.0  # JWT for web version
passlib[bcrypt]==1.7.4  # Password hashing for web version
```

**Development:**
```python
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2  # For testing async endpoints
black==23.12.0  # Code formatting
flake8==7.0.0  # Linting
mypy==1.7.1  # Type checking
```

**Packaging:**
```python
pyinstaller==6.3.0
```

---

## Database Design

### Entity Relationship Diagram (ERD)

```
                    ┌─────────────────────┐
                    │     CATEGORIES      │
                    ├─────────────────────┤
                    │ id (PK)             │
                    │ name                │
                    │ parent_id (FK) ─────┼───┐
                    │ type                │   │
                    │ color               │   │
                    │ icon                │   │
                    │ is_active           │   │
                    │ created_at          │   │
                    └─────────────────────┘   │
                           ▲                  │
                           │                  │
                           └──────────────────┘

         ┌──────────────────┴────────────────────┐
         │                                       │
         │                                       │
┌────────┴──────────┐                   ┌───────┴──────────┐
│    ACCOUNTS       │                   │   TRANSACTIONS   │
├───────────────────┤                   ├──────────────────┤
│ id (PK)           │◄──────────────────┤ id (PK)          │
│ name              │                   │ date             │
│ account_type      │                   │ amount           │
│ initial_balance   │         ┌─────────┤ transaction_type │
│ current_balance   │         │         │ direction        │
│ currency          │         │         │ account_id (FK)  │
│ is_active         │         │         │ category_id (FK) │
│ notes             │         │         │ description      │
│ created_at        │         │         │ notes            │
│ updated_at        │         │         │ merchant         │
└───────────────────┘         │         │ receipt_path     │
         ▲                    │         │ is_transfer      │
         │                    │         │ transfer_to_account_id (FK)
         │                    │         │ created_at       │
         └────────────────────┘         │ updated_at       │
           transfer_to_account          └──────────────────┘
                                                  │
                                                  │ (M:N)
                                                  │
                                         ┌────────┴──────────┐
                                         │  TRANSACTION_TAGS │
                                         ├───────────────────┤
                                         │ transaction_id(FK)│
                                         │ tag_id (FK)       │
                                         └───────────────────┘
                                                  │
                                                  │
                                         ┌────────┴──────────┐
                                         │      TAGS         │
                                         ├───────────────────┤
                                         │ id (PK)           │
                                         │ name              │
                                         │ color             │
                                         │ created_at        │
                                         └───────────────────┘
```

### Complete Database Schema (SQLAlchemy Models)

**File: `backend/app/models/account.py`**
```python
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    account_type = Column(String(50), nullable=False)  # bank, credit_card, cash, wallet, investment
    initial_balance = Column(Numeric(15, 2), nullable=False, default=0.00)
    current_balance = Column(Numeric(15, 2), nullable=False, default=0.00)
    currency = Column(String(3), nullable=False, default="USD")
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    transactions = relationship("Transaction", back_populates="account", foreign_keys="Transaction.account_id")
    transfers_to = relationship("Transaction", back_populates="transfer_to_account", foreign_keys="Transaction.transfer_to_account_id")
```

**File: `backend/app/models/category.py`**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    type = Column(String(20), nullable=False)  # income or expense
    color = Column(String(7))  # HEX color
    icon = Column(String(50))
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    transactions = relationship("Transaction", back_populates="category")
```

**File: `backend/app/models/transaction.py`**
```python
from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False, index=True)  # income, expense, transfer
    direction = Column(String(10), nullable=False)  # debit, credit
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    description = Column(String(255))
    notes = Column(Text)
    merchant = Column(String(100), index=True)
    receipt_path = Column(String(500))
    is_transfer = Column(Boolean, default=False, nullable=False)
    transfer_to_account_id = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    transfer_to_account = relationship("Account", back_populates="transfers_to", foreign_keys=[transfer_to_account_id])
    category = relationship("Category", back_populates="transactions")
    tags = relationship("Tag", secondary="transaction_tags", back_populates="transactions")
```

**File: `backend/app/models/tag.py`**
```python
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Association table for many-to-many relationship
transaction_tags = Table(
    'transaction_tags',
    Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id', ondelete="CASCADE"), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    transactions = relationship("Transaction", secondary=transaction_tags, back_populates="tags")
```

### Database Indexes

```sql
-- Performance indexes
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_transactions_merchant ON transactions(merchant);
CREATE INDEX idx_categories_type ON categories(type);
CREATE INDEX idx_categories_parent ON categories(parent_id);

-- Full-text search index (future)
CREATE VIRTUAL TABLE transactions_fts USING fts5(description, notes, merchant, content=transactions);
```

### Database Triggers (SQLite)

**File: `backend/app/database/triggers.sql`**
```sql
-- Trigger to update account balance on INSERT
CREATE TRIGGER update_account_balance_on_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    UPDATE accounts
    SET current_balance = current_balance +
        CASE
            WHEN NEW.direction = 'credit' THEN NEW.amount
            WHEN NEW.direction = 'debit' THEN -NEW.amount
        END,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.account_id;

    -- Update destination account for transfers
    UPDATE accounts
    SET current_balance = current_balance + NEW.amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.transfer_to_account_id AND NEW.is_transfer = 1;
END;

-- Trigger to update account balance on UPDATE
CREATE TRIGGER update_account_balance_on_update
AFTER UPDATE OF amount, direction, account_id ON transactions
FOR EACH ROW
BEGIN
    -- Reverse old transaction
    UPDATE accounts
    SET current_balance = current_balance -
        CASE
            WHEN OLD.direction = 'credit' THEN OLD.amount
            WHEN OLD.direction = 'debit' THEN -OLD.amount
        END
    WHERE id = OLD.account_id;

    -- Apply new transaction
    UPDATE accounts
    SET current_balance = current_balance +
        CASE
            WHEN NEW.direction = 'credit' THEN NEW.amount
            WHEN NEW.direction = 'debit' THEN -NEW.amount
        END,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.account_id;

    -- Handle transfer account changes
    UPDATE accounts
    SET current_balance = current_balance - OLD.amount
    WHERE id = OLD.transfer_to_account_id AND OLD.is_transfer = 1;

    UPDATE accounts
    SET current_balance = current_balance + NEW.amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.transfer_to_account_id AND NEW.is_transfer = 1;
END;

-- Trigger to update account balance on DELETE
CREATE TRIGGER update_account_balance_on_delete
AFTER DELETE ON transactions
FOR EACH ROW
BEGIN
    UPDATE accounts
    SET current_balance = current_balance -
        CASE
            WHEN OLD.direction = 'credit' THEN OLD.amount
            WHEN OLD.direction = 'debit' THEN -OLD.amount
        END,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.account_id;

    -- Update destination account for transfers
    UPDATE accounts
    SET current_balance = current_balance - OLD.amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.transfer_to_account_id AND OLD.is_transfer = 1;
END;

-- Trigger to update updated_at timestamp
CREATE TRIGGER update_transaction_timestamp
AFTER UPDATE ON transactions
FOR EACH ROW
BEGIN
    UPDATE transactions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

---

## API Specifications

### API Design Principles

1. **RESTful Design** - Resources as nouns, HTTP verbs for actions
2. **Consistent Naming** - snake_case for JSON keys, kebab-case for URLs
3. **Error Handling** - Standard HTTP status codes + detailed error messages
4. **Versioning** - `/api/v1/` prefix for future compatibility
5. **Pagination** - Query params: `page`, `limit`, `offset`
6. **Filtering** - Query params for filtering collections
7. **Sorting** - Query param: `sort_by`, `order` (asc/desc)

### Base URL

**Desktop:** `http://localhost:8000/api/v1`
**Web (Future):** `https://api.expensetracker.com/api/v1`

### Authentication (Web Version Only)

**Desktop:** No authentication (local only)
**Web:** JWT Bearer token

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Endpoints

#### 1. Transactions

**1.1 List Transactions**
```http
GET /api/v1/transactions

Query Parameters:
- page: int = 1
- limit: int = 50
- account_id: Optional[int] = None
- category_id: Optional[int] = None
- transaction_type: Optional[str] = None  # income, expense, transfer
- start_date: Optional[date] = None
- end_date: Optional[date] = None
- min_amount: Optional[float] = None
- max_amount: Optional[float] = None
- search: Optional[str] = None  # Search in description, merchant, notes
- sort_by: str = "date"  # date, amount, category, merchant
- order: str = "desc"  # asc, desc

Response: 200 OK
{
  "transactions": [
    {
      "id": 1,
      "date": "2026-01-03",
      "amount": 52.30,
      "transaction_type": "expense",
      "direction": "debit",
      "account_id": 1,
      "account_name": "Main Checking",
      "category_id": 3,
      "category_name": "Groceries",
      "description": "Weekly shopping",
      "merchant": "SuperMart",
      "notes": "Bought milk and bread",
      "is_transfer": false,
      "created_at": "2026-01-03T10:30:00Z",
      "updated_at": "2026-01-03T10:30:00Z"
    },
    ...
  ],
  "total": 247,
  "page": 1,
  "pages": 5,
  "limit": 50
}
```

**1.2 Get Single Transaction**
```http
GET /api/v1/transactions/{transaction_id}

Response: 200 OK
{
  "id": 1,
  "date": "2026-01-03",
  "amount": 52.30,
  "transaction_type": "expense",
  "direction": "debit",
  "account_id": 1,
  "category_id": 3,
  "description": "Weekly shopping",
  "merchant": "SuperMart",
  "notes": "Bought milk and bread",
  "receipt_path": null,
  "is_transfer": false,
  "transfer_to_account_id": null,
  "tags": ["personal", "weekly"],
  "created_at": "2026-01-03T10:30:00Z",
  "updated_at": "2026-01-03T10:30:00Z"
}

Error: 404 Not Found
{
  "detail": "Transaction not found"
}
```

**1.3 Create Transaction**
```http
POST /api/v1/transactions
Content-Type: application/json

Request Body:
{
  "date": "2026-01-03",
  "amount": 52.30,
  "transaction_type": "expense",  // income, expense, transfer
  "account_id": 1,
  "category_id": 3,  // Optional for transfers
  "description": "Weekly shopping",
  "merchant": "SuperMart",  // Optional
  "notes": "Bought milk and bread",  // Optional
  "transfer_to_account_id": null,  // Required for transfers
  "tags": ["personal", "weekly"]  // Optional
}

Response: 201 Created
{
  "id": 245,
  "date": "2026-01-03",
  "amount": 52.30,
  ...
}

Validation Errors: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**1.4 Update Transaction**
```http
PUT /api/v1/transactions/{transaction_id}
Content-Type: application/json

Request Body: (same as create, all fields optional)
{
  "amount": 55.00,
  "description": "Weekly shopping - updated"
}

Response: 200 OK
{
  "id": 245,
  "date": "2026-01-03",
  "amount": 55.00,
  "description": "Weekly shopping - updated",
  ...
}
```

**1.5 Delete Transaction**
```http
DELETE /api/v1/transactions/{transaction_id}

Response: 204 No Content

Error: 404 Not Found
{
  "detail": "Transaction not found"
}
```

#### 2. Accounts

**2.1 List Accounts**
```http
GET /api/v1/accounts

Query Parameters:
- include_inactive: bool = false

Response: 200 OK
{
  "accounts": [
    {
      "id": 1,
      "name": "Main Checking",
      "account_type": "bank",
      "initial_balance": 2000.00,
      "current_balance": 3200.00,
      "currency": "USD",
      "is_active": true,
      "transaction_count": 156,
      "last_transaction_date": "2026-01-03",
      "created_at": "2025-06-01T00:00:00Z"
    },
    ...
  ],
  "total_balance": 12450.75
}
```

**2.2 Get Account with Transactions**
```http
GET /api/v1/accounts/{account_id}

Query Parameters:
- include_transactions: bool = false
- limit: int = 10  // If include_transactions=true

Response: 200 OK
{
  "id": 1,
  "name": "Main Checking",
  "account_type": "bank",
  "initial_balance": 2000.00,
  "current_balance": 3200.00,
  "currency": "USD",
  "is_active": true,
  "notes": "Primary checking account",
  "created_at": "2025-06-01T00:00:00Z",
  "updated_at": "2026-01-03T15:30:00Z",
  "recent_transactions": [...]  // If include_transactions=true
}
```

**2.3 Create Account**
```http
POST /api/v1/accounts
Content-Type: application/json

Request Body:
{
  "name": "Savings Account",
  "account_type": "bank",
  "initial_balance": 5000.00,
  "currency": "USD",
  "notes": "Emergency fund"
}

Response: 201 Created
{
  "id": 5,
  "name": "Savings Account",
  "account_type": "bank",
  "initial_balance": 5000.00,
  "current_balance": 5000.00,
  ...
}
```

**2.4 Update Account**
```http
PUT /api/v1/accounts/{account_id}

Request Body: (partial updates allowed)
{
  "name": "Main Savings",
  "notes": "Updated description"
}

Response: 200 OK

Note: initial_balance cannot be updated if transactions exist
```

**2.5 Deactivate Account**
```http
PATCH /api/v1/accounts/{account_id}/deactivate

Response: 200 OK
{
  "id": 3,
  "is_active": false,
  ...
}
```

**2.6 Delete Account**
```http
DELETE /api/v1/accounts/{account_id}

Response: 204 No Content

Error: 400 Bad Request
{
  "detail": "Cannot delete account with existing transactions. Deactivate instead."
}
```

#### 3. Categories

**3.1 List Categories**
```http
GET /api/v1/categories

Query Parameters:
- type: Optional[str] = None  # income, expense
- include_inactive: bool = false
- include_tree: bool = true  # Return hierarchical structure

Response: 200 OK (Tree Structure)
{
  "categories": [
    {
      "id": 1,
      "name": "Housing",
      "parent_id": null,
      "type": "expense",
      "color": "#FF6B6B",
      "icon": "home",
      "is_active": true,
      "transaction_count": 24,
      "total_amount": 14400.00,  // Current year
      "children": [
        {
          "id": 10,
          "name": "Rent",
          "parent_id": 1,
          "type": "expense",
          "transaction_count": 12,
          "total_amount": 12000.00,
          "children": []
        },
        ...
      ]
    },
    ...
  ]
}
```

**3.2 Get Category**
```http
GET /api/v1/categories/{category_id}

Response: 200 OK
{
  "id": 1,
  "name": "Housing",
  "parent_id": null,
  "type": "expense",
  "color": "#FF6B6B",
  "icon": "home",
  "description": "All housing-related expenses",
  "is_active": true,
  "created_at": "2025-06-01T00:00:00Z",
  "parent": null,
  "children": [...]
}
```

**3.3 Create Category**
```http
POST /api/v1/categories

Request Body:
{
  "name": "Home Maintenance",
  "parent_id": 1,  // Optional
  "type": "expense",
  "color": "#FF6B6B",
  "icon": "wrench",
  "description": "Repairs and maintenance"
}

Response: 201 Created
```

**3.4 Update Category**
```http
PUT /api/v1/categories/{category_id}

Request Body: (partial updates)
{
  "name": "Housing & Utilities",
  "color": "#FF8888"
}

Response: 200 OK
```

**3.5 Delete Category**
```http
DELETE /api/v1/categories/{category_id}

Response: 204 No Content

Error: 400 Bad Request
{
  "detail": "Cannot delete category with existing transactions or child categories"
}
```

#### 4. Reports

**4.1 Dashboard Summary**
```http
GET /api/v1/reports/summary

Query Parameters:
- period: str = "month"  # today, week, month, year, custom
- start_date: Optional[date] = None  # For custom period
- end_date: Optional[date] = None
- account_ids: Optional[List[int]] = None

Response: 200 OK
{
  "period": "2026-01",
  "total_income": 3000.00,
  "total_expenses": 2450.00,
  "net_savings": 550.00,
  "savings_rate": 18.3,
  "comparison": {
    "previous_period": "2025-12",
    "income_change": 2.5,
    "income_change_amount": 75.00,
    "expense_change": -5.2,
    "expense_change_amount": -135.00,
    "savings_change": 15.4,
    "savings_change_amount": 73.00
  },
  "top_categories": [
    {
      "category_id": 1,
      "category_name": "Housing",
      "amount": 1200.00,
      "percentage": 25.3,
      "transaction_count": 2
    },
    ...
  ],
  "total_balance": 12450.75,
  "accounts": [
    {
      "account_id": 1,
      "account_name": "Main Checking",
      "balance": 3200.00
    },
    ...
  ]
}
```

**4.2 Monthly Report**
```http
GET /api/v1/reports/monthly

Query Parameters:
- year: int
- month: int
- account_ids: Optional[List[int]] = None

Response: 200 OK
{
  "period": "2026-01",
  "summary": {
    "total_income": 3000.00,
    "total_expenses": 2450.00,
    "net_savings": 550.00,
    "transaction_count": 108
  },
  "daily_breakdown": [
    {
      "date": "2026-01-01",
      "income": 0.00,
      "expenses": 105.50,
      "net": -105.50,
      "transaction_count": 5
    },
    ...
  ],
  "category_breakdown": [
    {
      "category_id": 1,
      "category_name": "Housing",
      "amount": 1200.00,
      "percentage": 25.3,
      "transaction_count": 2,
      "avg_transaction": 600.00
    },
    ...
  ],
  "account_summary": [
    {
      "account_id": 1,
      "account_name": "Main Checking",
      "opening_balance": 2850.00,
      "inflow": 3000.00,
      "outflow": 1850.00,
      "closing_balance": 4000.00
    },
    ...
  ]
}
```

**4.3 Yearly Report**
```http
GET /api/v1/reports/yearly

Query Parameters:
- year: int

Response: 200 OK
{
  "year": 2026,
  "summary": {
    "total_income": 36000.00,
    "total_expenses": 28400.00,
    "net_savings": 7600.00,
    "avg_monthly_savings": 633.33,
    "savings_rate": 21.1
  },
  "monthly_breakdown": [
    {
      "month": "2026-01",
      "income": 3000.00,
      "expenses": 2450.00,
      "savings": 550.00,
      "savings_rate": 18.3
    },
    ...
  ],
  "category_trends": [
    {
      "category_id": 1,
      "category_name": "Housing",
      "total": 14400.00,
      "monthly_avg": 1200.00,
      "monthly_values": [1200, 1200, 1200, ...]
    },
    ...
  ]
}
```

**4.4 Category Report**
```http
GET /api/v1/reports/category/{category_id}

Query Parameters:
- start_date: date
- end_date: date

Response: 200 OK
{
  "category": {
    "id": 3,
    "name": "Groceries",
    "type": "expense"
  },
  "period": {
    "start": "2026-01-01",
    "end": "2026-01-31"
  },
  "summary": {
    "total_amount": 850.00,
    "transaction_count": 45,
    "avg_transaction": 18.89,
    "largest_transaction": 125.00,
    "smallest_transaction": 5.50
  },
  "top_merchants": [
    {
      "merchant": "SuperMart",
      "amount": 450.00,
      "count": 25
    },
    ...
  ],
  "trend": [
    {
      "date": "2026-01-01",
      "amount": 52.30
    },
    ...
  ]
}
```

#### 5. Export

**5.1 Export to Excel**
```http
POST /api/v1/export/excel

Request Body:
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-31",
  "account_ids": [1, 2, 3],  // Optional
  "category_ids": [1, 3, 5],  // Optional
  "include_summary": true,
  "include_charts": false
}

Response: 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="expense_report_Jan2026.xlsx"

[Binary Excel file]
```

**5.2 Export to CSV**
```http
POST /api/v1/export/csv

Request Body: (same as Excel)

Response: 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="transactions_Jan2026.csv"

Date,Account,Category,Type,Amount,Description,Merchant,Notes
2026-01-03,Main Checking,Groceries,Expense,52.30,Weekly shopping,SuperMart,Bought milk
...
```

#### 6. Health & Metadata

**6.1 Health Check**
```http
GET /api/v1/health

Response: 200 OK
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

**6.2 Get Metadata (Dropdowns)**
```http
GET /api/v1/metadata

Response: 200 OK
{
  "account_types": ["bank", "credit_card", "cash", "wallet", "investment"],
  "transaction_types": ["income", "expense", "transfer"],
  "currencies": ["USD", "EUR", "GBP", "INR", "CAD"],
  "date_presets": ["today", "yesterday", "this_week", "this_month", "this_year"]
}
```

### Error Response Format

All errors follow this format:
```json
{
  "detail": "Error message here",
  "error_code": "INVALID_AMOUNT",  // Optional
  "timestamp": "2026-01-03T10:30:00Z"
}
```

**HTTP Status Codes:**
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body (DELETE)
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required (web version)
- `403 Forbidden` - No permission (web version)
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## Frontend Architecture

### Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── assets/
│       └── icons/
├── src/
│   ├── main.tsx              # Entry point
│   ├── App.tsx                # Root component
│   ├── index.css              # Global styles (Tailwind)
│   │
│   ├── components/            # Reusable components
│   │   ├── ui/                # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Badge.tsx
│   │   │
│   │   ├── layout/            # Layout components
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── MainLayout.tsx
│   │   │   └── StatusBar.tsx
│   │   │
│   │   ├── forms/             # Form components
│   │   │   ├── TransactionForm.tsx
│   │   │   ├── AccountForm.tsx
│   │   │   ├── CategoryForm.tsx
│   │   │   └── FilterPanel.tsx
│   │   │
│   │   ├── tables/            # Data display
│   │   │   ├── TransactionTable.tsx
│   │   │   ├── AccountList.tsx
│   │   │   └── CategoryTree.tsx
│   │   │
│   │   └── charts/            # Chart components
│   │       ├── PieChart.tsx
│   │       ├── LineChart.tsx
│   │       └── BarChart.tsx
│   │
│   ├── pages/                 # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Transactions.tsx
│   │   ├── Accounts.tsx
│   │   ├── Categories.tsx
│   │   ├── Reports.tsx
│   │   └── Settings.tsx
│   │
│   ├── hooks/                 # Custom React hooks
│   │   ├── useTransactions.ts
│   │   ├── useAccounts.ts
│   │   ├── useCategories.ts
│   │   ├── useReports.ts
│   │   └── useLocalStorage.ts
│   │
│   ├── services/              # API services
│   │   ├── api.ts             # Axios instance
│   │   ├── transactionService.ts
│   │   ├── accountService.ts
│   │   ├── categoryService.ts
│   │   └── reportService.ts
│   │
│   ├── types/                 # TypeScript types
│   │   ├── transaction.ts
│   │   ├── account.ts
│   │   ├── category.ts
│   │   └── api.ts
│   │
│   ├── utils/                 # Utility functions
│   │   ├── formatCurrency.ts
│   │   ├── formatDate.ts
│   │   ├── validation.ts
│   │   └── constants.ts
│   │
│   └── store/                 # State management (if needed)
│       └── uiStore.ts         # Zustand store for UI state
│
├── .env.development           # Dev environment vars
├── .env.production            # Prod environment vars
├── tsconfig.json              # TypeScript config
├── vite.config.ts             # Vite config
├── tailwind.config.js         # Tailwind config
├── package.json
└── README.md
```

### State Management Strategy

**React Query (TanStack Query) for Server State:**
- All API data (transactions, accounts, categories)
- Automatic caching and refetching
- Optimistic updates
- Background synchronization

**Zustand for UI State (Optional):**
- Sidebar open/closed
- Theme (light/dark)
- Filter panel state
- Modal state

**Example: Transaction Hook**
```typescript
// hooks/useTransactions.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { transactionService } from '../services/transactionService';
import { Transaction, TransactionFilters } from '../types/transaction';

export function useTransactions(filters?: TransactionFilters) {
  return useQuery({
    queryKey: ['transactions', filters],
    queryFn: () => transactionService.getAll(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useCreateTransaction() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: transactionService.create,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });
}
```

### Component Example

**Transaction Form Component:**
```typescript
// components/forms/TransactionForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateTransaction } from '../../hooks/useTransactions';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';

const transactionSchema = z.object({
  date: z.string(),
  amount: z.number().positive(),
  transaction_type: z.enum(['income', 'expense', 'transfer']),
  account_id: z.number(),
  category_id: z.number().optional(),
  description: z.string().max(255).optional(),
  merchant: z.string().max(100).optional(),
  notes: z.string().optional(),
});

type TransactionFormData = z.infer<typeof transactionSchema>;

export function TransactionForm({ onSuccess }: { onSuccess: () => void }) {
  const createMutation = useCreateTransaction();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TransactionFormData>({
    resolver: zodResolver(transactionSchema),
    defaultValues: {
      date: new Date().toISOString().split('T')[0],
      transaction_type: 'expense',
    },
  });

  const onSubmit = async (data: TransactionFormData) => {
    try {
      await createMutation.mutateAsync(data);
      reset();
      onSuccess();
    } catch (error) {
      console.error('Failed to create transaction:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Date"
        type="date"
        {...register('date')}
        error={errors.date?.message}
      />

      <Input
        label="Amount"
        type="number"
        step="0.01"
        {...register('amount', { valueAsNumber: true })}
        error={errors.amount?.message}
      />

      <Select
        label="Type"
        {...register('transaction_type')}
        options={[
          { value: 'income', label: 'Income' },
          { value: 'expense', label: 'Expense' },
          { value: 'transfer', label: 'Transfer' },
        ]}
      />

      {/* More fields... */}

      <Button
        type="submit"
        loading={createMutation.isPending}
      >
        Save Transaction
      </Button>
    </form>
  );
}
```

---

## Backend Architecture

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection
│   │
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── tag.py
│   │
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── common.py
│   │
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   ├── transactions.py
│   │   ├── accounts.py
│   │   ├── categories.py
│   │   ├── reports.py
│   │   └── export.py
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── transaction_service.py
│   │   ├── account_service.py
│   │   ├── category_service.py
│   │   ├── report_service.py
│   │   └── export_service.py
│   │
│   ├── crud/                  # Database operations
│   │   ├── __init__.py
│   │   ├── transaction.py
│   │   ├── account.py
│   │   └── category.py
│   │
│   ├── utils/                 # Utilities
│   │   ├── __init__.py
│   │   ├── date_helpers.py
│   │   ├── currency.py
│   │   └── validators.py
│   │
│   └── middleware/            # Middleware
│       ├── __init__.py
│       ├── error_handler.py
│       └── cors.py
│
├── migrations/                # Alembic migrations
│   ├── versions/
│   └── env.py
│
├── tests/                     # Tests
│   ├── conftest.py
│   ├── test_transactions.py
│   ├── test_accounts.py
│   └── test_reports.py
│
├── scripts/                   # Utility scripts
│   ├── init_db.py
│   ├── seed_categories.py
│   └── migrate_data.py
│
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── pytest.ini
└── README.md
```

### Main Application File

**File: `backend/app/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import webbrowser
import threading
import time

from app.config import settings
from app.database import engine, Base
from app.routes import transactions, accounts, categories, reports, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown"""
    # Startup
    Base.metadata.create_all(bind=engine)

    # Open browser after short delay (desktop mode only)
    if settings.DESKTOP_MODE:
        def open_browser():
            time.sleep(1.5)  # Wait for server to start
            webbrowser.open(f"http://localhost:{settings.PORT}")

        threading.Thread(target=open_browser, daemon=True).start()

    yield

    # Shutdown (cleanup if needed)


app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware (allow localhost for desktop mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite/React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(export.router, prefix="/api/v1/export", tags=["export"])


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Localhost only for security
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

### Configuration

**File: `backend/app/config.py`**
```python
from pydantic_settings import BaseSettings
import os
from pathlib import Path


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Expense Tracker"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 8000
    DESKTOP_MODE: bool = True  # Auto-open browser

    # Database
    DATABASE_URL: str = "sqlite:///./expense_tracker.db"

    # For production (web version)
    # DATABASE_URL: str = "postgresql://user:password@localhost/expensedb"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    BACKUP_DIR: Path = DATA_DIR / "backups"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"

    # Security (for web version)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()

# Create directories if they don't exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
```

### Service Example

**File: `backend/app/services/transaction_service.py`**
```python
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.crud import transaction as transaction_crud
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionFilters
from app.models.transaction import Transaction


class TransactionService:
    def get_all(
        self,
        db: Session,
        filters: TransactionFilters,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Transaction], int]:
        """Get all transactions with filters and pagination"""
        transactions = transaction_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters
        )
        total = transaction_crud.count(db, filters=filters)
        return transactions, total

    def get_by_id(self, db: Session, transaction_id: int) -> Optional[Transaction]:
        """Get single transaction by ID"""
        return transaction_crud.get(db, id=transaction_id)

    def create(self, db: Session, transaction_in: TransactionCreate) -> Transaction:
        """Create new transaction"""
        # Business logic (validation, calculations, etc.)

        # Handle transfer type
        if transaction_in.transaction_type == "transfer":
            return self._create_transfer(db, transaction_in)

        # Regular income/expense
        transaction = transaction_crud.create(db, obj_in=transaction_in)

        # Trigger handles account balance update
        db.commit()
        db.refresh(transaction)

        return transaction

    def _create_transfer(self, db: Session, transfer_in: TransactionCreate) -> Transaction:
        """Create linked transfer transactions"""
        # Validate transfer
        if not transfer_in.transfer_to_account_id:
            raise ValueError("Transfer requires destination account")

        if transfer_in.account_id == transfer_in.transfer_to_account_id:
            raise ValueError("Cannot transfer to same account")

        # Create debit transaction (from source)
        debit_data = transfer_in.model_copy()
        debit_data.direction = "debit"
        debit_data.is_transfer = True
        debit_transaction = transaction_crud.create(db, obj_in=debit_data)

        # Create credit transaction (to destination)
        credit_data = transfer_in.model_copy()
        credit_data.account_id = transfer_in.transfer_to_account_id
        credit_data.transfer_to_account_id = transfer_in.account_id
        credit_data.direction = "credit"
        credit_data.is_transfer = True
        credit_transaction = transaction_crud.create(db, obj_in=credit_data)

        db.commit()
        db.refresh(debit_transaction)

        return debit_transaction

    def update(
        self,
        db: Session,
        transaction_id: int,
        transaction_in: TransactionUpdate
    ) -> Optional[Transaction]:
        """Update existing transaction"""
        transaction = self.get_by_id(db, transaction_id)
        if not transaction:
            return None

        # Business logic for updates
        # Handle transfer updates specially
        if transaction.is_transfer:
            # Update both linked transactions
            pass

        updated = transaction_crud.update(db, db_obj=transaction, obj_in=transaction_in)
        db.commit()
        db.refresh(updated)

        return updated

    def delete(self, db: Session, transaction_id: int) -> bool:
        """Delete transaction"""
        transaction = self.get_by_id(db, transaction_id)
        if not transaction:
            return False

        # If transfer, delete linked transaction too
        if transaction.is_transfer and transaction.transfer_to_account_id:
            # Find and delete linked transaction
            pass

        transaction_crud.remove(db, id=transaction_id)
        db.commit()

        return True


transaction_service = TransactionService()
```

---

*(Continuing in next part due to length...)*

I'll continue the Technical Specifications document:
