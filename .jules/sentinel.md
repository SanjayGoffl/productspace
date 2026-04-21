## 2025-02-14 - Fix DOM-based XSS in index.html
**Vulnerability:** DOM-based XSS where string interpolation from LLMs and user inputs was directly passed to `innerHTML` without sanitization.
**Learning:** `innerHTML` allows arbitrary HTML execution, which leaves dynamically generated templates vulnerable to script injection. When rendering inline JS handlers (like `onclick="func('...')"`), simply escaping HTML is insufficient as attributes will be parsed, executing any JS string breakouts.
**Prevention:** Use `escapeHTML` for textual node insertions and always double escape with `escapeHTML(escapeJSString(val))` when embedding variables within an inline JS event handler attribute.
