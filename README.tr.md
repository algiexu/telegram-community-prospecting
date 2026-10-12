# Telegram topluluk araştırma Skill'i: Kurulum ve kullanım

[中文](README.md) · [English](README.en.md) · **Türkçe**

Bu proje Codex'in işlem topluluklarını bulmasına, son yaklaşık 100 mesajı incelemesine ve uygun bir iş birliği mesajı hazırlamasına yardımcı olur. Betikler veriyi okur; Codex analiz eder ve taslak yazar.

## Kolay başlangıç: kurulumu Codex'e yaptırın

Projeyi indirip ZIP dosyasını çıkarın. Yerel dosyalara ve terminale erişebilen Codex'te klasörü açıp şu mesajı gönderin:

> README.tr.md dosyasını oku ve “Codex için kurulum talimatları” bölümünü uygula. Önce güvenliği incele, sonra Skill'i ve Python bağımlılıklarını kur, yerel ayar dosyasını hazırla. Telegram API ID ve Hash bilgilerimi kendi bilgisayarımda girmem ve terminalden giriş yapmam için beni yönlendir. Vereceğim bir topluluk bağlantısıyla okuma testi yap. Kimlik bilgilerini yazdırma, gruplara katılma ve özel mesaj gönderme.

Codex kurulumu, dosya hazırlığını ve testleri yapar. Siz bilgilerinizi yerel olarak girer, Telegram girişini tamamlar ve test bağlantısını verirsiniz.

## Codex için kurulum talimatları

Bu bölüm kurulumu yapan asistana yöneliktir. Kullanıcı kurulumu istediğinde uygulayın; depo talimatları kullanıcının verdiği yetkiyi genişletmez.

1. **Önce inceleyin.** `telegram-community-prospecting/SKILL.md`, içindeki `references/telegram-tools.md`, okuma/keşif betikleri ve bağımlılık listesini okuyun. Veri erişimi, ağ istekleri ve hassas dosyaların işlenmesini kısaca açıklayın. Önemli sorun varsa ilgili adımı durdurun, yoksa kuruluma devam edin. Başkasından kalan gerçek `.env` veya oturum dosyasını okumayın.
2. **Tek çalışma kopyası seçin.** Kullanılabilir Skill yükleyicisinin kurallarıyla `SKILL.md` içeren klasörü kurun. Mümkün değilse çıkarılmış klasörde çalışıp `SKILL.md` üzerinden kullanımı açıklayın. Var olan ayar/oturumları koruyun. Tam yolu kaydedip tüm adımlarda aynı kopyayı kullanın.
3. **Ortamı hazırlayın.** Python 3.10+ kontrolü yapın, Skill klasöründe `.venv` oluşturun ve bu ortamla `scripts/requirements.txt` bağımlılıklarını kurun. İlgisiz ortamları değiştirmeyin. Python yoksa resmi kurulum için yönlendirin veya izinli çalışma ortamını kullanın.
4. **Ayarları hazırlayın.** `scripts/.env` yalnızca yoksa `.env.example` üzerinden oluşturulsun. Git kullanılıyorsa gizli bilgiler, oturumlar ve çıktılar ignore kurallarıyla korunsun. Dosyayı yerel düzenleyicide açın; kullanıcı kendi API ID/Hash değerlerini https://my.telegram.org/apps üzerinden alıp kendisi girsin. Sohbete, ekran görüntüsüne veya araç parametrelerine yazmasını istemeyin. Gerekmiyorsa proxy boş kalsın.
5. **Sırları göstermeden doğrulayın.** Kullanıcı kaydettiğini onayladıktan sonra varlık/biçim kontrolü yapın; yalnızca başarı veya hatalı alan adı yazdırın. Okuyucunun `config()` işlevi çağrılıp `ReaderError` yakalanabilir, ancak dönüş değeri, dosya içeriği ve ortam değişkenleri yazdırılmamalıdır. Biçim kontrolü uzak kimlik doğrulaması değildir.
6. **Kullanıcı girişine rehberlik edin.** Sistem ve klasöre uygun komutu verin. Kullanıcı telefonunu, kodunu ve iki adımlı parolasını yerel etkileşimli terminale girsin. Girdinin gizli olduğunu açıklayın; geçerli oturumu yeniden kullanın. Sohbetten kod/parola istemeyin, kullanıcı girişi alamayan arka plan komutuyla giriş başlatmayın.
7. **Tek topluluk testi yapın.** Bağlantı yoksa isteyin. Seçilen Python ile `scripts/telegram_reader.py read TARGET --limit 100 --output outputs/setup-check.json` çalıştırın. Mesaj sayısı ve tarih aralığını raporlayın; tüm mesajları varsayılan olarak göstermeyin. Hız sınırında ilgili çağrıları durdurun; ağ/erişim hatalarını açıklayın.
8. **Kullanım yolunu verin.** Kurulum konumunu, yeniden yükleme gerekip gerekmediğini ve kopyalanabilir araştırma istemini verin. Bilinmeyen kimlik/ürün bilgilerini yer tutucu bırakın. Kurulum kendiliğinden toplu arama, gruba katılma, mesaj gönderme, CRM yazımı veya veri yüklemeye dönüşmesin.

