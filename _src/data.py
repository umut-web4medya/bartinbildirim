# -*- coding: utf-8 -*-
"""Bartın Bildirim — site verisi. Görünür metinler kullanıcının verdiği tasarımdan (2026-10-04) birebir alındı.
⏳ = kullanıcıdan bekleniyor. Boş bırakılan alan sitede gizlenir / devre dışı kalır; denetim.py uyarı basar."""

SITE = {
    "ad": "Bartın Bildirim",
    "slogan": "Bartın’da Ne Var Ne Yok?",
    "alan": "https://umut-web4medya.github.io/bartinbildirim",   # şimdilik GitHub Pages; alan adı alınınca değiştir
    "kurulus": 2026,
    # ⛔ Örnek ilanlar yayındayken False kalsın → tüm sayfalar noindex, sitemap üretilmez.
    "yayin": False,
    "whatsapp": "905303158752",   # 90XXXXXXXXXX biçiminde — İlan Ekle formu buraya mesaj hazırlar
    "telefon": "0530 315 87 52",
    "eposta": "",          # ⏳
    "bildirim_link": "",   # ⏳ "Bildirimleri Aç" (WhatsApp kanalı / Instagram vb.)
    "sosyal": {            # ⏳ boş olan ikon bağlantısız gösterilir
        "instagram": "",
        "facebook": "",
        "x": "",
        "youtube": "",
    },
}

# yol: kategori kutucuğunun gittiği sayfa. Oteller / Etkinlikler / Mekanlar üst menüdeki sayfalarla aynı yere gider.
KATEGORILER = [
    {"slug": "canli-muzik",   "ad": "Canlı Müzik",     "rozet": "Canlı Müzik",     "ikon": "muzik",   "renk": "#1f9d55", "yol": "kategori/canli-muzik/"},
    {"slug": "restoran-cafe", "ad": "Restoran & Cafe", "rozet": "Restoran & Cafe", "ikon": "yemek",   "renk": "#3b5bdb", "yol": "kategori/restoran-cafe/"},
    {"slug": "oteller",       "ad": "Oteller",         "rozet": "Otel",            "ikon": "yatak",   "renk": "#1c7ed6", "yol": "oteller/"},
    {"slug": "etkinlikler",   "ad": "Etkinlikler",     "rozet": "Etkinlik",        "ikon": "takvim",  "renk": "#5c5fd6", "yol": "etkinlikler/"},
    {"slug": "tiyatro-sanat", "ad": "Tiyatro & Sanat", "rozet": "Tiyatro & Sanat", "ikon": "maske",   "renk": "#9c36b5", "yol": "kategori/tiyatro-sanat/"},
    {"slug": "mekanlar",      "ad": "Mekanlar",        "rozet": "Mekanlar",        "ikon": "konum",   "renk": "#4c6ef5", "yol": "mekanlar/"},
    {"slug": "ozel-gunler",   "ad": "Özel Günler",     "rozet": "Özel Günler",     "ikon": "yildiz",  "renk": "#d6336c", "yol": "kategori/ozel-gunler/"},
]

# tur: kategori slug'ı (Oteller sayfası tur=="oteller" mekanları listeler)
MEKANLAR = [
    {"slug": "kale-cafe-restaurant", "ad": "Kale Cafe & Restaurant", "tur": "restoran-cafe"},
    {"slug": "limanda-otel",         "ad": "Limanda Otel",           "tur": "oteller"},
    {"slug": "bartin-kultur-merkezi","ad": "Bartın Kültür Merkezi",  "tur": "etkinlikler"},
    {"slug": "amasra-restoran",      "ad": "Amasra Restoran",        "tur": "restoran-cafe"},
    {"slug": "zeytin-cafe-bar",      "ad": "Zeytin Cafe & Bar",      "tur": "restoran-cafe"},
]

