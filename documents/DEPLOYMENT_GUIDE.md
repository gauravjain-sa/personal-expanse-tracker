# Deployment Guide - Expense Tracker

This guide explains how to package and distribute the Expense Tracker application as a standalone Windows installer.

## Prerequisites

### For Building the Application

1. **Python 3.10+** installed
2. **All dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Inno Setup 6** (for creating the installer):
   - Download from: https://jrsoftware.org/isdl.php
   - Install to default location (C:\Program Files (x86)\Inno Setup 6)

4. **Optional: Icon file**
   - Place a `.ico` file at `resources/icon.ico` for custom application icon
   - If not provided, default Python icon will be used

## Building Process

### Step 1: Build the Executable

Run the build script:

```bash
python build.py
```

This will:
- Clean old build artifacts
- Install PyInstaller if needed
- Create a standalone executable in `dist/ExpenseTracker/`
- Bundle all dependencies
- Create a README.txt file

**Output Location:** `dist/ExpenseTracker/`

### Step 2: Test the Executable

Before creating the installer, test the application:

```bash
cd dist\ExpenseTracker
ExpenseTracker.exe
```

**What to test:**
- Application launches successfully
- Database initializes in %APPDATA%\Expense Tracker\
- All features work correctly
- No console window appears
- Can create accounts, categories, transactions
- Export functionality works
- Application closes cleanly

### Step 3: Create the Installer

Once testing is complete, create the installer:

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

Or simply right-click on `installer.iss` and select "Compile".

**Output Location:** `installer_output/ExpenseTracker_Setup_v1.0.0.exe`

## Distribution

### Distributing the Installer

The installer (`ExpenseTracker_Setup_v1.0.0.exe`) is a **100% self-contained** single file that:
- Can be distributed via email, website, USB drive, etc.
- Size: Approximately 50-80 MB (includes Python runtime + all dependencies)
- Requires **nothing else** on the target machine (no Python, no pip, no downloads)
- Works on Windows 10 and later

### Installation Process for End Users

Users simply:
1. Double-click the installer
2. Follow the wizard (Next, Next, Install)
3. Optionally create desktop shortcut
4. Launch the application

**First Run:**
- Database created in: `%APPDATA%\Expense Tracker\`
- Default categories seeded automatically
- Application opens to Dashboard

## Data Storage

### User Data Location

All user data is stored in:
```
%APPDATA%\Expense Tracker\
├── expense_tracker.db    (Main database)
├── backups/              (Backup files)
├── exports/              (Exported Excel/CSV files)
└── logs/                 (Application logs)
```

This location is:
- User-specific (each Windows user has their own data)
- Writable without admin privileges
- Survives application uninstall (optionally)
- Easy to backup

### Backing Up Data

Users can backup their data by:
1. Closing the application
2. Copying: `%APPDATA%\Expense Tracker\expense_tracker.db`
3. Storing the file safely

To restore:
1. Close the application
2. Replace the database file with the backup

## Uninstallation

When users uninstall via Windows Settings or Control Panel:
- Application files are removed from Program Files
- User is asked if they want to keep their financial data
- If "Yes": Data remains in AppData for future reinstall
- If "No": All data is permanently deleted

## Troubleshooting Build Issues

### Issue: PyInstaller fails with "Module not found"

**Solution:** Add the module to hidden imports in `build.py`:
```python
hidden_imports = [
    "customtkinter",
    "your_missing_module",  # Add here
    # ...
]
```

### Issue: Application crashes on launch

**Solution:**
1. Run from command line to see error messages:
   ```bash
   dist\ExpenseTracker\ExpenseTracker.exe
   ```
2. Check if all data files are included in the build
3. Verify database path is writable

### Issue: Missing DLL errors

**Solution:**
- Install Visual C++ Redistributable on the target machine
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Issue: Database not created

**Solution:**
- Ensure %APPDATA% is writable
- Check Windows permissions
- Run application as current user (not admin)

## Version Updates

### Updating the Application

To release a new version:

1. Update version number in three places:
   - `config.py`: `VERSION = "1.0.1"`
   - `installer.iss`: `#define MyAppVersion "1.0.1"`
   - `build.py`: (optional, for reference)

