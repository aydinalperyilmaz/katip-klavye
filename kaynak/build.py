# Kâtip Klavye: tek dosyalı kaynaktan çok sayfalı site üretir.  Kullanım: python3 build.py [SITE_URL]
import re,json,os,sys,shutil,html,datetime
_D=os.path.dirname(os.path.abspath(__file__)); KAYNAK=os.path.join(_D,'KatipKlavye.html'); CIKTI=os.path.join(_D,'..','site')
SITE_URL=(sys.argv[1].rstrip('/') if len(sys.argv)>1 else '')   # alan adı belli olunca verilecek
SIRKET='Bosphorus Global İnşaat Turizm ve Dış Ticaret Limited Şirketi'; EPOSTA='iletisim@katipklavyesi.com'; ADRES='Halil Rıfat Paşa Mah. Yüzer Havuz Sk. Perpa Ticaret Merkezi B Blok No: 1/1 İç Kapı No: 2484 Şişli / İstanbul<br>İstanbul Ticaret Sicili No: 341373-5 · MERSİS No: 0180094375400001 · Şişli Vergi Dairesi'
TEMAS="<script>(function(){var k=true;try{var t=JSON.parse(localStorage.getItem('katipKlavye_v1')||'{}');k=!(t.temaV&&t.tema==='acik');}catch(e){}if(k)document.body.classList.add('koyu');})();</script>"
TEMAY="<script>(function(){var A='katipKlavye_v1',b=document.getElementById('temaDugme');function yaz(){if(b)b.textContent=document.body.classList.contains('koyu')?'\\u2600 Aydınlık mod':'\\u263e Karanlık mod';}yaz();if(b)b.addEventListener('click',function(){var k=!document.body.classList.contains('koyu');document.body.classList.toggle('koyu',k);try{var t=JSON.parse(localStorage.getItem(A)||'{}');t.tema=k?'koyu':'acik';t.temaV=1;localStorage.setItem(A,JSON.stringify(t));}catch(e){}yaz();});})();</script>"
ILET=EPOSTA if EPOSTA else 'yukarıdaki adrese yazılı olarak başvurabilirsiniz.'
EK=(' · '+EPOSTA) if EPOSTA else ''
h=open(KAYNAK,encoding='utf-8').read()
css=re.search(r'<style>(.*?)</style>',h,re.S).group(1)
scripts=re.findall(r'<script>(.*?)</script>',h,re.S); assert len(scripts)==2
veri_js,app_js=scripts
m=re.search(r"var SALONSES='([A-Za-z0-9+/=]+)';\n",app_js); ses_js="window.SALONSES='"+m.group(1)+"';\n"; app_js=app_js.replace(m.group(0),'')
govde=re.search(r'<body>(.*?)<script>',h,re.S).group(1)
header=re.search(r'<header>.*?</header>',govde,re.S).group(0)
main=re.search(r'<main>(.*?)</main>',govde,re.S).group(1)
extra=govde[govde.index('</main>')+7:]  # footer vb.
footer0=re.search(r'<footer>(.*?)</footer>',extra,re.S).group(1)
DOSYA={'ana':'index.html','sinav':'sinav-simulasyonu.html','hiz':'klavye-hiz-testi.html','ders':'klavye-dersleri.html','kelime':'kelime-egzersizi.html','hata':'zayif-tus-ve-kelime.html','okuma':'hizli-okuma.html','oyun':'klavye-oyunlari.html','taban':'adliye-taban-puanlari.html','ist':'istatistik.html','arac':'araclar.html','ayar':'ayarlar.html','maas':'memur-maasi-ne-eder.html'}
def nav_yap(aktif):
    def f(mm):
        s=mm.group(1); return '<a data-s="%s" href="%s"%s>%s</a>'%(s,DOSYA[s],' class="on"' if s==aktif else '',mm.group(2))
    x=re.sub(r'<button data-s="(\w+)"(?: class="on")?>(.*?)</button>',f,header)
    return x.replace('<div class="logo" data-git="ana" style="cursor:pointer">','<a class="logo" href="index.html" style="text-decoration:none;color:#fff">').replace('</span></div>\n <button id="menuAc"','</span></a>\n <button id="menuAc"')
YASAL='<p><a href="hakkinda-ve-iletisim.html">Hakkında ve iletişim</a> · <a href="gizlilik-ve-cerez.html">Gizlilik ve çerez politikası</a> · <a href="kullanim-sartlari.html">Kullanım şartları</a></p>'
u=json.loads(re.search(r'var u=(\[.*?\]);var o=\[\]',veri_js,re.S).group(1))
def sade(t): 
    t=t.lower().replace('i̇','i'); return re.sub(r'[^a-zçğıöşüâîû\s]','',t)
def set_listesi(yil):
    xs=sorted([x for x in u if yil in x['y']],key=lambda x:x['n'])
    li=''.join('<li><b>Metin %d</b> (%d kelime): %s…</li>'%(x['n'],len(x['m'].split()),html.escape(' '.join(sade(x['m']).split()[:10]))) for x in xs)
    return len(xs),'<ol class="soluk" style="padding-left:20px">'+li+'</ol>'
