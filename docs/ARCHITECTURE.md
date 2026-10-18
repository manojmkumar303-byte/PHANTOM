# Architecture

## Current application

The application is a single-process Python desktop application using Tkinter for its UI and the cryptography package for cryptographic operations.

- \`main.py\`: UI, vault lifecycle, encrypted persistence, and password generator.
- \`requirements.txt\`: third-party runtime dependency.
- \`run.bat\`: Windows setup and launch helper.
- \`tests/test_core.py\`: unit tests for password generation and vault behavior.

The note collection is held in memory while unlocked and stored as one encrypted payload. Every save rewrites that payload.

## Vault file

The vault is a JSON envelope containing a format version, KDF identifier, cipher label, base64-encoded salt, and Fernet token. The notes JSON is encrypted before writing. The salt and metadata are not secret. Fernet authenticates ciphertext so tampering causes decryption to fail.

The current source retains the starter format and scrypt setting (N=16384, r=8, p=1) for compatibility with existing vaults. This is a modest work factor and should be improved through a versioned, tested migration path before a security-focused release.

Writes use a temporary file in the same directory followed by replacement. Before a save, the app checks the expected token to detect an external change and avoid blindly overwriting a changed vault.

## Password generator

The generator uses \`secrets.choice\` to choose characters and \`secrets.SystemRandom().shuffle\` to shuffle the result. It inserts one character from every enabled class before filling the remaining positions, so selected classes are represented. Generated values are only kept in the generator dialog until it closes, unless the user copies one to the OS clipboard.

## Design boundaries

The application is offline-first and does not currently implement GitHub or API integrations. A future modular refactor should separate presentation, vault services, cryptography, persistence, and integrations before those features are added.
