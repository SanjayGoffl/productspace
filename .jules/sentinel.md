## 2024-05-21 - Insecure Domain Validation via `.endswith()`
**Vulnerability:** The `is_valid_url` method used `.endswith(domain)` to validate the netloc of a parsed URL. This mistakenly allowed domains like `badexample.com` to pass verification when `example.com` was the target allowed domain.
**Learning:** Checking subdomains or validating domains purely with string suffixes is unsafe. It leaves crawlers and other network applications open to bypassing origin or domain restrictions.
**Prevention:** When validating URLs against a list of allowed domains, ensure the parsed netloc either perfectly matches the allowed domain (`netloc == domain`) or properly matches as a subdomain by including the dot boundary (`netloc.endswith("." + domain)`).
