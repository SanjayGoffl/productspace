## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-05-18 - [Missing Sanitization on innerHTML Interpolations]
**Vulnerability:** XSS vulnerability through lack of input sanitization in DOM rendering functions (`renderCompetitorGrid`, `renderHistoryDrawer`, `renderChatCtxList`).
**Learning:** Using template literals to inject dynamic data directly into `innerHTML` is inherently unsafe and leads to XSS if the data (like `c.name`, `s.product.name`, etc.) contains malicious code. Furthermore, data injected into inline JavaScript event handlers (like `onclick`) must be specially escaped for JavaScript string context.
**Prevention:** Always use the codebase's specific `escapeHTML()` function when injecting dynamic data into `innerHTML`. When the data is inside an inline event handler, use `escapeHTML(escapeJSString(val))` to properly sanitize the string for both JS and HTML contexts.
