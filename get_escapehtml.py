with open("index.html") as f:
    html = f.read()

import re
match = re.search(r"function escapeHTML\(str\).*?\{.*?\}", html, re.DOTALL)
if match:
    print(match.group(0))
