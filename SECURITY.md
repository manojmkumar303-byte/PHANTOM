# Security Policy

## Project status

PHANTOM Knowledge Vault is early-stage software and has not received an independent security audit. Do not use it as the only copy of irreplaceable data or as a professionally audited password manager.

## Reporting a vulnerability

Please do not publish exploit details or sensitive personal data in a public issue. Contact the maintainer through the GitHub profile and ask for a private reporting route. Include the affected version, impact, reproducible steps, and a proposed mitigation where possible. Never include real vault files, passwords, recovery phrases, or tokens.

## Current design and limitations

- The vault derives an encryption key from the master password using scrypt with a random salt. The current work factor (N=16384, r=8, p=1) is modest and should be reviewed before a public security-focused release.
- Note payloads use Fernet authenticated encryption.
- Generated passwords use Python's \`secrets\` module, ensure each selected character class is represented, and are not automatically saved or logged.
- Passwords explicitly copied by the user are placed on the operating system clipboard; the app does not control how long the OS retains them.
- Auto-lock drops application references but cannot guarantee secure erasure of Python memory.
- The app does not provide secure deletion guarantees, attachment encryption, cloud synchronization, or protection from malware running under the user's account.
- The application has not been independently audited. Cryptographic library presence is not itself proof of correct security.

## Supported versions

Security fixes will target the latest repository version. Until tagged releases and a support policy are established, no formal version support guarantee is made.
