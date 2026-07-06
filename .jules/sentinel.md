## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## $(date +%Y-%m-%d) - XSS Vulnerability in index.html innerHTML assignment
**Vulnerability:** Untrusted user input (product names, descriptions, competitor URLs, AI persona traits, generated quotes) was being dynamically assigned to the DOM via `.innerHTML` string templates without sanitization.
**Learning:** Even though the frontend uses vanilla JS (without a package manager like npm), the same secure coding practices apply. Fields injected directly into HTML markup via `innerHTML` must be properly escaped. There is a helper function `escapeHTML` defined at the top of the file, but it was not being utilized when rendering elements such as `c.name`, `f.category`, `data.persona`, etc. In cases where the JS strings had to be injected into inline JS handlers, `escapeHTML(escapeJSString(val))` is needed. Furthermore, a default fallback (e.g., `data.emoji || '👤'`) must be evaluated *before* passing to `escapeHTML` to prevent unexpected `undefined`/null evaluations or crashes.
**Prevention:** Always use `escapeHTML()` to sanitize dynamic inputs before injecting them into `.innerHTML`. Avoid using `.innerHTML` when setting text values directly, and instead prefer `.textContent`. When dynamic strings are used in inline event handlers, combine `escapeHTML` and `escapeJSString`. Review template literals that render dynamic fields.
