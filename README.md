# PHANTOM Knowledge Vault

PHANTOM Knowledge Vault is a lightweight, local-first Windows desktop application for keeping personal notes on your own device. It provides master-password access, authenticated encryption for stored notes, categories, search, automatic locking, and an offline password generator.

> **Project status:** early development. This software has not received an independent security audit. Do not use it as the only copy of irreplaceable information or as a substitute for a professionally audited password manager.

## Current features

- Create a vault protected by a master password.
- Encrypt the vault payload using Fernet authenticated encryption.
- Derive encryption keys with scrypt and a random 16-byte salt.
- Create, edit, search, categorize, and delete notes.
- Lock the vault after five minutes without keyboard or mouse activity.
- Generate passwords locally using Python's \`secrets\` module, with configurable length and character sets.
- Optionally exclude ambiguous characters and ensure every selected character class is represented.
- Copy a generated password to the system clipboard on explicit request.
- Keep the core application offline; no account, cloud sync, or network connection is required.

## Requirements

- Windows 10/11 recommended.
- Python 3.10 or newer.
- Tkinter (normally included with the standard Windows Python installer).
- Dependencies listed in \`requirements.txt\`.

## Run from source

1. Install Python from [python.org](https://www.python.org/downloads/windows/). Enable **Add Python to PATH** during installation.
2. Download or clone this repository.
3. Open a terminal in the repository folder and run:

   \`\`\`powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python main.py
   \`\`\`

   Or double-click \`run.bat\` on Windows.

## Local data

The vault is stored at \`%USERPROFILE%\\.personal_knowledge_vault\\vault.pkv\`. The vault file contains an encrypted payload, but its existence, size, and modification time are visible to the operating system. Back up the vault only while the application is closed, and store backups somewhere protected. If you forget the master password, there is no recovery mechanism.

## Password generator notes

Password generation uses Python's \`secrets\` module, not \`random\`. Generated passwords are not automatically saved or logged. Copying puts the password on the operating system clipboard, which may remain available to other applications until replaced.

## Security

Read [SECURITY.md](SECURITY.md) and [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) before using the app for sensitive data. This software has not been independently audited. It does not defend against malware running as your user, keyloggers, compromised operating systems, memory inspection, or insecure backups. Python cannot guarantee secure erasure of secrets from memory.

## Development

Run tests with:

\`\`\`powershell
python -m unittest discover -s tests -v
\`\`\`

See [CONTRIBUTING.md](CONTRIBUTING.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [docs/ROADMAP.md](docs/ROADMAP.md).

## Scope

This repository currently contains the Knowledge Vault desktop application. GitHub repository browsing, API request workbench, encrypted backup/restore UI, cloud synchronization, and AI features are not implemented in this version. The roadmap tracks possible future work separately from shipped functionality.

## License

A license has not yet been selected. Until a license is added, do not assume you have permission to redistribute or modify this project. Choose and add a license before advertising the repository as an officially licensed open-source release.
