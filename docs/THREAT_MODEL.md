# Threat Model (Initial)

## Assets

- Personal notes stored in the vault.
- The master password and derived encryption key while the app is running.
- Any generated password, once a generator is integrated.

## Intended protections

- Protect note contents at rest when the vault file is copied without the master password.
- Detect modifications to encrypted payloads through authenticated encryption.
- Reduce unattended access by locking after five minutes of inactivity.
- Keep the normal application workflow offline.

## Out of scope

- Malware, keyloggers, screen capture, or a compromised OS account.
- An attacker who can inspect the application's memory while unlocked.
- Secure erasure from RAM, swap, crash dumps, or backups.
- Protection of copied passwords from other applications that can read the system clipboard.
- Recovery when the master password is forgotten.
- Independent cryptographic certification or professional security audit.

## Important assumptions

The master password should be long and unique. The computer and OS account must be trusted. Users should maintain protected backups and verify restore procedures. KDF parameters should be benchmarked on supported hardware, and changes to vault formats must retain tested migration paths.

## Review priorities

1. Test corrupt and malformed vault files and interrupted writes.
2. Test KDF upgrades and migration failures without risking the original vault.
3. Review KDF parameter suitability across supported Windows hardware.
4. Review UI secret retention and lock semantics.
5. Perform independent review before making strong security claims.
