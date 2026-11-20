"""Click every sidebar link and check it scrolls to its heading without leaving the page.
Works on the live molab link (notebook inside the marimo.app iframe) or a local html-wasm build.
usage: nav_check.py URL [--fake-base]   (--fake-base adds a <base> tag like molab's, for local builds)"""
import os
import sys
import time

from playwright.sync_api import sync_playwright

URL = sys.argv[1]
EXE = os.environ.get("CHROMIUM_PATH")
fails = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.goto(URL)
    f = None
    for _ in range(180):
        f = next((x for x in pg.frames if x.get_by_text("Properties of Bitcoin").count() > 1 and x.get_by_text("Sources").count()), None)
        if f and f.evaluate("!!document.getElementById('sources')"):
            break
        time.sleep(1)
    if "--fake-base" in sys.argv:  # added after load: assets are already fetched, links resolve at click time
        f.evaluate("() => { const e = document.createElement('base'); e.href = location.origin + '/somewhere/else.py'; document.head.prepend(e); }")
    start_url = f.url
    labels = f.evaluate("""() => { const out = []; const walk = r => r.querySelectorAll('*').forEach(e => { if (e.shadowRoot) walk(e.shadowRoot); if (e.tagName === 'NAV') out.push(...Array.from(e.querySelectorAll('a')).map(a => [a.textContent, a.getAttribute('href').slice(1)])); }); walk(document); return out; }""")
    print(len(labels), "links")
    for label, hid in labels:
        f.evaluate("""(label) => { const walk = r => { for (const e of r.querySelectorAll('*')) { if (e.shadowRoot) { const x = walk(e.shadowRoot); if (x) return x; } if (e.tagName === 'A' && e.closest('nav') && e.textContent === label) return e; } }; walk(document).click(); }""", label)
        time.sleep(1.5)
        top = f.evaluate("id => document.getElementById(id).getBoundingClientRect().top", hid)
        ok = f.url == start_url and f.get_by_text("Page not found").count() == 0 and -5 <= top <= 300
        if not ok:
            fails.append(f"{label}: top={top:.0f} url_changed={f.url != start_url}")
        print("ok  " if ok else "FAIL", label, f"heading at {top:.0f}px")
    b.close()
print("FAILURES:", fails if fails else 0)
sys.exit(1 if fails else 0)
