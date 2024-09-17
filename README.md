# zk-SNARK & MerkleTree Ödeme Gücü Kanıtı

Bu proje, dijital para borsalarını merkeziyetsizliğe yakınlaştırma hedefine ulaşmak için zk-SNARK ve MerkleTree tabanlı şifreli teknolojiyi keşfetmeyi amaçlamaktadır. Bu fikir, Ethereum'un kurucu ortağı Vitalik Buterin'in "[Secure CEX: Proof of Solvency](https://vitalik.ca/general/2024/09/17/proof_of_solvency.html)" adlı makalesinden gelmektedir.

## Proje Tanıtımı

Proje, güçlü bir kriptografik teknoloji olan zk-SNARK'ın kullanımını içerir. Önce tüm kullanıcıların mevduatlarını bir Merkle ağacına yerleştiririz ve ardından ağaçtaki tüm bakiyelerin negatif olmadığını ve toplamlarının iddia edilen bir değere eşit olduğunu kanıtlamak için zk-SNARK'ı kullanırız. Borsanın zincir üzerinde halka açık olarak bulunan varlıkları bu değeri aşarsa, borsanın %100 ödeme gücüne sahip olduğu anlamına gelir.

Zk-SNARK'ı Merkle Tree ile birleştirerek, işlem gizliliğini korurken verilerin hem bütünlüğü hem de tutarlılığı doğrulanabilir. Kanıtlayıcı, kanıtın içeriğini ifşa etmeden belirli koşulları karşılayan bir Merkle kanıtı bildiğini kanıtlamak için zk-SNARK'ı kullanabilir. Bu, dijital para borsalarının müşterilerinin gizliliğini korurken tüm borçlarını karşılamak için yeterli fona sahip olduklarını kanıtlamalarına olanak tanır.


## İlk Merkle Ağacı Doğrulama Yöntemi

