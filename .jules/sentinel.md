## 2026-04-29 - [XSS Fix using escapeHTML and escapeJSString]
**Vulnerability:** XSS vulnerability found in inline JS rendering.
**Learning:** Browser decodes HTML entities before JS string execution in inline onclick handlers. Single `escapeHTML` is insufficient. Double escape `escapeHTML(escapeJSString(val))` is required when interpolating text inside inline JS strings using backticks.
**Prevention:** Apply escapeHTML directly to DOM values rendered with `innerHTML` and always combine `escapeJSString` and `escapeHTML` when generating inline JS attributes.
