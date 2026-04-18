## 2024-04-18 - XSS Vulnerability in innerHTML with inline handlers

**Vulnerability:** XSS vulnerability found in `index.html` where user input and LLM responses are injected into the DOM using `innerHTML` without sanitization. Specifically, the `renderChips` function injects user-provided product features, and `appendChatMsg` injects LLM chat responses.

**Learning:** When using `innerHTML`, any unsanitized user or external input can lead to XSS. A particularly tricky edge case is when input is injected both as text content AND as part of an inline event handler (like `onclick="removeFeature('${f}')"`). The browser parses HTML entities *before* evaluating JavaScript in an event handler. This means standard HTML escaping (`escapeHTML(val)`) inside an inline JS handler is insufficient and can lead to XSS if the value contains quotes or JS payloads that are evaluated.

**Prevention:**
1. Always sanitize any external/user input before rendering via `innerHTML` using an `escapeHTML` function.
2. For inline event handlers (which are an anti-pattern but exist in legacy/plain JS codebases), values must be **double-escaped**: first escaped for JS strings, then escaped for HTML. E.g., `escapeHTML(escapeJSString(val))`.
3. Prefer using `textContent` or `document.createElement` over `innerHTML` where possible to avoid these complexities entirely.