2. Rebuild:
   ```bash
   python build.py
   ```

3. Test the new build thoroughly

4. Create new installer:
   ```bash
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

5. Distribute the new installer

### User Update Process

Users can:
1. Install new version over old version (preserves data)
2. Or uninstall old version first (choose to keep data)

Data is automatically migrated if database schema changes are needed.

## Advanced Configuration

### Customizing the Build

**Change application name:**
- Update `APP_NAME` in `config.py`
- Update `MyAppName` in `installer.iss`
- Update `--name` in `build.py`

**Add custom icon:**
- Place 256x256 icon at `resources/icon.ico`
- Rebuild the application

**Reduce installer size:**
- Use `--onefile` instead of `--onedir` in PyInstaller (slower startup)
- Remove unnecessary dependencies from requirements.txt

**Add version info to EXE:**
- Create `version.rc` file with version information
- Add `--version-file` parameter to PyInstaller

### Distribution Channels

**Website Download:**
- Host the installer on your website
- Provide checksums (SHA256) for verification

**Auto-Updates:**
- Implement update checker in the application
- Download new installer in background
- Prompt user to install update

**Portable Version:**
- Use `--onefile` in PyInstaller
- Don't use installer (just ZIP the executable)
- Store database relative to EXE (not in AppData)

## Security Considerations

### Code Signing (Recommended for Production)

To avoid Windows SmartScreen warnings:

1. Obtain a code signing certificate
2. Sign the EXE and installer:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com ExpenseTracker.exe
   ```

### Virus Scanning

PyInstaller executables may trigger false positives:
- Test with Windows Defender
- Submit to VirusTotal
- Whitelist with major antivirus vendors

## Support

### End User Support

Create these resources for users:
1. User manual (PDF or online help)
2. FAQ document
3. Video tutorials
4. Support email/forum

### Technical Support

For developers building the application:
- Check GitHub Issues
- Review PyInstaller documentation
- Test on clean Windows VM

## Checklist

### Pre-Release Checklist

- [ ] All features tested and working
- [ ] Version numbers updated
- [ ] Icon file added
- [ ] Build.py runs without errors
- [ ] Executable tested on clean Windows machine
- [ ] Installer created and tested
- [ ] Installation tested on Windows 10
- [ ] Installation tested on Windows 11
- [ ] Uninstallation tested (keep data option)
- [ ] Uninstallation tested (delete data option)
- [ ] README.txt included and accurate
- [ ] User documentation prepared
- [ ] Code signed (if applicable)
- [ ] Virus scanned and false positives addressed

### Post-Release

- [ ] Monitor user feedback
- [ ] Track crash reports (if telemetry enabled)
- [ ] Prepare patch release for critical bugs
- [ ] Plan feature updates based on user requests

## Files Overview

### Build System Files (in project root)

- `build.py` - Main build script (creates executable via PyInstaller)
- `build_all.bat` - Automated full pipeline (build + test + installer)
- `installer.iss` - Inno Setup script (creates installer)
- `resources/icon.ico` - Application icon (optional, see note below)

### Documentation Files (in documents/ folder)

- `BUILD_QUICKSTART.md` - Quick start guide for building
- `DEPLOYMENT_GUIDE.md` - This file (comprehensive deployment guide)

### Output Files

- `dist/ExpenseTracker/` - Standalone application folder
- `installer_output/ExpenseTracker_Setup_v1.0.0.exe` - Final installer

### Build Artifacts (can be deleted)

- `build/` - Temporary build files
- `*.spec` - PyInstaller spec file (auto-generated)

## Contact

For questions about the deployment process:
- GitHub: https://github.com/yourusername/expanse-tracker
