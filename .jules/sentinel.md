## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-24 - Fix XSS Vulnerability in persona simulation output
**Vulnerability:** XSS vulnerability in `index.html` where LLM-generated simulation outputs (like quotes, names, and chosen products) were directly injected into the DOM via `innerHTML` without escaping.
**Learning:** Even though the LLM output comes as a structured JSON object, the individual fields must still be considered untrusted data as LLMs can hallucinate malicious scripts or act as vectors for prompt injection attacks.
**Prevention:** Always use `escapeHTML` for any dynamically generated content from LLMs (or users) before assigning to `innerHTML`. Also remember that default fallbacks (e.g. `data.emoji || '👤'`) should be placed inside the `escapeHTML` call so that missing values don't bypass sanitization.
