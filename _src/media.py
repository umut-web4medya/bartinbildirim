# -*- coding: utf-8 -*-
"""Görsel türevleri + favicon. Kaynak: images/bartin-bildirim-banner.webp (kullanıcının yüklediği, DOKUNMA).
Çalıştır: python3 _src/media.py   (yalnız banner/logo değişince; build.py'den önce)"""
import os, asyncio
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(KOK, "images")
BANNER = os.path.join(IMG, "bartin-bildirim-banner.webp")

def hero():
    im = Image.open(BANNER).convert("RGB")                     # 1664×624
    im.save(os.path.join(IMG, "hero-1664.webp"), "WEBP", quality=80, method=6)
    im.resize((960, round(624 * 960 / 1664)), Image.LANCZOS).save(os.path.join(IMG, "hero-960.webp"), "WEBP", quality=78, method=6)
    # mobil: sağdaki kale + köprü + ırmak kısmı; mobilde metnin ALTINDA durur (el yazısıyla çakışmasın)
    k = im.crop((620, 0, 1664, 624)).resize((900, 538), Image.LANCZOS)
    k.save(os.path.join(IMG, "hero-mobil.webp"), "WEBP", quality=78, method=6)
    # paylaşım görseli 1200×630
    og = im.crop((232, 0, 1664, 624)).resize((1200, 523), Image.LANCZOS)
    t = Image.new("RGB", (1200, 630), (8, 14, 32)); t.paste(og, (0, 54))
    t.save(os.path.join(IMG, "og.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("hero + og tamam")

def hayat_var():
    """Banner'daki el yazısını saydam PNG'ye çıkar (alt bilgi için)."""
    im = Image.open(BANNER).convert("RGB").crop((1370, 80, 1620, 220))
    cikti = Image.new("RGBA", im.size)
    px, po = im.load(), cikti.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            parlak = max(r, g)
            a = max(0, min(255, int((parlak - 95) * 255 / 105)))
            sari = r > 150 and g > 120 and b < 120
            po[x, y] = ((255, 204, 51, a) if sari else (255, 255, 255, a))
    cikti.save(os.path.join(IMG, "hayat-var.png"), optimize=True)
    print("hayat-var.png", cikti.size)

ZIL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="512" height="512">
<rect width="48" height="48" rx="11" fill="#0a1020"/>
<g fill="none" stroke="#FFC727" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
<g transform="rotate(-14 24 24)"><path d="M14 30c2.5-2 3-5 3-10a7 7 0 0 1 14 0c0 5 .5 8 3 10z"/>
<path d="M21 34.5a3.2 3.2 0 0 0 6 0"/><path d="M24 9.5v3"/></g>
<path d="M8.5 17.5a14 14 0 0 0-1 9.5"/><path d="M39.5 13.5a14 14 0 0 1 2 9"/></g></svg>"""

async def favicon():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 512, "height": 512})
        await pg.set_content(f'<html><body style="margin:0;background:transparent">{ZIL}</body></html>')
        yol = os.path.join(IMG, "favicon-512.png")
        await pg.screenshot(path=yol, omit_background=True, clip={"x": 0, "y": 0, "width": 512, "height": 512})
        await b.close()
    im = Image.open(yol).convert("RGBA")
    im.resize((48, 48), Image.LANCZOS).save(os.path.join(KOK, "favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)])
    for s in (48, 96, 180, 192):
        im.resize((s, s), Image.LANCZOS).save(os.path.join(IMG, f"favicon-{s}.png"), optimize=True)
    print("favicon tamam")

if __name__ == "__main__":
    hero()
    hayat_var()
    asyncio.run(favicon())
