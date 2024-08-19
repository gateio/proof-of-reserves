dizin
Değişme
Web3

%100 Rezerv Kanıtı
Gate.io, %100 sermaye rezervi sağlamayı taahhüt eden ilk ana akım platformdur


Gate.io PoR
Son denetim tarihi :

2024-05-20 00:00:00 (UTC+0)

Fazla rezerv değeri :

0,86 milyar dolar 

Algoritma:

Merkle Ağacı + zk-SNARK'lar

Toplam rezerv oranı :

115,34%

Merkle Kök Karması :

093d2036bc4a6bab3f956db74856ee98e43bd03b137f7129b5854750335e4940


Müşteri Net Bakiyesi

5.628.406.410 ABD doları 

Gate Cüzdan Bakiyesi

6.492.214.095 ABD doları 

Fazla rezerv değeri

863.807.685 ABD doları 


BTC
Rezerv Oranı
0123456789
0123456789
0123456789
.
0123456789
0123456789
%
Müşteri Net Bakiyesi

15.803,70

Gate Cüzdan Bakiyesi

18.420,00

Gate Cüzdan Bakiyesi USD

1.220.628.930 ABD doları 


USDT
Rezerv Oranı
0123456789
0
0123456789
.
0123456789
0123456789
%
Müşteri Net Bakiyesi

895.074.126,09

Gate Cüzdan Bakiyesi

943.992.283,00

Gate Cüzdan Bakiyesi USD

943.992.283 ABD doları 


ETH
Rezerv Oranı
0123456789
0123456789
0123456789
.
0123456789
0123456789
%
Müşteri Net Bakiyesi

208.147,69

Gate Cüzdan Bakiyesi

236.105,00

Gate Cüzdan Bakiyesi USD

725.118.592 ABD doları 


DOGE
Rezerv Oranı
0123456789
0
0123456789
.
0123456789
0123456789
%
Müşteri Net Bakiyesi

2.008.494.984,15

Gate Cüzdan Bakiyesi

2.194.636.960,00

Gate Cüzdan Bakiyesi USD

327.222.565 ABD doları 


ETH2
Rezerv Oranı
0123456789
0123456789
0123456789
.
0123456789
0
%
Müşteri Net Bakiyesi

68.452,52

Gate Cüzdan Bakiyesi

78.176,00

Gate Cüzdan Bakiyesi USD

240.336.476 ABD doları 


ŞİB
Rezerv Oranı
0123456789
0
0123456789
.
0123456789
0123456789
%
Müşteri Net Bakiyesi

8.401.492.279.474,73

Gate Cüzdan Bakiyesi

8.927.307.634.575,00

Gate Cüzdan Bakiyesi USD

213.005.560 ABD doları 

Hesap bakiyemi içerip içermediğini doğrulayın. Şimdi doğrulayın >

%100 Rezerv Kanıtı Nedir?
Merkezi bir ticaret platformu, kullanıcı varlıklarını bir veritabanında kaydetmek için bir muhasebe defteri yönetir. Bu nedenle, platformlar tüm kullanıcıların varlıklarının iyi durumda tam gözetimine sahip olduklarını kanıtlama zorluğuyla karşı karşıyadır.

Gate.io, bu sorunu çözmek için Merkle ağacını uyguladı ve her kullanıcının hesap varlıklarının karma değerini Merkle ağacının yaprak düğümlerinde depoladı. Her kullanıcı, Merkle ağacının yaprak düğümlerinde depolanan toplam kullanıcı varlık miktarını denetleyebilir ve fonlarının nitelikli bir üçüncü taraf denetim kuruluşu aracılığıyla dahil edilip edilmediğini doğrulayabilir.

Merkle ağacında saklanan varlıkların %100 veya daha büyük olduğu doğrulanırsa, bu, kullanıcıların varlıklarının platformda tam olarak tutulduğu, yani platformun kullanıcıların varlıkları için %100 Rezerv Kanıtı sağladığı anlamına gelir.

%100 Rezerv Kanıtı neden bu kadar önemlidir?

Platform %100 Rezerv Kanıtı sağlar
Platformun mali açıdan sağlam olması
Kullanıcıların güvenini artırın
Kullanıcıların varlıklarının güvenliğini garanti altına alın
Kalabalık bir çekimde %100 nakit çekme
%100 rezerv kanıtı taahhüdü olmadan
Kullanıcıların varlıklarının kötüye kullanılma riski altında olması
Varlıkların nakde çevrilmesinde gecikme veya imkânsızlık
Kullanıcıların para çekme talebinde bulunmak için kalabalık oluşturması durumunda platform zor durumda kalabilir
Platformun iflas etme veya varlık kaybına uğrama olasılığı daha yüksektir

