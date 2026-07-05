## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-25 - [Missing escapeHTML on Persona and Market Outcome LLM renders]
**Vulnerability:** XSS vulnerability through lack of input sanitization in LLM responses and LLM derived text properties.
**Learning:** We need to sanitize LLM generated data, such as Persona details (`persona`, `emoji`, `quote`, `chosen`, `top_features`), and calculated variables based on the generated data (like `winner`) when generating dynamic HTML directly in client-side code via `innerHTML` to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an `escapeHTML` function to sanitize any third-party or LLM-generated string inputs before inserting them into `innerHTML`. Keep a close eye on any `.innerHTML` assignments in the code.
