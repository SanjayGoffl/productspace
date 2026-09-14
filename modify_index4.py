import re

with open("index.html", "r") as f:
    html = f.read()

# 1. Revert unnecessary escapeHTML for numbers in renderPersonaCard
card_innerHTML_search = r"""                <div class="prob-bar-label">
                        <span>Purchase Probability</span>
                        <span>\$\{escapeHTML\(prob\)\}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill \$\{escapeHTML\(probClass\)\}" data-width="\$\{escapeHTML\(prob\)\}" style="width:0%"></div>
                    </div>"""

card_innerHTML_replace = r"""                <div class="prob-bar-label">
                        <span>Purchase Probability</span>
                        <span>${prob}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill ${escapeHTML(probClass)}" data-width="${prob}" style="width:0%"></div>
                    </div>"""

html = re.sub(card_innerHTML_search, card_innerHTML_replace, html)

# 2. Revert unnecessary escapeHTML for numbers in renderPhase7 KPI strip
kpi_strip_search = r"""                <div class="kpi"><div class="label">Personas Simulated</div><div class="val blue">\$\{escapeHTML\(total\)\}</div></div>
                <div class="kpi"><div class="label">Market Winner</div><div class="val green" style="font-size:1\.1rem;margin-top:\.3rem">\$\{escapeHTML\(winner\)\}</div></div>
                <div class="kpi"><div class="label">Winner's Market Share</div><div class="val yellow">\$\{escapeHTML\(share\)\}%</div></div>
                <div class="kpi"><div class="label">Products Evaluated</div><div class="val purple">\$\{escapeHTML\(Object\.keys\(summary\.product_votes \|\| \{\}\)\.length\)\}</div></div>"""

kpi_strip_replace = r"""                <div class="kpi"><div class="label">Personas Simulated</div><div class="val blue">${total}</div></div>
                <div class="kpi"><div class="label">Market Winner</div><div class="val green" style="font-size:1.1rem;margin-top:.3rem">${escapeHTML(winner)}</div></div>
                <div class="kpi"><div class="label">Winner's Market Share</div><div class="val yellow">${share}%</div></div>
                <div class="kpi"><div class="label">Products Evaluated</div><div class="val purple">${Object.keys(summary.product_votes || {}).length}</div></div>"""

html = re.sub(kpi_strip_search, kpi_strip_replace, html)

# 3. Revert unnecessary escapeHTML for numbers in renderPhase7 Persona Table
persona_table_search = r"""                    <td><span class="tbl-emoji">\$\{escapeHTML\(row\.emoji \|\| '👤'\)\}</span> \$\{escapeHTML\(row\.persona\)\}</td>
                    <td>\$\{escapeHTML\(row\.chosen\)\}</td>
                    <td>\$\{escapeHTML\(prob\)\}%</td>
                    <td>\$\{label\}</td>"""

persona_table_replace = r"""                    <td><span class="tbl-emoji">${escapeHTML(row.emoji || '👤')}</span> ${escapeHTML(row.persona)}</td>
                    <td>${escapeHTML(row.chosen)}</td>
                    <td>${prob}%</td>
                    <td>${label}</td>"""

html = re.sub(persona_table_search, persona_table_replace, html)

with open("index.html", "w") as f:
    f.write(html)
