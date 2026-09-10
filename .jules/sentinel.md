## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2025-02-28 - [Missing escapeHTML function usage in dynamically built views]
**Vulnerability:** XSS vulnerability through lack of input sanitization in DOM rendering functions (e.g. `renderCompetitorGrid`, `renderPersonaCard`, `renderPhase7`) where object properties are directly interpolated into string literals and then assigned to `innerHTML`.
**Learning:** We need to explicitly sanitize string values extracted from state or external data sources (including properties in JSON blobs and LLM responses) using `escapeHTML` when appending them via string interpolation into the DOM.
**Prevention:** Review DOM-mutating functions for direct variable interpolation, and consistently wrap values using the provided `escapeHTML` function before inserting them via `innerHTML`.
