<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark bankacılık</h1>

<p align="center"><strong>Test ortamınızın KVKK konuşması yapmadan tutabileceği Türkçe bireysel bankacılık verisi.</strong></p>

<p align="center">
  Müşteriler, hesaplar, kartlar, işlemler ve kişisel verinin asıl saklandığı<br>
  serbest metin yüzeyleri: şikâyetler, KYC notları ve destek dökümleri.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-banking/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-banking/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="53 test" src="https://img.shields.io/badge/test-53-3C873A?style=flat-square">
  <img alt="Sıfır motor kodu" src="https://img.shields.io/badge/motor%20kodu-yok-3C873A?style=flat-square">
  <a href="https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2"><img alt="Sürüm v0.1.2" src="https://img.shields.io/badge/sürüm-v0.1.2-3C873A?style=flat-square"></a>
  <a href="LICENSE"><img alt="Apache-2.0 lisansı" src="https://img.shields.io/badge/lisans-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Mintmark çekirdeğini gerektirir" src="https://img.shields.io/badge/çekirdek-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Yedi kayıt tipi" src="https://img.shields.io/badge/kayıt%20tipi-7-17191F?style=flat-square">
  <img alt="Üç tarif" src="https://img.shields.io/badge/tarif-3-17191F?style=flat-square">
  <img alt="26 kurgusal banka adı" src="https://img.shields.io/badge/kurgusal%20banka-26-D11F26?style=flat-square">
  <img alt="Tanımlayıcı politikası safe" src="https://img.shields.io/badge/tanımlayıcılar-checksum%20geçersiz-D11F26?style=flat-square">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/docs-English-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#kendiniz-basın"><strong>Kendiniz basın</strong></a>
  ·
  <a href="#değerlendirme-kümesi"><strong>Değerlendirme kümesi</strong></a>
  ·
  <a href="#burada-ne-var-ne-yok"><strong>Burada ne var</strong></a>
  ·
  <a href="README.md"><strong>English</strong></a>
</p>

---

