# -*- coding: utf-8 -*-
"""Commit öncesi denetim: kırık iç bağlantı/görsel, kök-göreli yol (alt yol önizlemesini kırar), eksik veri.
Çıkış kodu 1 = HATA."""
import os, re, sys, json
from urllib.parse import urlsplit, unquote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hata, uyari = [], []
sayfalar = []
for d, _, dosyalar in os.walk(KOK):
    if "/.git" in d or "/_src" in d: continue
    for f in dosyalar:
        if f.endswith(".html"): sayfalar.append(os.path.join(d, f))

ref = re.compile(r'(?:href|src)="([^"#]+)"|srcset="([^"]+)"')
for yol in sayfalar:
    g = os.path.relpath(yol, KOK)
    s = open(yol, encoding="utf-8").read()
    if "<title>" not in s or 'name="description"' not in s: hata.append(f"{g}: title/description yok")
    if s.count("<h1") != 1: hata.append(f"{g}: {s.count('<h1')} adet h1")
    for m in ref.finditer(s):
        adaylar = [m.group(1)] if m.group(1) else [p.strip().split(" ")[0] for p in m.group(2).split(",")]
        for u in adaylar:
            if re.match(r"^(https?:|mailto:|tel:|data:)", u): continue
            if u.startswith("/") and g != "404.html":
                hata.append(f"{g}: kök-göreli yol {u} (alt yol önizlemesinde 404)"); continue
            temiz = unquote(urlsplit(u).path)
            hedef = os.path.normpath(os.path.join(KOK if u.startswith("/") else os.path.dirname(yol), temiz.lstrip("/") if u.startswith("/") else temiz))
            if os.path.isdir(hedef): hedef = os.path.join(hedef, "index.html")
            if not os.path.exists(hedef): hata.append(f"{g}: kırık bağlantı {u}")
    for img in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in img: hata.append(f"{g}: alt'sız görsel")

S = D.SITE
for k in ("whatsapp", "eposta", "bildirim_link"):
    if not S[k]: uyari.append(f"SITE['{k}'] boş ⏳")
for k, v in S["sosyal"].items():
    if not v: uyari.append(f"sosyal['{k}'] boş ⏳")
if not S["yayin"]: uyari.append("yayın KAPALI — tüm sayfalar noindex (örnek ilanlar duruyor)")
eksik = [i["slug"] for i in D.ILANLAR if not any(os.path.exists(os.path.join(KOK, "images/ilanlar", f"{i['slug']}.{u}")) for u in ("webp", "jpg", "jpeg", "png"))]
if eksik: uyari.append(f"{len(eksik)} ilanın görseli yok (kapak çiziliyor): " + ", ".join(eksik))

for h in hata: print("HATA  ", h)
for u in uyari: print("uyarı ", u)
print(f"{len(sayfalar)} sayfa · {len(hata)} hata · {len(uyari)} uyarı")
sys.exit(1 if hata else 0)
