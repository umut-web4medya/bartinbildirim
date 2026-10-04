# -*- coding: utf-8 -*-
"""
Bartın Bildirim — statik site üreticisi (GitHub Pages).
  python3 _src/media.py   (yalnız banner / logo değişince)
  python3 _src/build.py && python3 _src/denetim.py
⛔ Üretilen HTML'i elle düzenleme; veri _src/data.py'de, şablon burada.

Tüm iç yollar sayfa derinliğine göre GÖRELİ üretilir (ic()) — hem
umut-web4medya.github.io/bartinbildirim/ önizlemesinde hem kök alan adında çalışır.
"""
import os, json, hashlib, html, shutil
from PIL import Image
import data as D

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = D.SITE
ALAN = S["alan"]
KAT = {k["slug"]: k for k in D.KATEGORILER}
MEK = {m["slug"]: m for m in D.MEKANLAR}
ILAN = {i["slug"]: i for i in D.ILANLAR}
ONEK = ""
URETILEN = []          # (yol, robots) — sitemap + denetim için

# ── yardımcılar ─────────────────────────────────────────────────────────────
def e(t): return html.escape(str(t), quote=True)

def ic(yol=""):
    return (ONEK + yol) if (ONEK + yol) else "./"

def surum(gorece):
    with open(os.path.join(KOK, gorece), "rb") as f:
        return gorece + "?v=" + hashlib.md5(f.read()).hexdigest()[:8]

def tarih_yaz(t):
    y, a, g = t.split("-")
    return f"{int(g)} {D.AYLAR[int(a) - 1]} {y}"

def sirala(liste): return sorted(liste, key=lambda i: (i["tarih"], i["saat"]))

def ilan_yolu(i): return f"ilan/{i['slug']}/"
def mekan_yolu(m): return f"mekan/{m['slug']}/"

IKON = {
    "muzik":  '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "yemek":  '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "yatak":  '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M12 4v6"/><path d="M2 18h20"/>',
    "takvim": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
    "maske":  '<path d="M10 11h.01"/><path d="M14 6h.01"/><path d="M18 6h.01"/><path d="M6.5 13.1h.01"/><path d="M22 5c0 9-4 12-6 12s-6-3-6-12c0-2 2-3 6-3s6 1 6 3"/><path d="M17.4 9.9c-.8.8-2 .8-2.8 0"/><path d="M10.1 7.1C9 7.2 7.7 7.7 6 8.6c-3.5 2-4.7 3.9-3.7 5.6 4.5 7.8 9.5 8.4 11.2 7.4.9-.5 1.9-2.1 1.9-4.7"/><path d="M9.1 16.5c.3-1.1 1.4-1.7 2.4-1.4"/>',
    "konum":  '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "yildiz": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    "ara":    '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "arti":   '<path d="M5 12h14M12 5v14"/>',
    "kisi":   '<circle cx="12" cy="8" r="4.5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "ok":     '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "zil":    '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "alev":   '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "simsek": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "asagi":  '<path d="m6 9 6 6 6-6"/>',
    "izgara": '<rect width="7" height="7" x="3" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="3" rx="1.5"/><rect width="7" height="7" x="14" y="14" rx="1.5"/><rect width="7" height="7" x="3" y="14" rx="1.5"/>',
    "menu":   '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "kapat":  '<path d="M18 6 6 18M6 6l12 12"/>',
    "saat":   '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "paylas": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
    "facebook":  '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "x":         '<path d="M4 4l11.7 16H20L8.3 4z"/><path d="M4 20l6.8-6.8m2.4-2.4L20 4"/>',
    "youtube":   '<path d="M2.5 17a24 24 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24 24 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
}
DOLU = {"alev", "simsek", "yildiz-dolu"}

def svg(ad, sinif="ik"):
    dolgu = 'fill="currentColor" stroke="none"' if ad in DOLU else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg class="{sinif}" viewBox="0 0 24 24" {dolgu} aria-hidden="true">{IKON[ad]}</svg>'

ZIL_LOGO = ('<svg class="logo-zil" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<g transform="rotate(-14 24 24)"><path d="M14 30c2.5-2 3-5 3-10a7 7 0 0 1 14 0c0 5 .5 8 3 10z"/>'
            '<path d="M21 34.5a3.2 3.2 0 0 0 6 0"/><path d="M24 9.5v3"/></g>'
            '<path d="M8.5 17.5a14 14 0 0 0-1 9.5"/><path d="M39.5 13.5a14 14 0 0 1 2 9"/></svg>')