K='3 dakikada en az 90 doğru kelime, yanlış kelime oranı en çok yüzde 25, en çok 21 atlanan kelime'
S=[] # (dosya,bolum,ek_attr,title,desc,h1,icerik,index)
def ekle(dosya,bolum,title,desc,h1,icerik,attr='',idx=True): S.append((dosya,bolum,attr,title,desc,h1,icerik,idx))
ekle('index.html','ana','Kâtip Klavye: Zabıt Kâtipliği Klavye Sınavı Çalışma Sitesi','Zabıt, icra ve cezaevi kâtipliği uygulamalı klavye sınavına hazırlık: çıkmış sınav metinleri, geri sayımlı sınav modu, hata analizi ve adliye taban puanları. Ücretsiz, kayıt gerekmez.','Kâtiplik klavye sınavına hazırlık',
 '<p>Kâtip Klavye; zabıt kâtipliği, icra kâtipliği ve cezaevi kâtipliği (büro personeli) uygulamalı sınavına hazırlananlar için yapılmış bir çalışma sitesidir. Sınav kuralı açıktır: '+K+'. Burada bu kuralla, sınavdaki gibi küçük harfli ve noktalamasız metinlerle çalışırsınız.</p><p>Sitede <a href="sinav-simulasyonu.html">sınav simülasyonu</a>, <a href="zabit-katipligi-2026-sinav-metinleri.html">çıkmış sınav metinleri</a>, <a href="klavye-dersleri.html">F ve Q klavye dersleri</a>, <a href="klavye-hiz-testi.html">hız testi</a> ve <a href="adliye-taban-puanlari.html">adliyelerin kaç kelime ve kaç KPSS ile kapattığını gösteren tablo</a> bulunur. Üyelik yoktur; sonuçlarınız yalnızca kendi tarayıcınızda saklanır.</p>')
ekle('sinav-simulasyonu.html','sinav','Kâtiplik Klavye Sınavı Simülasyonu: 3 Dakika, 90 Kelime | Kâtip Klavye','Gerçek sınav kurallarıyla kâtiplik klavye denemesi: geri sayımlı sınav modu, işaretsiz yazma, sınav salonu sesi ve metin üzerinde hata incelemesi.','Kâtiplik klavye sınavı simülasyonu',
 '<p>Bu ekran uygulamalı sınavı taklit eder: metin üstte, yazma alanı altta durur ve süre 3 dakikadır. <b>Sınav modu</b> düğmesi 5’ten geri sayar, süreyi kendiliğinden başlatır ve işaretlemeyi kapatır. Süre bitince sonucunuz üç ölçüte göre değerlendirilir: '+K+'.</p><p>Çalışırken kelime işaretlemeyi açabilir, yazı tipini ve boyutunu değiştirebilir, imlalı ya da imlasız metin seçebilirsiniz. Sınav heyecanına alışmak için kalabalık bir salondaki klavye seslerini de açabilirsiniz.</p>')
for tur,dosya,ad,ek in (('zabit','zabit-katipligi-klavye-sinavi.html','Zabıt Kâtipliği','Adalet Bakanlığı Memur Sınav, Atama ve Nakil Yönetmeliğine göre zabıt kâtibi adayları uygulama sınavında bilgisayarla üç dakikada yanlışsız en az doksan kelime yazmak zorundadır.'),
                        ('icra','icra-katipligi-klavye-sinavi.html','İcra Kâtipliği','İcra kâtipliği alımlarında da uygulama sınavı yapılır; adayın üç dakikada yanlışsız ve tekrarsız en az doksan kelime yazması gerekir.'),
                        ('cte','cezaevi-katibi-klavye-sinavi.html','Cezaevi Kâtipliği','Ceza infaz kurumu kâtibi (büro personeli) alımlarında uygulamalı sınav, Bakanlığın Onparmak Klavye Programı ile 180 saniye üzerinden yapılır.')):
    ekle(dosya,'sinav',ad+' Klavye Sınavı Çalışma ve Deneme | Kâtip Klavye',ad+' uygulamalı klavye sınavına hazırlık: 3 dakikalık deneme sınavı, sınav modu, hata analizi ve çıkmış metinler.',ad+' klavye sınavına hazırlık',
     '<p>'+ek+' Değerlendirmede kelime bazlı sonuç esas alınır: '+K+'. Bu ölçütler Bakanlığın yayımladığı değerlendirme kriterlerinden alınmıştır; başvurduğunuz ilanı ayrıca okuyun.</p><p>Bu sayfada sınav türü “'+ad+'” olarak seçili açılır. Deneme bitince sonucunuz aynı ölçütlerle değerlendirilir ve hatalarınız metin üzerinde gösterilir.</p>','data-tur="%s"'%tur)
