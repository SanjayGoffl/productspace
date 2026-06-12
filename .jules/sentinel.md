## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2026-06-12 - [XSS Fix Fallback Pattern]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** When using the custom escapeHTML function to sanitize data with a default fallback, apply the fallback inside the function argument (e.g., escapeHTML(data || 'default')) rather than chaining it outside, to explicitly handle null/undefined inputs before escaping and prevent TypeErrors.
**Prevention:** Use the pattern `escapeHTML(var || 'fallback')` instead of `escapeHTML(var) || 'fallback'`.