# ── görseller ───────────────────────────────────────────────────────────────
def ilan_gorseli(i, gen):
    """images/ilanlar/<slug>.(webp|jpg|jpeg|png) varsa <slug>-<gen>.webp türevini üretip yolunu döndürür."""
    for uz in ("webp", "jpg", "jpeg", "png"):
        kay = os.path.join(KOK, "images", "ilanlar", f"{i['slug']}.{uz}")
        if os.path.exists(kay):
            hedef_g = f"images/ilanlar/{i['slug']}-{gen}.webp"
            hedef = os.path.join(KOK, hedef_g)
            if not os.path.exists(hedef) or os.path.getmtime(hedef) < os.path.getmtime(kay):
                im = Image.open(kay).convert("RGB")
                if im.width > gen:
                    im = im.resize((gen, round(im.height * gen / im.width)), Image.LANCZOS)
                im.save(hedef, "WEBP", quality=78, method=6)
            with Image.open(hedef) as im:
                return hedef_g, im.size
    return None, None

def kapak(i, gen=480, sinif="kapak", oncelik=False):
    yol, boy = ilan_gorseli(i, gen)
    k = KAT[i["kategori"]]
    if yol:
        yukle = 'fetchpriority="high"' if oncelik else 'loading="lazy"'
        return (f'<img class="{sinif}" src="{ic(yol)}" width="{boy[0]}" height="{boy[1]}" '
                f'alt="{e(i["baslik"])}" {yukle} decoding="async">')
    yazi = f'<span class="kapak-yazi">{e(i["kapak_yazi"])}</span>' if i.get("kapak_yazi") else ""
    return (f'<span class="{sinif} kapak-bos" style="--r:{k["renk"]}" role="img" aria-label="{e(i["baslik"])}">'
            f'{svg(k["ikon"], "kapak-ik")}{yazi}</span>')

# ── iskelet ─────────────────────────────────────────────────────────────────
def head(baslik, aciklama, yol, sema=None, robots=None):
    robots = robots or ("index,follow" if S["yayin"] else "noindex,follow")
    URETILEN.append((yol, robots))
    tam = baslik if baslik.endswith(S["ad"]) else f"{baslik} | {S['ad']}"
    canon = f"{ALAN}/{yol}"
    ld = ""
    for s in (sema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(tam)}</title>
<meta name="description" content="{e(aciklama)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{e(S['ad'])}">
<meta property="og:title" content="{e(tam)}">
<meta property="og:description" content="{e(aciklama)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ALAN}/images/og.jpg">
<meta name="theme-color" content="#0a1020">
<link rel="preload" href="{ic('assets/fonts/pjs-var-tr.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{ic(surum('assets/css/site.css'))}">
<link rel="icon" href="{ic('favicon.ico')}" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="{ic('images/favicon-192.png')}">
<link rel="apple-touch-icon" href="{ic('images/favicon-180.png')}">
{ld}</head>
<body>
<a class="atla" href="#icerik">İçeriğe geç</a>
"""

def logo(sinif="logo"):
    return (f'<a class="{sinif}" href="{ic()}" aria-label="{e(S["ad"])} — Ana Sayfa">{ZIL_LOGO}'
            f'<span class="logo-yazi"><b>{e(S["ad"])}</b><small>{e(S["slogan"])}</small></span></a>')

def ust(aktif=""):
    def m(ad, yol, anahtar):
        a = ' class="aktif" aria-current="page"' if anahtar == aktif else ""
        return f'<a href="{ic(yol)}"{a}>{ad}</a>'
    kat = "".join(f'<a href="{ic(k["yol"])}">{svg(k["ikon"])}{e(k["ad"])}</a>' for k in D.KATEGORILER)
    kat_aktif = " aktif" if aktif == "kategori" else ""
    return f"""<header class="ust">
 <div class="kap ust-ic">
  {logo()}
  <nav class="menu" id="menu" aria-label="Ana menü">
   {m("Ana Sayfa", "", "ana")}
   {m("Etkinlikler", "etkinlikler/", "etkinlikler")}
   {m("Mekanlar", "mekanlar/", "mekanlar")}
   {m("Oteller", "oteller/", "oteller")}
   <div class="acilir">
    <button type="button" class="acilir-dg{kat_aktif}" aria-expanded="false" aria-controls="kat-panel">Kategoriler {svg("asagi")}</button>
    <div class="acilir-panel" id="kat-panel">{kat}</div>
   </div>
   <a class="menu-ilan" href="{ic('ilan-ekle/')}">{svg("arti")} İlan Ekle</a>
  </nav>
  <form class="arama" action="{ic('ara/')}" method="get" role="search">
   <input type="search" name="q" placeholder="Etkinlik, mekan veya sanatçı ara..." aria-label="Etkinlik, mekan veya sanatçı ara">
   <button type="submit" aria-label="Ara">{svg("ara")}</button>
  </form>
  <a class="dg dg-sari ust-ilan" href="{ic('ilan-ekle/')}">{svg("arti")}<span>İlan Ekle</span></a>
  <a class="ust-kisi" href="{ic('ilan-ekle/')}" aria-label="İlan ver">{svg("kisi")}</a>
  <button type="button" class="menu-ac" aria-expanded="false" aria-controls="menu" aria-label="Menüyü aç">{svg("menu")}</button>
 </div>
