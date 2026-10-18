# Contributing

Thanks for your interest in PHANTOM Knowledge Vault.

## Before opening a change

1. Check existing issues and the roadmap to avoid duplicate work.
2. Keep changes small and explain the problem they solve.
3. Never submit passwords, real vault files, API tokens, private keys, or other personal data.
4. Do not claim security improvements without explaining the threat addressed and adding tests where practical.
5. Avoid adding network calls, telemetry, auto-execution, or automatic clipboard monitoring to the offline core.

## Development setup

~~~powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py
~~~

## Pull request checklist

- [ ] Explain the motivation and user-visible impact.
- [ ] Add or update tests for changed behavior.
- [ ] Run the test suite and report the result.
- [ ] Update documentation and CHANGELOG.md where appropriate.
- [ ] Check that no secrets, generated vaults, build outputs, or local environment files are included.
- [ ] For security-sensitive changes, describe assumptions, limitations, and migration behavior.

A license has not yet been selected. Clarify licensing before accepting external contributions.
