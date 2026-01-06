# Quick Start - Build Installer

## For Non-Developers: Download Pre-Built Installer

If you just want to use the application:
1. Download `ExpenseTracker_Setup_v1.0.0.exe` from the releases page
2. Double-click to install
3. Launch and enjoy!

## For Developers: Building the Installer

### Prerequisites (One-Time Setup)

1. **Install Python 3.10 or later**
   - Download from: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Install Inno Setup 6** (for Windows installer)
   - Download from: https://jrsoftware.org/isdl.php
   - Install to default location

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Build (3 Steps)

#### Option A: Automated Build (Recommended)

Just run:
```bash
build_all.bat
```

This will:
1. Build the executable
2. Test it
3. Create the installer
4. Open the output folder

#### Option B: Manual Build

**Step 1: Build Executable**
```bash
python build.py
```
Wait 2-3 minutes for completion.

**Step 2: Test the Application**
```bash
cd dist\ExpenseTracker
ExpenseTracker.exe
```
Test all features to ensure everything works.

**Step 3: Create Installer**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

**Done!** Installer is at: `installer_output/ExpenseTracker_Setup_v1.0.0.exe`

## What Gets Created

```
expanse-tracker/
├── dist/
│   └── ExpenseTracker/          ← Standalone application (portable)
│       ├── ExpenseTracker.exe   ← Main executable
│       ├── _internal/            ← Dependencies
│       └── README.txt
│
└── installer_output/
    └── ExpenseTracker_Setup_v1.0.0.exe  ← Final installer (distribute this!)
```

## Distribution

**For Users:**
- Distribute: `ExpenseTracker_Setup_v1.0.0.exe`
- Size: ~50-80 MB
- Requirements: Windows 10 or later (no Python needed!)

**Data Location (After Install):**
- User data: `%APPDATA%\Expense Tracker\`
- Database: `%APPDATA%\Expense Tracker\expense_tracker.db`

## Troubleshooting

### Build fails with "PyInstaller not found"
```bash
pip install pyinstaller
```

### Build succeeds but EXE doesn't run
- Run from command line to see errors:
  ```bash
  dist\ExpenseTracker\ExpenseTracker.exe
  ```
- Check if antivirus is blocking it

### Inno Setup not found
- Install from: https://jrsoftware.org/isdl.php
- Or use portable ZIP instead of installer

### Want to add a custom icon?
1. Create/download a `.ico` file (256x256)
2. Save as: `resources/icon.ico`
3. Rebuild: `python build.py`

## Updating Version

Edit these files:
1. `config.py` → Change `VERSION = "1.0.1"`
2. `installer.iss` → Change `#define MyAppVersion "1.0.1"`
3. Rebuild and distribute!

## Need Help?

- Full guide: See `DEPLOYMENT_GUIDE.md`
- Issues: Open a GitHub issue
- Email: support@yourcompany.com