Gate.io, Merkle Tree teknolojisini kullanarak varlık doğrulamasını uygulayan en eski kripto para borsalarından biriydi. Ayrıca, doğrulama sürecine yardımcı olmak için bağımsız ve kriptografik olarak doğrulanmış bir denetim de gerçekleştiriyoruz. Daha fazla ayrıntı için lütfen **[merkle-proof](https://github.com/gateio/proof-of-reserves/tree/merkle-proof)** şubesine bakın.


## Hazırlıklar

### Veritabanlarını yükleyin

1. Mysql: Kanıtı, user_proof'u ve tanıklığı saklayın

```Düz metin
 docker run -[zkmerkle_cex_20240305.tar.gz](https://github.com/user-attachments/files/17025114/zkmerkle_cex_20240305.tar.gz)
--name zk-mysql -p 3306:3306 -e MYSQL_USER=zkroot -e MYSQL_PASSWORD=zkpasswd -e MYSQL_DATABASE=zkpos -e MYSQL_ROOT_PASSWORD=zkpasswd mysql
```

2. Redis: Dağıtılmış kilit

```Düz metin
 docker run -d --name dizin,-%100 yedek denetim belgesi
Gate.io, %100 rezerv tutarlılığı sağlayan ilk ana platformdur
-Gate.io PoR-En son denetim zamanı :2024-09-17-11:09:00 (UTC+0)-Fazla rezervlerin değeri :864 milyon dolar -Denetim açılışı:Merkle Ağacı + zk-SNARK'lar
-Toplam Rezerv Oranı :%115,34-Merkle kök karması:093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940- Müşterinin net bakiyesi: 5.628.406.410 $ - Gate gelir bakiyesi:6.492.214.095 $ -fazla rezerv değeri:863.807.685 $


```

3. Kvrocks: Kullanıcı hesap ağacını depola

```Düz metin
 docker run -d --name[Gate.io PoR Uygulaması upd.pdf](https://github.com/user-attachments/files/17024821/Gate.io.PoR.Implementation.upd.pdf)
 docker run -d --name dizin,-%100 yedek denetim belgesi
Gate.io, %100 rezerv tutarlılığı sağlayan ilk ana platformdur
-Gate.io PoR-En son denetim zamanı :2024-09-17-11:09:00 (UTC+0)-Fazla rezervlerin değeri :864 milyon dolar -Denetim açılışı:Merkle Ağacı + zk-SNARK'lar
-Toplam Rezerv Oranı :%115,34-Merkle kök karması:093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940- Müşterinin net bakiyesi: 5.628.406.410 $ - Gate gelir bakiyesi:6.492.214.095 $ -fazla rezerv değeri:863.807.685 $

```

  > Kvrocks kurulumundan sonra bağlantı başarısız olursa:   
  1: Docker'daki /var/lib/kvrocks/kvrocks.conf dosyasını değiştirmeyi deneyin, `bind 0.0.0.0` olarak değiştirin ve örneği yeniden başlatın Çözüm  
  2: Hizmeti [kaynak kodunu](https://github.com/apache/kvrocks) kullanarak yükleyin

### Go ortamını yükleyin

Programı derlemek için sistem sürümünüze göre kurabileceğiniz Go dil ortamını kullanmanız gerekiyor [Go'yu İndir](https://go.dev/dl/).

### Borsanın kullanıcı varlık verilerini dışa aktar

Dışa aktarılan borsa kullanıcı varlığı .csv veri yapısı aşağıdaki gibidir:

```Düz metin
[proof.csv,save](https://github.com/user-attachments/files/17025141/proof.csv)

Bitcoin,rezerv oranı:0123456789,0123456789,0123456789
.0123456789,0123456789,%
Müşteri net bakiyesi:15.803,70-Gate bütçe bakiyesi:18.420,00-Gate bütçe bakiyesi USD:1.220.628.930 $


USDT
rezerv oranı:01234567890'0123456789.0123456789'0123456789%
Müşteri net bakiyesi:895.074.126,09-GateCüzdanı:943.992.283,00-Gatewall bakiyesi USD-943.992.283 $


ETH
rezerv oranı
0123456789
0123456789
0123456789
.
0123456789
0123456789
%
Müşteri net bakiyesi

208.147,69

GateCüzdanı

236.105,00

Gatewall bakiyesi USD

725.118.592 $


DOGE
rezerv oranı
0123456789
0
0123456789
.
0123456789
0123456789
%
Müşteri net bakiyesi

2.008.494.984,15

GateCüzdanı

2.194.636.960,00

Gatewall bakiyesi USD

327.222.565 $


[ETH2](rezerv oranı:0123456789%0123456789%0123456789
.%01234567890%-Müşteri net bakiyesi:68.452,52
GateCüzdanı:78.176,00- Gatewall bakiyesiUSD:240.336.476 $)


[ŞİB'](rezerv oranı:0123456789
0' 0123456789.'0123456789'0123456789%-Müşteri net bakiyesi: 8.401.492.279.474,73-Gate bakiyesi bakiyesi:8.927.307.634.575,00-Gate bakiyesi USD: 213.005.560 $)
```

Ayrıntılar için `./example_data/example_users.csv` dosyasına bakın.

### Önerilen Sistem Yapılandırması

İşletim ortamı için en azından aşağıdaki yapılandırmanın olması önerilir:

- 128 GB bellek
- 32 çekirdekli sanal makine
- 50 GB disk alanı

 

## Yapılandırma Dosyası

Üretim ortamında zk anahtarları oluştururken, Batch değişkenini 864 olarak ayarlamanız önerilir; bu, bir toplu işte kaç kullanıcı oluşturulabileceğini gösterir. Değer ne kadar büyükse, zk anahtarını ve kanıtı oluşturmak o kadar uzun sürer.

Değer 864 olarak ayarlandığında, 128 GB bellekli, 32 çekirdekli sanal makinede zk ile ilgili anahtarların üretilmesi yaklaşık 6 saat, bir grup zk kanıtının üretilmesi ise 105 saniye sürmektedir.

Bu nedenle hata ayıklama aşamasında, `utils/constants.go` içindeki `BatchCreateUserOpsCounts` değerini `4` olarak değiştirebilir ve yeniden derleyebilirsiniz. Ancak, gerçek üretimde bu parametrenin `864` olarak ayarlanması yine de önerilir.

Batch'i değiştirmek istiyorsanız, aşağıdaki yapılandırma dosyalarını değiştirmeniz gerekir:

- ./config/config.json dosyasını değiştirin `"ZkKeyName": "./zkpor864"` => `"ZkKeyName": "./zkpor4"`
- ./config/cex_config.json dosyasını değiştirin `"ZkKeyVKDirectoryAndPrefix": "./zkpor864"` => `"ZkKeyVKDirectoryAndPrefix": "./zkpor4"`
- ./utils/constants.go dosyasını değiştirin `BatchCreateUserOpsCounts = 864` => `BatchCreateUserOpsCounts = 4`

### Jeton Ayarları

- ./utils/constants.go'yu değiştirin

#### Jeton Miktarı

```
 docker run -d --name dizin,-%100 yedek denetim belgesi
Gate.io, %100 rezerv tutarlılığı sağlayan ilk ana platformdur
-Gate.io PoR-En son denetim zamanı :2024-09-17-11:09:00 (UTC+0)-Fazla rezervlerin değeri :864 milyon dolar -Denetim açılışı:Merkle Ağacı + zk-SNARK'lar
-Toplam Rezerv Oranı :%115,34-Merkle kök karması:093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940- Müşterinin net bakiyesi: 5.628.406.410 $ - Gate gelir bakiyesi:6.492.214.095 $ -fazla rezerv değeri:863.807.685 $

```

> `AssetCounts` borsada bulunan token sayısını temsil eder. Gerçek sayı ayarlanan değerden düşük olamaz. Örneğin, 420 token varsa, bunu 500 olarak değiştirebilirsiniz. Bellek kullanımını göz önünde bulundurarak, duruma göre makul bir değer ayarlamanız önerilir.

#### Fiyat Hassasiyeti

`AssetTypeForTwoDigits` alanının anlamı, BTTC, SHIB, LUNC, XEC, WIN, BIDR, SPELL, HOT, DOGE gibi 10^2 fiyat hassasiyetidir.

Geri kalanlar için varsayılan fiyat hassasiyeti 10^8'dir

### Tanık ile ilgili yapılandırmayı ayarlayın

Tanık, kanıtlayıcı ve kullanıcı kanıtı için kanıt üretmek için kullanılır. config.json yapılandırması aşağıdaki gibidir:

```Düz metin
{
  "MysqlDataSource" : "zkroot:zkpasswd@tcp(127.0.0.1:3306)/zkpos?parseTime=true",
  "VeritabanıEki": "202307",
  "KullanıcıVeriDosyası": "./example_data/",
  "AğaçVT": {
    "Sürücü": "redis",
    "Seçenek": {
      "Adres": "127.0.0.1:6666"
    }
  },
  "Kısa": {
    "Ana Bilgisayar": "127.0.0.1:6379",
    "Tür": "düğüm"
  },
  "ZkKeyName": "./zkpor864"
}
```

- `MysqlDataSource`: Mysql veritabanı bağlantısı
- `DbSuffix`: Mysql tarafından oluşturulan tablonun son eki. Örneğin, 202307 saatini girerseniz, witness202307'yi oluşturacaktır. **Her oluşturulduğunda** değiştirilmelidir.
- `UserDataFile`: Borsa tarafından dışa aktarılan kullanıcı varlık dosyalarının dizini. Program bu dizin altındaki tüm csv dosyalarını okuyacaktır
- `TreeDB`: kvrocks ile ilgili yapılandırma
- `Redis`: Redis ile ilgili yapılandırma
- `ZkKeyName`: Hiyerarşik anahtarın dizini ve öneki. Örneğin, zkpor864, zkpor864.* dosya adı önekine sahip tüm dosyalarla eşleşir.

> `DbSuffix` alanı tablonun son ekidir. Her seferinde değiştirilmelidir. Ayda bir kez üretiliyorsa, 202306, 202307 gibi üretim zamanına göre de ayarlanabilir.

## Programı çalıştırın

Projeyi yerel makinenize indirin ve programı derlemeye başlayın.

### Programı derleyin

```Düz metin
yapmak inşa etmek
```

Eğer `Mac` bilgisayarınızda diğer platformlar için ikili programlar derlemeniz gerekiyorsa, aşağıdaki komutları çalıştırabilirsiniz:

- Mac'te Linux'u derleyin: `make build-linux`.
- Mac'te Windows'u derlemek: `make build-windows`.

### Anahtarları Oluştur

```Düz metin
./main anahtar üreticisi
```

Keygen hizmeti tamamlandıktan sonra, geçerli dizinde aşağıdaki gibi birkaç anahtar dosyası oluşturulacaktır:


> zkpor864.ccs.ct.kaydet  
> zkpor864.ccs.kaydet  
> zkpor864.pk.A.kaydet  
> zkpor864.pk.B1.kaydet  
> zkpor864.pk.B2.kaydet  
> zkpor864.pk.E.kaydet  
> zkpor864.pk.K.kaydet  
> zkpor864.vk.kaydet  
> zkpor864.pk.Z.kaydet  

Batch değeri 4 olarak ayarlanırsa `zkpor4.*.save` olacaktır.

Bu adımın çalışması uzun zaman alır. 4 olarak ayarlandığında, yaklaşık birkaç dakika sürer; 864 olarak ayarlandığında, birkaç saat sürebilir.

**Not:**

- `./main keygen` komutuyla oluşturulan anahtarlar uzun süre kullanılabilir. Örneğin, gelecek ay varlık doğrulama verisi oluşturmanız gerekirse, oluşturulan zk anahtarları hala kullanılabilir.
- Sonraki kullanıcı doğrulama süreçlerinde `zkpor864.vk.save` dosyası gereklidir. Bu nedenle, bir yedekleme yapmanız ve zk anahtarlarının toplu olarak güvenli bir şekilde saklanması önerilir.

### Geçmiş kvrocks verilerini temizle

Programı daha önce çalıştırdıysanız, çalıştırmadan önce kvrocks'taki mevcut hesap Merkle anahtar verilerini temizlemeniz gerekir; çünkü her defasında farklı hesap ağaçlarının oluşturulması gerekir.

```Düz metin
./main araç clean_kvrocks
```

**Uyarı:** Bu komut kvrocks'taki tüm verileri temizler, bu nedenle tek bir kvrocks örneğini diğer programlarla paylaşmayın. Önceki veriler temizlendikten sonra, kanıt üretmeye başlayabilirsiniz.

### Tanıklık hizmetini başlat

```Düz metin
./ana tanık
```

> İşlem tamamlandıktan sonra, Mysql veritabanında (`config.json` dosyasındaki `DbSuffix`'e göre) witness+suffix içeren bir tablo oluşturulacaktır. Tablo, witness proof verilerini gruplar halinde içerir ve tablodaki veriler, zk proof ve kullanıcı proof'unun sonraki üretiminde rol oynayacaktır.

### Zk kanıtı oluştur

Prover servisi zk kanıtları üretmek için kullanılır ve paralel işlemi destekler. Mysql'deki witness tablosundan witnessları okur.

Zk kanıt verilerini üretmek için aşağıdaki komutu çalıştırın:

```Düz metin
./ana kanıtlayıcı
```

> Bu komut paralel işlemi destekler. Ana dosyayı ve zkpor864 gibi diğer ilgili dosyaları diğer makinelere kopyalamanız ve `config.json` dosyasındaki yapılandırmanın aynı olduğundan emin olmanız gerekir. Bu şekilde, Redis aynı anda çalışmak üzere dağıtılmış bir kilit olarak kullanılabilir.

Yürütme durumunu sorgulamak için aşağıdaki komutu çalıştırabilirsiniz:

```Düz metin
./main araç check_prover_status
```

İşlem tamamlandığında şu şekilde geri dönecektir:

```Düz metin
 docker run -d --name dizin,-%100 yedek denetim belgesi
Gate.io, %100 rezerv tutarlılığı sağlayan ilk ana platformdur
-Gate.io PoR-En son denetim zamanı :2024-09-17-11:09:00 (UTC+0)-Fazla rezervlerin değeri :864 milyon dolar -Denetim açılışı:Merkle Ağacı + zk-SNARK'lar
-Toplam Rezerv Oranı :%115,34-Merkle kök karması:093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940- Müşterinin net bakiyesi: 5.628.406.410 $ - Gate gelir bakiyesi:6.492.214.095 $ -fazla rezerv değeri:863.807.685 $
```

Tüm tanık öğelerinin tamamlanmış durumda olduğundan, yani kanıtlayıcı işleminin tamamlandığından emin olun.

> Prover hizmeti yürütüldükten sonra, Mysql veritabanında proof+suffix'li (`config.json`'daki `DbSuffix`'e göre) ek bir tablo olacak. Tablodaki verilerin kullanıcılara açık hale getirilmesi gerekiyor, böylece kullanıcılar borsanın varlıklarını daha sonra doğrulayabilirler. Doğrulama aşamasında, bunun nasıl yapılacağı ayrıntılı olarak açıklanacaktır.

### Kullanıcı kanıtı oluşturun

Userproof servisi kullanıcı Merkle kanıtlarını oluşturmak ve kalıcı hale getirmek için kullanılır.

Kullanıcı kanıtı verilerini oluşturmak için aşağıdaki komutu çalıştırın:

```Düz metin
./main kullanıcı dostu
```

Performans: 128 GB bellek ve 32 çekirdekli sanal makinede kullanıcılar için saniyede yaklaşık 10 bin kanıt üretir.

> userproof komutunu çalıştırdıktan sonra, mysql veritabanında userproof+suffix adlı bir tablo (`DbSuffix` içindeki `config.json`'a dayalı) oluşturulacaktır. Bu tablodaki veriler kullanıcının varlık bilgilerini içerir ve gerektiği gibi izinlerle yapılandırılabilir. Bu tablonun, hesap varlıklarının bir kanıtını yapmak için, belirlenen kullanıcılara indirilmek üzere açılması gerekir. Belirli talimatlar aşağıdaki doğrulama bölümünde açıklanacaktır.

## Doğrulama verilerini sağlayın

Burada kullanıcılara iki doğrulama seçeneği sunmamız gerekiyor:

- Borsanın varlıklarını doğrulayın
- Kullanıcının kendi varlıklarını doğrulayın

Her aşama için ikili yürütülebilir dosyaları (mac ubuntu windows) önceden derleyip kullanıcılara indirmeleri için sunmamız gerekiyor. Ayrıntılar için Sürüm ekine bakın.

### Borsadaki varlıkları doğrulamak için gereken veriler ve biçim

Kullanıcılara borsadaki varlıkları doğrulamak için ikili dosyalar sağlamanın yanı sıra, aşağıdaki üç yapılandırma verisini de sağlamamız gerekiyor:

1. `proof.csv` dosyasını indirin: Daha önce oluşturulan proof tablosunu, başlıklar dahil olmak üzere, proof202307.csv gibi bir CSV dosyası olarak önceden dışa aktarın ve kullanıcıların indirmesine sunun.
2. `zkpor864.vk.save`: Kullanıcılara zk864 için daha önce oluşturulmuş doğrulama anahtar dosyasını sağlamamız gerekiyor.
3. `Borsanın varlıkları`: Yukarıdaki Kanıt dosyası oluşturulduktan sonra, borsanın sağladığı kullanıcının varlık tablosunun toplamını sorgulamak için aşağıdaki komutu kullanabilirsiniz:

```Düz metin
 ./main araç query_cex_assets
```

Aşağıdaki gibi bir sonuç döndürülecektir:

```Düz metin
 [{"ToplamÖzsermaye":10049232946,"ToplamBorç":0,"TemelFiyat":3960000000,"Sembol":"1inç","İndeks":0},{"ToplamÖzsermaye":421836,"ToplamBorç":0,"TemelFiyat":564000000000,"Sembol":"aave","İndeks":1},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat" :79800000,"Sembol":"ach","İndeks":2},{"ToplamÖzsermaye":3040000,"ToplamBorç":0,"TemelFiyat":25460000000,"Sembol":"acm","İndeks":3},{"ToplamÖzsermaye":17700050162640,"ToplamBorç":0,"TemelFiyat":2784000000,"Sembol":"ada","İndeks":4},{"Toplam Özkaynak":485400000,"ToplamBorç":0,"TemelFiyat":1182000000,"Sembol":"adx","İndeks":5},{"ToplamÖzkaynak":0,"ToplamBorç":0,"TemelFiyat":907000000,"Sembol":"aergo","İndeks":6},{"ToplamÖzkaynak":0,"ToplamBorç":0,"TemelFiyat":2720000000,"Sembol ":"agld","Index":7},{"Toplam Özsermaye":1969000000,"Toplam Borç":0,"Temel Fiyat":30500000,"Sembol":"akro","Index":8},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":141000000000,"Sembol":"alcx","Index":9},{"Toplam Özsermaye":15483340912,"Toplam lBorç":0,"Temel Fiyat":1890000000,"Sembol":"algo","İndeks":10},{"Toplam Özsermaye":3187400,"Toplam Borç":0,"Temel Fiyat":11350000000,"Sembol":"alice","İndeks":11},{"Toplam Özsermaye":1760000,"Toplam Borç":0,"Temel Fiyat":2496000000,"Sembol":"alp aca","Index":12},{"ToplamÖzsermaye":84596857600,"ToplamBorç":0,"TemelFiyat":785000000,"Sembol":"alfa","Index":13},{"ToplamÖzsermaye":3672090936,"ToplamBorç":0,"TemelFiyat":20849000000,"Sembol":"alpine","Index":14},{"ToplamÖzsermaye":19820 0000,"ToplamBorç":0,"TemelFiyat":132600000,"Sembol":"amb","İndeks":15},{"ToplamÖzsermaye":53800000,"ToplamBorç":0,"TemelFiyat":32200000,"Sembol":"amp","İndeks":16},{"ToplamÖzsermaye":3291606210,"ToplamBorç":0,"TemelFiyat":340300000,"Sembol ":"anc","İndeks":17},{"ToplamÖzsermaye":192954000,"ToplamBorç":0,"TemelFiyat":166000000,"Sembol":"ankr","İndeks":18},{"ToplamÖzsermaye":2160000,"ToplamBorç":0,"TemelFiyat":20940000000,"Sembol":"karınca","İndeks":19},{"ToplamÖzsermaye":5995002000,"ToplamBorç":0,"TemelFiyat":40370000000,"Sembol":"ape","İndeks":20},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":11110000000,"Sembol":"api3","İndeks":21},{"ToplamÖzsermaye":53728000,"ToplamBorç":0,"TemelFiyat":38560000000,"Sembol":"apt ","İndeks":22},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":68500000000,"Sembol":"ar","İndeks":23},{"ToplamÖzsermaye":55400000,"ToplamBorç":0,"TemelFiyat":667648400,"Sembol":"ardr","İndeks":24},{"ToplamÖzsermaye":8320000,"ToplamBorç":0,"Ba sePrice":266200000,"Sembol":"arpa","İndeks":25},{"ToplamÖzsermaye":18820000,"ToplamBorç":0,"TemelFiyat":401000000,"Sembol":"astr","İndeks":26},{"ToplamÖzsermaye":13205405410,"ToplamBorç":0,"TemelFiyat":934000000,"Sembol":"ata","İndeks":27 },{"ToplamSermaye":7016230960,"ToplamBorç":0,"TemelFiyat":102450000000,"Sembol":"atom","İndeks":28},{"ToplamSermaye":2619441828,"ToplamBorç":0,"TemelFiyat":40900000000,"Sembol":"müzayede","İndeks":29},{"ToplamSermaye":9640198,"ToplamBorç" :0,"Temel Fiyat":1432000000,"Sembol":"ses","İndeks":30},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":2306000000000,"Sembol":"otomatik","İndeks":31},{"Toplam Özsermaye":886400,"Toplam Borç":0,"Temel Fiyat":5390000000,"Sembol":"ava","İndeks":3 2},{"Toplam Özsermaye":2883562350,"Toplam Borç":0,"Temel Fiyat":117800000000,"Sembol":"avax","İndeks":33},{"Toplam Özsermaye":1864300912,"Toplam Borç":0,"Temel Fiyat":68200000000,"Sembol":"axs","İndeks":34},{"Toplam Özsermaye":843870,"Toplam Borç":0, "Temel Fiyat":23700000000,"Sembol":"porsuk","İndeks":35},{"Toplam Özsermaye":114869291528,"Toplam Borç":0,"Temel Fiyat":1379000000,"Sembol":"bake","İndeks":36},{"Toplam Özsermaye":95400,"Toplam Borç":0,"Temel Fiyat":54110000000,"Sembol":"bal","Ben ndex":37},{"Toplam Özsermaye":123113880,"Toplam Borç":0,"Temel Fiyat":14610000000,"Sembol":"bant","İndeks":38},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":37100000000,"Sembol":"çubuk","İndeks":39},{"Toplam Özsermaye":73090049578,"Toplam Borç":0,"Temel Fiyat":1774000000,"Sembol":"bat","İndeks":40},{"Toplam Özsermaye":28891300,"Toplam Borç":0,"Temel Fiyat":1017000000000,"Sembol":"bch","İndeks":41},{"Toplam Özsermaye":19889623294,"Toplam Borç":0,"Temel Fiyat":4130000000,"Sembol":"bel","İndeks x":42},{"Toplam Özkaynak":374840602180,"Toplam Borç":0,"Temel Fiyat":699700000,"Sembol":"beta","İndeks":43},{"Toplam Özkaynak":270294580,"Toplam Borç":0,"Temel Fiyat":12290900000000,"Sembol":"beth","İndeks":44},{"Toplam Özkaynak":35692901600,"Toplam Borç":0,"Temel Fiyat":2730000000,"Sembol":"bico","İndeks":45},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":639000,"Sembol":"bidr","İndeks":46},{"Toplam Özsermaye":240200000,"Toplam Borç":0,"Temel Fiyat":538000000,"Sembol":"blz","İndeks":47}, {"ToplamÖzsermaye":83614634622,"ToplamBorç":0,"TemelFiyat":2599000000000,"Sembol":"bnb","İndeks":48},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3490000000,"Sembol":"bnt","İndeks":49},{"ToplamÖzsermaye":1560,"ToplamBorç":0,"TemelFiyat":59200 0000000,"Sembol":"bnx","İndeks":50},{"ToplamÖzsermaye":2076000,"ToplamBorç":0,"TemelFiyat":32630000000,"Sembol":"tahvil","İndeks":51},{"ToplamÖzsermaye":44699589660,"ToplamBorç":0,"TemelFiyat":1768000000,"Sembol":"bsw","İndeks":52},{"ToplamEqu ity":291716078,"ToplamBorç":0,"TemelFiyat":169453900000000,"Sembol":"btc","İndeks":53},{"ToplamÖzsermaye":15500321300000000,"ToplamBorç":0,"TemelFiyat":6300,"Sembol":"bttc","İndeks":54},{"ToplamÖzsermaye":70771546756,"ToplamBorç":0,"TemelFiyat e":5240000000,"Symbol":"burger","Index":55},{"TotalEquity":12058907297354,"TotalBorç":1476223055432,"BasePrice":10000000000,"Symbol":"busd","Index":56},{"TotalE oldukça":34716440000,"ToplamBorç":0,"Taban Fiyat":1647000000,"Sembol": "c98","İndeks":57},{"ToplamÖzsermaye":1541723702,"ToplamBorç":0,"TemelFiyat":33140000000,"Sembol":"kek","İndeks":58},{"ToplamÖzsermaye":2112000,"ToplamBorç":0,"TemelFiyat":5200000000,"Sembol":"celo","İndeks":59},{"ToplamÖzsermaye":317091540000,"Toplam Borç": 0, "Temel Fiyat": 101000000, "Sembol":" celr","İndeks": 60}, {"Toplam Özsermaye": 137111365560, "Toplam Borç": 0, "Temel Fiyat": 228000000, "Sembol":" cfx","İndeks": 61}, {"Toplam Özsermaye": 0, "Toplam Borç": 0, "Temel Fiyat": 1820000000, "Sembol":" ch ess","Index":62},{"Toplam Özsermaye":258540000,"Toplam Borç":0,"Temel Fiyat":1140000000,"Sembol":"chr","Index":63},{"Toplam Özsermaye":289172288882,"Toplam Borç":0,"Temel Fiyat":1099000000,"Sembol":"chz","Index":64},{"Toplam Özsermaye":0,"ToplamD ebt":0,"Temel Fiyat":25100000,"Sembol":"ckb","İndeks":65},{"Toplam Özsermaye":1851135024806,"Toplam Borç":0,"Temel Fiyat":535500000,"Sembol":"clv","İndeks":66},{"Toplam Özsermaye":155010000,"Toplam Borç":0,"Temel Fiyat":5202000000,"Sembol":"co cos","İndeks":67},{"Toplam Özsermaye":52093390,"Toplam Borç":0,"Temel Fiyat":335800000000,"Sembol":"comp","İndeks":68},{"Toplam Özsermaye":13991592000,"Toplam Borç":0,"Temel Fiyat":44500000,"Sembol":"cos","İndeks":69},{"Toplam Özsermaye":5124078806 8,"Toplam Borç":0,"Temel Fiyat":557000000,"Sembol":"coti","İndeks":70},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":107900000000,"Sembol":"krem","İndeks":71},{"Toplam Özsermaye":15940224,"Toplam Borç":0,"Temel Fiyat":5470000000,"Sembol": "crv","İndeks":72},{"ToplamÖzsermaye":2336000,"ToplamBorç":0,"TemelFiyat":7450000000,"Sembol":"ctk","İndeks":73},{"ToplamÖzsermaye":88860000,"ToplamBorç":0,"TemelFiyat":1059000000,"Sembol":"ctsi","İndeks":74},{"ToplamÖzsermaye":440400000," talDebt":0,"Temel Fiyat":1763000000,"Sembol":"ctxc","İndeks":75},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":3375000000,"Sembol":"cvp","İndeks":76},{"Toplam Özsermaye":176202,"Toplam Borç":0,"Temel Fiyat":30810000000,"Sembol":"cvx","İçinde dex":77},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":9999000100,"Sembol":"dai","İndeks":78},{"Toplam Özsermaye":90702266836,"Toplam Borç":0,"Temel Fiyat":1293500000,"Sembol":"dar","İndeks":79},{"Toplam Özsermaye":29386961406,"Toplam Borç":0,"Temel Fiyat":458300000000,"Sembol":"tire","İndeks":80},{"Toplam Özsermaye":1628888000,"Toplam Borç":0,"Temel Fiyat":235500000,"Sembol":"veri","İndeks":81},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":186229836100,"Sembol":"dcr","İndeks":8 2},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":15920000000,"Sembol":"dego","İndeks":83},{"ToplamÖzsermaye":26105549312822,"ToplamBorç":0,"TemelFiyat":6830000,"Sembol":"dent","İndeks":84},{"ToplamÖzsermaye":670658000,"ToplamBorç":0,"TemelP pirinç":24000000000,"Sembol":"dexe","İndeks":85},{"ToplamÖzsermaye":517372774000,"ToplamBorç":0,"TemelFiyat":82200000,"Sembol":"dgb","İndeks":86},{"ToplamÖzsermaye":1120000,"ToplamBorç":0,"TemelFiyat":2970000000,"Sembol":"dia","İndeks":87}, {"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":151800000,"Sembol":"rıhtım","İndeks":88},{"ToplamÖzsermaye":19453393384,"ToplamBorç":0,"TemelFiyat":987000000,"Sembol":"dodo","İndeks":89},{"ToplamÖzsermaye":25526548451614,"ToplamBorç":0,"TemelPr buz":723900000,"Sembol":"doge","İndeks":90},{"ToplamÖzsermaye":466049240950,"ToplamBorç":0,"TemelFiyat":46820000000,"Sembol":"nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat":3138000000,"Sembol":"drep","İndeks":92 },{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":45675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","İndeks":94},{"ToplamÖzsermaye":241920370,"ToplamBorç":0,"TemelFiyat ce":343400000000,"Sembol":"egld","İndeks":95},{"ToplamÖzsermaye":3640000,"ToplamBorç":0,"TemelFiyat":1691000000,"Sembol":"elf","İndeks":96},{"ToplamÖzsermaye":200008070,"ToplamBorç":0,"TemelFiyat":2556000000,"Sembol":"enj","İndeks":97},{" Toplam Özkaynak":836000,"Toplam Borç":0,"Temel Fiyat":115500000000,"Sembol":"ens","İndeks":98},{"Toplam Özkaynak":23489390223668,"Toplam Borç":0,"Temel Fiyat":8960000000,"Sembol":"eos","İndeks":99},{"Toplam Özkaynak":83358943947200,"Toplam Borç":0,"Temel Fiyat":2960000,"Sembol":"epx","İndeks":100},{"Toplam Özsermaye":1539180000,"Toplam Borç":0,"Temel Fiyat":17540000000,"Sembol":"ern","İndeks":101},{"Toplam Özsermaye":48056621250,"Toplam Borç":0,"Temel Fiyat":204100000000,"Sembol":"vb","I ndex":102},{"Toplam Özsermaye":28478224392,"Toplam Borç":0,"Temel Fiyat":12688000000000,"Sembol":"eth","İndeks":103},{"Toplam Özsermaye":21790805772,"Toplam Borç":0,"Temel Fiyat":10641000000,"Sembol":"eur","İndeks":104},{"Toplam Özsermaye":196200,"T otalDebt":0,"Temel Fiyat":307000000000,"Sembol":"çiftlik","İndeks":105},{"ToplamSermaye":31040000,"ToplamBorç":0,"Temel Fiyat":1240000000,"Sembol":"fet","İndeks":106},{"ToplamSermaye":26460000,"ToplamBorç":0,"Temel Fiyat":3354000000,"Sembol" :"fida","İndeks":107},{"ToplamÖzsermaye":5539231876,"ToplamBorç":0,"TemelFiyat":33380000000,"Sembol":"fil","İndeks":108},{"ToplamÖzsermaye":152000000,"ToplamBorç":0,"TemelFiyat":275000000,"Sembol":"fio","İndeks":109},{"ToplamÖzsermaye":1014252 612,"ToplamBorç":0,"TemelFiyat":16540000000,"Sembol":"firo","İndeks":110},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3313000000,"Sembol":"fis","İndeks":111},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":765931600,"Sembol":"flm","İçinde dex":112},{"ToplamÖzsermaye":3688000,"ToplamBorç":0,"TemelFiyat":6990000000,"Sembol":"akış","İndeks":113},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":5090000000,"Sembol":"akış","İndeks":114},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat" :162500000,"Sembol":"için","İndeks":115},{"ToplamÖzsermaye":80000,"ToplamBorç":0,"TemelFiyat":29400000000,"Sembol":"ileri","İndeks":116},{"ToplamÖzsermaye":14430200000,"ToplamBorç":0,"TemelFiyat":1808000000,"Sembol":"ön","İndeks":117},{" Toplam Özsermaye":26629480000,"Toplam Borç":0,"Temel Fiyat":2211000000,"Sembol":"ftm","İndeks":118},{"Toplam Özsermaye":16207428000,"Toplam Borç":0,"Temel Fiyat":9125000000,"Sembol":"ftt","İndeks":119},{"Toplam Özsermaye":679597613272,"Toplam Borç":0,"Temel Fiyat":61663700,"Sembol":"eğlence","İndeks":120},{"Toplam Sermaye":0,"Toplam Borç":0,"Temel Fiyat":51410000000,"Sembol":"fxs","İndeks":121},{"Toplam Sermaye":4110633550,"Toplam Borç":0,"Temel Fiyat":11540000000,"Sembol":"gal","İndeks":122} ,{"ToplamÖzsermaye":2551466375170,"ToplamBorç":0,"TemelFiyat":234700000,"Sembol":"gala","İndeks":123},{"ToplamÖzsermaye":1252940134,"ToplamBorç":0,"TemelFiyat":20260000000,"Sembol":"gaz","İndeks":124},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelP rice":1850000000,"Sembol":"glm","İndeks":125},{"ToplamÖzsermaye":25058958996,"ToplamBorç":0,"TemelFiyat":3195000000,"Sembol":"glmr","İndeks":126},{"ToplamÖzsermaye":443980786672,"ToplamBorç":0,"TemelFiyat":2588000000,"Sembol":"gmt","İndeks ":127},{"Toplam Özsermaye":160000,"Toplam Borç":0,"Temel Fiyat":417300000000,"Sembol":"gmx","İndeks":128},{"Toplam Özsermaye":178800,"Toplam Borç":0,"Temel Fiyat":878736379100,"Sembol":"gno","İndeks":129},{"Toplam Özsermaye":6828000,"Toplam Borç":0,"B asePrice":620000000,"Sembol":"grt","İndeks":130},{"ToplamÖzsermaye":20784000,"ToplamBorç":0,"TemelFiyat":13340000000,"Sembol":"gtc","İndeks":131},{"ToplamÖzsermaye":94280000,"ToplamBorç":0,"TemelFiyat":1494000000,"Sembol":"zor","İndeks":1 32},{"ToplamÖzsermaye":336206273140,"ToplamBorç":0,"TemelFiyat":391000000,"Sembol":"hbar","İndeks":133},{"ToplamÖzsermaye":1791317190,"ToplamBorç":0,"TemelFiyat":8870000000,"Sembol":"yüksek","İndeks":134},{"ToplamÖzsermaye":6485637600,"ToplamBorç t":0,"Temel Fiyat":2700000000,"Sembol":"kovan","İndeks":135},{"Toplam Özsermaye":1956144,"Toplam Borç":0,"Temel Fiyat":18400000000,"Sembol":"hnt","İndeks":136},{"Toplam Özsermaye":9587039140000,"Toplam Borç":0,"Temel Fiyat":14820000,"Sembol":"sıcak" ,"Endeks":137},{"ToplamÖzsermaye":223895102366,"ToplamBorç":0,"TemelFiyat":38980000000,"Sembol":"icp","Endeks":138},{"ToplamÖzsermaye":52168047570,"ToplamBorç":0,"TemelFiyat":1516000000,"Sembol":"icx","Endeks":139},{"ToplamÖzsermaye":15480000,"ToplamBorç":0,"TemelFiyat":388000000,"Sembol":"idex","İndeks":140},{"ToplamÖzsermaye":8400000,"ToplamBorç":0,"TemelFiyat":388700000000,"Sembol":"ilv","İndeks":141},{"ToplamÖzsermaye":12686368000,"ToplamBorç":0,"TemelFiyat":4230000000,"Sembol ol":"imx","İndeks":142},{"ToplamÖzsermaye":139990936000,"ToplamBorç":0,"TemelFiyat":13680000000,"Sembol":"inj","İndeks":143},{"ToplamÖzsermaye":69430091021436,"ToplamBorç":0,"TemelFiyat":72500000,"Sembol":"iost","İndeks":144},{"ToplamÖzsermaye ":71259628200,"ToplamBorç":0,"TemelFiyat":1823000000,"Sembol":"iota","İndeks":145},{"ToplamÖzsermaye":428000000,"ToplamBorç":0,"TemelFiyat":221500000,"Sembol":"iotx","İndeks":146},{"ToplamÖzsermaye":858126200,"ToplamBorç":0,"TemelFiyat":432 00000,"Sembol":"iq","İndeks":147},{"ToplamÖzsermaye":8680000,"ToplamBorç":0,"TemelFiyat":132174000,"Sembol":"iris","İndeks":148},{"ToplamÖzsermaye":1889177748140,"ToplamBorç":0,"TemelFiyat":37600000,"Sembol":"jasmy","İndeks":149},{"ToplamEqu ity":2000,"ToplamBorç":0,"TemelFiyat":1416000000,"Sembol":"joe","İndeks":150},{"ToplamÖzsermaye":927921956,"ToplamBorç":0,"TemelFiyat":201400000,"Sembol":"jst","İndeks":151},{"ToplamÖzsermaye":560000,"ToplamBorç":0,"TemelFiyat":6590000000," Sembol":"kava","İndeks":152},{"ToplamÖzsermaye":30527442000,"ToplamBorç":0,"TemelFiyat":9480000000,"Sembol":"kda","İndeks":153},{"ToplamÖzsermaye":7587760000,"ToplamBorç":0,"TemelFiyat":29350000,"Sembol":"anahtar","İndeks":154},{"ToplamÖzsermaye": 372181704,"ToplamBorç":0,"TemelFiyat":1613000000,"Sembol":"klay","İndeks":155},{"ToplamÖzsermaye":81600000,"ToplamBorç":0,"TemelFiyat":1904661800,"Sembol":"kmd","İndeks":156},{"ToplamÖzsermaye":493317080,"ToplamBorç":0,"TemelFiyat":49400000 00,"Sembol":"knc","İndeks":157},{"ToplamÖzsermaye":1700000,"ToplamBorç":0,"TemelFiyat":621600000000,"Sembol":"kp3r","İndeks":158},{"ToplamÖzsermaye":27180,"ToplamBorç":0,"TemelFiyat":250100000000,"Sembol":"ksm","İndeks":159},{"ToplamÖzsermaye":1656679204,"ToplamBorç":0,"TemelFiyat":30978000000,"Sembol":"lazio","İndeks":160},{"ToplamÖzsermaye":295510852208,"ToplamBorç":0,"TemelFiyat":15200000000,"Sembol":"ldo","İndeks":161},{"ToplamÖzsermaye":1158728143570,"ToplamBorç":0,"TemelFiyat ":17230000,"Sembol":"kaldıraç","İndeks":162},{"ToplamÖzsermaye":6505365672842,"ToplamBorç":0,"TemelFiyat":52690000,"Sembol":"lina","İndeks":163},{"ToplamÖzsermaye":8162369516,"ToplamBorç":0,"TemelFiyat":57120000000,"Sembol":"bağlantı","İndeks":164} ,{"ToplamÖzsermaye":95484000,"ToplamBorç":0,"TemelFiyat":7220000000,"Sembol":"aydınlatılmış","İndeks":165},{"ToplamÖzsermaye":12682220,"ToplamBorç":0,"TemelFiyat":3632000000,"Sembol":"loka","İndeks":166},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":409 400000,"Sembol":"tezgah","İndeks":167},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":44400000000,"Sembol":"lpt","İndeks":168},{"ToplamÖzsermaye":10715077402,"ToplamBorç":0,"TemelFiyat":2063000000,"Sembol":"lrc","İndeks":169},{"ToplamÖzsermaye": 8050236298,"Toplam Borç":0,"Temel Fiyat":7240000000,"Sembol":"lsk","İndeks":170},{"Toplam Özsermaye":1122426768,"Toplam Borç":0,"Temel Fiyat":758900000000,"Sembol":"ltc","İndeks":171},{"Toplam Özsermaye":22654000,"Toplam Borç":0,"Temel Fiyat":7100000 00,"Sembol":"lto","İndeks":172},{"ToplamÖzsermaye":16580624988,"ToplamBorç":0,"TemelFiyat":13251000000,"Sembol":"luna","İndeks":173},{"ToplamÖzsermaye":1705595428000000,"ToplamBorç":0,"TemelFiyat":1560500,"Sembol":"lunc","İndeks":174},{"Toplam lSermaye":0,"ToplamBorç":0,"TemelFiyat":4759000000,"Sembol":"sihirli","İndeks":175},{"ToplamSermaye":77632636722,"ToplamBorç":0,"TemelFiyat":3278000000,"Sembol":"mana","İndeks":176},{"ToplamSermaye":1990776000,"ToplamBorç":0,"TemelFiyat":238 50000000,"Sembol":"maske","İndeks":177},{"ToplamÖzsermaye":1076925578756,"ToplamBorç":0,"TemelFiyat":7989000000,"Sembol":"matik","İndeks":178},{"ToplamÖzsermaye":2785908800000,"ToplamBorç":0,"TemelFiyat":23690000,"Sembol":"mbl","İndeks":179},{"ToplamÖzsermaye":934922304,"ToplamBorç":0,"TemelFiyat":3850000000,"Sembol":"mbox","İndeks":180},{"ToplamÖzsermaye":13377446308,"ToplamBorç":0,"TemelFiyat":2670000000,"Sembol":"mc","İndeks":181},{"ToplamÖzsermaye":258144000,"ToplamBorç":0,"Ba sePrice":201100000,"Sembol":"mdt","İndeks":182},{"ToplamÖzsermaye":3081330908,"ToplamBorç":0,"TemelFiyat":716000000,"Sembol":"mdx","İndeks":183},{"ToplamÖzsermaye":32512116000,"ToplamBorç":0,"TemelFiyat":4500000000,"Sembol":"mina","İndeks" :184},{"Toplam Özsermaye":12110,"Toplam Borç":0,"Temel Fiyat":5400000000000,"Sembol":"mkr","İndeks":185},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":194100000000,"Sembol":"mln","İndeks":186},{"Toplam Özsermaye":132208000000,"Toplam Borç":0,"Ba sePrice":8660000000,"Sembol":"mob","İndeks":187},{"ToplamÖzsermaye":262072600,"ToplamBorç":0,"TemelFiyat":63100000000,"Sembol":"movr","İndeks":188},{"ToplamÖzsermaye":3096000,"ToplamBorç":0,"TemelFiyat":7020000000,"Sembol":"mtl","İndeks":1 89},{"ToplamÖzsermaye":5615144716,"ToplamBorç":0,"TemelFiyat":15900000000,"Sembol":"yakın","İndeks":190},{"ToplamÖzsermaye":6048000,"ToplamBorç":0,"TemelFiyat":13000000000,"Sembol":"nebl","İndeks":191},{"ToplamÖzsermaye":484605847032,"ToplamÖzsermaye t":0,"Temel Fiyat":65600000000,"Sembol":"neo","İndeks":192},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":7260000000,"Sembol":"nexo","İndeks":193},{"Toplam Özsermaye":2013960000,"Toplam Borç":0,"Temel Fiyat":862000000,"Sembol":"nkn","İndeks" :194},{"Toplam Özsermaye":39400,"Toplam Borç":0,"Temel Fiyat":129300000000,"Sembol":"nmr","İndeks":195},{"Toplam Özsermaye":99676000,"Toplam Borç":0,"Temel Fiyat":1901000000,"Sembol":"nuls","İndeks":196},{"Toplam Özsermaye":1063446,"Toplam Borç":0,"Ba sePrice":1906000000,"Sembol":"okyanus","İndeks":197},{"ToplamÖzsermaye":380000,"ToplamBorç":0,"TemelFiyat":23960000000,"Sembol":"og","İndeks":198},{"ToplamÖzsermaye":30491752,"ToplamBorç":0,"TemelFiyat":906000000,"Sembol":"ogn","İndeks":199},{"ToplamÖzsermaye":117360000,"ToplamBorç":0,"TemelFiyat":289000000,"Sembol":"om","İndeks":200},{"ToplamÖzsermaye":213392241236,"ToplamBorç":0,"TemelFiyat":10630000000,"Sembol":"omg","İndeks":201},{"ToplamÖzsermaye":561009012134,"ToplamBorç":0," TabanFiyat":106700000,"Sembol":"bir","İndeks":202},{"ToplamÖzsermaye":64315053780,"ToplamBorç":0,"TabanFiyat":2177482600,"Sembol":"uzun","İndeks":203},{"ToplamÖzsermaye":4682530773048,"ToplamBorç":0,"TabanFiyat":1609000000,"Sembol":"ont","İçinde dex":204},{"Toplam Özsermaye":893960000,"Toplam Borç":0,"Temel Fiyat":30800000,"Sembol":"ooki","İndeks":205},{"Toplam Özsermaye":383291200,"Toplam Borç":0,"Temel Fiyat":10840000000,"Sembol":"op","İndeks":206},{"Toplam Özsermaye":11568582000,"Toplam Borç t":0,"Temel Fiyat":7680000000,"Sembol":"orn","İndeks":207},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":7240000000,"Sembol":"osmo","İndeks":208},{"Toplam Özsermaye":178748000,"Toplam Borç":0,"Temel Fiyat":687000000,"Sembol":"oxt","İndeks":209 },{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":18530000000000,"Sembol":"paxg","İndeks":210},{"ToplamÖzsermaye":21441646500892,"ToplamBorç":0,"TemelFiyat":215100000,"Sembol":"insanlar","İndeks":211},{"ToplamÖzsermaye":1648337620,"ToplamBorç":0 ,"Temel Fiyat":3831300000,"Sembol":"perp","İndeks":212},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":1112000000,"Sembol":"pha","İndeks":213},{"Toplam Özsermaye":35466658000,"Toplam Borç":0,"Temel Fiyat":5237000000,"Sembol":"phb","İndeks":214} ,{"Toplam Özsermaye":28791180000,"Toplam Borç":0,"Temel Fiyat":1430000000,"Sembol":"pla","İndeks":215},{"Toplam Özsermaye":175000000,"Toplam Borç":0,"Temel Fiyat":1358592400,"Sembol":"pnt","İndeks":216},{"Toplam Özsermaye":3494881620000,"Toplam Borç":0 ,"Temel Fiyat":3570000000,"Sembol":"pols","İndeks":217},{"Toplam Özsermaye":74823148144,"Toplam Borç":0,"Temel Fiyat":1234000000,"Sembol":"polyx","İndeks":218},{"Toplam Özsermaye":493224786192,"Toplam Borç":0,"Temel Fiyat":77900000,"Sembol":"havuz","Dizin":219},{"ToplamÖzsermaye":72399098108,"ToplamBorç":0,"TemelFiyat":25696000000,"Sembol":"porto","Dizin":220},{"ToplamÖzsermaye":21005000000,"ToplamBorç":0,"TemelFiyat":1273000000,"Sembol":"güç","Dizin":221},{"ToplamÖzsermaye":0,"Toplam Borç":0,"Temel Fiyat":39200000000,"Sembol":"prom","İndeks":222},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":4230000000,"Sembol":"pros","İndeks":223},{"Toplam Özsermaye":2246200,"Toplam Borç":0,"Temel Fiyat":56400000000,"Sembol":"psg","İnd ex":224},{"Toplam Özsermaye":57372118540,"Toplam Borç":0,"Temel Fiyat":3240000000,"Sembol":"pundix","İndeks":225},{"Toplam Özsermaye":172800,"Toplam Borç":0,"Temel Fiyat":29800000000,"Sembol":"pyr","İndeks":226},{"Toplam Özsermaye":152556846850,"Toplam alDebt":0,"Temel Fiyat":65200000,"Sembol":"qi","İndeks":227},{"Toplam Özsermaye":703867724,"Toplam Borç":0,"Temel Fiyat":1118000000000,"Sembol":"qnt","İndeks":228},{"Toplam Özsermaye":209070344,"Toplam Borç":0,"Temel Fiyat":19610000000,"Sembol":"q tum","Index":229},{"TotalEquity":107668,"TotalDebt":0,"BasePrice":464000000000,"Symbol":"hızlı","Index":230},{"TotalEquity":15960000,"TotalDebt":0,"BasePrice":15330000000,"Symbol":"rad","Index":231},{"TotalEquity":0,"TotalDebt bt":0,"Temel Fiyat":1007000000,"Sembol":"nadir","İndeks":232},{"Toplam Özsermaye":20536980000,"Toplam Borç":0,"Temel Fiyat":1502000000,"Sembol":"ışın","İndeks":233},{"Toplam Özsermaye":2330100436820,"Toplam Borç":0,"Temel Fiyat":24230000,"Sembol":" resif","İndeks":234},{"ToplamÖzsermaye":692913057840,"ToplamBorç":0,"TemelFiyat":225000000,"Sembol":"rei","İndeks":235},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":630420000,"Sembol":"ren","İndeks":236},{"ToplamÖzsermaye":223600190,"ToplamD ebt":0,"Temel Fiyat":872000000,"Sembol":"req","İndeks":237},{"Toplam Özsermaye":18748000,"Toplam Borç":0,"Temel Fiyat":12427749000,"Sembol":"rlc","İndeks":238},{"Toplam Özsermaye":376358800,"Toplam Borç":0,"Temel Fiyat":4200000000,"Sembol":"rndr","Endeks":239},{"ToplamÖzsermaye":2094224000,"ToplamBorç":0,"TemelFiyat":370400000,"Sembol":"gül","Endeks":240},{"ToplamÖzsermaye":119940000,"ToplamBorç":0,"TemelFiyat":31690000,"Sembol":"rsr","Endeks":241},{"ToplamÖzsermaye":269393997600,"Toplam Borç":0,"Temel Fiyat":13750000000,"Sembol":"rune","İndeks":242},{"Toplam Özsermaye":539117133400,"Toplam Borç":0,"Temel Fiyat":203000000,"Sembol":"rvn","İndeks":243},{"Toplam Özsermaye":154754594184,"Toplam Borç":0,"Temel Fiyat":4309000000,"Sembol" :"kum","İndeks":244},{"ToplamÖzsermaye":2790903662,"ToplamBorç":0,"TemelFiyat":44700000000,"Sembol":"santos","İndeks":245},{"ToplamÖzsermaye":353200000,"ToplamBorç":0,"TemelFiyat":23600000,"Sembol":"sc","İndeks":246},{"ToplamÖzsermaye":0,"Toplam Borç":0,"Temel Fiyat":6390000000,"Sembol":"scrt","İndeks":247},{"Toplam Özsermaye":493481218,"Toplam Borç":0,"Temel Fiyat":4033000000,"Sembol":"sfp","İndeks":248},{"Toplam Özsermaye":92811810818000000,"Toplam Borç":0,"Temel Fiyat":84300,"Sembol":"sh ib","İndeks":249},{"Toplam Özsermaye":338633610064,"Toplam Borç":0,"Temel Fiyat":227300000,"Sembol":"skl","İndeks":250},{"Toplam Özsermaye":17412372632502,"Toplam Borç":0,"Temel Fiyat":20900000,"Sembol":"slp","İndeks":251},{"Toplam Özsermaye":19400000, "Toplam Borç": 0, "Temel Fiyat": 4858000000, "Sembol":"snm","İndeks": 252}, {"Toplam Özsermaye": 12518184, "Toplam Borç": 0, "Temel Fiyat": 16280000000, "Sembol":"snx","İndeks": 253}, {"Toplam Özsermaye": 7697220542, "Toplam Borç": 0, "Temel Fiyat": 135100000000, "Sembol l":"sol","Index":254},{"ToplamÖzsermaye":43400244636,"ToplamBorç":0,"TemelFiyat":5522000,"Sembol":"büyü","Index":255},{"ToplamÖzsermaye":145168230000,"ToplamBorç":0,"TemelFiyat":1567800000,"Sembol":"srm","Index":256},{"ToplamÖzsermaye":0,"Kime talDebt":0,"Temel Fiyat":3544000000,"Sembol":"stg","İndeks":257},{"Toplam Özsermaye":1375707000000,"Toplam Borç":0,"Temel Fiyat":38110000,"Sembol":"stmx","İndeks":258},{"Toplam Özsermaye":8912432530,"Toplam Borç":0,"Temel Fiyat":2582000000,"Sembol":"storj","İndeks":259},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":275900000,"Sembol":"stpt","İndeks":260},{"ToplamÖzsermaye":14047500,"ToplamBorç":0,"TemelFiyat":4050000000,"Sembol":"strax","İndeks":261},{"ToplamÖzsermaye":1423000,"ToplamD ebt":0,"Temel Fiyat":2190000000,"Sembol":"stx","İndeks":262},{"Toplam Özsermaye":326978131392,"Toplam Borç":0,"Temel Fiyat":50400000,"Sembol":"güneş","İndeks":263},{"Toplam Özsermaye":30595425600,"Toplam Borç":0,"Temel Fiyat":867000000,"Sembol":"su per","Index":264},{"ToplamSermaye":128556304136,"ToplamBorç":0,"TemelFiyat":10420000000,"Sembol":"suşi","Index":265},{"ToplamSermaye":1059292108408,"ToplamBorç":0,"TemelFiyat":2130000000,"Sembol":"sxp","Index":266},{"ToplamSermaye":1 30320000,"ToplamBorç":0,"TemelFiyat":1017000000,"Sembol":"sys","İndeks":267},{"ToplamÖzsermaye":5172000,"ToplamBorç":0,"TemelFiyat":163000000,"Sembol":"t","İndeks":268},{"ToplamÖzsermaye":1030910000,"ToplamBorç":0,"TemelFiyat":327000000,"Sembol":"sys","İndeks":267},{"ToplamÖzsermaye ...sys","İndeks":267},{"ToplamÖzsermaye":163000000,"Sembol":"t","İndeks":268},{"ToplamÖzsermaye":1030910000,"ToplamBorç":0,"TemelFiyat" bol":"tfuel","İndeks":269},{"ToplamÖzsermaye":160460684218,"ToplamBorç":0,"TemelFiyat":7590000000,"Sembol":"theta","İndeks":270},{"ToplamÖzsermaye":198770314330,"ToplamBorç":0,"TemelFiyat":2292000000,"Sembol":"tko","İndeks":271},{"ToplamEqu ity":256387034218,"Toplam Borç":0,"Temel Fiyat":128600000,"Sembol":"tlm","İndeks":272},{"Toplam Özsermaye":2508400,"Toplam Borç":0,"Temel Fiyat":2762000000,"Sembol":"tomo","İndeks":273},{"Toplam Özsermaye":9400,"Toplam Borç":0,"Temel Fiyat":12480000 0000,"Sembol":"trb","İndeks":274},{"ToplamÖzsermaye":33800000,"ToplamBorç":0,"TemelFiyat":2070797400,"Sembol":"kabile","İndeks":275},{"ToplamÖzsermaye":46160000,"ToplamBorç":0,"TemelFiyat":25980000,"Sembol":"troy","İndeks":276},{"ToplamÖdeme y":0,"ToplamBorç":0,"TemelFiyat":288071600,"Sembol":"tru","İndeks":277},{"ToplamÖzsermaye":2043669562480,"ToplamBorç":0,"TemelFiyat":524600000,"Sembol":"trx","İndeks":278},{"ToplamÖzsermaye":63678800000,"ToplamBorç":0,"TemelFiyat":301000000,"Sembol":"tvk","İndeks":279},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":14100000000,"Sembol":"twt","İndeks":280},{"ToplamÖzsermaye":13980000,"ToplamBorç":0,"TemelFiyat":15400000000,"Sembol":"uma","İndeks":281},{"ToplamÖzsermaye":1912000 0,"ToplamBorç":0,"TemelFiyat":39360000000,"Sembol":"unfi","İndeks":282},{"ToplamÖzsermaye":11981756100,"ToplamBorç":0,"TemelFiyat":55220000000,"Sembol":"uni","İndeks":283},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":10000650400,"Sembol ":"usdc","İndeks":284},{"ToplamÖzsermaye":12876907115652,"ToplamBorç":0,"TemelFiyat":9997000900,"Sembol":"usdt","İndeks":285},{"ToplamÖzsermaye":220063518946,"ToplamBorç":0,"TemelFiyat":203321700,"Sembol":"ustc","İndeks":286},{"ToplamÖzsermaye ":0,"ToplamBorç":0,"TemelFiyat":777000000,"Sembol":"utk","İndeks":287},{"ToplamÖzsermaye":7430929587566,"ToplamBorç":0,"TemelFiyat":164100000,"Sembol":"vet","İndeks":288},{"ToplamÖzsermaye":169058297966,"ToplamBorç":0,"TemelFiyat":694900000 ,"Sembol":"vib","İndeks":289},{"ToplamÖzsermaye":252046634,"ToplamBorç":0,"TemelFiyat":195000000,"Sembol":"vite","İndeks":290},{"ToplamÖzsermaye":25254109536,"ToplamBorç":0,"TemelFiyat":1671000000,"Sembol":"voxel","İndeks":291},{"ToplamÖzsermaye ity":5153547313742,"ToplamBorç":0,"TemelFiyat":9237200,"Sembol":"vtho","İndeks":292},{"ToplamÖzsermaye":17493828000,"ToplamBorç":0,"TemelFiyat":1658321600,"Sembol":"wan","İndeks":293},{"ToplamÖzsermaye":2852616,"ToplamBorç":0,"TemelFiyat":1 4130000000,"Sembol":"dalgalar","İndeks":294},{"ToplamÖzsermaye":20000180,"ToplamBorç":0,"TemelFiyat":440000000,"Sembol":"balmumu","İndeks":295},{"ToplamÖzsermaye":24776160000000,"ToplamBorç":0,"TemelFiyat":738000,"Sembol":"kazanmak","İndeks":296},{"T otalEquity":2370200,"ToplamBorç":0,"TemelFiyat":52100000000,"Sembol":"wing","İndeks":297},{"ToplamEquity":0,"ToplamBorç":0,"TemelFiyat":80975707300,"Sembol":"wnxm","İndeks":298},{"ToplamEquity":75262779600,"ToplamBorç":0,"TemelFiyat":1347000000,"Sembol":"woo","İndeks":299},{"ToplamÖzsermaye":415631596070,"ToplamBorç":0,"TemelFiyat":1401000000,"Sembol":"wrx","İndeks":300},{"ToplamÖzsermaye":183890000,"ToplamBorç":0,"TemelFiyat":1916 523600,"Sembol":"wtc","İndeks":301},{"ToplamÖzsermaye":172906064000000,"ToplamBorç":0,"TemelFiyat":246700,"Sembol":"xec","İndeks":302},{"ToplamÖzsermaye":129072400,"ToplamBorç":0,"TemelFiyat":291912400, "Sembol":"xem","İndeks":303},{"ToplamÖzsermaye":152986398800,"ToplamBorç":0,"TemelFiyat":751000000,"Sembol":"xlm","İndeks":304},{"ToplamÖzsermaye":109317164,"ToplamBorç":0,"TemelFiyat":1548000000000,"S ymbol":"xmr","İndeks":305},{"ToplamÖzsermaye":1954309930640,"ToplamBorç":0,"TemelFiyat":3442000000,"Symbol":"xrp","İndeks":306},{"ToplamÖzsermaye":388360923948,"ToplamBorç":0,"TemelFiyat":7720000000,"Sy mbol":"xtz","İndeks":307},{"ToplamÖzsermaye":45916405132400,"ToplamBorç":0,"TemelFiyat":27200000,"Sembol":"xvg","İndeks":308},{"ToplamÖzsermaye":1725600,"ToplamBorç":0,"TemelFiyat":42900000000,"Sembol" :"xvs","İndeks":309},{"ToplamÖzsermaye":1940,"ToplamBorç":0,"TemelFiyat":54420000000000,"Sembol":"yfi","İndeks":310},{"ToplamÖzsermaye":393918000,"ToplamBorç":0,"TemelFiyat":1749000000,"Sembol":"ygg","I ndex":311},{"ToplamÖzsermaye":4124782260,"ToplamBorç":0,"TemelFiyat":414000000000,"Sembol":"zec","İndeks":312},{"ToplamÖzsermaye":1900092,"ToplamBorç":0,"TemelFiyat":84900000000,"Sembol":"zen","İndeks": 313},{"Toplam Özsermaye":2075635646560,"Toplam Borç":0,"Temel Fiyat":174100000,"Sembol":"zil","İndeks":314},{"Toplam Özsermaye":119194400,"Toplam Borç":0,"Temel Fiyat":1603000000,"Sembol":"zrx","İndeks":315}]302},{"Toplam Özsermaye":129072400,"Toplam Borç":0,"Temel Fiyat":291912400,"Sembol":"xem","İndeks":303},{"Toplam Özsermaye":152986398800,"Toplam Borç":0,"Temel Fiyat":751000000,"Sembol":"xlm","İndeks":304},{"Toplam Özsermaye":109317164,"Toplam Borç":0,"Temel Fiyat":1548000000000,"Sembol":"xmr","İndeks":305},{"Toplam Özsermaye":1954 309930640,"ToplamBorç":0,"TemelFiyat":3442000000,"Sembol":"xrp","İndeks":306},{"ToplamÖzsermaye":388360923948,"ToplamBorç":0,"TemelFiyat":7720000000,"Sembol":"xtz","İndeks":307},{"ToplamÖzsermaye":45916405132400,"ToplamBorç":0,"TemelFiyat":27200000,"Sembol":"xvg","İndeks":308},{"ToplamÖzsermaye":1725600,"ToplamBorç":0, "Temel Fiyat":42900000000,"Sembol":"xvs","İndeks":309},{"Toplam Özsermaye":1940,"Toplam Borç":0,"Temel Fiyat":54420000000000,"Sembol":"yfi","İndeks":310},{"Toplam Özsermaye":393918000,"Toplam Borç":0,"Temel Fiyat":1749000000,"Sembol":"ygg","İndeks":311},{"Toplam Özsermaye":4124782260,"Toplam Borç":0,"Temel Fiyat":414000000000,"S ymbol":"zec","Index":312},{"TotalEquity":1900092,"TotalBorç":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalBorç":0,"BasePrice ":174100000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalBorç":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]302},{"Toplam Özsermaye":129072400,"Toplam Borç":0,"Temel Fiyat":291912400,"Sembol":"xem","İndeks":303},{"Toplam Özsermaye":152986398800,"Toplam Borç":0,"Temel Fiyat":751000000,"Sembol":"xlm","İndeks":304},{"Toplam Özsermaye":109317164,"Toplam Borç":0,"Temel Fiyat":1548000000000,"Sembol":"xmr","İndeks":305},{"Toplam Özsermaye":1954 309930640,"ToplamBorç":0,"TemelFiyat":3442000000,"Sembol":"xrp","İndeks":306},{"ToplamÖzsermaye":388360923948,"ToplamBorç":0,"TemelFiyat":7720000000,"Sembol":"xtz","İndeks":307},{"ToplamÖzsermaye":45916405132400,"ToplamBorç":0,"TemelFiyat":27200000,"Sembol":"xvg","İndeks":308},{"ToplamÖzsermaye":1725600,"ToplamBorç":0, "Temel Fiyat":42900000000,"Sembol":"xvs","İndeks":309},{"Toplam Özsermaye":1940,"Toplam Borç":0,"Temel Fiyat":54420000000000,"Sembol":"yfi","İndeks":310},{"Toplam Özsermaye":393918000,"Toplam Borç":0,"Temel Fiyat":1749000000,"Sembol":"ygg","İndeks":311},{"Toplam Özsermaye":4124782260,"Toplam Borç":0,"Temel Fiyat":414000000000,"S ymbol":"zec","Index":312},{"TotalEquity":1900092,"TotalBorç":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalBorç":0,"BasePrice ":174100000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalBorç":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]"Sembol":"xvs","İndeks":309},{"ToplamÖzsermaye":1940,"ToplamBorç":0,"TemelFiyat":54420000000000,"Sembol":"yfi","İndeks":310},{"ToplamÖzsermaye":393918000,"ToplamBorç":0,"TemelFiyat":1749000000,"Sembol":"ygg","İndeks":311},{"ToplamÖzsermaye":4124782260,"ToplamBorç":0,"TemelFiyat":414000000000,"Sembol":"zec" ,"Endex":312},{"TotalEquity":1900092,"TotalBorç":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalBorç":0,"BasePrice":17410 0000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalBorç":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]"Sembol":"xvs","İndeks":309},{"ToplamÖzsermaye":1940,"ToplamBorç":0,"TemelFiyat":54420000000000,"Sembol":"yfi","İndeks":310},{"ToplamÖzsermaye":393918000,"ToplamBorç":0,"TemelFiyat":1749000000,"Sembol":"ygg","İndeks":311},{"ToplamÖzsermaye":4124782260,"ToplamBorç":0,"TemelFiyat":414000000000,"Sembol":"zec" ,"Endex":312},{"TotalEquity":1900092,"TotalBorç":0,"BasePrice":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"TotalBorç":0,"BasePrice":17410 0000,"Symbol":"zil","Index":314},{"TotalEquity":119194400,"TotalBorç":0,"BasePrice":1603000000,"Symbol":"zrx","Index":315}]
```

Her seferinde kanıt verisi ürettikten sonra, cex varlıklarını bir kez sorgulamanız ve ardından bu verileri kaydetmeniz gerekir; bu veriler aşağıdaki `cex_config.json` dosyasının `CexAssetsInfo` alanında kullanılacaktır.

> Not: Buradaki proof.csv dosyası, kaydedilen varlık kanıtı verileriyle aynı gruptan olmalıdır, aksi takdirde doğrulama başarısız olabilir.

#### Yapılandırma Dosyası

cex_config.json, borsadaki varlıkların doğrulanması için kullanılan yapılandırma dosyasıdır.

```Düz metin
{
  "KanıtCsv": "./config/proof.csv",
  "ZkKeyVKDirectoryAndPrefix": "./zkpor864",
  "CexAssetsInfo": [{"ToplamÖzsermaye":10049232946,"ToplamBorç":0,"TemelFiyat":3960000000,"Sembol":"1inç","İndeks":0},{"ToplamÖzsermaye":421836,"ToplamBorç":0,"TemelFiyat":564000000000,"Sembol":"aave","İndeks":1},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelPr buz":79800000,"Sembol":"ach","İndeks":2},{"ToplamÖzsermaye":3040000,"ToplamBorç":0,"TemelFiyat":25460000000,"Sembol":"acm","İndeks":3},{"ToplamÖzsermaye":17700050162640,"ToplamBorç":0,"TemelFiyat":2784000000,"Sembol":"ada","İndeks":4}, {"ToplamSermaye":485400000,"ToplamBorç":0,"TemelFiyat":1182000000,"Sembol":"adx","İndeks":5},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":907000000,"Sembol":"aergo","İndeks":6},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":27200000 00,"Sembol":"agld","İndeks":7},{"ToplamÖzsermaye":1969000000,"ToplamBorç":0,"TemelFiyat":30500000,"Sembol":"akro","İndeks":8},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":141000000000,"Sembol":"alcx","İndeks":9},{"ToplamÖzsermaye":1548 3340912,"ToplamBorç":0,"TemelFiyat":1890000000,"Sembol":"algo","İndeks":10},{"ToplamÖzsermaye":3187400,"ToplamBorç":0,"TemelFiyat":11350000000,"Sembol":"alice","İndeks":11},{"ToplamÖzsermaye":1760000,"ToplamBorç":0,"TemelFiyat":2496000 000,"Sembol":"alpaca","İndeks":12},{"ToplamÖzsermaye":84596857600,"ToplamBorç":0,"TemelFiyat":785000000,"Sembol":"alfa","İndeks":13},{"ToplamÖzsermaye":3672090936,"ToplamBorç":0,"TemelFiyat":20849000000,"Sembol":"alpine","İndeks":14}, {"ToplamÖzsermaye":198200000,"ToplamBorç":0,"TemelFiyat":132600000,"Sembol":"amb","İndeks":15},{"ToplamÖzsermaye":53800000,"ToplamBorç":0,"TemelFiyat":32200000,"Sembol":"amp","İndeks":16},{"ToplamÖzsermaye":3291606210,"ToplamBorç":0,"TemelP pirinç":340300000,"Sembol":"anc","İndeks":17},{"ToplamÖzsermaye":192954000,"ToplamBorç":0,"TemelFiyat":166000000,"Sembol":"ankr","İndeks":18},{"ToplamÖzsermaye":2160000,"ToplamBorç":0,"TemelFiyat":20940000000,"Sembol":"karınca","İndeks":19},{"ToplamÖzsermaye":5995002000,"ToplamBorç":0,"TemelFiyat":40370000000,"Sembol":"ape","İndeks":20},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":11110000000,"Sembol":"api3","İndeks":21},{"ToplamÖzsermaye":53728000,"ToplamBorç":0,"TemelFiyat" :38560000000,"Sembol":"apt","İndeks":22},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":68500000000,"Sembol":"ar","İndeks":23},{"ToplamÖzsermaye":55400000,"ToplamBorç":0,"TemelFiyat":667648400,"Sembol":"ardr","İndeks":24},{"ToplamÖzsermaye" :8320000,"ToplamBorç":0,"TemelFiyat":266200000,"Sembol":"arpa","İndeks":25},{"ToplamÖzsermaye":18820000,"ToplamBorç":0,"TemelFiyat":401000000,"Sembol":"astr","İndeks":26},{"ToplamÖzsermaye":13205405410,"ToplamBorç":0,"TemelFiyat":934000000 ,"Sembol":"ata","İndeks":27},{"ToplamÖzsermaye":7016230960,"ToplamBorç":0,"TemelFiyat":102450000000,"Sembol":"atom","İndeks":28},{"ToplamÖzsermaye":2619441828,"ToplamBorç":0,"TemelFiyat":40900000000,"Sembol":"müzayede","İndeks":29},{"ToplamE quity":9640198,"ToplamBorç":0,"TemelFiyat":1432000000,"Sembol":"ses","İndeks":30},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":2306000000000,"Sembol":"otomatik","İndeks":31},{"ToplamÖzsermaye":886400,"ToplamBorç":0,"TemelFiyat":539000000 0,"Sembol":"ava","İndeks":32},{"ToplamÖzsermaye":2883562350,"ToplamBorç":0,"TemelFiyat":117800000000,"Sembol":"avax","İndeks":33},{"ToplamÖzsermaye":1864300912,"ToplamBorç":0,"TemelFiyat":68200000000,"Sembol":"axs","İndeks":34},{"ToplamÖzsermaye ity":843870,"ToplamBorç":0,"TemelFiyat":23700000000,"Sembol":"porsuk","İndeks":35},{"ToplamÖzsermaye":114869291528,"ToplamBorç":0,"TemelFiyat":1379000000,"Sembol":"pişir","İndeks":36},{"ToplamÖzsermaye":95400,"ToplamBorç":0,"TemelFiyat":541 10000000,"Sembol":"bal","İndeks":37},{"ToplamÖzsermaye":123113880,"ToplamBorç":0,"TemelFiyat":14610000000,"Sembol":"bant","İndeks":38},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":37100000000,"Sembol":"çubuk","İndeks":39},{"ToplamÖzsermaye":73090049578,"ToplamBorç":0,"TemelFiyat":1774000000,"Sembol":"bat","İndeks":40},{"ToplamÖzsermaye":28891300,"ToplamBorç":0,"TemelFiyat":1017000000000,"Sembol":"bch","İndeks":41},{"ToplamÖzsermaye":19889623294,"ToplamBorç":0,"TemelFiyat":41300 00000,"Sembol":"bel","İndeks":42},{"ToplamÖzsermaye":374840602180,"ToplamBorç":0,"TemelFiyat":699700000,"Sembol":"beta","İndeks":43},{"ToplamÖzsermaye":270294580,"ToplamBorç":0,"TemelFiyat":12290900000000,"Sembol":"beth","İndeks":44},{"Toplam lSermaye":35692901600,"ToplamBorç":0,"TemelFiyat":2730000000,"Sembol":"bico","İndeks":45},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":639000,"Sembol":"bidr","İndeks":46},{"ToplamSermaye":240200000,"ToplamBorç":0,"TemelFiyat":538000000, "Sembol":"blz","İndeks":47},{"ToplamÖzsermaye":83614634622,"ToplamBorç":0,"TemelFiyat":2599000000000,"Sembol":"bnb","İndeks":48},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3490000000,"Sembol":"bnt","İndeks":49},{"ToplamÖzsermaye":1560,"Toplam alDebt":0,"Temel Fiyat":592000000000,"Sembol":"bnx","İndeks":50},{"Toplam Özsermaye":2076000,"Toplam Borç":0,"Temel Fiyat":32630000000,"Sembol":"tahvil","İndeks":51},{"Toplam Özsermaye":44699589660,"Toplam Borç":0,"Temel Fiyat":1768000000,"Sembol":" bsw","İndeks":52},{"ToplamÖzsermaye":291716078,"ToplamBorç":0,"TemelFiyat":169453900000000,"Sembol":"btc","İndeks":53},{"ToplamÖzsermaye":15500321300000000,"ToplamBorç":0,"TemelFiyat":6300,"Sembol":"bttc","İndeks":54},{"ToplamÖzsermaye":7077154 6756,"ToplamBorç":0,"TabanFiyat":5240000000,"Symbol":"burger","Endeks":55},{"TotalEquity":12058907297354,"ToplamBorç":1476223055432,"BazFiyat":10000000000,"Sembol" :"busd","Index":56},{"TotalEquity":34716440000,"TotalBorç":0,"Bas ePrice":1647000000,"Sembol":"c98","İndeks":57},{"ToplamÖzsermaye":1541723702,"ToplamBorç":0,"TemelFiyat":33140000000,"Sembol":"kek","İndeks":58},{"ToplamÖzsermaye":2112000,"ToplamBorç":0,"TemelFiyat":5200000000,"Sembol":"celo","İndeks":59},{"ToplamÖzsermaye":317091540000,"ToplamBorç":0,"TemelFiyat":101000000,"Sembol":"celr","İndeks":60},{"ToplamÖzsermaye":137111365560,"ToplamBorç":0,"TemelFiyat":228000000,"Sembol":"cfx","İndeks":61},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat e":1820000000,"Sembol":"satranç","İndeks":62},{"ToplamÖzsermaye":258540000,"ToplamBorç":0,"TemelFiyat":1140000000,"Sembol":"chr","İndeks":63},{"ToplamÖzsermaye":289172288882,"ToplamBorç":0,"TemelFiyat":1099000000,"Sembol":"chz","İndeks":64} ,{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":25100000,"Sembol":"ckb","İndeks":65},{"ToplamÖzsermaye":1851135024806,"ToplamBorç":0,"TemelFiyat":535500000,"Sembol":"clv","İndeks":66},{"ToplamÖzsermaye":155010000,"ToplamBorç":0,"TemelFiyat": 5202000000,"Sembol":"cocos","İndeks":67},{"ToplamÖzsermaye":52093390,"ToplamBorç":0,"TemelFiyat":335800000000,"Sembol":"comp","İndeks":68},{"ToplamÖzsermaye":13991592000,"ToplamBorç":0,"TemelFiyat":44500000,"Sembol":"cos","İndeks":69},{"Kime talEquity":51240788068,"ToplamBorç":0,"TemelFiyat":557000000,"Sembol":"coti","İndeks":70},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":107900000000,"Sembol":"cream","İndeks":71},{"ToplamSermaye":15940224,"ToplamBorç":0,"TemelFiyat":5 470000000,"Sembol":"crv","İndeks":72},{"ToplamÖzsermaye":2336000,"ToplamBorç":0,"TemelFiyat":7450000000,"Sembol":"ctk","İndeks":73},{"ToplamÖzsermaye":88860000,"ToplamBorç":0,"TemelFiyat":1059000000,"Sembol":"ctsi","İndeks":74},{"ToplamÖzsermaye":74},{"ToplamÖzsermaye":740000000,"ToplamÖzsermaye":74 ... ity":440400000,"ToplamBorç":0,"TemelFiyat":1763000000,"Sembol":"ctxc","İndeks":75},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3375000000,"Sembol":"cvp","İndeks":76},{"ToplamÖzsermaye":176202,"ToplamBorç":0,"TemelFiyat":30810000000,"S ymbol":"cvx","İndeks":77},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":9999000100,"Symbol":"dai","İndeks":78},{"ToplamÖzsermaye":90702266836,"ToplamBorç":0,"TemelFiyat":1293500000,"Symbol":"dar","İndeks":79},{"ToplamÖzsermaye":29386961406,"ToplamBorç":0,"TemelFiyat":458300000000,"Sembol":"tire","İndeks":80},{"ToplamÖzsermaye":1628888000,"ToplamBorç":0,"TemelFiyat":235500000,"Sembol":"veri","İndeks":81},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":186229836100,"Sembol":" dcr","İndeks":82},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":15920000000,"Sembol":"dego","İndeks":83},{"ToplamÖzsermaye":26105549312822,"ToplamBorç":0,"TemelFiyat":6830000,"Sembol":"dent","İndeks":84},{"ToplamÖzsermaye":670658000,"Toplam Borç":0,"Temel Fiyat":24000000000,"Sembol":"dexe","İndeks":85},{"Toplam Özsermaye":517372774000,"Toplam Borç":0,"Temel Fiyat":82200000,"Sembol":"dgb","İndeks":86},{"Toplam Özsermaye":1120000,"Toplam Borç":0,"Temel Fiyat":2970000000,"Sembol":"dia ","İndeks":87},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":151800000,"Sembol":"dock","İndeks":88},{"ToplamÖzsermaye":19453393384,"ToplamBorç":0,"TemelFiyat":987000000,"Sembol":"dodo","İndeks":89},{"ToplamÖzsermaye":25526548451614,"ToplamD ebt":0,"Temel Fiyat":723900000,"Sembol":"doge","İndeks":90},{"Toplam Özsermaye":466049240950,"Toplam Borç":0,"Temel Fiyat":46820000000,"Sembol":"nokta","İndeks":91},{"Toplam Özsermaye":69200000,"Toplam Borç":0,"Temel Fiyat":3138000000,"Sembol":"dr ep","Index":92},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":870000000,"Sembol":"alacakaranlık","Index":93},{"ToplamÖzsermaye":45675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","Index":94},{"ToplamÖzsermaye":241920370,"ToplamÖzsermaye bt":0,"Temel Fiyat":343400000000,"Sembol":"egld","İndeks":95},{"Toplam Özsermaye":3640000,"Toplam Borç":0,"Temel Fiyat":1691000000,"Sembol":"elf","İndeks":96},{"Toplam Özsermaye":200008070,"Toplam Borç":0,"Temel Fiyat":2556000000,"Sembol":"enj", "Dizin":97},{"Toplam Özsermaye":836000,"Toplam Borç":0,"Temel Fiyat":115500000000,"Sembol":"ens","Dizin":98},{"Toplam Özsermaye":23489390223668,"Toplam Borç":0,"Temel Fiyat":8960000000,"Sembol":"eos","Dizin":99},{"Toplam Özsermaye":83358943947200,"ToplamBorç":0,"TemelFiyat":2960000,"Sembol":"epx","İndeks":100},{"ToplamÖzsermaye":1539180000,"ToplamBorç":0,"TemelFiyat":17540000000,"Sembol":"ern","İndeks":101},{"ToplamÖzsermaye":48056621250,"ToplamBorç":0,"TemelFiyat":204100000000,"Sy mbol":"etc","Index":102},{"ToplamÖzsermaye":28478224392,"ToplamBorç":0,"TemelFiyat":12688000000000,"Sembol":"eth","Index":103},{"ToplamÖzsermaye":21790805772,"ToplamBorç":0,"TemelFiyat":10641000000,"Sembol":"eur","Index":104},{"ToplamEqu ity":196200,"ToplamBorç":0,"TemelFiyat":307000000000,"Sembol":"çiftlik","İndeks":105},{"ToplamÖzsermaye":31040000,"ToplamBorç":0,"TemelFiyat":1240000000,"Sembol":"fet","İndeks":106},{"ToplamÖzsermaye":26460000,"ToplamBorç":0,"TemelFiyat":33540 00000,"Sembol":"fida","İndeks":107},{"ToplamÖzsermaye":5539231876,"ToplamBorç":0,"TemelFiyat":33380000000,"Sembol":"fil","İndeks":108},{"ToplamÖzsermaye":152000000,"ToplamBorç":0,"TemelFiyat":275000000,"Sembol":"fio","İndeks":109},{"ToplamE quity":1014252612,"Toplam Borç":0,"Temel Fiyat":16540000000,"Sembol":"firo","İndeks":110},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":3313000000,"Sembol":"fis","İndeks":111},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":765931600,"Sembol bol":"flm","Index":112},{"ToplamÖzsermaye":3688000,"ToplamBorç":0,"TemelFiyat":6990000000,"Sembol":"akış","Index":113},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":5090000000,"Sembol":"akış","Index":114},{"ToplamÖzsermaye":0,"ToplamBorç" :0,"Temel Fiyat":162500000,"Sembol":"için","İndeks":115},{"Toplam Özsermaye":80000,"Toplam Borç":0,"Temel Fiyat":29400000000,"Sembol":"ileri","İndeks":116},{"Toplam Özsermaye":14430200000,"Toplam Borç":0,"Temel Fiyat":1808000000,"Sembol":"ön"," Dizin":117},{"Toplam Özkaynak":26629480000,"Toplam Borç":0,"Temel Fiyat":2211000000,"Sembol":"ftm","Dizin":118},{"Toplam Özkaynak":16207428000,"Toplam Borç":0,"Temel Fiyat":9125000000,"Sembol":"ftt","Dizin":119},{"Toplam Özkaynak":679597613272,"ToplamBorç":0,"TemelFiyat":61663700,"Sembol":"eğlence","İndeks":120},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":51410000000,"Sembol":"fxs","İndeks":121},{"ToplamÖzsermaye":4110633550,"ToplamBorç":0,"TemelFiyat":11540000000,"Sembol":"gal" ,"Endeks":122},{"ToplamÖzsermaye":2551466375170,"ToplamBorç":0,"TemelFiyat":234700000,"Sembol":"gala","Endeks":123},{"ToplamÖzsermaye":1252940134,"ToplamBorç":0,"TemelFiyat":20260000000,"Sembol":"gaz","Endeks":124},{"ToplamÖzsermaye":0,"ToplamÖzsermaye bt":0,"Temel Fiyat":1850000000,"Sembol":"glm","İndeks":125},{"Toplam Özsermaye":25058958996,"Toplam Borç":0,"Temel Fiyat":3195000000,"Sembol":"glmr","İndeks":126},{"Toplam Özsermaye":443980786672,"Toplam Borç":0,"Temel Fiyat":2588000000,"Sembol": "gmt","İndeks":127},{"ToplamÖzsermaye":160000,"ToplamBorç":0,"TemelFiyat":417300000000,"Sembol":"gmx","İndeks":128},{"ToplamÖzsermaye":178800,"ToplamBorç":0,"TemelFiyat":878736379100,"Sembol":"gno","İndeks":129},{"ToplamÖzsermaye":6828000,"Toplam lBorç":0,"Temel Fiyat":620000000,"Sembol":"grt","İndeks":130},{"Toplam Özsermaye":20784000,"Toplam Borç":0,"Temel Fiyat":13340000000,"Sembol":"gtc","İndeks":131},{"Toplam Özsermaye":94280000,"Toplam Borç":0,"Temel Fiyat":1494000000,"Sembol":"zor ","İndeks":132},{"ToplamÖzsermaye":336206273140,"ToplamBorç":0,"TemelFiyat":391000000,"Sembol":"hbar","İndeks":133},{"ToplamÖzsermaye":1791317190,"ToplamBorç":0,"TemelFiyat":8870000000,"Sembol":"yüksek","İndeks":134},{"ToplamÖzsermaye":6485637600 ,"ToplamBorç":0,"TemelFiyat":2700000000,"Sembol":"kovan","İndeks":135},{"ToplamÖzsermaye":1956144,"ToplamBorç":0,"TemelFiyat":18400000000,"Sembol":"hnt","İndeks":136},{"ToplamÖzsermaye":9587039140000,"ToplamBorç":0,"TemelFiyat":14820000,"Sembol bol":"sıcak","İndeks":137},{"ToplamÖzsermaye":223895102366,"ToplamBorç":0,"TemelFiyat":38980000000,"Sembol":"icp","İndeks":138},{"ToplamÖzsermaye":52168047570,"ToplamBorç":0,"TemelFiyat":1516000000,"Sembol":"icx","İndeks":139},{"ToplamÖzsermaye":15480000,"ToplamBorç":0,"TemelFiyat":388000000,"Sembol":"idex","İndeks":140},{"ToplamÖzsermaye":8400000,"ToplamBorç":0,"TemelFiyat":388700000000,"Sembol":"ilv","İndeks":141},{"ToplamÖzsermaye":12686368000,"ToplamBorç":0,"TemelFiyat":423000 0000,"Sembol":"imx","İndeks":142},{"ToplamÖzsermaye":139990936000,"ToplamBorç":0,"TemelFiyat":13680000000,"Sembol":"inj","İndeks":143},{"ToplamÖzsermaye":69430091021436,"ToplamBorç":0,"TemelFiyat":72500000,"Sembol":"iost","İndeks":144},{"T otalEquity":71259628200,"ToplamBorç":0,"TemelFiyat":1823000000,"Sembol":"iota","İndeks":145},{"ToplamEquity":428000000,"ToplamBorç":0,"TemelFiyat":221500000,"Sembol":"iotx","İndeks":146},{"ToplamEquity":858126200,"ToplamBorç":0,"Temel ePrice":43200000,"Sembol":"iq","İndeks":147},{"ToplamSermaye":8680000,"ToplamBorç":0,"TemelFiyat":132174000,"Sembol":"iris","İndeks":148},{"ToplamSermaye":1889177748140,"ToplamBorç":0,"TemelFiyat":37600000,"Sembol":"jasmy","İndeks":149 },{"ToplamÖzsermaye":2000,"ToplamBorç":0,"TemelFiyat":1416000000,"Sembol":"joe","İndeks":150},{"ToplamÖzsermaye":927921956,"ToplamBorç":0,"TemelFiyat":201400000,"Sembol":"jst","İndeks":151},{"ToplamÖzsermaye":560000,"ToplamBorç":0,"TemelFiyat" :6590000000,"Sembol":"kava","İndeks":152},{"ToplamÖzsermaye":30527442000,"ToplamBorç":0,"TemelFiyat":9480000000,"Sembol":"kda","İndeks":153},{"ToplamÖzsermaye":7587760000,"ToplamBorç":0,"TemelFiyat":29350000,"Sembol":"anahtar","İndeks":154},{" ToplamÖzsermaye":372181704,"ToplamBorç":0,"TemelFiyat":1613000000,"Sembol":"klay","İndeks":155},{"ToplamÖzsermaye":81600000,"ToplamBorç":0,"TemelFiyat":1904661800,"Sembol":"kmd","İndeks":156},{"ToplamÖzsermaye":493317080,"ToplamBorç":0,"TemelP pirinç":4940000000,"Sembol":"knc","İndeks":157},{"ToplamÖzsermaye":1700000,"ToplamBorç":0,"TemelFiyat":621600000000,"Sembol":"kp3r","İndeks":158},{"ToplamÖzsermaye":27180,"ToplamBorç":0,"TemelFiyat":250100000000,"Sembol":"ksm","İndeks":159},{"ToplamÖzsermaye":1656679204,"ToplamBorç":0,"TemelFiyat":30978000000,"Sembol":"lazio","İndeks":160},{"ToplamÖzsermaye":295510852208,"ToplamBorç":0,"TemelFiyat":15200000000,"Sembol":"ldo","İndeks":161},{"ToplamÖzsermaye":1158728143570,"ToplamBorç t":0,"Temel Fiyat":17230000,"Sembol":"kaldıraç","İndeks":162},{"Toplam Özsermaye":6505365672842,"Toplam Borç":0,"Temel Fiyat":52690000,"Sembol":"lina","İndeks":163},{"Toplam Özsermaye":8162369516,"Toplam Borç":0,"Temel Fiyat":57120000000,"Sembol":"lin k","İndeks":164},{"ToplamÖzsermaye":95484000,"ToplamBorç":0,"TemelFiyat":7220000000,"Sembol":"lit","İndeks":165},{"ToplamÖzsermaye":12682220,"ToplamBorç":0,"TemelFiyat":3632000000,"Sembol":"loka","İndeks":166},{"ToplamÖzsermaye":0,"ToplamBorç":0, "Temel Fiyat":409400000,"Sembol":"tezgah","İndeks":167},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":44400000000,"Sembol":"lpt","İndeks":168},{"Toplam Özsermaye":10715077402,"Toplam Borç":0,"Temel Fiyat":2063000000,"Sembol":"lrc","İndeks":169},{ "Toplam Özkaynak":8050236298,"Toplam Borç":0,"Temel Fiyat":7240000000,"Sembol":"lsk","İndeks":170},{"Toplam Özkaynak":1122426768,"Toplam Borç":0,"Temel Fiyat":758900000000,"Sembol":"ltc","İndeks":171},{"Toplam Özkaynak":22654000,"Toplam Borç":0,"Temel Fiyat":710000000,"Sembol":"lto","İndeks":172},{"ToplamÖzsermaye":16580624988,"ToplamBorç":0,"TemelFiyat":13251000000,"Sembol":"luna","İndeks":173},{"ToplamÖzsermaye":1705595428000000,"ToplamBorç":0,"TemelFiyat":1560500,"Sembol":"lunc","İndeks x":174},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":4759000000,"Sembol":"sihirli","İndeks":175},{"ToplamÖzsermaye":77632636722,"ToplamBorç":0,"TemelFiyat":3278000000,"Sembol":"mana","İndeks":176},{"ToplamÖzsermaye":1990776000,"ToplamBorç":0," TabanFiyat":23850000000,"Sembol":"maske","İndeks":177},{"ToplamÖzsermaye":1076925578756,"ToplamBorç":0,"TabanFiyat":7989000000,"Sembol":"matik","İndeks":178},{"ToplamÖzsermaye":2785908800000,"ToplamBorç":0,"TabanFiyat":23690000,"Sembol":"mbl","Dizin":179},{"ToplamÖzsermaye":934922304,"ToplamBorç":0,"TemelFiyat":3850000000,"Sembol":"mbox","Dizin":180},{"ToplamÖzsermaye":13377446308,"ToplamBorç":0,"TemelFiyat":2670000000,"Sembol":"mc","Dizin":181},{"ToplamÖzsermaye":258144000,"Toplam alDebt":0,"Temel Fiyat":201100000,"Sembol":"mdt","İndeks":182},{"Toplam Özsermaye":3081330908,"Toplam Borç":0,"Temel Fiyat":716000000,"Sembol":"mdx","İndeks":183},{"Toplam Özsermaye":32512116000,"Toplam Borç":0,"Temel Fiyat":4500000000,"Sembol":" mina","Index":184},{"TotalEquity":12110,"TotalBorç":0,"BasePrice":54000000000000,"Symbol":"mkr","Index":185},{"TotalEquity":0,"TotalBorç":0,"BasePrice":194100000000," Sembol":"mln","Dizin":186},{"TotalEquity":132208000000,"Toplam alDebt":0,"Temel Fiyat":8660000000,"Sembol":"mob","İndeks":187},{"Toplam Özsermaye":262072600,"Toplam Borç":0,"Temel Fiyat":63100000000,"Sembol":"movr","İndeks":188},{"Toplam Özsermaye":3096000,"Toplam Borç":0,"Temel Fiyat":7020000000,"Sembol":"m tl","Index":189},{"ToplamÖzsermaye":5615144716,"ToplamBorç":0,"TemelFiyat":15900000000,"Sembol":"yakın","Index":190},{"ToplamÖzsermaye":6048000,"ToplamBorç":0,"TemelFiyat":13000000000,"Sembol":"nebl","Index":191},{"ToplamÖzsermaye":484605847 032,"ToplamBorç":0,"TemelFiyat":65600000000,"Sembol":"neo","İndeks":192},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":7260000000,"Sembol":"nexo","İndeks":193},{"ToplamÖzsermaye":2013960000,"ToplamBorç":0,"TemelFiyat":862000000,"Sembol": "nkn","İndeks":194},{"ToplamÖzsermaye":39400,"ToplamBorç":0,"TemelFiyat":129300000000,"Sembol":"nmr","İndeks":195},{"ToplamÖzsermaye":99676000,"ToplamBorç":0,"TemelFiyat":1901000000,"Sembol":"nuls","İndeks":196},{"ToplamÖzsermaye":1063446,"Toplam alDebt":0,"Temel Fiyat":1906000000,"Sembol":"okyanus","İndeks":197},{"Toplam Özsermaye":380000,"Toplam Borç":0,"Temel Fiyat":23960000000,"Sembol":"og","İndeks":198},{"Toplam Özsermaye":30491752,"Toplam Borç":0,"Temel Fiyat":906000000,"Sembol":"ogn","Dizin":199},{"ToplamÖzsermaye":117360000,"ToplamBorç":0,"TemelFiyat":289000000,"Sembol":"om","Dizin":200},{"ToplamÖzsermaye":213392241236,"ToplamBorç":0,"TemelFiyat":10630000000,"Sembol":"omg","Dizin":201},{"ToplamÖzsermaye":561009012134,"Kime talDebt":0,"Temel Fiyat":106700000,"Sembol":"bir","İndeks":202},{"Toplam Özsermaye":64315053780,"Toplam Borç":0,"Temel Fiyat":2177482600,"Sembol":"uzun","İndeks":203},{"Toplam Özsermaye":4682530773048,"Toplam Borç":0,"Temel Fiyat":1609000000,"Sembol ":"ont","İndeks":204},{"Toplam Özsermaye":893960000,"Toplam Borç":0,"Temel Fiyat":30800000,"Sembol":"ooki","İndeks":205},{"Toplam Özsermaye":383291200,"Toplam Borç":0,"Temel Fiyat":10840000000,"Sembol":"op","İndeks":206},{"Toplam Özsermaye":11568582000 ,"ToplamBorç":0,"TemelFiyat":7680000000,"Sembol":"orn","İndeks":207},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":7240000000,"Sembol":"osmo","İndeks":208},{"ToplamÖzsermaye":178748000,"ToplamBorç":0,"TemelFiyat":687000000,"Sembol":"oxt"," Dizin":209},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":18530000000000,"Sembol":"paxg","Dizin":210},{"ToplamÖzsermaye":21441646500892,"ToplamBorç":0,"TemelFiyat":215100000,"Sembol":"insanlar","Dizin":211},{"ToplamÖzsermaye":1648337620,"Toplam alDebt":0,"Temel Fiyat":3831300000,"Sembol":"perp","İndeks":212},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":1112000000,"Sembol":"pha","İndeks":213},{"Toplam Özsermaye":35466658000,"Toplam Borç":0,"Temel Fiyat":5237000000,"Sembol":"phb","İçinde dex":214},{"Toplam Özkaynak":28791180000,"Toplam Borç":0,"Temel Fiyat":1430000000,"Sembol":"pla","İndeks":215},{"Toplam Özkaynak":175000000,"Toplam Borç":0,"Temel Fiyat":1358592400,"Sembol":"pnt","İndeks":216},{"Toplam Özkaynak":3494881620000,"Toplam lBorç":0,"Temel Fiyat":3570000000,"Sembol":"pols","İndeks":217},{"Toplam Özsermaye":74823148144,"Toplam Borç":0,"Temel Fiyat":1234000000,"Sembol":"polyx","İndeks":218},{"Toplam Özsermaye":493224786192,"Toplam Borç":0,"Temel Fiyat":77900000,"Sembol":"gölet","İndeks":219},{"ToplamÖzsermaye":72399098108,"ToplamBorç":0,"TemelFiyat":25696000000,"Sembol":"porto","İndeks":220},{"ToplamÖzsermaye":21005000000,"ToplamBorç":0,"TemelFiyat":1273000000,"Sembol":"güç","İndeks":221},{"ToplamÖzsermaye":0 ,"ToplamBorç":0,"TemelFiyat":39200000000,"Sembol":"prom","İndeks":222},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":4230000000,"Sembol":"artıları","İndeks":223},{"ToplamÖzsermaye":2246200,"ToplamBorç":0,"TemelFiyat":56400000000,"Sembol":"ps g","İndeks":224},{"ToplamÖzsermaye":57372118540,"ToplamBorç":0,"TemelFiyat":3240000000,"Sembol":"pundix","İndeks":225},{"ToplamÖzsermaye":172800,"ToplamBorç":0,"TemelFiyat":29800000000,"Sembol":"pyr","İndeks":226},{"ToplamÖzsermaye":1525568468 50,"Toplam Borç":0,"Temel Fiyat":65200000,"Sembol":"qi","İndeks":227},{"Toplam Özsermaye":703867724,"Toplam Borç":0,"Temel Fiyat":1118000000000,"Sembol":"qnt","İndeks":228},{"Toplam Özsermaye":209070344,"Toplam Borç":0,"Temel Fiyat":19610000000,"Sembol bol":"qtum","İndeks":229},{"ToplamÖzsermaye":107668,"ToplamBorç":0,"TemelFiyat":464000000000,"Sembol":"hızlı","İndeks":230},{"ToplamÖzsermaye":15960000,"ToplamBorç":0,"TemelFiyat":15330000000,"Sembol":"rad","İndeks":231},{"ToplamÖzsermaye":0," ToplamBorç":0,"TemelFiyat":1007000000,"Sembol":"nadir","İndeks":232},{"ToplamÖzsermaye":20536980000,"ToplamBorç":0,"TemelFiyat":1502000000,"Sembol":"ışın","İndeks":233},{"ToplamÖzsermaye":2330100436820,"ToplamBorç":0,"TemelFiyat":24230000,"Sy mbol":"resif","İndeks":234},{"Toplam Özsermaye":692913057840,"Toplam Borç":0,"Temel Fiyat":225000000,"Sembol":"rei","İndeks":235},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":630420000,"Sembol":"ren","İndeks":236},{"Toplam Özsermaye":223600190, "ToplamBorç":0,"TemelFiyat":872000000,"Sembol":"req","İndeks":237},{"ToplamÖzsermaye":18748000,"ToplamBorç":0,"TemelFiyat":12427749000,"Sembol":"rlc","İndeks":238},{"ToplamÖzsermaye":376358800,"ToplamBorç":0,"TemelFiyat":4200000000,"Sembol":"rndr","İndeks":239},{"ToplamÖzsermaye":2094224000,"ToplamBorç":0,"TemelFiyat":370400000,"Sembol":"gül","İndeks":240},{"ToplamÖzsermaye":119940000,"ToplamBorç":0,"TemelFiyat":31690000,"Sembol":"rsr","İndeks":241},{"ToplamÖzsermaye":269393997600 ,"ToplamBorç":0,"TemelFiyat":13750000000,"Sembol":"rune","İndeks":242},{"ToplamÖzsermaye":539117133400,"ToplamBorç":0,"TemelFiyat":203000000,"Sembol":"rvn","İndeks":243},{"ToplamÖzsermaye":154754594184,"ToplamBorç":0,"TemelFiyat":4309000000," Sembol":"kum","İndeks":244},{"ToplamÖzsermaye":2790903662,"ToplamBorç":0,"TemelFiyat":44700000000,"Sembol":"santos","İndeks":245},{"ToplamÖzsermaye":353200000,"ToplamBorç":0,"TemelFiyat":23600000,"Sembol":"sc","İndeks":246},{"ToplamÖzsermaye":0 ,"ToplamBorç":0,"TemelFiyat":6390000000,"Sembol":"scrt","İndeks":247},{"ToplamÖzsermaye":493481218,"ToplamBorç":0,"TemelFiyat":4033000000,"Sembol":"sfp","İndeks":248},{"ToplamÖzsermaye":92811810818000000,"ToplamBorç":0,"TemelFiyat":84300,"Sembol bol":"shib","İndeks":249},{"ToplamÖzsermaye":338633610064,"ToplamBorç":0,"TemelFiyat":227300000,"Sembol":"skl","İndeks":250},{"ToplamÖzsermaye":17412372632502,"ToplamBorç":0,"TemelFiyat":20900000,"Sembol":"slp","İndeks":251},{"ToplamÖzsermaye":1 9400000,"ToplamBorç":0,"TemelFiyat":4858000000,"Sembol":"snm","İndeks":252},{"ToplamÖzsermaye":12518184,"ToplamBorç":0,"TemelFiyat":16280000000,"Sembol":"snx","İndeks":253},{"ToplamÖzsermaye":7697220542,"ToplamBorç":0,"TemelFiyat":13510000000 0,"Sembol":"sol","İndeks":254},{"ToplamÖzsermaye":43400244636,"ToplamBorç":0,"TemelFiyat":5522000,"Sembol":"büyü","İndeks":255},{"ToplamÖzsermaye":145168230000,"ToplamBorç":0,"TemelFiyat":1567800000,"Sembol":"srm","İndeks":256},{"ToplamÖzsermaye y":0,"ToplamBorç":0,"TemelFiyat":3544000000,"Sembol":"stg","İndeks":257},{"ToplamÖzsermaye":1375707000000,"ToplamBorç":0,"TemelFiyat":38110000,"Sembol":"stmx","İndeks":258},{"ToplamÖzsermaye":8912432530,"ToplamBorç":0,"TemelFiyat":2582000000,"Sembol":"storj","İndeks":259},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":275900000,"Sembol":"stpt","İndeks":260},{"ToplamÖzsermaye":14047500,"ToplamBorç":0,"TemelFiyat":4050000000,"Sembol":"strax","İndeks":261},{"ToplamÖzsermaye":1423000,"ToplamBorç":0,"Temel Fiyat":2190000000,"Sembol":"stx","İndeks":262},{"ToplamÖzsermaye":326978131392,"ToplamBorç":0,"TemelFiyat":50400000,"Sembol":"güneş","İndeks":263},{"ToplamÖzsermaye":30595425600,"ToplamBorç":0,"TemelFiyat":867000000,"Sembol":"süper","İndeks":264},{"ToplamÖzsermaye":128556304136,"ToplamBorç":0,"TemelFiyat":10420000000,"Sembol":"suşi","İndeks":265},{"ToplamÖzsermaye":1059292108408,"ToplamBorç":0,"TemelFiyat":2130000000,"Sembol":"sxp","İndeks":266},{"ToplamÖzsermaye":130320000,"ToplamBorç":0,"TemelFiyat ":1017000000,"Sembol":"sys","İndeks":267},{"ToplamÖzsermaye":5172000,"ToplamBorç":0,"TemelFiyat":163000000,"Sembol":"t","İndeks":268},{"ToplamÖzsermaye":1030910000,"ToplamBorç":0,"TemelFiyat":327000000,"Sembol":"tfuel","İndeks":269},{"Toplam Özkaynak":160460684218,"ToplamBorç":0,"TemelFiyat":7590000000,"Sembol":"theta","İndeks":270},{"ToplamÖzkaynak":198770314330,"ToplamBorç":0,"TemelFiyat":2292000000,"Sembol":"tko","İndeks":271},{"ToplamÖzkaynak":256387034218,"ToplamBorç":0,"B asePrice":128600000,"Sembol":"tlm","İndeks":272},{"ToplamÖzsermaye":2508400,"ToplamBorç":0,"TemelFiyat":2762000000,"Sembol":"tomo","İndeks":273},{"ToplamÖzsermaye":9400,"ToplamBorç":0,"TemelFiyat":124800000000,"Sembol":"trb","İndeks":274},{ "ToplamÖzsermaye":33800000,"ToplamBorç":0,"TemelFiyat":2070797400,"Sembol":"kabile","İndeks":275},{"ToplamÖzsermaye":46160000,"ToplamBorç":0,"TemelFiyat":25980000,"Sembol":"troy","İndeks":276},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":288 071600,"Sembol":"tru","İndeks":277},{"ToplamÖzsermaye":2043669562480,"ToplamBorç":0,"TemelFiyat":524600000,"Sembol":"trx","İndeks":278},{"ToplamÖzsermaye":63678800000,"ToplamBorç":0,"TemelFiyat":301000000,"Sembol":"tvk","İndeks":279},{"Toplam lSermaye":0,"ToplamBorç":0,"TemelFiyat":14100000000,"Sembol":"twt","İndeks":280},{"ToplamSermaye":13980000,"ToplamBorç":0,"TemelFiyat":15400000000,"Sembol":"uma","İndeks":281},{"ToplamSermaye":19120000,"ToplamBorç":0,"TemelFiyat":39360000 000,"Sembol":"unfi","İndeks":282},{"ToplamÖzsermaye":11981756100,"ToplamBorç":0,"TemelFiyat":55220000000,"Sembol":"uni","İndeks":283},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":10000650400,"Sembol":"usdc","İndeks":284},{"ToplamÖzsermaye":12876907115652,"Toplam Borç":0,"Temel Fiyat":9997000900,"Sembol":"usdt","Endeks":285},{"Toplam Özsermaye":220063518946,"Toplam Borç":0,"Temel Fiyat":203321700,"Sembol":"ustc","Endeks":286},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":77700000 0,"Symbol":"utk","Index":287},{"TotalEquity":7430929587566,"TotalBorç":0,"BasePrice":164100000,"Symbol":"vet","Index":288},{"TotalEquity":169058297966,"TotalBorç": 0,"BasePrice":694900000,"Symbol":"vib","Index":289},{"TotalEqu ity":252046634,"ToplamBorç":0,"TemelFiyat":195000000,"Sembol":"vite","İndeks":290},{"ToplamÖzsermaye":25254109536,"ToplamBorç":0,"TemelFiyat":1671000000,"Sembol":"voxel","İndeks":291},{"ToplamÖzsermaye":5153547313742,"ToplamBorç":0,"TemelPri ce":9237200,"Sembol":"vtho","İndeks":292},{"ToplamÖzsermaye":17493828000,"ToplamBorç":0,"TemelFiyat":1658321600,"Sembol":"wan","İndeks":293},{"ToplamÖzsermaye":2852616,"ToplamBorç":0,"TemelFiyat":14130000000,"Sembol":"dalgalar","İndeks":294},{ "ToplamÖzsermaye":20000180,"ToplamBorç":0,"TemelFiyat":440000000,"Sembol":"waxp","İndeks":295},{"ToplamÖzsermaye":24776160000000,"ToplamBorç":0,"TemelFiyat":738000,"Sembol":"kazan","İndeks":296},{"ToplamÖzsermaye":2370200,"ToplamBorç":0,"TemelFiyat e":52100000000,"Symbol":"wing","Index":297},{"TotalEquity":0,"TotalBorç":0,"BasePrice":80975707300,"Symbol":"wnxm","Index":298},{"TotalEquity":75262779600,"TotalBorç" :0,"Temel Fiyat":1347000000,"Simbol":"woo","Dizin":299},{"Toplam alEquity":415631596070,"ToplamBorç":0,"TemelFiyat":1401000000,"Sembol":"wrx","İndeks":300},{"ToplamEquity":183890000,"ToplamBorç":0,"TemelFiyat":1916523600,"Sembol":"wtc","İndeks":301},{"ToplamEquity":172906064000000,"ToplamBorç":0,"B asePrice":246700,"Sembol":"xec","İndeks":302},{"ToplamÖzsermaye":129072400,"ToplamBorç":0,"TemelFiyat":291912400,"Sembol":"xem","İndeks":303},{"ToplamÖzsermaye":152986398800,"ToplamBorç":0,"TemelFiyat":751000000,"Sembol":"xlm","İndeks":304},{"ToplamÖzsermaye":109317164,"ToplamBorç":0,"TemelFiyat":1548000000000,"Sembol":"xmr","İndeks":305},{"ToplamÖzsermaye":1954309930640,"ToplamBorç":0,"TemelFiyat":3442000000,"Sembol":"xrp","İndeks":306},{"ToplamÖzsermaye":388360923948,"ToplamBorç":0,"TemelFiyat":7720000000 ,"Sembol":"xtz","İndeks":307},{"ToplamÖzsermaye":45916405132400,"ToplamBorç":0,"TemelFiyat":27200000,"Sembol":"xvg","İndeks":308},{"ToplamÖzsermaye":1725600,"ToplamBorç":0,"TemelFiyat":42900000000,"Sembol":"xvs","İndeks":309},{"ToplamÖzsermaye":1940,"ToplamBorç":0,"TemelPr buz":54420000000000,"Sembol":"yfi","İndeks":310},{"ToplamÖzsermaye":393918000,"ToplamBorç":0,"TemelFiyat":1749000000,"Sembol":"ygg","İndeks":311},{"ToplamÖzsermaye":4124782260,"ToplamBorç":0,"TemelFiyat":414000000000,"Sembol":"zec","İndeks":312},{"ToplamÖzsermaye":19000 92,"ToplamBorç":0,"BazFiyat":84900000000,"Symbol":"zen","Index":313},{"TotalEquity":2075635646560,"ToplamBorç":0,"BazFiyat":174100000,"Symbol":"zil","Index":314},{ "Toplam Özsermaye":119194400,"ToplamBorç":0,"TabanFiyat":1603000000,"Sembol":"zrx","Dizin":315}]"Dizin":313},{"ToplamÖzsermaye":2075635646560,"ToplamBorç":0,"TemelFiyat":174100000,"Sembol":"zil","Dizin":314},{"ToplamÖzsermaye":119194400,"ToplamBorç":0,"TemelFiyat":1603000000,"Sembol":"zrx","Dizin":315}]"Dizin":313},{"ToplamÖzsermaye":2075635646560,"ToplamBorç":0,"TemelFiyat":174100000,"Sembol":"zil","Dizin":314},{"ToplamÖzsermaye":119194400,"ToplamBorç":0,"TemelFiyat":1603000000,"Sembol":"zrx","Dizin":315}]
}
```

`ProofCsv` : proof.csv tablosunun yolunu belirtin

`ZkKeyVKDirectoryAndPrefix`: zkpor doğrulama anahtarının yolunu ve önekini belirtin

`CexAssetsInfo`: Yukarıdaki komut sorgusundan elde edilen varlıkları değiştirin

### Kullanıcı varlıklarını doğrulamak için gereken dosyalar

- `user_config.json` dosyasını sağlayın

Yukarıdaki kullanıcı kanıtı aşamasında oluşturulan `userproof` tablosunu kullanmamız, ardından daha önce sağlanan `example_users.csv` dosyasındaki borsa kullanıcı varlıklarının benzersiz tanımlayıcısına göre kullanıcıyı bulmamız ve `userproof` tablosundaki `account_id` alanına karşılık gelen kullanıcıyı bulmamız gerekir. `config` alanını sorgularız, `user_config.json` dosyasına kaydederiz ve kullanıcı indirmesi için sağlarız.

user_config.json dosyasının yapısı aşağıdaki gibidir

```Düz metin
```

## Son Kullanıcı İçeriği

Yani kullanıcının son olarak elde ettiği dosya yapısı kabaca şu şekildedir:

```Düz metin
- yapılandırma
    cex_config.json
    user_config.json
    kanıt.csv
zkpor864.vk.kaydet
ana
```

> `main` ikili dosyasının cihaza bağlı olarak farklı adları olabilir

- Mac İşletim Sistemi (Intel): zkproof_darwin_amd64
- Mac İşletim Sistemi (M1): zkproof_darwin_arm64
- Linux: zkproof_linux_amd64
- Windows: zkproof_windows_amd64.exe

## Kullanıcı Borsa Varlıklarını Doğrular

Doğrulamayı başlatmak için aşağıdaki komutu çalıştırın

```Düz metin
./main cex'i doğrula
```

Doğrulama başarılı olursa, çıktı olarak şu verilir:

```Düz metin
Tüm kanıtlar doğrulandı!!!
```

## Kullanıcı Kendi Varlıklarını Doğrular

```Düz metin
./main kullanıcıyı doğrula
```

Doğrulama başarılı olursa, çıktı olarak şu verilir:

```Düz metin
merkle bırakma karması: 164bc38a71b7a757455d93017242b4960cd1fea6842d8387b60c5780205858ce
onayla geç!!!
```

## Katkı

Merkezi olmayan borsalar, zk-SNARK ve MerkleTree teknolojisiyle ilgilenen tüm dostlarımızı bu projeye katılmaya davet ediyoruz. Projenin iyileştirilmesine yönelik bir tavsiye, hata bildirimi veya kod gönderme olsun, her türlü katkı takdir edilecektir.


## Lisans
Telif Hakkı 2023 © Gate Technology Inc.. Tüm hakları saklıdır.

GPLv3 lisansı altında lisanslanmıştır.
