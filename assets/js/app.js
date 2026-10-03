/* Bartın Bildirim — app.js
   1) mobil menü  2) Kategoriler açılır menüsü  3) arama sayfası  4) İlan Ekle formu → WhatsApp / e-posta  5) paylaş */
(function () {
  var d = document;

  var ac = d.querySelector('.menu-ac'), menu = d.getElementById('menu');
  if (ac && menu) {
    ac.addEventListener('click', function () {
      var acik = menu.classList.toggle('acik');
      ac.setAttribute('aria-expanded', acik ? 'true' : 'false');
      ac.setAttribute('aria-label', acik ? 'Menüyü kapat' : 'Menüyü aç');
      d.body.classList.toggle('menu-acik', acik);
    });
  }

  var acilir = d.querySelector('.acilir'), adg = acilir && acilir.querySelector('.acilir-dg');
  if (adg) {
    adg.addEventListener('click', function (e) {
      e.stopPropagation();
      var acik = acilir.classList.toggle('acik');
      adg.setAttribute('aria-expanded', acik ? 'true' : 'false');
    });
    d.addEventListener('click', function (e) {
      if (!acilir.contains(e.target)) { acilir.classList.remove('acik'); adg.setAttribute('aria-expanded', 'false'); }
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { acilir.classList.remove('acik'); adg.setAttribute('aria-expanded', 'false'); }
    });
  }

  // arama sayfası
  var dz = d.getElementById('ara-dizin');
  if (dz) {
    var veri = JSON.parse(dz.textContent), q = d.getElementById('ara-q'),
        sonuc = d.getElementById('ara-sonuc'), ozet = d.getElementById('ara-ozet');
    var norm = function (s) {
      return (s || '').toLocaleLowerCase('tr').replace(/[’']/g, '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
    };
    var esc = function (s) { var t = d.createElement('span'); t.textContent = s; return t.innerHTML; };
    var ikon = function (p) { return '<svg class="ik" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>'; };
    var TAKVIM = '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        KONUM = '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>';
    var kok = '../';
    var ciz = function () {
      var t = norm(q.value.trim());
      if (!t) { sonuc.innerHTML = ''; ozet.textContent = 'Aramak istediğiniz etkinliği, mekanı ya da sanatçıyı yazın.'; return; }
      var parca = t.split(/\s+/);
      var bulunan = veri.filter(function (i) {
        var h = norm([i.b, i.a, i.m, i.k].join(' '));
        return parca.every(function (p) { return h.indexOf(p) !== -1; });
      });
      ozet.textContent = bulunan.length ? '“' + q.value.trim() + '” için ' + bulunan.length + ' sonuç' : '“' + q.value.trim() + '” için sonuç bulunamadı.';
      sonuc.innerHTML = bulunan.map(function (i) {
        return '<article class="ilan" style="grid-template-columns:minmax(0,1fr) auto"><div class="ilan-govde">' +
          '<div class="rozetler"><span class="rozet" style="--r:' + i.r + '">' + esc(i.k) + '</span></div>' +
          '<h2 class="ilan-baslik"><a href="' + kok + i.y + '">' + esc(i.b) + '</a></h2>' +
          (i.a ? '<p class="ilan-acik">' + esc(i.a) + '</p>' : '') +
          '<ul class="ilan-bilgi"><li>' + ikon(TAKVIM) + '<span>' + esc(i.t) + '<i>|</i>' + esc(i.s) + '</span></li>' +
          '<li>' + ikon(KONUM) + '<a href="' + kok + i.my + '">' + esc(i.m) + '</a></li></ul></div>' +
          '<a class="dg dg-cizgi ilan-dg" href="' + kok + i.y + '">Detaylar</a></article>';
      }).join('');
    };
    q.value = new URLSearchParams(location.search).get('q') || '';
    q.addEventListener('input', ciz);
    ciz();
  }

  // İlan Ekle formu
  var form = d.getElementById('ilan-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var satir = ['Bartın Bildirim — yeni ilan'];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.value) satir.push(el.name + ': ' + el.value);
      });
      var metin = satir.join('\n'), wa = form.dataset.wa, ep = form.dataset.eposta;
      if (wa) window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(metin), '_blank', 'noopener');
      else if (ep) location.href = 'mailto:' + ep + '?subject=' + encodeURIComponent('Yeni ilan') + '&body=' + encodeURIComponent(metin);
    });
  }

  // paylaş
  var pb = d.querySelector('.paylas');
  if (pb) {
    pb.addEventListener('click', function () {
      var veri = { title: pb.dataset.baslik, url: location.href };
      if (navigator.share) { navigator.share(veri).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () {
        var eski = pb.innerHTML; pb.textContent = 'Bağlantı kopyalandı';
        setTimeout(function () { pb.innerHTML = eski; }, 1800);
      });
    });
  }
})();
