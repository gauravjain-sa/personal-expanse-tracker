
FINANCE APP DESIGN DISCUSSION – STRUCTURED EXPORT
#################################################

SECTION 1: PROBLEM STATEMENT
----------------------------
You currently manage personal finances using multiple Excel sheets.
Pain points:
- Manual categorization of expenses
- Incorrect categories from banks/cards
- Transfers vs expenses confusion
- Too much repetitive correction work
Goal:
- Simple, modern, easy-to-use application
- Manual entry first (no imports initially)
- Auto-categorization with override
- Lightweight, self-contained
- Desktop-first, scalable to web later
- Easy maintenance and strong community support

------------------------------------------------

SECTION 2: INITIAL OPTIONS DISCUSSED
------------------------------------
Options explored:
- Excel + Power Query + rules
- Desktop apps (PySide, .NET, Delphi, JavaFX)
- Modern hybrid apps (Electron, Tauri, Flutter)
- Browser-based local apps

Key decision:
Move away from Excel and heavy native stacks toward a modern, scalable architecture.

------------------------------------------------

SECTION 3: CORE REQUIREMENTS CLARIFIED
--------------------------------------
Hard requirements:
- Single-user
- Manual entry only (v1)
- Auto-categorization + learning rules
- Transfers treated separately
- No external dependencies for user
- Click-and-run experience
- Lightweight
- Easy future web version

------------------------------------------------

SECTION 4: DESKTOP STRATEGY EVOLUTION
-------------------------------------
Rejected:
- Heavy native stacks (.NET, Electron)
- Spreadsheet-driven systems
- Apps requiring runtime installs

Accepted:
- Browser-based UI opened automatically
- Local backend + local database
- App behaves like desktop but architected as web

Key insight:
Desktop # Web app running locally

------------------------------------------------

SECTION 5: TECH STACK COMPARISON SUMMARY
---------------------------------------

Go:
+ Best packaging (single binary)
- Learning curve
- Smaller ecosystem familiarity

Python:
+ Very large community
+ FastAPI is modern and clean
+ Easy rules engine
- Heavier packaged binaries

Node:
+ Modern JS ecosystem
- Native SQLite packaging complexity

Ruby:
+ Excellent web productivity
- Weak desktop packaging story

PHP:
+ Web friendly
- Poor desktop-first experience

------------------------------------------------

SECTION 6: FINAL RECOMMENDED STACK
----------------------------------

Frontend:
- React + TypeScript
- Vite
- Tailwind CSS

Backend:
- Python + FastAPI

Database:
- SQLite (desktop)
- PostgreSQL (future web)

Desktop Packaging:
- PyInstaller bundled executable
- App starts FastAPI locally
- Auto-opens browser
- SQLite stored locally

Why this wins:
- Modern UI
- Easy maintenance
- Massive community support
- Clean upgrade path to real web app
- Supports Docker/containerization later

------------------------------------------------

SECTION 7: CORE APP FEATURES (V1)
---------------------------------
- Add Transaction form
- Auto-category suggestion
- Merchant memory
- Rules engine (contains/regex)
- Transfer as transaction type
- Monthly reports
- CSV/Excel export

------------------------------------------------

APPENDIX: RAW CONVERSATION SUMMARY
---------------------------------
This document is derived from a continuous design discussion focused on
balancing simplicity, modern UI, desktop usability, and future scalability.