</header>
<main id="icerik">
"""

def w4_imza():
    return ('<div class="w4"><div class="w4-bag"><span class="w4-etiket">Web Tasarım:</span>'
            '<a class="w4-ad" href="https://www.web4medya.com/" target="_blank" rel="noopener">'
            'Web<span class="w4-d">4</span>Medya</a></div></div>')

def sosyal():
    adlar = {"instagram": "Instagram", "facebook": "Facebook", "x": "X", "youtube": "YouTube"}
    p = []
    for k, ad in adlar.items():
        url = S["sosyal"].get(k)
        if url:
            p.append(f'<a href="{e(url)}" target="_blank" rel="noopener" aria-label="{ad}">{svg(k)}</a>')
        else:
            p.append(f'<span class="sos-bos" title="{ad} — yakında">{svg(k)}</span>')
    return "".join(p)

def alt():
    return f"""</main>
<footer class="alt">
 <div class="kap alt-ic">
  {logo("logo logo-alt")}
  <nav class="alt-link" aria-label="Alt menü">
   <a href="{ic('hakkimizda/')}">Hakkımızda</a><a href="{ic('iletisim/')}">İletişim</a><a href="{ic('gizlilik-politikasi/')}">Gizlilik Politikası</a><a href="{ic('kullanim-sartlari/')}">Kullanım Şartları</a>
  </nav>
  <div class="alt-sos">{sosyal()}</div>
  <img class="alt-yazi" src="{ic('images/hayat-var.png')}" width="250" height="140" alt="Bartın’da hayat var!" loading="lazy">
 </div>
 <p class="kap alt-telif">© {S['kurulus']} {e(S['ad'])}. Tüm hakları saklıdır.</p>
 {w4_imza()}
</footer>
<script src="{ic(surum('assets/js/app.js'))}" defer></script>
</body>
</html>
"""

def yaz(yol, icerik):
    hedef = os.path.join(KOK, yol, "index.html") if not yol.endswith(".html") else os.path.join(KOK, yol)
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    with open(hedef, "w", encoding="utf-8") as f:
        f.write(icerik)

def onek(yol):
    """ONEK'i sayfanın derinliğine ayarla — kirinti()/ic() çağrılmadan ÖNCE çalışmalı."""
    global ONEK
    ONEK = "../" * yol.count("/")

def sayfa(yol, baslik, aciklama, govde, aktif="", sema=None, robots=None):
    onek(yol)
    yaz(yol, head(baslik, aciklama, yol, sema, robots) + ust(aktif) + govde() + alt())

# ── bileşenler ──────────────────────────────────────────────────────────────
def rozetler(i):
    k = KAT[i["kategori"]]
    r = f'<span class="rozet" style="--r:{k["renk"]}">{e(k["rozet"])}</span>'
    if i["yeni"]: r += '<span class="rozet rozet-yeni">Yeni</span>'
    return f'<div class="rozetler">{r}</div>'

