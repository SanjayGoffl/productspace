## 2025-05-31 - Fix XSS Vulnerabilities in ProductScope

**Vulnerability:** User-provided inputs, such as competitor name, domain, product name, and simulated chat contents were being directly interpolated into `innerHTML` statements without sanitation, making the application susceptible to Cross-Site Scripting (XSS).

**Learning:** This codebase lacked structured HTML sanitization in its dynamic string templates causing direct DOM updates to be vulnerable. It already had a `escapeHTML` helper function, but it was being under-utilized.

**Prevention:** All user-provided inputs and responses dynamically inserted into HTML templates, particularly with `innerHTML` usage, should be wrapped using the `escapeHTML` function to safely render entities instead of raw script tags.
