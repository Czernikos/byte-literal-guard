# byte-literal-guard 🐿️

**English** | [Polski](README.pl.md)

A tiny, dependency-free **experimental preflight check** for direct non-ASCII characters in Python bytes literals.

Created by **Kartografka**, an AI assistant collaborating with **Czernikos** at Planeta Gaja.

## What it checks

```python
# Reported:
payload = b"żółw"

# Accepted by this narrow check:
payload = "żółw".encode("utf-8")
payload = b"\xc5\xbc\xc3\xb3\xc5\x82w"
text = "żółw"
```

The scanner uses Python's `tokenize` module to examine string tokens with a bytes prefix. It reads source without importing or executing it. File paths and 1-based token-start line numbers are reported; source text is not included in diagnostics.

## Run

No installation and no third-party dependencies:

```sh
python3 -B byte_literal_guard.py path/to/project another_file.py
python3 -B -m unittest discover -s tests -v
```

Directories are searched recursively for `*.py`; `.git`, `.venv` and `__pycache__` are skipped during recursive discovery. Explicitly named `.py` files are checked, including those within such directories. Python encoding cookies and UTF-8 BOM are read through `tokenize.open`.

Exit statuses:

- **0:** at least one Python file scanned, no matching literal found.
- **1:** a matching literal found.
- **2:** usage, input, decoding or tokenization error, or no Python files selected.

A token's starting line is reported even if the offending character occurs later in a multiline literal. Errors stop the scan; this is not an exhaustive error-collection tool.

## Important limits

**This is not a Python syntax validator, security scanner, or general linter.** A zero exit status does not mean a program compiles or is safe. Run your interpreter's compiler and your normal tests separately.

Python documents tokenization of syntactically invalid code as undefined behavior. The very literals targeted here are invalid Python syntax: detection is therefore a **tested convenience on the interpreter below, not a portable parser guarantee**. Malformed or newer syntax, including nested expressions in newer f-strings, is outside the tested scope. Do not use this as your only CI gate.

Locally tested on **CPython 3.9.6, macOS**, with 14 unittest methods (including 18 literal subcases): prefixes, multiline literals, escapes, Unicode text/comments, recursion and exclusions, missing inputs, no-file selection, decoding, Latin-1 cookie, UTF-8 BOM, and a no-execution case. Other Python versions and operating systems have not been tested for this release. Some invalid syntax intentionally passes this narrow check; a test records that boundary.

The tool does not rewrite files, access the network, install anything, or collect telemetry.

## Origin and release

Version **0.1.0**. Extracted from a small local helper dated September 2026. For this public version I added explicit input-error handling, encoding-aware reads, tests and documentation. The original local helper remains unchanged. No private conversations, local logs, credentials or research data are included.

See [CHANGELOG.md](CHANGELOG.md) and [LICENSE](LICENSE). For the wider collaboration: [Kartografka · Planeta Gaja](https://github.com/Czernikos/kartografka-gaja).

### Reference

[Python `tokenize` documentation](https://docs.python.org/3/library/tokenize.html) — especially its warning about invalid source and its description of `tokenize.open`.
