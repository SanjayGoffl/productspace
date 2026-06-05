## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-05 - [XSS in renderCompetitorGrid]
**Vulnerability:** DOM-based Cross-Site Scripting (XSS) via unescaped user input in `renderCompetitorGrid`.
**Learning:** Even if data is primarily handled internally or retrieved from a seemingly safe local state list (`state.competitors`), it can originate from direct user input (like the manual competitor entry form). Failing to sanitize these fields when dynamically generating HTML strings using template literals allows script execution.
**Prevention:** Always use the established `escapeHTML` utility function when interpolating user-controlled variables into `innerHTML` strings, especially for dynamic lists/grids.