def ilan_karti(i, h="h3"):
    m = MEK[i["mekan"]]
    acik = f'<p class="ilan-acik">{e(i["aciklama"])}</p>' if i["aciklama"] else ""
    return f"""<article class="ilan">
 <a class="ilan-gorsel" href="{ic(ilan_yolu(i))}" tabindex="-1" aria-hidden="true">{kapak(i)}</a>
 <div class="ilan-govde">
  {rozetler(i)}
  <{h} class="ilan-baslik"><a href="{ic(ilan_yolu(i))}">{e(i["baslik"])}</a></{h}>
  {acik}
  <ul class="ilan-bilgi">
   <li>{svg("takvim")}<span><time datetime="{i['tarih']}T{i['saat']}">{tarih_yaz(i["tarih"])}</time><i>|</i>{i["saat"]}</span></li>
   <li>{svg("konum")}<a href="{ic(mekan_yolu(m))}">{e(m["ad"])}</a></li>
  </ul>
 </div>
 <a class="dg dg-cizgi ilan-dg" href="{ic(ilan_yolu(i))}" aria-label="{e(i['baslik'])} — detaylar">Detaylar {svg("ok")}</a>
</article>"""

def bos_liste(metin):
    return (f'<div class="bos"><p>{e(metin)}</p>'
            f'<a class="dg dg-sari" href="{ic("ilan-ekle/")}">{svg("arti")} İlan Ekle</a></div>')

def one_cikanlar():
    satir = []
    for s in D.ONE_CIKAN:
        i = ILAN[s]; m = MEK[i["mekan"]]
        satir.append(f"""<li><a href="{ic(ilan_yolu(i))}">
  {kapak(i, 160, "kapak kapak-kucuk")}
  <span class="oc-metin"><b>{e(i["kisa"])}</b><small>{e(m["ad"])}</small>
  <small class="oc-zaman">{tarih_yaz(i["tarih"])}<i>|</i>{i["saat"]}</small></span></a></li>""")
    return f"""<section class="kutu oc" aria-labelledby="oc-b">
 <h2 class="kutu-b" id="oc-b">{svg("alev", "ik ik-alev")}Bugünün Öne Çıkanları</h2>
 <ul>{"".join(satir)}</ul>
</section>"""

def bildirim_karti():
    hedef = S["bildirim_link"] or ic("iletisim/")
    dis = ' target="_blank" rel="noopener"' if S["bildirim_link"] else ""
    return f"""<section class="bildirim" aria-labelledby="bl-b">
 <h2 id="bl-b">Bartın’daki tüm etkinliklerden ilk sen haberdar ol!</h2>
 <p>Bildirimleri aç, kaçırma!</p>
 <a class="dg dg-sari" href="{hedef}"{dis}>{svg("zil")} Bildirimleri Aç</a>
 {ZIL_LOGO.replace('class="logo-zil"', 'class="bildirim-zil"')}
</section>"""

def kategori_kutusu():
    l = "".join(f'<li><a href="{ic(k["yol"])}">{svg(k["ikon"])}{e(k["ad"])}</a></li>' for k in D.KATEGORILER)
    return f"""<section class="kutu kat-kutu" aria-labelledby="kk-b">
 <h2 class="kutu-b kutu-b-kucuk" id="kk-b">{svg("izgara")}Kategoriler</h2>
 <ul>{l}</ul>
</section>"""

def yan():
    return f'<aside class="yan">{one_cikanlar()}{bildirim_karti()}{kategori_kutusu()}</aside>'

def kategori_seridi():
    return '<nav class="kap kat-serit" aria-label="Kategoriler">' + "".join(
        f'<a href="{ic(k["yol"])}">{svg(k["ikon"])}<span>{e(k["ad"])}</span></a>' for k in D.KATEGORILER) + "</nav>"

def kirinti(parcalar):
    li, ld = [], []
    for n, (ad, yol) in enumerate(parcalar, 1):
        if yol is None:
            li.append(f'<li aria-current="page">{e(ad)}</li>')
            ld.append({"@type": "ListItem", "position": n, "name": ad})
        else:
            li.append(f'<li><a href="{ic(yol)}">{e(ad)}</a></li>')
            ld.append({"@type": "ListItem", "position": n, "name": ad, "item": f"{ALAN}/{yol}"})
    return (f'<nav class="kirinti" aria-label="Sayfa yolu"><ol>{"".join(li)}</ol></nav>',
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld})

def sayfa_basi(kir, baslik, alt_metin=""):
    a = f"<p>{alt_metin}</p>" if alt_metin else ""
    return f'<section class="sb"><div class="kap">{kir}<h1>{baslik}</h1>{a}</div></section>'

