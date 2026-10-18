# Architecture

## Current application

The supplied starter implementation is a single-process Python desktop application using Tkinter for its UI and the cryptography package for cryptographic operations.

- \`main.py\`: UI, vault lifecycle, encrypted persistence.
- \`requirements.txt\`: third-party runtime dependency.
- \`run.bat\`: Windows setup and launch helper.

The initial version keeps the note collection in memory while unlocked and stores it as one encrypted payload. This is simple but means every save rewrites the entire payload.

## Vault file

The vault is a JSON envelope containing a format version, KDF identifier, cipher label, base64-encoded salt, and Fernet token. The notes JSON is encrypted before writing. The salt and metadata are not secret. Fernet authenticates ciphertext so tampering causes decryption to fail.

The starter code uses scrypt with N=16384, r=8, p=1. Any change to KDF parameters must be versioned and must include a tested migration path, so existing vaults remain readable.

Writes use a temporary file in the same directory followed by replacement. The implementation should validate the existing envelope before saving and detect external modifications to avoid overwriting a changed vault.

## Design boundaries

The application is offline-first and does not currently implement GitHub or API integrations. A future modular refactor should separate presentation, vault services, cryptography, persistence, and integrations before those features are added.
