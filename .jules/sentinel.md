## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-15 - [XSS via Unsanitized LLM JSON Output in `innerHTML`]
**Vulnerability:** XSS vulnerability through direct `innerHTML` injection of fields parsed from LLM JSON output.
**Learning:** Even if data comes from an LLM and is correctly structured as JSON, its text fields (like names, quotes, emojis, or dynamically generated IDs) must still be treated as untrusted user input. Using them directly in `innerHTML` templates without sanitization allows for DOM injection and cross-site scripting (XSS).
**Prevention:** Always wrap variables interpolated into `innerHTML` strings with a sanitization function like `escapeHTML`. Default fallbacks should be applied within the sanitization function (e.g., `escapeHTML(data.field || 'default')`) to ensure null/undefined cases do not bypass sanitization logic.