for yil in (2026,2025,2023,2022,2021):
    n,li=set_listesi(yil)
    ekle('zabit-katipligi-%d-sinav-metinleri.html'%yil,'sinav','%d Zabıt Kâtipliği Çıkmış Klavye Sınavı Metinleri (%d Metin) | Kâtip Klavye'%(yil,n),'%d zabıt kâtipliği uygulamalı sınavında yayımlanan %d metinle 3 dakikalık klavye denemesi yapın; sonucunuzu sınav ölçütleriyle görün.'%(yil,n),'%d zabıt kâtipliği çıkmış sınav metinleri'%yil,
     '<p>%d yılı zabıt kâtipliği uygulamalı sınavı için Adalet Bakanlığı Personel Genel Müdürlüğünün yayımladığı %d metin aşağıdadır. Üstteki “Metin” listesinden birini seçip 3 dakikalık deneme yapabilirsiniz.</p>'%(yil,n)+li,'data-set="c%d"'%yil)
ekle('klavye-hiz-testi.html','hiz','Klavye Hız Testi: Dakikada Kaç Kelime Yazıyorsunuz? | Kâtip Klavye','1, 2, 3 ve 5 dakikalık Türkçe klavye hız testi. Sınav metinlerinde en sık geçen kelimelerle ve hukuk terimleriyle ölçün.','Klavye hız testi','<p>Hız testi, dakikada kaç doğru kelime yazdığınızı ölçer. Kâtiplik sınavında baraj 3 dakikada 90 kelime, yani dakikada 30 kelimedir. Kelime türü olarak sınav metinlerinde en sık geçen kelimeleri, hukuk terimlerini ya da genel kelimeleri seçebilirsiniz.</p>')
ekle('klavye-dersleri.html','ders','F Klavye ve Q Klavye On Parmak Dersleri | Kâtip Klavye','Adım adım F klavye ve Q klavye on parmak dersleri: ekranda parmak gösteren klavye, yıldızlı 20 adım ve zayıf tuşunuza göre uyarlanan akıllı çalışma. Ücretsiz, kayıt gerekmez.','F ve Q klavye dersleri','<p>Adım adım on parmak bölümünde her adımda iki yeni tuş öğrenilir; ekrandaki klavye hangi tuşa hangi parmakla basılacağını gösterir. Akıllı çalışma, en yavaş ve en çok hata yaptığınız tuşu bulup o tuşun geçtiği kelimeleri verir. Serbest dersler temel sıradan başlar; üst sıra, alt sıra ve tüm harflerle devam eder. Ardından hukuk terimleri ile rakam ve sayı çalışması gelir. Klavye düzenini Ayarlar bölümünden F ya da Q olarak seçebilirsiniz.</p>')
ekle('kelime-egzersizi.html','kelime','Kelime Egzersizi: Sınav Metinlerinde En Sık Geçen Kelimeler | Kâtip Klavye','Kâtiplik sınav metinlerinde en sık geçen kelimeleri, hukuk terimlerini ve uzun kelimeleri art arda yazarak çalışın.','Kelime egzersizi','<p>Bir kelimeyi art arda birkaç kez yazmak, o kelimeyi parmak hafızasına yerleştirmenin en hızlı yoludur. Listeler çıkmış sınav metinlerindeki kelime sıklığına göre hazırlanmıştır.</p>')
ekle('zayif-tus-ve-kelime.html','hata','Zayıf Tuş ve Hatalı Kelime Çalışması | Kâtip Klavye','En çok hata yaptığınız tuşları ve kelimeleri görün; yalnızca onlarla çalışın.','Zayıf tuş ve kelime çalışması','<p>Her denemede yanlış bastığınız tuşlar ve yanlış yazdığınız kelimeler burada birikir. Klavye haritası hangi harflerde zorlandığınızı gösterir; tek düğmeyle yalnızca o harfleri içeren kelimelerle çalışırsınız.</p>')
ekle('hizli-okuma.html','okuma','Hızlı Okuma Testi ve Kelime Akışı Egzersizi | Kâtip Klavye','Okuma hızınızı ölçün ve kelime akışı egzersiziyle geliştirin. Metni hızlı okuyan, hızlı yazar.','Hızlı okuma','<p>Klavye sınavında metni gözle takip edip yazarsınız; okuma hızınız yazma hızınızı doğrudan etkiler. Okuma hızı testi dakikada kaç kelime okuduğunuzu ölçer, kelime akışı egzersizi gözünüzü hızlı okumaya alıştırır.</p>')
ekle('klavye-oyunlari.html','oyun','Klavye Oyunları: Kelime Yağmuru ve Rakiple Yarış | Kâtip Klavye','Oynarken hızlanın: düşen kelimeleri yazın ya da seçtiğiniz hızdaki rakibe karşı yarışın.','Klavye oyunları','<p>Kelime Yağmuru’nda kelimeler yukarıdan düşer; yere değmeden yazmanız gerekir. Rakiple Yarış’ta sabit hızda yazan bir rakibe karşı 60 kelimelik metni önce bitirmeye çalışırsınız.</p>')
ekle('adliye-taban-puanlari.html','taban','Hangi Adliye Kaç Kelime ve Kaç KPSS ile Kapattı? | Kâtip Klavye','Zabıt ve icra kâtipliği alımlarında adliyelere göre klavye taban kelime sayıları ve KPSS taban puanları. Kelime sayınızı yazın, nerelere yettiğini görün.','Hangi adliye kaç kelime ve kaç KPSS ile kapattı?','<p>Bu tablo, geçmiş alımlarda her adliyeye giren son adayın klavye kelime sayısını ve KPSS puanını gösterir. Rakamlar resmî değildir; adayların bildirdiği sonuçlardan derlenmiştir. Kesin bilgi için başvurduğunuz adalet komisyonunun ilanına bakın.</p><p>Her adliyenin kendi sayfası da var: <a href="adliyeler.html">adliyelere göre taban kelime ve KPSS puanları</a>.</p>')
ekle('araclar.html','arac','Kâtiplik Sınavı Araçları: Baraj Hedefi, Hız Çevirici, Kalan Gün | Kâtip Klavye','Baraja ne kadar kaldığını görün, kelime hızını vuruşa çevirin, sınava kalan günü sayın.','Araçlar','<p>Baraj hedefi son sınav denemelerinizin ortalamasını barajla karşılaştırır. Hız çevirici dakikadaki kelime sayısını 3 dakikalık toplama ve yaklaşık vuruşa çevirir.</p>')
ekle('istatistik.html','ist','İstatistik | Kâtip Klavye','Deneme geçmişiniz ve gelişim grafiğiniz.','İstatistik','',idx=False)
ekle('ayarlar.html','ayar','Ayarlar | Kâtip Klavye','Klavye düzeni, süre, baraj ve görünüm ayarları.','Ayarlar','',idx=False)
BUGUN=datetime.date.today().isoformat()
def kafa(title,desc,dosya,idx=True):
    can='<link rel="canonical" href="%s/%s">\n'%(SITE_URL,'' if dosya=='index.html' else dosya) if SITE_URL else ''
    return '<!DOCTYPE html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s</title>\n<meta name="description" content="%s">\n%s%s<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:type" content="website">\n<link rel="stylesheet" href="app.css">\n</head>\n'%(html.escape(title),html.escape(desc,True),can,'' if idx else '<meta name="robots" content="noindex">\n',html.escape(title,True),html.escape(desc,True))
