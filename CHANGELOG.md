# Changelog

## 0.1.0 — 2026-10-15

- First public extraction of the local byte-literal helper.
- Preserve the narrow token-based detection, with its invalid-source portability caveat.
- Read Python encoding cookies and UTF-8 BOM through `tokenize.open`.
- Report missing paths, unreadable input and empty selections as errors rather than a misleading PASS.
- Add 14 unittest methods and explicit scope/exit-status documentation.
- Original private-workspace helper left untouched.