> **Bu depo hiç motor kodu içermez.** Bildirim ve veridir: kayıt şekilleri,
> sözlükler, şablonlar ve tarifler. Bunları okuyan motor
> [mintmark](https://github.com/lokomotifai/mintmark) deposunda yaşar ve burada
> kapalı üst sınırlı bir sürüm aralığıyla sabitlenmiştir.

Türk bankaları ve fintekleri üretim verisini KVKK riski almadan test,
değerlendirme veya yapay zekâ pilot ortamlarına taşıyamaz; tedarikçileri de bunu
makul olarak isteyemez. Bu paket o ortamların ihtiyaç duyduğu veriyi beyan eder,
motor da basar: deterministik, span düzeyinde etiketli ve herkesin
denetleyebileceği bir manifestoyla mühürlenmiş.

**Sürüm 0.1.2. İki referans veri kümesi
[v0.1.2 sürümüne](https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2) ekli olarak
yayımlandı; her biri künyesini ve sağlamalarını taşıyor.** Bugün doğru olan: `packcheck` sabitlenmiş çekirdeğe karşı
geçiyor, 53 test geçiyor ve değerlendirme tarifi on sekiz kapsam hedefinin
hepsini tutturuyor.

> [!IMPORTANT]
> **Bu paket ne değildir.** Bankacılık verinizin anonimleştirilmesi değildir; hiç
> veri almaz. Uyumluluk garantisi değildir, hukuki güvenli liman değildir. Anomali
> tarifi dedektör tarafı test verisidir ve bu depo hiçbir atlatma rehberliği
> içermez. Üretilen telefon numaraları atanmış numaralarla çakışabilir, çünkü
> Türkiye numara planı kurgusal bir aralık ayırmaz. Bu veri sistemleri test etmek
> içindir. Hiçbir zaman kimseye ulaşmak için değildir.
> Bunun Türk veri koruma hukuku karşısında ne anlama gelip gelmediği
> [docs/kvkk.tr.md](docs/kvkk.tr.md) dosyasında açıklanmıştır.

## Burada ne var, ne yok

![Bankacılık paketinin kayıt tiplerinin diyagramı: üstte dört yapısal tip; kişi adı, kimlik numarası, doğum tarihi, e-posta, telefon ve adres taşıyan müşteri; müşteri başına bir ilâ üç adet, IBAN ve kuruş cinsinden bakiye taşıyan hesap; hesap başına sıfır ilâ iki adet, daima maskeli kart numarası taşıyan kart; ve hesap başına çok sayıda, IBAN, kurum ve kısa bir belge alanı taşıyan işlem. Altta kırmızıyla, her biri etiket dosyası üreten üç belge tipi: şikâyet kaydı, KYC notu ve destek dökümü](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">Erişilebilir SVG kaynağını görüntüleyin</a></sub></p>

| Var | Yok |
| --- | --- |
| Yedi kayıt tipi, üçü serbest metin | Motor kodu. Tek Python `tests/` altında ve yalnızca kamusal API'yi içe aktarıyor |
| CI'da gerçek kurum siciline karşı taranan 26 uydurma banka adı | Gerçek banka, işyeri veya kişi. Çakışma derlemeyi düşürür |
| Üç tarif, biri etiketli değerlendirme kümesi | Git'te veri kümesi. Yalnızca tip başına 50 kayıtla sınırlı örnekler |
| Varsayılan olarak checksum geçersiz her tanımlayıcı | Kurumsal müşteri kayıt tipi. Bu paket bireyseldir; vergi numaraları bu yüzden belgeler üzerinden gelir |

## Kendiniz basın

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-banking
cd mintmark-banking

mintmark packcheck .
mintmark mint --pack . --recipe retail-baseline --seed 20260901 --out ./run
mintmark verify ./run
```

Bağımlılık kurulumundan sonra çevrimdışı. `packcheck` bildirimleri katı
yükleyiciyle doğrular, mini basım yapar ve invariant ile denylist taramalarını
çalıştırır.

Önce bir bakmak, hiçbir şey basmamak mı istiyorsunuz? [`samples/`](samples/) her
tipten elli kayıt taşır ve bir test bunları sabit tohumdan yeniden üretip özetle
karşılaştırır; böylece bildirimlerden sapmış bir örnek, onları sessizce yanlış
temsil etmek yerine derlemeyi düşürür.

Üretildiği hâliyle bir şikâyet metni:

```
Sayin yetkili, Hasan Yılmaz adima kayitli hesabimla ilgili bir
sorun yasiyorum. kart konusunda defalarca basvurmama ragmen cozum
alamadim. Kimlik numaram 97978600710, hesabim
TR379999903250607630343066. Adresim Gültepe Mahallesi,
ulasilabilecegim numara +90 583 703 41 67. Konunun
degerlendirilmesini ve tarafima geri donus yapilmasini rica
ederim.
```

Bu, [`samples/complaint_ticket.jsonl`](samples/complaint_ticket.jsonl) içindeki
ilk kayıttır; README için yazılmış bir örnek değil. Bir test ikisini
karşılaştırır, böylece örnek paketin gerçekte ürettiğinden sapamaz.

İçindeki her değer sentetiktir ve kimlik numarası kendi kontrol basamağı
kuralında düşer. O belgenin etiket dosyası her biri için bir span kaydeder.

## Değerlendirme kümesi

`pii-eval` tarifi, bu paketin bu şekilde var olmasının nedenidir. hushmark-tr
model kartı, benimseyenlerden dedektörü üretimde kullanmadan önce temsili veriyle
değerlendirmelerini ister; bu, Türkçe bankacılık için o veridir.

Her etiket için bir kapsam hedefi beyan eder ve on sekizini de tutturur:

| Etiket grubu | Hedef | Ulaşılan |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | her biri 300 | her biri 2000 veya üzeri |
| HEALTH, RELIGION, ETHNICITY, POLITICAL | her biri 300 | 482 ilâ 529 |
| SEXUAL_LIFE, CRIMINAL, BIOMETRIC_REF, UNION | her biri 300 | 473 ilâ 532 |
| TCKN, IBAN, PAN, PHONE, EMAIL | her biri 500 | her biri 2000 veya üzeri |
| VKN | 500 | 2074 |

Son satır bir not hak ediyor. Bu paketteki her kayıt tipi bireyseldir, dolayısıyla
bir alanda vergi numarası taşıyacak kurumsal müşteri yoktur. VKN veriye bunun
yerine belge şablonları üzerinden girer: vergi numarasının Türkçe bankacılık
metninde gerçekten göründüğü yerlerden, itiraz edilen bir kurumsal talimattan,
KYC sırasında bunu teyit eden bir şahıs şirketinden, bir işyerinin numarasını
anan fatura ödemesinden.

Özel nitelikli satırların ardındaki aritmetik de söylenmeye değer, çünkü aşikâr
değil. Sekiz etiketin her birinden 300 span, 2000 belge içinde 2400 enjeksiyon
demek; yani belge başına birden fazla. Taban oranı olan 0.02 yaklaşık kırk tane
üretirdi. Değerlendirme tarifi bu yüzden ayrı bir şablon ailesini bir oranıyla
kullanır: belge başına iki özel nitelik slotu ve etiketler set boyunca eşit
dağıtılmış. Taban ve değerlendirme şablonları, bir tarifin ikisini yarı yarıya
karıştıramaması için tek bir set üzerinde düğme değil, ayrı setlerdir.

## Üç tarif

| Tarif | Şekil | Ne için |
| --- | --- | --- |
| **retail-baseline** | 10 000 müşteri, yaklaşık 18 000 hesap, 9 000 kart, 250 000 işlem ve 2 800 belge | Bir test ortamını portföy gibi davranan bir şeyle doldurmak |
| **pii-eval** | 2 000 belge, her etiket hedefinin üzerinde | Bir dedektörün Türkçe bankacılık metnindeki duyarlılık ve kesinliğini ölçmek |
| **anomaly-mix** | Taban artı her işlemde etiketli bir anomali alanı | Bir izleme sistemini gerçek referansa karşı puanlamak |

### anomaly-mix'in açıkça belirtilen bir sınırı

Her işlem `anomaly_kind` ve `is_anomaly` taşır ve ikisi hiç çelişmez. Ancak dört
tür, **beyan edilen oranlarda çekilmiş satır bazlı etiketlerdir, gerçek zamansal
yapılar değil**. Gerçek bir yığılma, tek bir hesapta zamanda kümelenmiş çok sayıda
işlemdir; burada bir etikettir.

Bu bir gözden kaçırma değil, paket sözleşmesinin sınırıdır: her alan bağımsız bir
akıştan çekilir, dolayısıyla bir paket satırları ilişkilendiren bir örüntü beyan
edemez. Gerçek zamansal şekiller bir çekirdek değişikliği ister ve öyle
kaydedilmiştir. Bu tarifi hattınızın etiketleri doğru taşıdığını denetlemek için
kullanın. Bir dedektörün gerçek yığılmaları bulup bulmadığını ölçmek için
kullanmayın.

## Tanımlayıcılar gerçek olamaz

Çekirdekten devralınır ve vaat edilmek yerine `verify` tarafından artefaktlar
üzerinde yeniden denetlenir:

- **TCKN** ve **VKN** doğru hesaplanır, sonra sıfırdan farklı bir kaydırmayla
  bozulur; böylece bir doğrulayıcının uyguladığı tam kuralda düşerler.
- **IBAN** `99999` banka kodunu taşır; yayımlanmış ödeme sistemleri katılımcı
  sicilinde bulunmadığı doğrulanmıştır. Validator modundaki bir IBAN bile hiçbir
  gerçek kurumu adlandırmaz.
- **PAN** `9` ile başlar; hiçbir ticari kart ağının kullanmadığı bir sektör
  tanımlayıcısıdır ve maskeli üretilir.
- **EMAIL** yalnızca RFC 2606 ve RFC 6761 ile rezerve edilmiş, kimsenin
  kaydettiremeyeceği adlar altındadır.

Bu deponun yayımladığı her referans veri kümesi safe politikasıyla basılır. Bir
test bunu her biri için doğrular.

## Kurgusal kurumlar, gerçeklere karşı denetlenir

Buradaki 26 banka adı, kişi adı yerine yer-ve-nitelik kalıbını izler; çünkü kişi
türevli kurum adları gerçek varlıklarla daha sık çakışır ve gerçek bir kişinin
işletmesine benzeyebilir.

Her biri, zorunlu CI'da lisanslı bankaların yayımlanmış katılımcı sicilinden
kurulmuş bir denylist'e karşı taranır. Çakışma derlemeyi düşürür ve her iki
tarafı da adlandırır. Çakışan bir ad savunulmaz, kaldırılır.

Tarama sözlükler, şablonlar ve basılmış çıktı üzerinde çalışır; böylece gerçek bir
ad şablon içindeki düz metinden de giremez.

## Depo haritası

```
pack.yaml           kimlik, çekirdek pini, izin verilen tanımlayıcı politikaları
fields/             üretim sırasına göre kayıt tipi başına bir dosya
recipes/            retail-baseline, pii-eval, anomaly-mix
templates/          taban setleri ve ayrı değerlendirme setleri
lexicons/           uydurma bankalar, ürünler, karşı taraflar ve denylist
samples/            tip başına elli kayıt, sabit tohumdan yeniden üretilir
vendor/             zorunlu CI'ın karşı koştuğu çekirdek wheel, özetiyle kayıtlı
tests/              uygunluk paketi
docs/               referans veri kümesi kaydı ve mühendislik notları
```

## Depoyu geliştirin

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

Hepsi vendor'lanmış çekirdek wheel'ine karşı çevrimdışı çalışır. Ayrı ve ağ
etiketli bir iş akışı, vendor'lanmış artefaktın sabitlenmiş etiketteki çekirdek
deposuyla hâlâ eşleştiğini haftalık doğrular; çünkü çevrimdışı kontrol, karşı
koştuğu artefakt kadar iyidir.

## Proje durumu

Sürüm 0.1.2, yayımlandı. İki referans veri kümesi
[v0.1.2](https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2) sürümüne ekli;
[docs/reference-datasets.json](docs/reference-datasets.json) içinde bildirilen
tohumlarla ve güvenli kimlik politikasıyla üretildiler. Motor PyPI'de
[`mintmark`](https://pypi.org/project/mintmark/) olarak yayımlanmıştır.

Tohumlar bilerek yerleşiktir. Değişen bir tohum yayımlanmış bir manifestoyu
sessizce geçersizleştirir, dolayısıyla asla bir kapsam eksiğinin çözümü değildir;
onun yerine şablonlar veya belge karışımı değişir.

Semantik sürümleme altında buradaki kamusal yüzey `pack.yaml`, alan bildirimleri,
tarifler, şablon setleri, sözlükler ve sabit bir tohumun ürettiği baytlardır. İlk
etiketli sürümden sonra bir sözlüğe giriş eklemek sonraki her indeksin çekimini
değiştirir; bu da onu minör değil majör bir yükseltme yapar.

## Topluluk sözleşmesi

Katkılar, katkı lisans sözleşmesi olmaksızın Developer Certificate of Origin 1.1
kapsamında. Burada neden motor kodu olmadığını ve bir bildirim paketin ihtiyacını
karşılayamadığında ne yapılacağını anlatan [CONTRIBUTING.md](CONTRIBUTING.md)
dosyasına bakın. [GOVERNANCE.md](GOVERNANCE.md) bu deponun neye karar verip neye
vermediğini ortaya koyar. [SECURITY.md](SECURITY.md) özel bildirim yolunu ve hiç
kod çalıştırmayan bir depoda neyin güvenlik açığı sayıldığını kapsar.

[README.md](README.md) kanoniktir ve bu belge tam bir aynadır.

## Lisans ve marka

Apache-2.0. Bakınız [LICENSE](LICENSE) ve [NOTICE](NOTICE). Lisans, Mintmark adı
veya logosu üzerinde hiçbir hak vermez; bakınız [TRADEMARKS.md](TRADEMARKS.md).

Referans veri kümeleri **CC BY 4.0** ile lisanslıdır: ticari kullanım dahil her
amaçla kullanabilirsiniz, kaynağı belirtmeniz yeterlidir. Her veri kümesi kendi
atıf satırını `MINTMARK.json` içinde taşır ve `mintmark verify` bunu yazdırır;
elle bir şey kurmanız gerekmez. Bakınız
[LICENSE-DATASETS.md](LICENSE-DATASETS.md). Hukuki teyit beklemektedir; burada
hiçbir şey bunu yerleşik olarak belirtmez.

<p align="center"><sub>Mintmark ailesinin parçası: <a href="https://github.com/lokomotifai/mintmark">çekirdek</a> · <a href="https://github.com/lokomotifai/mintmark-insurance">sigorta</a> · <a href="https://github.com/lokomotifai/mintmark-hr">insan kaynakları</a></sub></p>