shutil.rmtree(CIKTI,ignore_errors=True); os.makedirs(CIKTI)
open(CIKTI+'/app.css','w',encoding='utf-8').write(css+'\n#seoMetin h1{font-size:22px}\n.yazi{max-width:820px}.yazi h1{font-size:26px}.yazi h2{font-size:19px;margin-top:22px}\n')
open(CIKTI+'/veri-metinler.js','w',encoding='utf-8').write(veri_js); open(CIKTI+'/app.js','w',encoding='utf-8').write(app_js); open(CIKTI+'/ses.js','w',encoding='utf-8').write(ses_js)
for dosya,bolum,attr,title,desc,h1,icerik,idx in S:
    seo='<div class="kart" id="seoMetin"><h1>%s</h1>%s</div>'%(html.escape(h1),icerik) if icerik else ''
    sayfa=kafa(title,desc,dosya,idx)+'<body data-site="1" data-bolum="%s" %s>\n@@TS@@%s\n<main>%s\n%s\n</main>\n<footer>%s%s</footer>\n<script src="veri-metinler.js"></script>\n<script src="app.js"></script>\n</body>\n</html>\n'%(bolum,attr,nav_yap(bolum),main,seo,footer0,YASAL)
    open(os.path.join(CIKTI,dosya),'w',encoding='utf-8').write(sayfa)
# ---- yasal sayfalar (uygulama kodu olmadan)
KUCUK="<script>try{var v=JSON.parse(localStorage.getItem('katipKlavye_v1')||'{}');if(v.tema==='koyu')document.body.classList.add('koyu');}catch(e){}document.getElementById('menuAc').addEventListener('click',function(){document.querySelector('nav').classList.toggle('acik');});</script>"
def yasal(dosya,title,desc,govde_html):
    open(os.path.join(CIKTI,dosya),'w',encoding='utf-8').write(kafa(title,desc,dosya)+'<body>\n@@TS@@%s\n<main><div class="kart yazi">%s<p class="soluk">Son güncelleme: %s</p></div></main>\n<footer>%s%s</footer>\n@@TY@@%s\n</body>\n</html>\n'%(nav_yap(''),govde_html,BUGUN,footer0,YASAL,KUCUK))
yasal('hakkinda-ve-iletisim.html','Hakkında ve İletişim | Kâtip Klavye','Kâtip Klavye nedir, kim işletir, nasıl iletişim kurulur.',
 '<h1>Hakkında ve iletişim</h1><p>Kâtip Klavye; zabıt kâtipliği, icra kâtipliği ve cezaevi kâtipliği uygulamalı klavye sınavına hazırlananlar için hazırlanmış bağımsız bir çalışma sitesidir. Adalet Bakanlığı ya da başka bir resmî kurumla bağlantısı yoktur.</p><h2>Site sahibi</h2><p>'+SIRKET+'<br>'+ADRES+'</p><h2>İletişim</h2><p>Görüş, hata bildirimi ve içerik düzeltme talepleri için: '+ILET+'</p><h2>İçerik ve veriler</h2><p>“Çıkmış” etiketli metinler Adalet Bakanlığı Personel Genel Müdürlüğünün uygulamalı sınavlar için yayımladığı metinlerdir. Diğer metinler çalışma amacıyla yazılmış özgün metinlerdir. Adliye taban kelime sayıları ve KPSS puanları resmî değildir; adayların bildirdiği sonuçlardan derlenmiştir ve hatalı olabilir. Yanlış olduğunu düşündüğünüz bir bilgiyi yukarıdaki adrese bildirebilirsiniz.</p>')