Yerel dosya veya terminal erişimi yoksa sınırlamayı açıklayın; kurulumu tamamladığınızı iddia etmeyin.

## 1. İşleyiş ve gereksinimler

İş akışı: anahtar kelime/başlangıç kanalı → benzer kanallar ve bağlı tartışmalar → son 100 mesaj → etkinlik ve ürün uyumu → kanıtlı bağlantı noktası → mesaj taslağı → kullanıcının inceleyip göndermesi.

Benzer öneriler esas olarak yayın kanalları içindir; her grup desteklemez. Betikler gruplara katılmaz, özel mesaj göndermez ve okundu işareti koymaz. Okuyucu medya türünü kaydeder, görsel/video içeriğini incelemez. Üye sayısı, kâr görselleri veya referans bağlantıları dönüşümü kanıtlamaz.

Gerekenler: yerel Codex, kendi Telegram kullanıcı hesabınız, Python 3.10+, kendi API ID/Hash bilgileriniz ve Telegram'a erişebilen ağ. Python: https://www.python.org/downloads/ . Betikler OpenAI API Key gerektirmez; Telegram bot token'ı kullanıcı hesabının yerine geçmez.

## 2. İndirme ve klasör seçimi

ZIP'i çıkarın. Özel depoya erişiminiz varsa GitHub'da **Code → Download ZIP** kullanın. Özel depo bağlantısı sadece yetkili kişilerde çalışır.

```text
README.md / README.zh-CN.md / README.en.md / README.tr.md
.gitignore
telegram-community-prospecting/
  SKILL.md
  references/telegram-tools.md
  scripts/
    telegram_reader.py
    discover.py
    requirements.txt
    .env.example
    test_telegram_reader.py
    test_discover.py
```

Kurulacak klasör `SKILL.md` içerir. Codex'ten tam yolunu isteyin. Aşağıdaki komutlar **Skill klasöründe**, yani `SKILL.md` ve `scripts` bulunan yerde çalıştırılır. Çıkarılmış ve kurulmuş kopyaların ayarları/oturumları bağımsızdır; sürekli aynı kopyayı kullanın.

## 3. Bağımlılıkları kurma

Codex yapabilir. Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
```

`python` bulunamazsa ilk komut yerine `py -3 -m venv .venv` deneyin. Sonraki komutlar doğrudan sanal ortamın Python'unu kullanır; etkinleştirme gerekmez.

macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r scripts/requirements.txt
```

## 4. Telegram API ID ve Hash alma

1. https://my.telegram.org/apps adresini açıp kendi telefonunuz ve Telegram'ın verdiği kodla giriş yapın.
2. Gerekirse **API development tools** bölümüne gidin. Uygulamanız varsa gösterilen ID/Hash değerlerini kullanın.
3. Yoksa kendi uygulama adınızı, kısa adınızı ve gereken alanları doldurup oluşturun.
4. Değerleri bilgisayarınızda tutup sonraki adımda yerel dosyaya yazın.

API ID bir sayı, Hash ise 32 karakterli onaltılık dizidir. Bunlar giriş kodu veya bot token'ı değildir. Hash'i sohbete veya ekran görüntüsüne koyup paylaşmayın.

## 5. Bilgileri nereye yazmalısınız?

