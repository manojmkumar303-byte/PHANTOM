# Roadmap

Roadmap items are intentions, not claims about current functionality.

## Core reliability

- [ ] Add automated tests for vault creation, unlock, save, delete, malformed files, and interrupted writes.
- [ ] Improve validation of vault envelope and note data.
- [ ] Improve save-failure behavior so in-memory state cannot silently diverge from disk.
- [ ] Review scrypt parameters and add a tested migration path before changing existing vault formats.
- [ ] Add encrypted backup/restore with validation and explicit overwrite protection.
- [ ] Choose and add an open-source license.

## Planned features

- [ ] Integrate an offline password generator using Python's \`secrets\` module.
- [ ] Add configurable length, character sets, ambiguous-character exclusion, and explicit copy-to-clipboard.
- [ ] Add Markdown and developer snippet library.
- [ ] Add quick capture and keyboard shortcuts.
- [ ] Consider optional GitHub repository references and local annotations.
- [ ] Consider an API request workbench with strict URL validation and safe defaults.

## Explicitly not in the current starter version

Cloud sync, AI integrations, continuous clipboard monitoring, arbitrary code execution, automatic repository cloning, and a full credential manager.