yasal('gizlilik-ve-cerez.html','Gizlilik ve Çerez Politikası | Kâtip Klavye','Kâtip Klavye hangi verileri saklar, çerez kullanır mı.',
 '<h1>Gizlilik ve çerez politikası</h1><h2>Hangi veriler saklanır?</h2><p>Sitede üyelik yoktur; ad, e-posta ya da telefon gibi kişisel bilgi istenmez. Deneme sonuçlarınız, hatalı kelimeleriniz ve ayarlarınız yalnızca kullandığınız tarayıcının yerel depolama alanında tutulur. Bu veriler sunucularımıza gönderilmez ve başka cihazlarda görünmez.</p><h2>Verilerimi nasıl silerim?</h2><p>İstatistik bölümündeki “Tüm geçmişi sil” ve Zayıf Tuş ve Kelime bölümündeki temizleme düğmeleriyle silebilirsiniz. Tarayıcınızın site verilerini temizlemesi de tüm kayıtları kaldırır.</p><h2>Ziyaret istatistiği</h2><p>Sitede kaç kişinin hangi sayfayı ziyaret ettiğini görmek için Cloudflare Web Analytics kullanılır. Bu hizmet çerez kullanmaz, tarayıcınızda iz bırakmaz ve ziyaretçileri tek tek tanımlamaz; yalnızca sayfa görüntüleme sayısı, yönlendiren site, ülke ve tarayıcı türü gibi toplu bilgiler tutulur.</p><h2>Çerezler</h2><p>Site çerez kullanmamaktadır. İleride reklam hizmeti eklenirse bu hizmet çerez kullanabilir; o durumda bu sayfa güncellenecek ve zorunlu olmayan çerezler için onayınız istenecektir.</p><h2>Üçüncü taraf bağlantıları</h2><p>Sitede resmî kurum sayfalarına bağlantılar bulunur. Bu sitelerin gizlilik uygulamalarından Kâtip Klavye sorumlu değildir.</p><h2>Veri sorumlusu ve iletişim</h2><p>'+SIRKET+EK+'</p>')
yasal('kullanim-sartlari.html','Kullanım Şartları | Kâtip Klavye','Kâtip Klavye kullanım şartları ve sorumluluk sınırları.',
 '<h1>Kullanım şartları</h1><h2>Hizmetin niteliği</h2><p>Kâtip Klavye bir çalışma aracıdır. Buradaki deneme sonuçları gerçek sınav sonucunuzu garanti etmez. Puanlama, Bakanlığın yayımladığı değerlendirme kriterleri esas alınarak hazırlanmıştır; ancak resmî sınav programıyla birebir aynı sonucu vereceği taahhüt edilmez.</p><h2>Bilgilerin doğruluğu</h2><p>Sınav kuralları, süre ve baraj bilgileri resmî ilan ve yönetmeliklerden derlenmiştir ve değişebilir. Adliye taban kelime sayıları ve KPSS puanları resmî değildir. Başvuru ve tercih kararlarınızı vermeden önce ilgili adalet komisyonunun ve Bakanlığın güncel ilanlarını esas alın.</p><h2>Sorumluluk</h2><p>Site “olduğu gibi” sunulur. Sitedeki bilgilere dayanarak verilen kararlardan doğabilecek sonuçlardan site sahibi sorumlu tutulamaz.</p><h2>Kullanım</h2><p>Siteyi kişisel çalışma amacıyla kullanabilirsiniz. Sitenin işleyişini bozacak, otomatik yollarla içerik toplayacak ya da başkalarının kullanımını engelleyecek davranışlar yasaktır.</p><h2>Değişiklikler</h2><p>Bu şartlar güncellenebilir; güncel metin bu sayfada yayımlanır.</p><h2>İletişim</h2><p>'+SIRKET+EK+'</p>')
yasal('404.html','Sayfa bulunamadı | Kâtip Klavye','Aradığınız sayfa bulunamadı.','<h1>Sayfa bulunamadı</h1><p>Aradığınız sayfa taşınmış ya da hiç olmamış olabilir. <a href="index.html">Ana sayfaya dönün</a> ya da <a href="sinav-simulasyonu.html">sınav simülasyonunu açın</a>.</p>')

# ---- adliye sayfalari (taban verilerinden otomatik)
def _dizi(ad):
    i=app_js.index(ad); j=app_js.index('[[',i); d=0
    for k in range(j,len(app_js)):
        c=app_js[k]
        if c=='[': d+=1
        elif c==']':
            d-=1
            if d==0: return json.loads(app_js[j:k+1])
