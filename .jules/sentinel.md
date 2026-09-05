## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2024-03-24 - [Fix XSS in Dynamic Rendering]
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability due to direct `innerHTML` assignment of untrusted data in competitor and persona views.
**Learning:** Even internal mock data or LLM responses cannot be trusted blindly. When using `innerHTML`, explicitly non-string types like numbers (e.g., `prob`) can be safely passed to `escapeHTML` if the function casts inputs via `String()`.
**Prevention:** Consistently apply `escapeHTML` to all dynamic variables within template literals assigned to `innerHTML`.