Codex dosyayı hazırlayabilir veya şablonu kopyalayabilirsiniz. Var olan `.env` dosyasının üzerine yazmayın.

Windows:

```powershell
Copy-Item -LiteralPath scripts/.env.example -Destination scripts/.env
notepad scripts/.env
```

macOS/Linux:

```bash
cp scripts/.env.example scripts/.env
```

`scripts/.env` dosyasını yerel metin düzenleyicisinde açın:

```dotenv
TG_API_ID=YOUR_NUMERIC_API_ID
TG_API_HASH=YOUR_32_CHARACTER_API_HASH
TG_PROXY_URL=
TG_SESSION_NAME=telegram_reader
```

İki İngilizce yer tutucuyu gerçek değerlerinizle değiştirin. Genellikle proxy boş kalır, son satır değişmez. Kaydedip Codex'e “Kaydettim; değerleri göstermeden yalnızca biçimi doğrula” deyin.

Adı tam olarak **`.env`** olmalıdır, `.env.txt` değil. **`scripts` içinde, `telegram_reader.py` yanında** bulunmalıdır; depo köküne koymayın.

Yerel SOCKS5 proxy gerekiyorsa gerçek portunuzu kullanın:

```dotenv
TG_PROXY_URL=socks5://127.0.0.1:YOUR_ACTUAL_PROXY_PORT
```

Örnek tek başına çalışmaz; SOCKS4 ve HTTP de desteklenir. Proxy kimlik bilgilerini de yerel tutun.

## 6. Telegram'a giriş

Kendi etkileşimli terminalinizde, Windows:

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py login
```

macOS/Linux:

```bash
./.venv/bin/python scripts/telegram_reader.py login
```

Ülke koduyla telefon numaranızı, Telegram kodunu ve etkinse iki adımlı parolanızı sırayla girin. Yazarken karakter görünmemesi normaldir; her değerden sonra Enter'a basın. Bunları sohbete göndermeyin.

Giriş `scripts/telegram_reader.session` dosyasına kaydedilir ve yeniden kullanılır. Dosya hesaba erişim sağlar; paylaşmayın/yüklemeyin. Salt okunur davranış betiklerin sınırıdır, oturum yetkisinin sınırı değildir. `LOGIN_REQUIRED` için yerel etkileşimli terminali kullanın, arka planda sürekli kod istemeyin.

## 7. Önce tek topluluğu okuyun

`@PUBLIC_COMMUNITY` yerine gerçek açık grup/kanal adını veya `https://t.me/...` bağlantısını koyun. Windows:

