# Changelog

This project is in early development. Changes are listed in reverse chronological order.

## Unreleased

- Added a built-in offline password generator using Python's \`secrets\` module.
- Added configurable length and character sets, optional ambiguous-character exclusion, and explicit copy-to-clipboard.
- Improved vault envelope validation and file replacement behavior.
- Added protection against overwriting a vault that changed externally while the app was open.
- Avoided committing note changes to in-memory state when saving fails.
- Added initial unit tests and a Windows GitHub Actions workflow.
- Added security, contribution, architecture, threat-model, and roadmap documentation.
