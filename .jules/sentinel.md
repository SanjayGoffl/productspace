## 2024-05-18 - Inline JS Handler XSS Mitigation
**Vulnerability:** XSS vulnerability in `index.html` where user input was interpolated directly into `innerHTML` strings and inline JavaScript event handlers (e.g., `onclick="removeFeature('${f}')"`).
**Learning:** Basic `escapeHTML` is not sufficient for strings injected into inline JS parameters because the browser parses the HTML attributes and unescapes HTML entities *before* the JS engine executes them. This can lead to JS syntax errors or XSS bypasses.
**Prevention:** When injecting variables into inline JS string parameters within HTML strings, first safely escape JS-specific characters (like `\` and `'`), and *then* run `escapeHTML`.