T26=_dizi('var TABAN26='); _tb=app_js[app_js.index('var TB={'):]
def _tbl(k): 
    global _tb
    i=_tb.index('\n'+k+':{'); j=_tb.index('[[',i); d=0
    for q in range(j,len(_tb)):
        c=_tb[q]
        if c=='[': d+=1
        elif c==']':
            d-=1
            if d==0: return json.loads(_tb[j:q+1])
K25=_tbl('k25'); KP26=_tbl('kp26'); MOD=_tbl('mod'); I21=_tbl('i21')
def slug(s):
    s=s.replace('İ','i').replace('I','i').lower()
    for a,c in zip('çğıöşüâîû','cgiosuaiu'): s=s.replace(a,c)
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def temel(ad):
    ad=ad.replace('Afyonkarahisar','Afyon').replace('Doğubeyazıt','Doğubayazıt')
    m=re.match(r'^(.*?)\s*\((Genel|Öncelikli)\)$',ad)
    return (m.group(1),m.group(2)) if m else (ad,'')
A={}
def al(ad):
    return A.setdefault(ad,{'ad':ad,'k26':None,'kp26':None,'k25':[],'mod':None,'i21':None})
for x in T26: al(temel(x[0])[0])['k26']=(x[1],x[2])
for x in KP26: al(temel(x[0])[0])['kp26']=x[1:4]
for x in K25:
    a,tur=temel(x[0]); al(a)['k25'].append({'tur':tur or 'Genel','kon':x[1],'kel':x[2],'kp':x[3:6],'yak':x[6]})
for x in MOD:
    if x[0] in A: A[x[0]]['mod']=x[1]
for x in I21:
    if x[0] in A: A[x[0]]['i21']=(x[1],x[3])
def tamad(ad):
    ad='Afyonkarahisar' if ad=='Afyon' else ad
    return ad[:-4]+' Bölge Adliye Mahkemesi' if ad.endswith(' BAM') else (ad[:-4]+' Bölge İdare Mahkemesi' if ad.endswith(' BİM') else ad+' Adliyesi')
def vg(v): return '—' if v is None else ('%.2f'%v).replace('.',',')
def dosya_ad(ad):
    ad='Afyonkarahisar' if ad=='Afyon' else ad
    return (slug(ad[:-4])+'-bolge-adliye-mahkemesi' if ad.endswith(' BAM') else slug(ad)+'-adliyesi')+'-zabit-katipligi-taban-puani.html'