def liste_duzeni(sol):
    return f'<div class="kap duzen"><div class="ana">{sol}</div>{yan()}</div>'

def bolum_basligi(baslik, ikon="simsek", link=None):
    l = f'<a class="tumu" href="{ic(link)}">Tümünü Gör {svg("ok")}</a>' if link else ""
    return f'<div class="bolum-b"><h2>{svg(ikon, "ik ik-" + ikon)}{baslik}</h2>{l}</div>'

# ── sayfalar ────────────────────────────────────────────────────────────────
def anasayfa():
    def g():
        kartlar = "".join(ilan_karti(ILAN[s]) for s in D.YENI_EKLENEN)
        return f"""<section class="hero">
 <picture>
  <source media="(max-width:700px)" srcset="{ic('images/hero-mobil.webp')}" width="900" height="538">
  <img class="hero-gorsel" src="{ic('images/hero-1664.webp')}" srcset="{ic('images/hero-960.webp')} 960w, {ic('images/hero-1664.webp')} 1664w" sizes="100vw" width="1664" height="624" alt="Gece ışıkları yanan Bartın ırmağı, köprü ve tepedeki kale" fetchpriority="high">
 </picture>
 <div class="kap hero-ic">
  <p class="hero-yer">{svg("konum")}Bartın</p>
  <h1><span>Şehrin Tüm</span> <span class="sari">Etkinlikleri</span> <span>Tek Bir Yerde!</span></h1>
  <p class="hero-p">Restoranlar, kafeler, oteller, konserler, canlı müzikler ve daha fazlası... Bartın’da bugün neler var, hemen keşfet!</p>
  <a class="dg dg-sari" href="{ic('etkinlikler/')}">{svg("takvim")} Bugünün Etkinlikleri {svg("ok")}</a>
 </div>
</section>
{kategori_seridi()}
{liste_duzeni(bolum_basligi("Yeni Eklenen İlanlar", "simsek", "etkinlikler/") + '<div class="ilanlar">' + kartlar + '</div>')}"""
    sema = [{"@context": "https://schema.org", "@type": "WebSite", "name": S["ad"], "url": ALAN + "/",
             "potentialAction": {"@type": "SearchAction", "target": ALAN + "/ara/?q={q}", "query-input": "required name=q"}}]
    sayfa("", f"{S['ad']} — Bartın’da Ne Var Ne Yok?",
          "Restoranlar, kafeler, oteller, konserler, canlı müzikler ve daha fazlası... Bartın’da bugün neler var, hemen keşfet!",
          g, "ana", sema)

def liste_sayfasi(yol, baslik, aciklama, ilanlar, aktif, ust_ek="", bos_metin="Bu bölümde şu an ilan yok."):
    onek(yol)
    if callable(ust_ek): ust_ek = ust_ek()   # ic() doğru derinlikte çalışsın
    kir, kld = kirinti([("Ana Sayfa", ""), (baslik, None)])
    def g():
        kartlar = "".join(ilan_karti(i, "h2") for i in sirala(ilanlar))
        govde = ust_ek + (f'<div class="ilanlar">{kartlar}</div>' if ilanlar else bos_liste(bos_metin))
        return sayfa_basi(kir, e(baslik)) + liste_duzeni(govde)
    robots = None if ilanlar or ust_ek else "noindex,follow"
    sayfa(yol, baslik, aciklama, g, aktif, [kld], robots)

def mekan_izgarasi(mekanlar):
    k = []
    for m in mekanlar:
        t = KAT[m["tur"]]
        n = sum(1 for i in D.ILANLAR if i["mekan"] == m["slug"])
        k.append(f"""<a class="mekan" href="{ic(mekan_yolu(m))}" style="--r:{t['renk']}">
 <span class="mekan-ik">{svg(t["ikon"])}</span><b>{e(m["ad"])}</b><small>{e(t["ad"])} · {n} ilan</small></a>""")
    return f'<div class="mekanlar">{"".join(k)}</div>'

