# Roadmap

Roadmap items are intentions, not claims about current functionality.

## Core reliability

- [x] Local encrypted notes and master-password unlock
- [x] Search, categories, and five-minute inactivity lock
- [x] Offline password generator using Python's \`secrets\` module
- [x] Initial automated tests and Windows CI workflow
- [x] Initial threat model and security policy
- [ ] Review scrypt parameters and add a tested migration path before changing existing vault formats.
- [ ] Add more tests for corrupted ciphertext, malformed note records, and interrupted writes.
- [ ] Add encrypted backup/restore with validation and explicit overwrite protection.
- [ ] Improve separation between UI, storage, and security services.
- [ ] Choose and add an open-source license.

## Later, only after the core is reliable

- [ ] Markdown and developer snippet library.
- [ ] Quick capture and keyboard shortcuts.
- [ ] Optional GitHub repository references and local annotations.
- [ ] Optional API request workbench with strict URL validation and safe defaults.

## Explicitly not in the current release

Cloud sync, AI integrations, continuous clipboard monitoring, arbitrary code execution, automatic repository cloning, and a full credential manager.
