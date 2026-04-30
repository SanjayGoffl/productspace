## 2026-04-30 - XSS in innerHTML Rendering
**Vulnerability:** XSS vulnerability through unsafe `innerHTML` assignments rendering user input without sanitization.
**Learning:** The frontend dashboard directly interpolates unsanitized `state` variables (e.g., product features, competitor names, user inputs in chat) into HTML strings, leaving it open to script injection from externally fetched APIs (like scraped competitor data) and user forms.
**Prevention:** Must ensure utility functions like `escapeHTML` and `escapeJSString` are utilized correctly before setting DOM properties like `innerHTML` or creating elements via string interpolation.