def mekan_sayfasi(m):
    onek(mekan_yolu(m))
    ilanlar = [i for i in D.ILANLAR if i["mekan"] == m["slug"]]
    t = KAT[m["tur"]]
    ust_yol = ("Oteller", "oteller/") if m["tur"] == "oteller" else ("Mekanlar", "mekanlar/")
    kir, kld = kirinti([("Ana Sayfa", ""), ust_yol, (m["ad"], None)])
    def g():
        kartlar = "".join(ilan_karti(i, "h2") for i in sirala(ilanlar))
        return (sayfa_basi(kir, e(m["ad"]), f'<span class="rozet" style="--r:{t["renk"]}">{e(t["ad"])}</span>')
                + liste_duzeni(bolum_basligi("Bu mekandaki ilanlar", "takvim") +
                               (f'<div class="ilanlar">{kartlar}</div>' if ilanlar else bos_liste("Bu mekanda şu an ilan yok."))))
    sayfa(mekan_yolu(m), f"{m['ad']} — Etkinlikler", f"{m['ad']} etkinlikleri ve ilanları — {S['ad']}.",
          g, "oteller" if m["tur"] == "oteller" else "mekanlar", [kld])

def ilan_sayfasi(i):
    onek(ilan_yolu(i))
    m = MEK[i["mekan"]]; k = KAT[i["kategori"]]
    kir, kld = kirinti([("Ana Sayfa", ""), ("Etkinlikler", "etkinlikler/"), (i["baslik"], None)])
    gorsel, _ = ilan_gorseli(i, 960)
    ev = {"@context": "https://schema.org", "@type": "Event", "name": i["baslik"],
          "startDate": f"{i['tarih']}T{i['saat']}:00+03:00",
          "eventStatus": "https://schema.org/EventScheduled",
          "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "location": {"@type": "Place", "name": m["ad"],
                       "address": {"@type": "PostalAddress", "addressRegion": "Bartın", "addressCountry": "TR"}}}
    if i["aciklama"]: ev["description"] = i["aciklama"]
    if gorsel: ev["image"] = f"{ALAN}/{gorsel}"
    diger = [x for x in sirala(D.ILANLAR) if x["mekan"] == m["slug"] and x["slug"] != i["slug"]]
    def g():
        acik = f'<p class="detay-acik">{e(i["aciklama"])}</p>' if i["aciklama"] else ""
        dig = ""
        if diger:
            dig = bolum_basligi(f"{e(m['ad'])} — diğer ilanlar", "takvim") + \
                  '<div class="ilanlar">' + "".join(ilan_karti(x) for x in diger) + "</div>"
        return f"""<div class="kap">{kir}</div>
<div class="kap duzen"><div class="ana">
 <article class="detay">
  <div class="detay-gorsel">{kapak(i, 960, "kapak kapak-buyuk", True)}</div>
  <div class="detay-govde">
   {rozetler(i)}
   <h1>{e(i["baslik"])}</h1>
   {acik}
   <ul class="detay-bilgi">
    <li>{svg("takvim")}<span><small>Tarih</small><time datetime="{i['tarih']}">{tarih_yaz(i["tarih"])}</time></span></li>
    <li>{svg("saat")}<span><small>Saat</small>{i["saat"]}</span></li>
    <li>{svg("konum")}<span><small>Mekan</small><a href="{ic(mekan_yolu(m))}">{e(m["ad"])}</a></span></li>
   </ul>
   <div class="detay-dg">
    <a class="dg dg-sari" href="{ic(mekan_yolu(m))}">{svg("konum")} Mekanı Gör</a>
    <button type="button" class="dg dg-cizgi paylas" data-baslik="{e(i['baslik'])}">{svg("paylas")} Paylaş</button>
   </div>
  </div>
 </article>
 {dig}
</div>{yan()}</div>"""
    ack = i["aciklama"] or f"{i['baslik']} — {tarih_yaz(i['tarih'])} {i['saat']}, {m['ad']}."
    sayfa(ilan_yolu(i), f"{i['baslik']} — {tarih_yaz(i['tarih'])}", ack, g, "etkinlikler", [kld, ev])

