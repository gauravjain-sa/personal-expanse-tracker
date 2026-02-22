# CLAUDE.md - Project Rules for Claude AI

## Project Overview
This is a Python desktop Expense Tracker application built with CustomTkinter, SQLAlchemy, and SQLite. It uses PyInstaller for packaging and Inno Setup for creating Windows installers.

## CRITICAL SECURITY RULES

### Never Include in Responses or Code
- **API keys**, tokens, or secrets of any kind
- **Database credentials** or connection strings with real passwords
- **User credentials** (usernames, passwords, PINs)
- **Financial data** (real account numbers, transaction amounts, bank details)
- **Personal information** (names, addresses, phone numbers, SSN, email addresses)
- **Private keys**, certificates, or encryption keys
- **Environment variable values** that contain secrets

### Code Practices
- Never hardcode credentials, API keys, or secrets in source code
- Use `os.getenv()` or secure config for any sensitive values
- Use placeholder values like `"your-api-key-here"` or `os.getenv("API_KEY")`
- Never generate real-looking API keys, tokens, or credentials
- Never log or print sensitive data (passwords, keys, financial details)
- Database files (`.db`, `.sqlite`) contain user financial data — never read or share them

### Files to Never Read or Reference
- `*.db`, `*.sqlite`, `*.sqlite3` — contain user financial data
- `*.sql`, `*.dump`, `*.bson` — database dumps
- `*.pem`, `*.key`, `*.cert`, `*.crt`, `*.cer`, `*.csr`, `*.der` — PEM/OpenSSL keys/certs
- `*.p12`, `*.pfx`, `*.p7b`, `*.p8` — PKCS formats
- `*.jks`, `*.jceks`, `*.keystore`, `*.truststore` — Java keystores
- `*.keychain`, `*.keychain-db` — macOS keychains
- `.env`, `.env.*`, `.envrc` — environment secrets
- `secrets.*`, `credentials.*`, `*.secret`, `*.token` — credential/secret files
- `.vault-token` — HashiCorp Vault tokens
- `*secret*.yaml`, `*secret*.ini`, `*credential*.yaml`, `*password*.yaml` — config files containing secrets
- `config.local.*`, `*.local.yaml`, `*.production.yaml` — environment-specific configs with secrets
- Note: project structure configs (`pyproject.toml`, `setup.cfg`, `docker-compose.yml`) are OK to read
- `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`, `*.ppk` — SSH keys
- `*.gpg`, `*.asc` — GPG keys
- `*.jwk`, `*.jwks` — OAuth/JWT keys
- `*.htpasswd`, `*.netrc`, `*.pgpass`, `.my.cnf` — password/auth files
- `*.kdbx`, `*.kdb` — password manager databases
- `wallet.dat`, `*.wallet` — crypto wallets
- `.aws/`, `.gcloud/`, `.azure/` — cloud provider credentials
- `.npmrc`, `.pypirc`, `.git-credentials`, `.dockercfg` — tool auth tokens
- `.*_history`, `.bash_history`, `.python_history` — history files (may contain passwords)
- `*.ovpn`, `*.rdp`, `*.vnc` — VPN/remote access configs
- `*.enc`, `*.encrypted` — encrypted files
- `*.tfvars`, `*.tfstate` — Terraform state (may contain secrets)

## Project Structure
```
├── main.py                 # Entry point
├── config.py               # Centralized configuration (no secrets)
├── requirements.txt        # Python dependencies
├── models/                 # SQLAlchemy ORM models
├── repositories/           # Data access layer
├── services/               # Business logic
├── ui/                     # CustomTkinter interface
├── database/               # DB connection, init, seeding
├── documents/              # Project documentation
├── resources/              # App resources (icons etc.)
├── build.py                # PyInstaller build script
├── build_all.bat           # Full build pipeline
├── installer.iss           # Inno Setup installer script
├── start.bat               # Application launcher
└── .gitignore              # Version control exclusions
```

## Development Guidelines
- All configuration is centralized in `config.py` — no hardcoding
- Database is stored in `%APPDATA%\Expense Tracker\` — never in the source directory
- Keep changes minimal and simple, do not over-engineer
- Follow existing folder structure and naming conventions
- Changes should be easy to maintain and debug
- Propose changes with minimal impact and no regression

## Build System
- `build.py` — PyInstaller build script (creates standalone `.exe`)
- `build_all.bat` — orchestrates full build pipeline (build + installer)
- `installer.iss` — Inno Setup script for Windows installer
- Build documentation: `documents/BUILD_QUICKSTART.md`, `documents/DEPLOYMENT_GUIDE.md`

