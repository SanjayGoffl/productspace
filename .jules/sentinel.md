## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-09-07 - [XSS Vulnerability in renderCompetitorGrid]
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability in `renderCompetitorGrid()` when rendering competitor data (name, domain, price).
**Learning:** Even if `escapeHTML` is defined, failing to apply it to all dynamically injected fields (especially text fields that could contain LLM-generated payloads) creates XSS risks.
**Prevention:** Ensure all dynamically rendered fields from external or generated sources are wrapped in `escapeHTML()` before insertion via `innerHTML`.