ADL=sorted(A.values(),key=lambda r:slug(r['ad']))
UYARI='<p class="soluk"><b>Bu rakamlar resmî değildir.</b> Adayların ve sınav hazırlık hesaplarının paylaştığı sonuçlardan derlenmiştir, hatalı ya da eksik olabilir. Başvuru kararınızı vermeden önce ilgili adalet komisyonunun kendi ilanına bakın. Yanlış gördüğünüz bir rakamı '+(EPOSTA or 'bize')+' adresine bildirebilirsiniz.</p>'
ADL_URL=[]
for n,r in enumerate(ADL):
    ad=r['ad']; T=tamad(ad); cum=[]; sat=''
    if r['k26']:
        cum.append('2026 alımında %s <b>%s%d kelime</b> ile kapattı'%(T,'yaklaşık ' if r['k26'][1] else '',r['k26'][0]))
    kp=r['kp26']
    if r['k26'] or kp:
        sat+='<tr><td><b>2026</b></td><td>—</td><td class="buyuk">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%((('≈ ' if r['k26'][1] else '')+str(r['k26'][0])+' <small>kelime</small>') if r['k26'] else '—',vg(kp[0]) if kp else '—',vg(kp[1]) if kp else '—',vg(kp[2]) if kp else '—')
    for z in r['k25']:
        sat+='<tr><td><b>2025</b>%s</td><td>%s</td><td class="buyuk">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(' <small>(öncelikli)</small>' if z['tur']=='Öncelikli' else '',('%d kişi'%z['kon']) if z['kon'] else '—',(('≈ ' if z['yak'] else '')+'%d <small>kelime</small>'%z['kel']) if z['kel'] else '—',vg(z['kp'][0]),vg(z['kp'][1]),vg(z['kp'][2]))
    g25=[z for z in r['k25'] if z['tur']=='Genel' and z['kel']]
    if g25: cum.append('2025 alımında <b>%d kelime</b> ile kapatmıştı'%g25[0]['kel'])
    if r['k26'] and g25:
        f=r['k26'][0]-g25[0]['kel']; cum.append('yani taban bir yılda %s'%('%d kelime yükseldi'%f if f>0 else ('%d kelime düştü'%-f if f<0 else 'değişmedi')))
    en=min([x for x in [r['k26'][0] if r['k26'] else None]+[z['kel'] for z in r['k25'] if z['tur']=='Genel'] if x] or [0])
    son=r['k26'][0] if r['k26'] else (g25[0]['kel'] if g25 else 0)
    giris='<p>'+('; '.join(cum)+'.' if cum else T+' için elimizde klavye taban kelime sayısı yok.')+' Taban kelime, o adliyeye yerleşen son adayın uygulamalı sınavda 3 dakikada yazdığı doğru kelime sayısıdır. Baraj her yerde 90 kelimedir; kontenjan az, başvuru çok olduğunda taban barajın üstüne çıkar.</p>'
    ek=''
    if r['mod']: ek+='<h2>Sınavda kullanılan klavye</h2><p>%s uygulamalı sınavında kullanıldığı bildirilen klavye: <b>%s</b>. Sınavdaki klavyeye benzer bir klavyeyle çalışmak tuş hissine alışmanızı sağlar.</p>'%(T,html.escape(r['mod']))
    if r['i21']: ek+='<h2>İcra kâtipliği</h2><p>2021 icra kâtipliği alımında %s için bildirilen taban: <b>%d kelime</b>, KPSS %s.</p>'%(ad,r['i21'][0],vg(r['i21'][1]))
    hesap=''
    if son:
        hesap='<h2>Kelime sayınız yetiyor mu?</h2><div class="satir"><label>3 dakikada yazdığınız doğru kelime<input type="number" id="adK" min="0" max="400" placeholder="örnek: %d"></label></div><p id="adS" class="okuma">Kelime sayınızı yazın; %s son tabanıyla (%d kelime) karşılaştıralım.</p><script>document.getElementById("adK").addEventListener("input",function(){var n=Number(this.value)||0,t=%d,s=document.getElementById("adS");if(!n){s.textContent="Kelime sayınızı yazın.";return;}s.innerHTML=n>=t?"<b>Yetiyor.</b> Son tabanın "+(n-t)+" kelime üstündesiniz. Taban her alımda değişir; payınız ne kadar genişse o kadar iyi.":"<b>"+(t-n)+" kelime eksik.</b> Son taban "+t+" kelime. Sınav simülasyonunda bu hedefle çalışın."+(n<90?" Ayrıca 90 kelimelik barajın da altındasınız.":"");});</script>'%(son,T,son,son)
    onc=ADL[n-1]; snr=ADL[(n+1)%len(ADL)]
    govde='<h1>%s zabıt kâtipliği taban kelime ve KPSS puanı</h1>%s'%(T,giris)
    if sat: govde+='<div style="overflow-x:auto"><table><tr><th>Alım</th><th>Kontenjan</th><th>Kaç kelime ile kapattı</th><th>KPSS lise</th><th>KPSS önlisans</th><th>KPSS lisans</th></tr>%s</table></div>'%sat
    govde+=UYARI+hesap+ek
    govde+='<h2>Bu adliyeye hazırlanın</h2><p><a class="btn" href="sinav-simulasyonu.html">Sınav simülasyonunu başlat</a> <a class="btn gri" href="zabit-katipligi-2026-sinav-metinleri.html">Çıkmış sınav metinleri</a> <a class="btn gri" href="klavye-dersleri.html">Klavye dersleri</a></p>'
    govde+='<p class="soluk">Diğer adliyeler: <a href="%s">%s</a> · <a href="%s">%s</a> · <a href="adliyeler.html">Bütün adliyeler</a> · <a href="adliye-taban-puanlari.html">Karşılaştırmalı tablo</a></p>'%(dosya_ad(onc['ad']),html.escape(tamad(onc['ad'])),dosya_ad(snr['ad']),html.escape(tamad(snr['ad'])))
    bas='%s Zabıt Kâtipliği Taban Kelime ve KPSS Puanı | Kâtip Klavye'%T
    des='%s zabıt kâtipliği alımında kaç kelime ve kaç KPSS ile kapattı? %s Kelime sayınızı yazın, yetip yetmediğini görün.'%(T,re.sub('<[^>]+>','','; '.join(cum[:2]))+'.' if cum else '')
    yasal(dosya_ad(ad),bas,des[:300],govde); ADL_URL.append(dosya_ad(ad))
_li=''.join('<li><a href="%s">%s</a>%s</li>'%(dosya_ad(r['ad']),html.escape(tamad(r['ad'])),(' — %s%d kelime'%('2026: ' if r['k26'] else '2025: ',r['k26'][0] if r['k26'] else [z['kel'] for z in r['k25'] if z['kel']][0])) if (r['k26'] or [z for z in r['k25'] if z['kel']]) else '') for r in ADL)
yasal('adliyeler.html','Adliyelere Göre Zabıt Kâtipliği Taban Kelime ve KPSS Puanları | Kâtip Klavye','%d adliye ve bölge adliye mahkemesi için zabıt kâtipliği klavye taban kelime sayıları ve KPSS taban puanları. Adliyenizi seçin.'%len(ADL),
 '<h1>Adliyelere göre zabıt kâtipliği taban kelime ve KPSS puanları</h1><p>Aşağıda %d adliye ve bölge adliye mahkemesinin sayfası var. Her sayfada o adliyenin son alımlardaki taban kelime sayısı, KPSS taban puanları, kontenjanı ve sınavda kullanılan klavye bilgisi yer alır. Hepsini tek tabloda karşılaştırmak için <a href="adliye-taban-puanlari.html">karşılaştırmalı tabloyu</a> kullanın.</p>%s<ul style="columns:2;padding-left:18px;line-height:1.9">%s</ul>'%(len(ADL),UYARI,_li))