# ⚠️ ÖRNEK İLANLAR (tasarımdaki metinler). Gerçek ilanlar gelince değiştir, sonra SITE["yayin"] = True.
# gorsel: images/ilanlar/<slug>.webp (ya da .jpg/.png) varsa otomatik kullanılır; yoksa kategori renginde kapak çizilir.
# ⚠️ Şu anki görseller ÖRNEK (CC0, kaynaklar _src/kaynak/ornek-gorseller.json) — gerçek afişler gelince üzerine yaz.
# kapak_yazi: görsel yokken kapakta yazan kısa metin (tasarımdaki afişlerden).
ILANLAR = [
    {"slug": "emre-kaya-akustik-konser", "baslik": "Emre Kaya Akustik Konser", "kisa": "Emre Kaya Akustik Konser",
     "kategori": "canli-muzik", "yeni": True, "tarih": "2026-10-12", "saat": "21:00", "mekan": "kale-cafe-restaurant",
     "aciklama": "Bartın’ın sevilen sanatçısı Emre Kaya, bu akşam Kale Cafe’de sahne alıyor. Unutulmaz bir akşam sizi bekliyor!"},
    {"slug": "kale-cafede-canli-muzik-gecesi", "baslik": "Kale Cafe’de Canlı Müzik Gecesi", "kisa": "Kale Cafe’de Canlı Müzik",
     "kategori": "restoran-cafe", "yeni": True, "tarih": "2026-10-12", "saat": "20:30", "mekan": "kale-cafe-restaurant",
     "aciklama": "Her cuma ve cumartesi akşamı canlı müzik, özel menü ve eşsiz manzara sizleri bekliyor."},
    {"slug": "limanda-otel-ozel-konser-aksami", "baslik": "Limanda Otel – Özel Konser Akşamı", "kisa": "Limanda Otel – Özel Konser Akşamı",
     "kategori": "oteller", "yeni": True, "tarih": "2026-10-12", "saat": "19:30", "mekan": "limanda-otel",
     "aciklama": "Otelimizin terasında canlı müzik eşliğinde keyifli bir akşam geçirmeye davetlisiniz."},
    {"slug": "bartin-kultur-sanat-gunleri", "baslik": "Bartın Kültür Sanat Günleri", "kisa": "Bartın Kültür Sanat Günleri",
     "kategori": "etkinlikler", "yeni": True, "tarih": "2026-10-13", "saat": "20:00", "mekan": "bartin-kultur-merkezi",
     "aciklama": "Ünlü sanatçı Sıla, Bartın Kültür Merkezi’nde sahne alıyor. Kaçırmayın!",
     "kapak_yazi": "BARTIN KÜLTÜR SANAT GÜNLERİ"},
    {"slug": "amasrada-aksam-yemegi", "baslik": "Amasra’da Akşam Yemeği", "kisa": "Amasra’da Akşam Yemeği",
     "kategori": "mekanlar", "yeni": True, "tarih": "2026-10-12", "saat": "19:00", "mekan": "amasra-restoran",
     "aciklama": "Amasra’nın eşsiz manzarasında, deniz ürünleri ve özel lezzetler eşliğinde unutulmaz bir akşam sizi bekliyor."},
    {"slug": "the-last-band-canli-muzik", "baslik": "The Last Band – Canlı Müzik", "kisa": "The Last Band",
     "kategori": "canli-muzik", "yeni": False, "tarih": "2026-10-14", "saat": "21:00", "mekan": "zeytin-cafe-bar",
     "aciklama": "Rock ve popun en sevilen parçalarıyla The Last Band bu akşam sahnede!",
     "kapak_yazi": "Live Music"},
    # yalnızca "Bugünün Öne Çıkanları" listesinde görünenler (tasarımda açıklama metni yok)
    {"slug": "sila-konseri", "baslik": "Sıla Konseri", "kisa": "Sıla Konseri",
     "kategori": "canli-muzik", "yeni": False, "tarih": "2026-10-13", "saat": "20:00", "mekan": "bartin-kultur-merkezi",
     "aciklama": ""},
    {"slug": "deniz-urunleri-aksami", "baslik": "Deniz Ürünleri Akşamı", "kisa": "Deniz Ürünleri Akşamı",
     "kategori": "restoran-cafe", "yeni": False, "tarih": "2026-10-12", "saat": "19:00", "mekan": "amasra-restoran",
     "aciklama": ""},
]

