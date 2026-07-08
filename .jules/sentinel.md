## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-06-25 - XSS in client-side HTML generation
**Vulnerability:** Unsanitized variables concatenated directly into `innerHTML` strings in functions like `renderCompetitorGrid`, `renderPersonaCard`, and `renderPhase7`.
**Learning:** Relying purely on expected JSON structures from LLMs is not sufficient for frontend security, as outputs can contain script payloads. Explicitly escaping variables in UI rendering is mandatory.
**Prevention:** Always use `escapeHTML()` when injecting dynamic variables derived from user input or LLM responses into HTML template strings.
