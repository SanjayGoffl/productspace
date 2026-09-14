with open("index.html", "r") as f:
    html = f.read()

card_search = """                <div class="prob-bar-label">
                        <span>Purchase Probability</span>
                        <span>${escapeHTML(prob)}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill ${escapeHTML(probClass)}" data-width="${escapeHTML(prob)}" style="width:0%"></div>
                    </div>"""
card_replace = """                <div class="prob-bar-label">
                        <span>Purchase Probability</span>
                        <span>${prob}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill ${probClass}" data-width="${prob}" style="width:0%"></div>
                    </div>"""

html = html.replace(card_search, card_replace)

kpi_search = """                <div class="kpi"><div class="label">Personas Simulated</div><div class="val blue">${escapeHTML(total)}</div></div>
                <div class="kpi"><div class="label">Market Winner</div><div class="val green" style="font-size:1.1rem;margin-top:.3rem">${escapeHTML(winner)}</div></div>
                <div class="kpi"><div class="label">Winner's Market Share</div><div class="val yellow">${escapeHTML(share)}%</div></div>
                <div class="kpi"><div class="label">Products Evaluated</div><div class="val purple">${escapeHTML(Object.keys(summary.product_votes || {}).length)}</div></div>"""
kpi_replace = """                <div class="kpi"><div class="label">Personas Simulated</div><div class="val blue">${total}</div></div>
                <div class="kpi"><div class="label">Market Winner</div><div class="val green" style="font-size:1.1rem;margin-top:.3rem">${escapeHTML(winner)}</div></div>
                <div class="kpi"><div class="label">Winner's Market Share</div><div class="val yellow">${share}%</div></div>
                <div class="kpi"><div class="label">Products Evaluated</div><div class="val purple">${Object.keys(summary.product_votes || {}).length}</div></div>"""

html = html.replace(kpi_search, kpi_replace)

table_search = """                    <td><span class="tbl-emoji">${escapeHTML(row.emoji || '👤')}</span> ${escapeHTML(row.persona)}</td>
                    <td>${escapeHTML(row.chosen)}</td>
                    <td>${escapeHTML(prob)}%</td>
                    <td>${label}</td>"""
table_replace = """                    <td><span class="tbl-emoji">${escapeHTML(row.emoji || '👤')}</span> ${escapeHTML(row.persona)}</td>
                    <td>${escapeHTML(row.chosen)}</td>
                    <td>${prob}%</td>
                    <td>${label}</td>"""

html = html.replace(table_search, table_replace)

with open("index.html", "w") as f:
    f.write(html)
