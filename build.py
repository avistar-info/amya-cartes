"""Génère les fiches contact, les vCards et les QR codes à partir de contacts.json.

Usage : python3 build.py   (nécessite : pip install segno)
"""
import html
import json
from pathlib import Path

import segno

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "contacts.json").read_text(encoding="utf-8"))
ORG = DATA["entreprise"]
SITE = DATA["site"]
BASE = DATA["base_url"].rstrip("/")

ICONS = {
    "message": '<path d="M12 3C6.5 3 2 6.6 2 11c0 2.4 1.3 4.6 3.4 6-.2 1.3-.9 2.6-1.9 3.6 2-.1 3.9-.8 5.3-2 1 .3 2.1.4 3.2.4 5.5 0 10-3.6 10-8s-4.5-8-10-8z"/>',
    "appeler": '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/>',
    "e-mail": '<path d="M3 5h18c.6 0 1 .4 1 1v12c0 .6-.4 1-1 1H3c-.6 0-1-.4-1-1V6c0-.6.4-1 1-1zm9 7.2L4.2 7v.1L12 13l7.8-5.9V7L12 12.2z"/>',
    "site": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.9a15.7 15.7 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h2.9c.3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zM8 8H5.1a8 8 0 0 1 4.3-3.6C8.8 5.5 8.3 6.7 8 8zm4 12c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h2.9a8 8 0 0 1-4.3 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z"/>',
}

CSS = """
:root{--bg:#f2f2f7;--card:#fff;--txt:#000;--sub:#6c6c70;--sep:#c6c6c8;--blue:#007aff;--av1:#a6abb6;--av2:#868b96}
@media (prefers-color-scheme:dark){:root{--bg:#000;--card:#1c1c1e;--txt:#fff;--sub:#8e8e93;--sep:#38383a;--blue:#0a84ff;--av1:#7d828c;--av2:#5f636b}}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--txt);font:17px/1.3 -apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;min-height:100vh}
main{max-width:440px;margin:0 auto;padding:28px 16px 40px}
a{color:inherit;text-decoration:none}
.brand{text-align:center;font-size:12px;font-weight:600;letter-spacing:.32em;color:var(--sub);margin-bottom:28px}
.head{text-align:center}
.avatar{width:112px;height:112px;border-radius:50%;margin:0 auto 14px;display:grid;place-items:center;background:linear-gradient(180deg,var(--av1),var(--av2));color:#fff;font-size:44px;font-weight:500;letter-spacing:.02em}
h1{font-size:28px;font-weight:600;letter-spacing:-.01em}
.org{color:var(--sub);font-size:15px;margin-top:4px}
.actions{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:8px;margin:24px 0}
.act{background:var(--card);border-radius:12px;padding:10px 4px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--blue);font-size:11px;font-weight:500}
.act svg{width:24px;height:24px;fill:currentColor}
.act:active,.row:active{opacity:.55}
.group{background:var(--card);border-radius:12px;overflow:hidden}
.row{display:block;padding:11px 16px;position:relative}
.row+.row::before{content:"";position:absolute;top:0;left:16px;right:0;border-top:.5px solid var(--sep)}
.lbl{font-size:13px;color:var(--txt)}
.val{color:var(--blue);word-break:break-all}
.cta{display:block;margin-top:24px;background:var(--blue);color:#fff;text-align:center;font-weight:600;padding:15px;border-radius:14px}
.cta:active{opacity:.8}
.foot{text-align:center;color:var(--sub);font-size:12px;margin-top:28px}
.list .row{display:flex;align-items:center;gap:12px;padding:10px 16px}
.list .row+.row::before{left:72px}
.mini{width:44px;height:44px;font-size:17px;margin:0;flex:none}
.list .name{flex:1;font-weight:500}
.chev{color:var(--sep);font-size:22px}
"""


def esc(s):
    return html.escape(s, quote=True)


def full_name(c):
    return f'{c["prenom"]} {c["nom"]}'


def initials(c):
    return (c["prenom"][:1] + c["nom"][:1]).upper()


def fmt_tel(tel):
    # +33695047223 -> +33 6 95 04 72 23
    if tel.startswith("+33") and len(tel) == 12:
        d = tel[3:]
        return "+33 " + d[0] + " " + " ".join(d[i:i + 2] for i in range(1, 9, 2))
    return tel


def site_label():
    return SITE.split("//", 1)[-1].rstrip("/")


def vcard(c):
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f'N:{c["nom"]};{c["prenom"]};;;',
        f"FN:{full_name(c)}",
        f"ORG:{ORG}",
    ]
    if c["poste"]:
        lines.append(f'TITLE:{c["poste"]}')
    if c["tel"]:
        lines.append(f'TEL;TYPE=CELL,VOICE:{c["tel"]}')
    if c["email"]:
        lines.append(f'EMAIL;TYPE=INTERNET,WORK:{c["email"]}')
    if SITE:
        lines.append(f"URL:{SITE}")
    lines.append("END:VCARD")
    return "\r\n".join(lines) + "\r\n"


