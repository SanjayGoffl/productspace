## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-24 - Cross-Site Scripting (XSS) in UI Elements via LLM Outputs
**Vulnerability:** XSS vulnerability was found in `index.html` where AI/LLM-generated output (like persona names, product choices, and quotes) was directly injected into the DOM via `innerHTML` without sanitization in `renderPersonaCard` and `sim-persona-tbody` population.
**Learning:** Even though the LLM's output is generated within a constrained simulation, it's structurally parsed but its string fields must still be treated as untrusted input. Directly setting HTML with unescaped fields can allow arbitrary script execution, especially if an attacker finds a way to manipulate the simulated prompt or output (e.g. prompt injection causing the LLM to output malicious payloads).
**Prevention:** Always use the natively provided `escapeHTML` function to sanitize any dynamic string data (especially those originating from LLM responses or untrusted sources) before embedding it into HTML using string interpolation for `innerHTML`.
