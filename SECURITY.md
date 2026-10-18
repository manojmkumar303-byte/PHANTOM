# Security Policy

## Project status

PHANTOM Knowledge Vault is early-stage software and has not received an independent security audit. Do not use it as the only copy of irreplaceable data or as a professionally audited password manager.

## Reporting a vulnerability

Please do not publish exploit details or sensitive personal data in a public issue. Contact the maintainer through the GitHub profile and ask for a private reporting route. Include the affected version, impact, reproducible steps, and a proposed mitigation where possible. Never include real vault files, passwords, recovery phrases, or tokens.

## Current design and limitations

- The application derives an encryption key from a master password using scrypt with a random salt.
- Note payloads are encrypted with Fernet authenticated encryption.
- The current source uses a relatively modest scrypt work factor; stronger parameters and a tested vault migration path should be reviewed before a public security-focused release.
- Auto-lock drops application references but cannot guarantee secure erasure of Python memory.
- The app does not provide secure deletion guarantees, attachment encryption, cloud synchronization, or protection from malware running under the user's account.
- Generated passwords, when implemented, should use Python's \`secrets\` module and should not be automatically stored or logged.
- The application has not been independently audited.

## Supported versions

Security fixes will target the latest repository version. Until tagged releases and a support policy are established, no formal version support guarantee is made.