def arama_sayfasi():
    onek("ara/")
    dizin = [{"b": i["baslik"], "a": i["aciklama"], "m": MEK[i["mekan"]]["ad"], "k": KAT[i["kategori"]]["rozet"],
              "r": KAT[i["kategori"]]["renk"], "t": tarih_yaz(i["tarih"]), "s": i["saat"], "y": ilan_yolu(i),
              "my": mekan_yolu(MEK[i["mekan"]])} for i in sirala(D.ILANLAR)]
    kir, _ = kirinti([("Ana Sayfa", ""), ("Arama", None)])
    def g():
        return (sayfa_basi(kir, "Arama") + liste_duzeni(
            f"""<form class="arama arama-buyuk" action="./" method="get" role="search">
 <input type="search" name="q" id="ara-q" placeholder="Etkinlik, mekan veya sanatçı ara..." aria-label="Etkinlik, mekan veya sanatçı ara">
 <button type="submit" aria-label="Ara">{svg("ara")}</button>
</form>
<p class="ara-ozet" id="ara-ozet" aria-live="polite"></p>
<div class="ilanlar" id="ara-sonuc"></div>
<script id="ara-dizin" type="application/json">{json.dumps(dizin, ensure_ascii=False)}</script>"""))
    sayfa("ara/", "Arama", "Bartın’daki etkinlik, mekan ve sanatçıları arayın.", g, "", None, "noindex,follow")

def ilan_ekle():
    onek("ilan-ekle/")
    kir, kld = kirinti([("Ana Sayfa", ""), ("İlan Ekle", None)])
    katsec = "".join(f'<option value="{e(k["ad"])}">{e(k["ad"])}</option>' for k in D.KATEGORILER)
    hazir = bool(S["whatsapp"] or S["eposta"])
    def g():
        uyari = "" if hazir else '<p class="not">İlan gönderimi çok yakında açılıyor.</p>'
        return sayfa_basi(kir, "İlan Ekle") + liste_duzeni(f"""<form class="form kutu" id="ilan-form" data-wa="{e(S['whatsapp'])}" data-eposta="{e(S['eposta'])}">
 {uyari}
 <label>İlan başlığı<input name="Başlık" required maxlength="90"></label>
 <div class="form-iki">
  <label>Kategori<select name="Kategori" required>{katsec}</select></label>
  <label>Mekan<input name="Mekan" required maxlength="80"></label>
 </div>
 <div class="form-iki">
  <label>Tarih<input type="date" name="Tarih" required></label>
  <label>Saat<input type="time" name="Saat" required></label>
 </div>
 <label>Açıklama<textarea name="Açıklama" rows="4" maxlength="400"></textarea></label>
 <div class="form-iki">
  <label>Adınız<input name="Ad" required maxlength="60" autocomplete="name"></label>
  <label>Telefon<input type="tel" name="Telefon" required maxlength="20" autocomplete="tel"></label>
 </div>
 <button class="dg dg-sari" type="submit"{"" if hazir else " disabled"}>{svg("arti")} İlanı Gönder</button>
</form>""")
    sayfa("ilan-ekle/", "İlan Ekle", "Bartın’daki etkinliğinizi, mekanınızı veya özel gününüzü Bartın Bildirim’de duyurun.",
          g, "", [kld])

def duz_sayfa(yol, baslik, aciklama, ek=""):
    onek(yol)
    kir, kld = kirinti([("Ana Sayfa", ""), (baslik, None)])
    def g():
        # Metin data.SAYFA_METIN'den (şimdilik örnek); yoksa "hazırlanıyor" notu.
        bloklar = D.SAYFA_METIN.get(yol.strip("/"), [])
        govde = "".join((f"<h2>{e(b)}</h2>" if b else "") + f"<p>{e(p)}</p>" for b, p in bloklar) \
            or '<p class="not">Bu sayfanın metni hazırlanıyor.</p>'
        return sayfa_basi(kir, e(baslik)) + liste_duzeni(f'<div class="kutu metin">{govde}{ek}</div>')
    sayfa(yol, baslik, aciklama, g, "", [kld], "noindex,follow")

def iletisim_ek():
    s = []
    if S.get("telefon"):
        s.append(f'<li><a href="tel:+{S["whatsapp"] or ""}">{e(S["telefon"])}</a></li>' if S["whatsapp"]
                 else f'<li>{e(S["telefon"])}</li>')
    if S["whatsapp"]:
        s.append(f'<li><a href="https://wa.me/{S["whatsapp"]}" target="_blank" rel="noopener">WhatsApp</a></li>')
    if S["eposta"]:
        s.append(f'<li><a href="mailto:{S["eposta"]}">{e(S["eposta"])}</a></li>')
    return f'<ul class="ilet">{"".join(s)}</ul>' if s else ""