Rezervlerin %100 seviyesinde tutulmasını nasıl sağlarız?
Borsa tarafından blok zincirinde yönetilen toplam token sayısı, anlık görüntüde yakalanan tüm kullanıcı hesaplarının toplam bakiyesini karşılar veya aşarsa, platform bu tokenlar için %100 marj korur


Cüzdan üzerindeki mülkiyet

Hesap bakiyesinin anlık görüntüsü

zk-SNARK kanıtının oluşturulması

Bir Merkle ağacı oluşturun
Generate a Merkle tree - Gate.io
Generate a Merkle tree
Generate the underlying data block by linking the hashed UID and balance of each user, and then generate a Merkle tree based upon all users' data.

The Merkle root will change if any account ID or balance in the leaf node changes.

Every user can verify whether his assets are included in the leaf node.

Karma kullanıcı kimliği ve kullanıcı bakiyesi ile Merkle ağacı nasıl oluşturulur?
Karma kullanıcı kimliği (UID) ve kullanıcı bakiyeleri ilk önce Gate'in veritabanından dışarı aktarılır.
Karma hale getirilmiş her UID ve kullanıcı bakiyesi çifti sırasıyla karma hale getirilecek ve ardından birleştirilerek temel veri bloğu oluşturulacaktır.
Her veri bloğu için, Merkle ağacının yaprak düğümlerini oluşturmak için aynı karma işlevi uygulanacaktır. Elde edilen karma veriler daha sonra yaprak düğümlerinin ana düğümlerini oluşturmak için çiftler halinde birlikte karma haline getirilir.
Bu işlem, merkle kökü adı verilen tek bir hash elde edilene kadar devam eder.
Lütfen örnek için aşağıdaki şemaya bakın. Merkle ağacı başarıyla oluşturulduktan sonra, yaprak düğümleri düz metin dosyasına aktarılacak ve bu dosya denetçi tarafından merkle kök karması ile birlikte yayınlanacaktır.


Merkle ağacı - Gate.io
Merkle Ağacı Nedir?
Kriptografi ve bilgisayar biliminde, karma ağacı veya Merkle ağacı, her yaprak düğümünün bir veri bloğunun kriptografik karmasıyla etiketlendiği bir ağaçtır. Yaprak olmayan her düğüm, alt düğümlerinin etiketlerinin karmasıyla etiketlenir. Karma ağaçları, büyük veri yapılarının içeriklerinin etkili ve güvenli bir şekilde doğrulanmasını sağlar.


Rezerv Kanıtı sağlamak için Merkle Ağacını nasıl kullanırız?
Her kullanıcının hesap varlığının karma değerini Merkle Ağacında bir yaprak düğümü olarak kaydederiz. Daha sonra, tüm kullanıcıların varlıklarını tam olarak tuttuğumuzu doğrulamak için zk-SNARK teknolojisini kullanırız. Bu süreç boyunca hiçbir varlık verisi ifşa edilmez. Doğrulama adımları şu şekildedir:
1. zk-SNARK, kullanıcıların varlıklarının toplam bakiyesinin Merkle Ağacı'ndaki yaprak düğümleri olarak saklandığını denetlemeye yardımcı olur (yani, kullanıcı hesap bakiyesi). Her yaprak düğümü için aşağıdaki noktaları onaylıyoruz:
a. Platform tarafından yönetilen varlıkların toplam tutarı, tüm kullanıcıların toplam varlık bakiyesini içerir.

b. Her kullanıcının net bakiyesi sıfıra eşit veya büyüktür.

c. Herhangi bir kullanıcının varlıklarında meydana gelen değişiklik Merkle kök karma değerinin değişmesine neden olacaktır.

2. Kullanıcı doğrulaması: Kullanıcılar, zk-SNARK kullanarak Merkle kök karma değerini doğrulayarak kanıtın gerçekliğini doğrulayabilir. Teknoloji, gizlilik veya ticari sır sızıntısı risklerinden kaçınırken %100 rezerv denetimini verimli ve güvenli bir şekilde tamamlamamızı sağlar ve bu da şeffaf operasyonlara olan bağlılığımızı yerine getirmemize ve müşterilerin güvenini artırmamıza yardımcı olur.
zk-SNARK’lar nelerdir?
zk-SNARK, Zero-Knowledge Succinct Non-Interactive Argument of Knowledge (Sıfır Bilgili Özlü Etkileşimsiz Bilgi Argümanı) anlamına gelir ve kriptografide kök salmış çığır açıcı bir araçtır. Gelişmiş matematiksel algoritmalar kullanarak, belirli varlık ayrıntılarını ifşa etmeden rezerv miktarını yetkin bir şekilde doğrulayabilir. zk-SNARK yalnızca hızlı varlık doğrulamasını kolaylaştırmakla kalmaz, aynı zamanda gizlilik ihlali risklerini de ortadan kaldırır. Bu avantajlar, etkileşimsiz yapısı ve yüksek ölçeklenebilirliği ile birleştiğinde, zincir içi işlem doğrulaması, veri gizliliği korumaları ve kimlik doğrulaması gibi alanlarda kapsamlı uygulamalar bulur


