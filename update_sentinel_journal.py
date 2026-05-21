import os
import datetime

journal_dir = ".jules"
journal_file = os.path.join(journal_dir, "sentinel.md")

if not os.path.exists(journal_dir):
    os.makedirs(journal_dir)

today = datetime.date.today().isoformat()

entry = f"""
## {today} - Cross-Site Scripting (XSS) Vulnerability in `index.html`

**Vulnerability:** Found widespread use of `innerHTML` assignments injecting unescaped user-provided and LLM-generated strings directly into the DOM across various phases (features, competitors, matrix, chat history, etc.).

**Learning:** The application heavily relies on dynamic DOM updates via string interpolation into `innerHTML`, but lacked centralized or local HTML escaping mechanisms, leading to potential arbitrary JavaScript execution if malicious input were processed.

**Prevention:** To avoid this next time, always enforce robust escaping on strings prior to using `innerHTML`. Global utility functions like `escapeHTML` and `escapeJSString` should be used consistently. For inline event handlers, double-escaping (`escapeHTML(escapeJSString(val))`) is necessary to prevent breakout from quotes and HTML tags.
"""

with open(journal_file, "a") as f:
    f.write(entry + "\n")

print("Sentinel journal updated.")
