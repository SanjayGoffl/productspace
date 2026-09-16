## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2025-02-24 - XSS in dynamic DOM element attributes
**Vulnerability:** XSS vulnerability in multiple `index.html` functions (`renderCompetitorGrid`, `renderPersonaCard`, `renderPhase7`) where unsanitized dynamic user input (e.g., product names, competitor domains, emojis) was directly injected into template literal HTML strings setting `innerHTML`.
**Learning:** Even internal mock/simulation data flows or AI-generated inputs can present an XSS risk when directly appended to the DOM via string interpolation, and reliance purely on JSON structure parsing doesn't provide injection safety.
**Prevention:** Always use the custom `escapeHTML` function available to sanitize string variables injected into `innerHTML` HTML templates, handling potential undefined/null with fallbacks inside the function argument.