def sayfa_404():
    global ONEK
    # GitHub her derinlikte servis eder → mutlak yol; alt yolda (…github.io/bartinbildirim/) yolu ALAN'dan al
    from urllib.parse import urlparse
    ONEK = urlparse(ALAN).path.rstrip("/") + "/"
    def g():
        return (f'<section class="sb sb-404"><div class="kap"><h1>Sayfa bulunamadı</h1>'
                f'<p>Aradığınız sayfa taşınmış ya da kaldırılmış olabilir.</p>'
                f'<a class="dg dg-sari" href="{ONEK}">Ana Sayfa {svg("ok")}</a></div></section>')
    icerik = head("Sayfa bulunamadı", "Aradığınız sayfa bulunamadı.", "404.html", None, "noindex") + ust() + g() + alt()
    yaz("404.html", icerik)
    ONEK = ""

def sitemap_robots():
    with open(os.path.join(KOK, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n" + (f"\nSitemap: {ALAN}/sitemap.xml\n" if S["yayin"] else ""))
    sm = os.path.join(KOK, "sitemap.xml")
    if not S["yayin"]:
        if os.path.exists(sm): os.remove(sm)
        return
    url = "".join(f"<url><loc>{ALAN}/{y}</loc></url>" for y, r in URETILEN if r.startswith("index"))
    with open(sm, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{url}</urlset>\n')

def temizle():
    """Üretilmiş klasörleri sil (kaldırılan ilan/mekan sayfası kalmasın)."""
    for d in ("ilan", "mekan", "kategori", "etkinlikler", "mekanlar", "oteller", "ara", "ilan-ekle",
              "hakkimizda", "iletisim", "gizlilik-politikasi", "kullanim-sartlari"):
        shutil.rmtree(os.path.join(KOK, d), ignore_errors=True)

def main():
    temizle()
    anasayfa()
    liste_sayfasi("etkinlikler/", "Etkinlikler", "Bartın’daki tüm etkinlikler, konserler ve canlı müzik geceleri tek listede.",
                  D.ILANLAR, "etkinlikler")
    mek = [m for m in D.MEKANLAR if m["tur"] != "oteller"]
    liste_sayfasi("mekanlar/", "Mekanlar", "Bartın’daki restoran, kafe ve etkinlik mekanları.",
                  [i for i in D.ILANLAR if i["kategori"] == "mekanlar"], "mekanlar",
                  lambda: bolum_basligi("Tüm mekanlar", "konum") + mekan_izgarasi(mek) + bolum_basligi("Mekan ilanları", "simsek"))
    ote = [m for m in D.MEKANLAR if m["tur"] == "oteller"]
    liste_sayfasi("oteller/", "Oteller", "Bartın’daki oteller ve otel etkinlikleri.",
                  [i for i in D.ILANLAR if i["kategori"] == "oteller"], "oteller",
                  (lambda: bolum_basligi("Oteller", "yatak") + mekan_izgarasi(ote) + bolum_basligi("Otel ilanları", "simsek")) if ote else "")
    for k in D.KATEGORILER:
        if k["yol"].startswith("kategori/"):
            liste_sayfasi(k["yol"], k["ad"], f"Bartın {k['ad']} ilanları — {S['ad']}.",
                          [i for i in D.ILANLAR if i["kategori"] == k["slug"]], "kategori")
    for m in D.MEKANLAR: mekan_sayfasi(m)
    for i in D.ILANLAR: ilan_sayfasi(i)
    arama_sayfasi()
    ilan_ekle()
    duz_sayfa("hakkimizda/", "Hakkımızda", f"{S['ad']} hakkında.")
    duz_sayfa("iletisim/", "İletişim", f"{S['ad']} iletişim bilgileri.", iletisim_ek())
    duz_sayfa("gizlilik-politikasi/", "Gizlilik Politikası", f"{S['ad']} gizlilik politikası.")
    duz_sayfa("kullanim-sartlari/", "Kullanım Şartları", f"{S['ad']} kullanım şartları.")
    sayfa_404()
    sitemap_robots()
    with open(os.path.join(KOK, "_src", ".uretilen.json"), "w") as f:
        json.dump(URETILEN, f)
    print(f"{len(URETILEN)} sayfa üretildi · yayın={'AÇIK' if S['yayin'] else 'KAPALI (noindex)'}")

if __name__ == "__main__":
    main()
