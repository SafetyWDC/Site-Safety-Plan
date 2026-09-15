# -*- coding: utf-8 -*-
"""Builds the static GitHub Pages site for SafetyWDC/Site-Safety-Plan:
index.html (landing) + 1600.html + 1825.html (essentials + sign-off).

Reuses the same site data as the short 7-page plan
(../wdc-safety-plan/sites/*.json, ../wdc-safety-plan/people.json) so the
essentials shown here never drift from the approved short plan.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "wdc-safety-plan")

PEOPLE = json.load(open(os.path.join(DATA_DIR, "people.json"), encoding="utf8"))
SITES = {
    "1600": json.load(open(os.path.join(DATA_DIR, "sites", "1600.json"), encoding="utf8")),
    "1825": json.load(open(os.path.join(DATA_DIR, "sites", "1825.json"), encoding="utf8")),
}

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScaPhwGZ3eeZgW3zS566Qg2x_iJBbOGGAU_AYMQ6uXIuafbXQ/viewform"
REV = "September 15, 2026"

STYLE = """
:root{--blue:#003D52;--green:#96C61C;--grey:#A5A5A5;--dgrey:#444444;--line:#E4E4E4}
*{box-sizing:border-box}
body{margin:0;font-family:'Raleway',sans-serif;color:#1a1a1a;background:#ffffff;
  line-height:1.5;padding-bottom:48px}
.wrap{max-width:640px;margin:0 auto;padding:20px 20px 8px}
.brand{font-size:12px;font-weight:700;color:var(--blue);letter-spacing:.04em;margin:0}
h1{font-size:26px;font-weight:800;color:var(--blue);margin:2px 0 4px;line-height:1.15}
.sub{font-size:14px;color:var(--dgrey);margin:0 0 16px}
.rule{border:none;border-top:2px solid var(--green);margin:14px 0 18px}
h2{font-size:16px;font-weight:800;color:var(--blue);margin:22px 0 8px}
p{font-size:14.5px;margin:0 0 10px}
ul{margin:0 0 10px;padding-left:20px}
li{font-size:14.5px;margin-bottom:6px}
.card{border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.card b{color:var(--blue)}
.btn{display:block;text-align:center;text-decoration:none;font-weight:700;
  font-size:15px;padding:14px 18px;border-radius:10px;margin:10px 0}
.btn-primary{background:var(--blue);color:#fff}
.btn-sign{background:var(--green);color:#0d1a02}
.btn-outline{background:#fff;color:var(--blue);border:2px solid var(--blue)}
.tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--blue);
  border-radius:5px;padding:2px 8px;margin-bottom:10px}
.tag.grey{background:var(--grey);color:#222}
.footer{max-width:640px;margin:24px auto 0;padding:0 20px;font-size:11.5px;color:var(--grey)}
.back{display:inline-block;margin-bottom:14px;font-size:13px;color:var(--blue);text-decoration:none;font-weight:700}
.sitegrid{display:flex;flex-direction:column;gap:14px;margin-top:10px}
.sitecard{display:block;text-decoration:none;border:1px solid var(--line);border-radius:12px;
  padding:18px 18px;color:#1a1a1a}
.sitecard .name{font-size:19px;font-weight:800;color:var(--blue)}
.sitecard .addr{font-size:13px;color:var(--dgrey);margin-top:2px}
.sign-box{border:2px solid var(--blue);border-radius:12px;padding:16px 18px;margin:26px 0 6px}
.sign-box h2{margin-top:0}
"""

HEAD = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{style}</style>
</head><body>
"""

TAIL = "</body></html>"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_index():
    body = HEAD.format(title="WDC Site Safety Plan", style=STYLE)
    body += """
<div class="wrap">
  <p class="brand">WDC</p>
  <h1>Site Specific Safety Plan</h1>
  <p class="sub">Whistler 2020 Development Corporation</p>
  <hr class="rule">
  <p>Pick your site to read the plan and sign off.</p>
  <div class="sitegrid">
    <a class="sitecard" href="1600.html">
      <div class="name">Site 1600</div>
      <div class="addr">1600 Mount Fee Road, Whistler, BC</div>
    </a>
    <a class="sitecard" href="1825.html">
      <div class="name">Site 1825</div>
      <div class="addr">1825 Mount Fee Road (Lot 6), Whistler, BC</div>
    </a>
  </div>
</div>
<div class="footer">Prepared by: Safety WDC &mdash; Rev. """ + REV + """</div>
"""
    body += TAIL
    return body


def build_site_page(key):
    S = SITES[key]
    other = "1825" if key == "1600" else "1600"
    cso, supt, fa3 = PEOPLE["cso"], PEOPLE["supt"], PEOPLE["fa3"]
    hospital = PEOPLE["hospital"]

    built_html = "".join("<li>%s</li>" % esc(b) for b in S["built"])
    hazards_html = "".join(
        '<div class="card"><b>%s</b><br>%s</div>' % (esc(h[0]), esc(h[1]))
        for h in S["hazards"]
    )

    body = HEAD.format(title="Site %s Safety Plan — WDC" % key, style=STYLE)
    body += """
<div class="wrap">
  <a class="back" href="index.html">&larr; Both sites</a>
  <p class="brand">WDC</p>
  <span class="tag%s">Site %s</span>
  <h1>Site Safety Plan — the essentials</h1>
  <p class="sub">%s</p>
  <hr class="rule">

  <h2>What is on this site</h2>
  <ul>%s</ul>

  <h2>Muster point, first aid, extinguishers</h2>
  <p><b>Muster point:</b> %s</p>
  <p><b>First aid:</b> %s</p>
  <p><b>Fire extinguishers:</b> %s</p>

  <h2>Hazards and what we do</h2>
  %s

  <h2>Contacts</h2>
  <p><b>%s</b> &mdash; %s &mdash; %s</p>
  <p><b>%s</b> &mdash; %s &mdash; %s</p>
  <p><b>%s</b> &mdash; %s &mdash; %s</p>
  <p><b>Nearest hospital:</b> %s, %s &mdash; %s</p>

  <hr class="rule">
  <a class="btn btn-outline" href="plans/WDC_Site_Specific_Safety_Plan_%s.pdf" target="_blank" rel="noopener">Read the full Site Specific Safety Plan (PDF)</a>

  <div class="sign-box">
    <h2>Sign off</h2>
    <p>By signing, you confirm that you have read this page and understand
    the hazards and rules for Site %s.</p>
    <a class="btn btn-sign" href="%s" target="_blank" rel="noopener">I have read and understood &mdash; Sign</a>
  </div>
</div>
<div class="footer">Prepared by: Safety WDC &mdash; Rev. %s</div>
""" % (
        " grey" if S.get("sticker") == "grey" else "", key, S["address"],
        built_html,
        esc(S["muster"]), esc(S["firstaid"]), esc(S["extinguishers"]),
        hazards_html,
        esc(cso[0]), esc(cso[1]), esc(cso[2]),
        esc(supt[0]), esc(supt[1]), esc(supt[2]),
        esc(fa3[0]), esc(fa3[1]), esc(fa3[2]),
        esc(hospital[0]), esc(hospital[1]), esc(hospital[2]),
        key, key, FORM_URL, REV,
    )
    body += TAIL
    return body


if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w", encoding="utf8").write(build_index())
    open(os.path.join(HERE, "1600.html"), "w", encoding="utf8").write(build_site_page("1600"))
    open(os.path.join(HERE, "1825.html"), "w", encoding="utf8").write(build_site_page("1825"))
    print("built: index.html, 1600.html, 1825.html")
