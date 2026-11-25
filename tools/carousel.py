"""Kaydırmalı gönderi üretici (HTML -> Playwright). python3 carousel.py <slides.json> <outdir>
slides.json: {"handle": "@sonraapp", "slides": [{"kind": "cover|text|app|end", ...}]}
Instagram 1080x1350 (ig-XX.jpg) ve TikTok 1080x1920 (tt-XX.jpg) basar."""
import json, sys, os, html
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
import tempfile
TMP = tempfile.mkdtemp(prefix="carousel-")
FD = "/usr/share/fonts/opentype/inter/"
CSS = f"""




* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Inter Display', Inter, sans-serif; }}
.e {{ font-family: 'Noto Color Emoji'; }}
.s {{ width: 1080px; position: relative; overflow: hidden; background: #F2EDE3; color: #1B3020; display: flex;
     flex-direction: column; justify-content: center; padding: 0 110px; }}
.s.dark {{ background: #2F5233; color: #F2EDE3; }}
.num {{ position: absolute; top: 64px; right: 80px; font-weight: 600; font-size: 34px; opacity: .6; }}
.handle {{ position: absolute; bottom: 60px; left: 80px; font-weight: 600; font-size: 34px; opacity: .6; }}
.kick {{ font-weight: 800; font-size: 40px; letter-spacing: 3px; color: #548C4C; margin-bottom: 28px; text-transform: none; }}
.dark .kick {{ color: #C9DCC3; }}
.emo {{ font-size: 150px; line-height: 1; margin-bottom: 40px; font-family: 'Noto Color Emoji'; }}
h1 {{ font-weight: 900; font-size: 170px; line-height: 1.04; text-wrap: balance; }}
h2 {{ font-weight: 900; font-size: 78px; line-height: 1.08; text-wrap: balance; margin-bottom: 36px; }}
p {{ font-weight: 500; font-size: 44px; line-height: 1.32; text-wrap: pretty; opacity: .88; }}
.promise {{ font-weight: 600; font-size: 48px; margin-top: 40px; opacity: .85; text-wrap: balance; }}
.phones {{ display: flex; gap: 34px; justify-content: center; margin-top: 44px; }}
.ph {{ background: #121212; padding: 12px; border-radius: 48px; }}
.ph img {{ display: block; border-radius: 38px; }}
.list {{ font-weight: 600; font-size: 42px; line-height: 1.55; margin: 26px 0 30px; }}
.list b {{ font-weight: 900; color: #548C4C; display: inline-block; width: 62px; }}
.cta {{ font-weight: 900; font-size: 56px; line-height: 1.12; text-wrap: balance; }}
.foot {{ display: flex; align-items: center; gap: 26px; margin-top: 46px; }}
.foot .logo {{ width: 130px; height: 130px; }}
.foot .badges img {{ height: 74px; margin-right: 14px; }}
"""

def slide(s, i, n, h, handle):
    k = s["kind"]; e = html.escape
    inner = ""
    if k == "cover":
        inner = f'<div class="emo">{s["emoji"]}</div><div class="kick" style="font-size:52px;color:#F2EDE3">{e(s["kicker"])}</div><h1 style="font-size:{s.get('title_size',170)}px">{e(s["title"])}</h1><div class="promise">{e(s["promise"])}</div>'
    elif k == "text":
        inner = f'<div class="emo">{s["emoji"]}</div><div class="kick">{e(s["kicker"])}</div><h2>{e(s["title"])}</h2><p>{e(s["body"])}</p>'
    elif k == "app":
        pw = 330 if h == 1350 else 400
        imgs = "".join(f'<div class="ph"><img src="file://{p}" width="{pw}"></div>' for p in s["screens"])
        inner = f'<div class="kick">{e(s["kicker"])}</div><h2 style="font-size:70px;margin-bottom:22px">{e(s["title"])}</h2><p style="font-size:38px">{e(s["body"])}</p><div class="phones">{imgs}</div>'
    elif k == "end":
        items = "".join(f"<div><b>{j+1}</b>{e(x)}</div>" for j, x in enumerate(s["list"]))
        inner = (f'<div class="kick">{e(s["kicker"])}</div><div class="list">{items}</div><div class="cta">{e(s["cta"])}</div>'
                 f'<div class="foot"><img class="logo" src="file://{HERE}/logo-transparent.png"><div class="badges">'
                 f'<img src="file://{HERE}/badge-appstore.png"><img src="file://{HERE}/badge-googleplay.png"></div></div>')
    cls = "s dark" if s.get("dark") else "s"
    return f'<section class="{cls}" style="height:{h}px"><div class="num">{i}/{n}</div>{inner}<div class="handle">{handle}</div></section>'

def build(spec, out):
    os.makedirs(out, exist_ok=True); n = len(spec["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch()
        for prefix, h in (("ig", 1350), ("tt", 1920)):
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
            for i, s in enumerate(spec["slides"], 1):
                tmp = os.path.join(TMP, f"slide-{prefix}-{i}.html")
                open(tmp, "w").write(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{slide(s, i, n, h, spec['handle'])}</body></html>")
                pg.goto("file://" + tmp); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(200)
                pg.screenshot(path=f"{out}/{prefix}-{i:02d}.jpg", type="jpeg", quality=90, clip={"x": 0, "y": 0, "width": 1080, "height": h})
        b.close()

if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