def page(title, body, desc):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f2f2f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta name="robots" content="noindex">
<meta name="description" content="{esc(desc)}">
<title>{esc(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def contact_page(c):
    name = full_name(c)
    actions, rows = [], []
    if c["tel"]:
        actions.append(("message", f'sms:{c["tel"]}', ""))
        actions.append(("appeler", f'tel:{c["tel"]}', ""))
        rows.append(("mobile", f'tel:{c["tel"]}', fmt_tel(c["tel"]), ""))
    if c["email"]:
        actions.append(("e-mail", f'mailto:{c["email"]}', ""))
        rows.append(("e-mail", f'mailto:{c["email"]}', c["email"], ""))
    if SITE:
        ext = ' target="_blank" rel="noopener"'
        actions.append(("site", SITE, ext))
        rows.append(("site web", SITE, site_label(), ext))

    acts = "".join(
        f'<a class="act" href="{esc(href)}"{extra}><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg>{k}</a>'
        for k, href, extra in actions
    )
    lst = "".join(
        f'<a class="row" href="{esc(href)}"{extra}><div class="lbl">{lbl}</div><div class="val">{esc(val)}</div></a>'
        for lbl, href, val, extra in rows
    )
    poste = f'{esc(c["poste"])} · ' if c["poste"] else ""
    body = f"""<div class="brand">{esc(ORG.upper())}</div>
<div class="head">
  <div class="avatar" aria-hidden="true">{initials(c)}</div>
  <h1>{esc(name)}</h1>
  <div class="org">{poste}{esc(ORG)}</div>
</div>
<nav class="actions" style="--n:{len(actions)}">{acts}</nav>
<div class="group">{lst}</div>
<a class="cta" href="{c["slug"]}.vcf">Ajouter aux contacts</a>
<div class="foot">{esc(ORG)}</div>"""
    return page(f"{name} · {ORG}", body, f"Fiche contact de {name}, {ORG}")


def team_page():
    rows = "".join(
        f'<a class="row" href="{c["slug"]}/"><div class="avatar mini" aria-hidden="true">{initials(c)}</div>'
        f'<span class="name">{esc(full_name(c))}</span><span class="chev">›</span></a>'
        for c in DATA["contacts"]
    )
    site = (
        f'<a class="cta" href="{esc(SITE)}" target="_blank" rel="noopener">Visiter {esc(site_label())}</a>'
        if SITE else ""
    )
    body = f"""<div class="brand">{esc(ORG.upper())}</div>
<div class="head" style="margin-bottom:24px"><h1>Notre équipe</h1><div class="org">Touchez un nom pour enregistrer le contact</div></div>
<div class="group list">{rows}</div>
{site}
<div class="foot">{esc(ORG)}</div>"""
    return page(f"Équipe · {ORG}", body, f"Contacts de l'équipe {ORG}")


def qr(url, name, label):
    q = segno.make(url, error="m")
    q.save(ROOT / "qr" / f"{name}.svg", scale=10, border=4)
    q.save(ROOT / "qr" / f"{name}.png", scale=24, border=4)
    return f'<figure><img src="{name}.svg" alt=""><figcaption>{esc(label)}</figcaption></figure>'


def main():
    (ROOT / "qr").mkdir(exist_ok=True)
    (ROOT / ".nojekyll").write_text("")
    figs = []
    for c in DATA["contacts"]:
        d = ROOT / c["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(contact_page(c), encoding="utf-8")
        (d / f'{c["slug"]}.vcf').write_bytes(vcard(c).encode("utf-8"))
        figs.append(qr(f'{BASE}/{c["slug"]}/', c["slug"], full_name(c)))
    (ROOT / "index.html").write_text(team_page(), encoding="utf-8")
    figs.append(qr(f"{BASE}/", "equipe", f"Équipe {ORG}"))

    # Planche imprimable avec tous les QR codes
    (ROOT / "qr" / "planche.html").write_text(f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>QR codes · {esc(ORG)}</title>
<style>
@page{{size:A4;margin:12mm}}
body{{font:14px -apple-system,Helvetica,Arial,sans-serif;margin:0;padding:12mm;color:#000;background:#fff}}
h1{{font-size:16px;letter-spacing:.3em;text-align:center;margin:0 0 10mm}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10mm}}
figure{{margin:0;text-align:center;break-inside:avoid}}
img{{width:100%;max-width:55mm}}
figcaption{{margin-top:2mm;font-weight:600}}
</style></head><body>
<h1>{esc(ORG.upper())}</h1>
<div class="grid">{"".join(figs)}</div>
</body></html>
""", encoding="utf-8")
    print(f"OK : {len(DATA['contacts'])} fiches + page équipe + QR codes générés.")


if __name__ == "__main__":
    main()