ADL_URL.append('adliyeler.html')

# ---- memur maaşı sayfası (maas.katipklavyesi.com gömülü)
MAAS_GOVDE=('<h1>Memur maaşın ne eder?</h1><p>Maaşını yaz; kaç gram altın, kaç dolar ettiğini, Ocak\'tan beri enflasyon karşısında ne kadar eridiğini ve 2027 zammının neyi karşılayacağını gör. '
 'Hazır düğmelerde en düşük memur maaşı (aile yardımı dahil, Temmuz 2026: 70.224 TL), en düşük emekli aylığı ve asgari ücret var; kendi maaşını da yazabilirsin. Yazdığın rakam yalnızca kendi tarayıcında kalır.</p>'
 '<p><a class="btn" href="https://maas.katipklavyesi.com/?yukle=1" target="_blank" rel="noopener">Uygulamayı telefona indir</a> <a class="btn gri" href="https://maas.katipklavyesi.com/" target="_blank" rel="noopener">Tam ekran aç</a></p>'
 '<p class="soluk">Asgari ücret: Çalışma ve Sosyal Güvenlik Bakanlığı · Enflasyon: TÜİK · Altın ve dolar: piyasa ortalamaları. Sonuçlar yaklaşıktır. <a href="https://maas.katipklavyesi.com/" target="_blank" rel="noopener">Hesaplayıcıyı tam ekran aç</a></p>')
MAAS_CER=('<iframe id="maasCerceve" title="Maaşın Ne Eder hesaplayıcısı" style="width:100%;height:1400px;border:0;border-radius:14px;display:block;margin-top:16px;background:transparent"></iframe>'
 "<script>(function(){var c=document.getElementById('maasCerceve');c.src='https://maas.katipklavyesi.com/?gom=1&tema='+(document.body.classList.contains('koyu')?'koyu':'acik');"
 "window.addEventListener('message',function(e){if(e.origin!=='https://maas.katipklavyesi.com'||!e.data||typeof e.data.mneH!=='number')return;c.style.height=Math.max(600,Math.min(20000,e.data.mneH))+'px';});})();</script>")
open(os.path.join(CIKTI,DOSYA['maas']),'w',encoding='utf-8').write(kafa('Memur Maaşı Kaç Gram Altın, Kaç Dolar? 2026 Maaş Hesaplama | Kâtip Klavye','Memur maaşın kaç gram altın, kaç dolar ediyor? Ocak\'tan beri enflasyonla ne kadar eridi, 2027 zammı neyi karşılar? En düşük memur maaşıyla hemen hesapla.',DOSYA['maas'])+'<body>\n@@TS@@%s\n<main><div class="kart">%s</div>%s</main>\n<footer>%s%s</footer>\n@@TY@@%s\n</body>\n</html>\n'%(nav_yap('maas'),MAAS_GOVDE,MAAS_CER,footer0,YASAL,KUCUK))
ADL_URL.append(DOSYA['maas'])
open(CIKTI+'/robots.txt','w').write('User-agent: *\nAllow: /\n'+('Sitemap: %s/sitemap.xml\n'%SITE_URL if SITE_URL else ''))
if SITE_URL:
    urls=[d for d,_,_,_,_,_,_,i in S if i]+['hakkinda-ve-iletisim.html','gizlilik-ve-cerez.html','kullanim-sartlari.html']+ADL_URL
    open(CIKTI+'/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n'%(SITE_URL,'' if d=='index.html' else d,BUGUN) for d in urls)+'</urlset>\n')
print(len(os.listdir(CIKTI)),'dosya'); 
for f in sorted(os.listdir(CIKTI)): print('  %7d %s'%(os.path.getsize(os.path.join(CIKTI,f)),f))

import glob
for _f in glob.glob(os.path.join(CIKTI,'*.html')):
    _t=open(_f,encoding='utf-8').read()
    if '@@TS@@' in _t or '@@TY@@' in _t:
        open(_f,'w',encoding='utf-8').write(_t.replace('@@TS@@',TEMAS+'\n').replace('@@TY@@',TEMAY))

# onbellek kirici: js/css adreslerine icerik ozeti ekle
import hashlib
def _oz(ad): return hashlib.md5(open(os.path.join(CIKTI,ad),'rb').read()).hexdigest()[:8]
_v={a:_oz(a) for a in ('app.js','app.css','veri-metinler.js')}
for _f in glob.glob(os.path.join(CIKTI,'*.html')):
    _t=open(_f,encoding='utf-8').read()
    for a,h in _v.items(): _t=_t.replace('"%s"'%a,'"%s?v=%s"'%(a,h))
    open(_f,'w',encoding='utf-8').write(_t)
