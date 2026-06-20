## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2023-10-27 - [High] Cross-Site Scripting (XSS) via LLM output DOM injection
**Vulnerability:** XSS vulnerability found in `index.html` where LLM-generated persona attributes (e.g., name, emoji, product_chosen, quote) and simulated summary output (e.g., winner, total) were directly injected into DOM via `innerHTML` without sanitization.
**Learning:** Parsing JSON structure from LLM output is not sufficient for security. Although the output adheres to a JSON schema, its contents (like `persona`, `quote`, `chosen_product`) may still contain arbitrary scripts which execute when rendered. Falsy/undefined checks combined with default values (e.g., `data.emoji || '👤'`) also need proper string escaping inside the sanitization function argument (e.g., `escapeHTML(data.emoji || '👤')`).
**Prevention:** Always sanitize dynamically constructed inputs. For dynamic data embedded directly in `innerHTML`, explicitly sanitize outputs with `escapeHTML()`. In explicitly numeric operations where a function demands a string type, cast to a string beforehand (`escapeHTML(String(value))`).