Doğrulama süreci.

1. Programı kurun ve verileri indirin:

1)Doğrulama programını indirin:

Öncelikle, verilen bağlantı üzerinden doğrulama programını indirin veya doğrulama programını indirmek için GitHub'a erişin. Ardından adını main olarak değiştirin .

Yerel İndirme

Mac işletim sistemi


Yerel İndirme

Linux

Yerel İndirme

Pencereler

2)Gerekli verileri indirin:

Denetim Sayfasına erişin ve doğrulamanız gereken partiyi bulun. Verileri indirmek için [Merkle Ağacını İndir] ve [Kullanıcı Yapılandırmasını İndir] öğelerine tıklayın.

Sıkıştırılmış zkmerkle_cex_xxx.tar.gz dosyasını açın , ana programı bu klasörün içine yerleştirin ve user_config.json dosyasını config klasörünün içine koyun .

Program klasörü artık


zkmerkle_cex_xxx


Yapılandırma


cex_config.json


user_config.json


kanıt.csv


zkpor864.vk.kaydet


ana

2. Varlıkların doğrulanması:

Cmd veya terminalden, indirilen klasöre (örneğin cd ~/Downloads/zkmerkle_cex_xxx) gitmek için cd komutunu kullanın .

(Programı çalıştırmadan önce, izinleri vermek veya güvenlik öğelerini ayarlamak için chmod 777 main komutunu çalıştırmanız gerekebilir .)


değişim varlıklarını doğrula

Borsadaki varlıkları doğrulayın.
Doğrulamayı başlatmak için aşağıdaki komutu yürütün.

./main cex'i doğrula

Doğrulama başarılı olduğunda mesaj görüntülenecektir.

Tüm kanıtlar doğrulandı!!!

Ayrıntılı teknik dokümantasyon ve doğrulama prensipleri için lütfen GitHub açık kaynaklı projesini kontrol edin

Gate.io PoR Uygulaması

HACKEN

Denetim firması
Denetim zamanı

3 Ocak 2024

Denetçi

Luciano Ciattaglia, Sofiane Akermoun, Nino Lipartiia, Bartosz Barwikowski

Depolar

https://github.com/gateio/proof-of-reserves

Denetim Raporu

Gate.io PoR Uygulaması

Hakkında
Hakkımızda
Kariyer
Kullanıcı Sözleşmesi
Gizlilik Politikası
Ücretler
Medya Kiti
%100 Rezerv Kanıtı
Lisans
Kapı Laboratuvarları
Kapı Girişimleri
Kapı Hibeleri
Güvenlik
Duyuru
Toplum
GT Kullanıcı Ayrıcalıkları
Kapı Zinciri
Takvim
Hukukun uygulanması
Ürünler
Kripto satın al
Kripto Sat
Kripto Para Fiyatları
Ticaret
Sürekli Vadeli İşlemler
Kaldıraçlı Tokenlar
Başlatmak
NFT
Çapraz zincir
Kapıda Ödeme
Kapı Hayatı
Hediye Kartı
Kapı OTC
Kapı Yardım Kuruluşu
Kapı Kartı
Büyük Veri
Kapı dükkanı
Hizmetler
Kullanıcı Geri Bildirimi
Yardım Merkezi
Bir İstek Gönder
Listeleme
Akıllı Sözleşme Güvenliği
Geliştiriciler（API）
Doğrulama Araması
P2P Tüccar Uygulaması
P2P Blue V Uygulaması
Kurumsal
Kurumsal ve VIP Hizmetleri
Broker Programı
Etkileyici Programı
Yönlendirme Programı
Ortaklık Programı
Anlar
Anlar
Kapı direği
Canlı Yayın
Sohbet
Haberler
Gelecek Etkinlikler
Blog
Öğrenmek
Kapı Öğren
Kripto Kursları
Kripto Sözlüğü
Bitcoin Yarılanması
ETH 2.0 Yükseltmesi
Kripto Fiyatları
Kripto Nasıl Satın Alınır
Kripto Fiyat Tahmini
Kriptodan Fiat'a Dönüştürücü
Finans
Basit Kazanç
HODL & Kazan
Yapılandırılmış Ürünler
Çift Yatırım
Kapı Zenginliği
Kripto Kredisi
ETH2.0 Hisse Senedi
Otomatik Yatırım
Likidite Madenciliği
Bulut Madenciliği
Slot Müzayedeleri
İngilizce
Telif Hakkı © 2013-2024.
Merhaba, size nasıl yardımcı olabilirim?