# Anasayfa sıraları (tasarımdaki sırayla)
YENI_EKLENEN = ["emre-kaya-akustik-konser", "kale-cafede-canli-muzik-gecesi", "limanda-otel-ozel-konser-aksami",
                "bartin-kultur-sanat-gunleri", "amasrada-aksam-yemegi", "the-last-band-canli-muzik"]
ONE_CIKAN = ["emre-kaya-akustik-konser", "kale-cafede-canli-muzik-gecesi", "sila-konseri",
             "deniz-urunleri-aksami", "the-last-band-canli-muzik"]

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# ⏳ ÖRNEK METİNLER — kullanıcı "şimdilik örnek doldur" dedi (2026-10-04). Kendi metni gelince değiştir.
# Her sayfa: [(ara başlık ya da None, paragraf), ...]
SAYFA_METIN = {
    "hakkimizda": [
        (None, "Bartın Bildirim, Bartın’daki konser, canlı müzik, tiyatro, festival ve mekan etkinliklerini tek bir yerde toplayan yerel bir ilan sitesidir."),
        (None, "Amacımız basit: “Bu akşam Bartın’da ne var?” sorusunun cevabını aramak zorunda kalmadan bulabilmeniz. Mekanlar ve organizatörler etkinliklerini bize iletir, biz de herkesin görebileceği şekilde yayınlarız."),
        ("Kimler ilan verebilir?", "Bartın merkez ve ilçelerindeki kafe, restoran, otel, kültür merkezi ve etkinlik düzenleyen herkes İlan Ekle sayfasından ilan gönderebilir."),
    ],
    "iletisim": [
        (None, "İlan vermek, bir ilanı düzeltmek ya da kaldırmak için bize WhatsApp veya telefon üzerinden ulaşabilirsiniz."),
        (None, "Etkinliğinizi hızlıca yayınlamamız için başlık, mekan, tarih, saat ve varsa afiş görselini birlikte göndermeniz yeterlidir."),
    ],
    "gizlilik-politikasi": [
        (None, "Bu sayfa, Bartın Bildirim’i kullanırken hangi bilgilerin nasıl işlendiğini açıklar."),
        ("Topladığımız bilgiler", "Sitede üyelik yoktur. İlan Ekle formuna yazdığınız bilgiler sitede saklanmaz; formu gönderdiğinizde bu bilgiler WhatsApp üzerinden bize mesaj olarak iletilir."),
        ("Bilgilerin kullanımı", "İlan için gönderdiğiniz ad ve telefon bilgisi yalnızca ilanınızla ilgili sizinle iletişim kurmak için kullanılır, üçüncü kişilerle paylaşılmaz."),
        ("Çerezler", "Site, çalışması için zorunlu olanlar dışında çerez kullanmaz."),
        ("İletişim", "Bilgilerinizin silinmesini istemeniz hâlinde İletişim sayfasındaki numaradan bize ulaşabilirsiniz."),
    ],
    "kullanim-sartlari": [
        (None, "Bartın Bildirim’i kullanarak aşağıdaki şartları kabul etmiş sayılırsınız."),
        ("İlan içerikleri", "İlanlardaki tarih, saat, fiyat ve diğer bilgiler ilan sahibi tarafından iletilir. Etkinliğe gitmeden önce bilgileri mekanla teyit etmenizi öneririz."),
        ("İlan gönderimi", "Gönderilen ilanlar incelendikten sonra yayınlanır. Yanıltıcı, yasalara aykırı ya da Bartın dışı ilanlar yayınlanmayabilir veya kaldırılabilir."),
        ("Görseller", "İlanla birlikte gönderilen afiş ve fotoğrafların kullanım hakkının ilan sahibine ait olduğu kabul edilir."),
        ("Değişiklikler", "Bu şartlar gerektiğinde güncellenebilir; güncel hâli her zaman bu sayfadadır."),
    ],
}
