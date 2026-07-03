## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-28 - XSS in dynamic HTML rendering with default values
**Vulnerability:** XSS vulnerability when directly assigning LLM JSON outputs or user inputs to `innerHTML` blocks in `index.html`.
**Learning:** LLM JSON output structure guarantees schema but does not sanitize content. Therefore, it's prone to script injections if inserted directly into DOM via `innerHTML`. When using the custom `escapeHTML` function to sanitize data with a default fallback, the fallback must be applied inside the function argument (e.g., `escapeHTML(data.emoji || '👤')`) rather than chaining it outside, to explicitly handle null/undefined inputs before escaping.
**Prevention:** Always use `escapeHTML` for dynamic strings inserted into the DOM. For strings used as dynamic attributes inside inline JavaScript events like `onclick`, use `escapeHTML(escapeJSString(data))` for complete security. Ensure fallbacks occur inside the `escapeHTML` invocation.