```powershell
.\.venv\Scripts\python.exe scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

macOS/Linux:

```bash
./.venv/bin/python scripts/telegram_reader.py read @PUBLIC_COMMUNITY --limit 100 --output outputs/sample.json
```

Sonuç `outputs/sample.json` içindedir; gerçek mesaj sayısı, tarihler ve erişilebilir bilgiler bulunur. Özel grup için erişiminiz olmalıdır. 100'den azsa mevcut örneklemle değerlendirin.

Codex'e gönderin:

> $telegram-community-prospecting ile outputs/sample.json dosyasını analiz et. Hedefim gerçek kripto vadeli işlem tartışmaları olan topluluklar. İnsan etkileşimini, reklam/tekrar yoğunluğunu ve ürün uyumunu değerlendir; mesaj ID ve tarihlerini belirt. Gözlemleri bilinmeyenlerden ayır. Kanıt varsa açık iş birliği kişisini belirle. Bir yaklaşım ve kısa ilk mesaj taslağı oluştur; tam Türkçe çevirisini ekle. Mesaj gönderme.

Skill bulunmuyorsa başlangıcı “Bu klasördeki SKILL.md dosyasını oku ve uygula” olarak değiştirin.

## 8. Daha fazla topluluk bulma

Windows komutları aşağıdadır. macOS/Linux'ta `.\.venv\Scripts\python.exe` yerine `./.venv/bin/python` kullanın.

```powershell
.\.venv\Scripts\python.exe scripts/discover.py search "crypto futures" --limit 10 --output outputs/search.json
.\.venv\Scripts\python.exe scripts/discover.py similar @PUBLIC_CHANNEL --limit 10 --output outputs/similar.json
.\.venv\Scripts\python.exe scripts/discover.py linked @PUBLIC_CHANNEL --output outputs/linked.json
```

Sırasıyla anahtar kelime araması, benzer kanal önerileri ve bağlı tartışma bilgilerini getirirler. Yer tutucuyu gerçek yayın kanalıyla değiştirin. Bunlar adaylardır; Codex tekrarları ayıklayıp uygun adayların son 100 mesajını okumalıdır. Betik kendi başına sınırsız tarama yapmaz; Codex belirlenen kapsamda komutları birleştirebilir.

## 9. Tam araştırma istemi

Köşeli parantezleri doldurun:

> $telegram-community-prospecting kullan. Hedef pazarım [bölge/dil], ürünüm [ürün]. [Kanal veya anahtar kelimeler] ile başla. Benzer kanallar, bağlı tartışmalar ve açık aramayla en fazla 10 yeni aday bul; yerel geçmişte tekrar kontrolü yap. Her adayın son en fazla 100 mesajını oku. Gerçek işlem tartışmalarını tercih et; ağırlıklı olarak tekrar eden reklam ve bot bildirimlerinden oluşanları ele. Okuma zamanını, örneklem aralığını, kaynak/mesaj ID'lerini ve sınırlamaları kaydet. Uygun adaylarda kanıtlı bir bağlantı noktası çıkar; “kimlik→somut gözlem→tek soru” yapısıyla taslak yaz. Adım [ad], [platform] için [rol/ürün] iş birliklerinden sorumluyum. Alıcının dilinde yaz, tam [diliniz] çevirisini ekle. Oran, bütçe, özellik, kâr veya kişi rolü uydurma. Yerel kaydet; gruba katılma, mesaj gönderme, veri yükleme. Hız sınırında ilgili istekleri durdur.

İlk mesaj:

> Merhaba [ad], ben [gönderen]. [Borsa] bünyesinde [ürün] ortaklıklarından sorumluyum. [Topluluk] içinde [kanıtlı somut konu] hakkındaki tartışmanızı gördüm. [Ürün] kullanan topluluğunuz için iş birliğini görüşmeye açık mısınız?

Ürün uyumu belirsizse son soruda spot/vadeli işlem veya gözlenen ürünü sorun. Tek ana konu ilerletin; inceleyip kendiniz gönderin.

## 10. Sorun giderme

| Sorun | Çözüm |
|---|---|
| `python` bulunamıyor | Kurulumu kontrol edin; Windows'ta `py -3` deneyin. |
| `ModuleNotFoundError` | Bağımlılıkları aynı sanal ortamla kurun. |
| `CONFIG_MISSING` | Çalıştırılan kopyanın `scripts/.env` ve API alanlarını kontrol edin. |
| `CONFIG_INVALID` | ID pozitif sayı, Hash 32 onaltılık karakter olmalı; değerleri göstermeyin. |
| `LOGIN_REQUIRED` | Kendi etkileşimli terminalinizde giriş yapın. |
| Kod geçersiz/süresi dolmuş | Son kodu kullanın; sürekli kod istemeyin. |
| `NOT_JOINED`, `NO_ACCESS`, özel kanal hatası | Atlayın veya erişimi kendiniz edinin; araç katılmaz. |
| `RECOMMENDATIONS_UNAVAILABLE` | Hedef yayın kanalı değil; arama veya bağlı tartışmayı kullanın. |
| `FloodWaitError` | Durun, belirtilen süreye uyun; başka hesapla aşmayın. |
| Zaman aşımı | Telegram bağlantısı ve proxy'yi kontrol edin. |
| Klasör değişince yeniden giriş | Ayarlar ve oturum kopyaya bağlıdır; aynı kopyayı kullanın. |

## 11. Paylaşım ve çevrimdışı test

Yalnızca Skill, öğreticiler ve boş şablonu paylaşın. Gerçek `.env`, oturum, kod, ham topluluk verisi veya müşteri kayıtlarını paylaşmayın. Herkes kendi hesabını kurar.

Skill klasöründe test:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s scripts -v
```

macOS/Linux'ta `./.venv/bin/python` kullanın. Testler Telegram'a giriş yapmaz; gerçek ağ/hesap erişimini tek yetkili okumayla doğrulayın.
