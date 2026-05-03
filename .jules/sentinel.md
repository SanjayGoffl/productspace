## 2024-05-03 - Prevent XSS in index.html
**Vulnerability:** Found multiple XSS vulnerabilities where user-controlled text and API responses were injected into the DOM via `.innerHTML` without escaping.
**Learning:** `index.html` lacked built-in escaping functions, and directly injected things like product features and API error responses into DOM string templates. Also, escaping strings meant for inline JS attributes like `onclick` require two layers of escaping (JavaScript escaping and then HTML escaping) to prevent breakout attacks.
**Prevention:** Implement and consistently use `escapeHTML(String(data))` for all text interpolation, and `escapeHTML(escapeJSString(data))` for strings within inline HTML event handlers.
