diff --git a/README.md b/README.md
dizin 1f1e8405..bb9bcd81 100644
--- a/README.md
+++ b/README.md
@@ -27,13 +27,752 @@ Gate.io, varlık doğrulamasını uygulayan ilk kripto para borsalarından biriydi
 2. Redis: Dağıtılmış kilit
 
 ```Düz metin
- docker run -d --name zk-redis -p 6379:6379 redis
+ docker run -d -/**sözleşme WETH9 {
+ string public name = "Sarılmış Ether";
+ string public symbol = "WETH";
+ uint8 genel ondalıklar = 18;
+
+ event Approval(adres dizinli src, adres dizinli guy, uint wad);
+ olay Transfer(adres dizinli src, adres dizinli dst, uint wad);
+ olay Deposit(adres dizinli dst, uint wad);
+ olay Çekme(adres dizinli src, uint wad);
+
+ mapping (adres => uint) public balanceOf;
+ mapping (adres => mapping (adres => uint)) kamu ödeneği;
+
+ function() genel ödenebilir {
+ para yatırma();
+ }
+ fonksiyon deposit() kamuya ödenebilir {
+ balanceOf[msg.sender] += msg.value;
+ Deposit(mesaj.gönderen, mesaj.değeri);
+ }
+ fonksiyon geri çekme(uint wad) public {
+ require(balanceOf[msg.sender] >= wad);
+ balanceOf[msg.sender] -= wad;
+ msg.sender.transfer(wad);
+ Çekme(msg.sender, wad);
+ }
+
+ toplamTedarik fonksiyonu() genel görünüm (uint) döndürür {
+ bu.bakiyeyi geri döndür;
+ }
+
+ onayla işlevi(adres adamı, uint wad) genel dönüşler (bool) {
+ ödenek[msg.gönderen][adam] = wad;
+ Onay(mesaj.gönderen, adam, wad);
+ true döndür;
+ }
+
+ fonksiyon transferi(adres dst, uint wad) public returns (bool) {
+ return transferFrom(msg.sender, dst, wad);
+ }
+
+ fonksiyon transferFrom(adres src, adres dst, uint wad)
+ genel
+ döner (bool)
+ {
+ require(balanceOf[kaynak] >= wad);
+
+ eğer (src != msg.sender && ödenek[src][msg.sender] != uint(-1)) {
+ require(izin[kaynak][msg.sender] >= wad);
+ ödenek[kaynak][msg.sender] -= wad;
+ }
+
+ balanceOf[kaynak] -= wad;
+ bakiye[dst] += wad;
+
+ Transfer(kaynak, hedef, wad);
+
+ true döndür;
+ }
+}
+
+
+/*
+```
+ GNU GENEL KAMU LİSANSI
+ Sürüm 3, 29 Haziran 2007
+
+ Telif Hakkı (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
+ Herkesin birebir kopyalarını kopyalamasına ve dağıtmasına izin verilir
+ Bu lisans belgesinin, ancak değiştirilmesine izin verilmemektedir.
+
+ Önsöz
+
+ GNU Genel Kamu Lisansı, telif hakkıyla korunan, özgür bir lisanstır.
+yazılım ve diğer her türlü işler.
+
+ Çoğu yazılım ve diğer pratik çalışmalar için lisanslar tasarlanmıştır
+ eserleri paylaşma ve değiştirme özgürlüğünüzü elinizden almak. Buna karşılık,
+GNU Genel Kamu Lisansı, özgürlüğünüzü garanti altına almak için tasarlanmıştır.
+bir programın tüm sürümlerini paylaşın ve değiştirin--ücretsiz kalmasını sağlamak için
+tüm kullanıcıları için yazılım. Biz, Özgür Yazılım Vakfı,
+Yazılımlarımızın çoğu için GNU Genel Kamu Lisansı; aynı zamanda aşağıdakiler için de geçerlidir:
+yazarları tarafından bu şekilde yayınlanan diğer tüm çalışmalar. Bunu şuraya uygulayabilirsiniz:
+programlarınız da.
+
+ Özgür yazılımdan bahsettiğimizde, özgürlükten bahsediyoruz, özgürlükten değil.
+fiyat. Genel Kamu Lisanslarımız, size
+özgür yazılımların kopyalarını dağıtma özgürlüğüne sahip olmak (ve bunun için ücret talep etmek)
+isterseniz onları da alabilirsiniz), kaynak kodunu alırsınız veya isterseniz alabilirsiniz
+istediğiniz gibi, yazılımı değiştirebilir veya parçalarını yeni bir şekilde kullanabilirsiniz
+ücretsiz programlar ve bunları yapabileceğinizi biliyorsunuz.
+
+ Haklarınızı korumak için başkalarının sizi reddetmesini engellememiz gerekiyor
+bu haklar veya hakları teslim etmenizi istemek. Bu nedenle, siz
+Yazılımın kopyalarını dağıtırsanız veya
+siz değiştirin: başkalarının özgürlüğüne saygı gösterme sorumluluğu.
+
+ Örneğin, böyle bir programın kopyalarını dağıtırsanız,
+ücretsiz veya ücretli olarak, aynısını alıcılara iletmeniz gerekir
+Aldığınız özgürlükler. Onların da aldığından emin olmalısınız
+veya kaynak kodunu alabilir. Ve onlara bu şartları göstermelisiniz ki
+Haklarını bilirler.
+
+ GNU GPL kullanan geliştiriciler haklarınızı iki adımda korur:
+(1) yazılım üzerinde telif hakkı iddia etmek ve (2) size bu Lisansı sunmak
+Kopyalamanıza, dağıtmanıza ve/veya değiştirmenize yasal izin veriyoruz.
+
+ Geliştiricilerin ve yazarların korunması için GPL açıkça şunları açıklar:
+bu özgür yazılım için hiçbir garanti yoktur. Hem kullanıcılar hem de
+Yazarların iyiliği için, GPL, değiştirilmiş sürümlerin şu şekilde işaretlenmesini gerektirir:
+değiştirildi, böylece sorunları yanlışlıkla başkalarına atfedilmesin
+önceki sürümlerin yazarları.
+
+ Bazı cihazlar kullanıcıların yükleme veya çalıştırma erişimini engelleyecek şekilde tasarlanmıştır
+İçlerindeki yazılımların değiştirilmiş sürümleri, üretici olmasına rağmen
+bunu yapabilir. Bu, temelde amacı ile bağdaşmaz.
+Kullanıcıların yazılımı değiştirme özgürlüğünü korumak. Sistematik
+bu tür suistimallerin bir örüntüsü, bireylerin ürün alanında ortaya çıkmaktadır.
+use, tam da en kabul edilemez olduğu yerdir. Bu nedenle, biz
+GPL'nin bu sürümünü, bu uygulamayı yasaklamak için tasarladık
+ürünler. Bu tür sorunlar diğer alanlarda önemli ölçüde ortaya çıkarsa, biz
+Bu hükmü gelecekteki sürümlerde söz konusu alanlara genişletmeye hazırız
+Kullanıcıların özgürlüğünü korumak için gerektiği gibi GPL'nin uygulanması.
+
+ Son olarak, her program sürekli olarak yazılım patentleri tarafından tehdit edilmektedir.
+Devletler, patentlerin, teknolojinin geliştirilmesini ve kullanımını kısıtlamasına izin vermemelidir.
+Genel amaçlı bilgisayarlarda yazılım, ancak bunu yapanlarda,
+özgür bir programa uygulanan patentlerin özel tehlikesinden kaçının
+etkili bir şekilde tescilli hale getirin. Bunu önlemek için GPL, şunu garanti eder:
+patentler programı özgür olmayan hale getirmek için kullanılamaz.
+
+ Kopyalama, dağıtım ve kullanım için kesin şartlar ve koşullar
+Değişiklik takip edilir.
+
+ ŞARTLAR VE KOŞULLAR
+
+ 0. Tanımlar.
+
+ "Bu Lisans", GNU Genel Kamu Lisansı'nın 3. sürümünü ifade eder.
+
+ "Telif hakkı" aynı zamanda diğer türdeki ürünlere uygulanan telif hakkı benzeri yasalar anlamına da gelir.
+yarı iletken maskeler gibi çalışmalar.
+
+ "Program" bu lisans kapsamında lisanslanan telif hakkına konu olabilecek her türlü çalışmayı ifade eder.
+Lisans. Her lisans sahibine "siz" olarak hitap edilir. "Lisans sahipleri" ve
+"Alıcı"lar bireyler veya kuruluşlar olabilir.
+
+ Bir eseri "değiştirmek", eserin tamamını veya bir kısmını kopyalamak veya uyarlamak anlamına gelir
+telif hakkı izni gerektiren bir şekilde, bir eserin yapılması dışında
+tam kopya. Ortaya çıkan esere "değiştirilmiş versiyon" denir
+önceki çalışma veya önceki çalışmaya "dayalı" bir çalışma.
+
+ "Kapsanan eser", değiştirilmemiş Program veya temel alınan bir eser anlamına gelir
+Programda.
+
+ Bir eseri "yaymak", onunla herhangi bir şey yapmak anlamına gelir;
+izin, sizi doğrudan veya ikincil olarak sorumlu kılar
+Uygulanabilir telif hakkı yasası kapsamında ihlal, ancak bunu bir
+bilgisayar veya özel bir kopyayı değiştirme. Yayılma, kopyalamayı içerir,
+ dağıtım (değişiklik yapılarak veya yapılmadan), kullanıma sunulması
+kamu ve bazı ülkelerde diğer faaliyetler de.
+
+ Bir eseri "iletmek", diğerlerinin de yararlanmasına olanak sağlayan her türlü yayılım anlamına gelir.
+tarafların kopyalarını yapması veya alması. Bir kullanıcıyla yalnızca etkileşim
+Bir kopyanın transferi olmayan bir bilgisayar ağı, iletim yapmaz.
+
+ Etkileşimli bir kullanıcı arayüzü "Uygun Yasal Bildirimleri" görüntüler
+uygun ve belirgin bir şekilde görülebilen bir yer içerdiği ölçüde
+ (1) uygun bir telif hakkı bildirimi görüntüleyen ve (2)
+Kullanıcıya, yapılan işin (sadece
+garanti sağlandığı ölçüde), lisans sahiplerinin
+bu Lisans altında çalışın ve bu Lisansın bir kopyasını nasıl görüntüleyeceğinizi öğrenin. Eğer
+arayüz, kullanıcı komutları veya seçeneklerinin bir listesini sunar, örneğin
+menu, listede öne çıkan bir öğe bu kriteri karşılar.
+
+ 1. Kaynak Kodu.
+
+ Bir eserin "kaynak kodu", eserin tercih edilen biçimi anlamına gelir
+bunda değişiklik yapmak için. "Nesne kodu" herhangi bir kaynak dışı kod anlamına gelir
+bir eserin biçimi.
+
+ "Standart Arayüz", resmi bir arayüz olan bir arayüz anlamına gelir
+tanınmış bir standart kuruluşu tarafından tanımlanan standart veya,
+Belirli bir programlama dili için belirtilen arayüzler,
+bu dili kullanan geliştiriciler arasında yaygın olarak kullanılır.
+
+ Yürütülebilir bir çalışmanın "Sistem Kitaplıkları" her şeyi içerir, diğer
+çalışmanın bütününden daha fazla, (a) normal biçime dahil edilmiştir
+Bir Ana Bileşeni paketlemek, ancak bu Ana Bileşenin bir parçası değildir
+Bileşen ve (b) yalnızca o bileşenle çalışmanın kullanılmasını sağlamaya yarar
+ Ana Bileşen veya bir Standart Arayüz uygulamak için
+Uygulama kaynak kodu biçiminde kamuya açıktır.
+"Ana Bileşen" bu bağlamda, ana bir temel bileşen anlamına gelir
+(çekirdek, pencere sistemi vb.) belirli işletim sisteminin
+(eğer varsa) yürütülebilir çalışmanın çalıştığı veya bunu yapmak için kullanılan bir derleyici
+Çalışmayı veya onu çalıştırmak için kullanılan nesne kodu yorumlayıcısını üretmek.
+
+ Nesne kodu biçimindeki bir eser için "İlgili Kaynak" tüm
+bir yürütülebilir dosyanın oluşturulması, kurulması ve (için) gereken kaynak kodu
+work) nesne kodunu çalıştırmak ve betikler de dahil olmak üzere işi değiştirmek için
+bu aktiviteleri kontrol edin. Ancak, işin
+Sistem Kütüphaneleri veya genel amaçlı araçlar veya genel olarak ücretsiz olarak kullanılabilir
+bu aktiviteleri gerçekleştirirken değiştirilmeden kullanılan programlar ancak
+çalışmanın bir parçası olmayanlar. Örneğin, İlgili Kaynak
+kaynak dosyalarıyla ilişkili arayüz tanımlama dosyalarını içerir
+çalışma ve paylaşılan kütüphaneler için kaynak kodu ve dinamik olarak
+Çalışmanın özel olarak gerektirecek şekilde tasarlandığı bağlantılı alt programlar,
+örneğin, bu birimler arasındaki yakın veri iletişimi veya kontrol akışı yoluyla
+alt programlar ve işin diğer kısımları.
+
+ İlgili Kaynak, kullanıcıların herhangi bir şey içermesi gerekmez
+ Karşılık gelen diğer kısımlardan otomatik olarak yenilenebilir
+Kaynak.
+
+ Kaynak kod biçimindeki bir çalışma için Karşılık Gelen Kaynak şudur:
+aynı çalışma.
+
+ 2. Temel İzinler.
+
+ Bu Lisans kapsamında verilen tüm haklar, aşağıdaki süre boyunca verilir:
+ Program üzerindeki telif hakkı, belirtilen koşullar sağlandığı takdirde geri alınamaz
+koşullar karşılandı. Bu Lisans, sınırsız kullanımınızı açıkça teyit eder
+Değiştirilmemiş Programı çalıştırma izni. Bir programı çalıştırmanın çıktısı
+Kapsanan çalışma, yalnızca çıktının, belirtilen şekilde olması durumunda bu Lisans tarafından kapsanır.
+içerik, kapsanan bir eser oluşturur. Bu Lisans,
+Telif hakkı yasasının sağladığı adil kullanım hakları veya eşdeğer haklar.
+
+ Kapsamına almadığınız örtülü eserleri yapabilir, çalıştırabilir ve yayabilirsiniz.
+Lisansınız aksi halde geçerliliğini koruduğu sürece koşulsuz olarak iletin
+yürürlükte. Kapsanan eserleri yalnızca aşağıdaki amaçlar için başkalarına devredebilirsiniz:
+Onların sizin için özel olarak değişiklikler yapmasını veya size
+ bu işleri yürütmek için tesislerle birlikte, bunlara uymanız şartıyla
+bu Lisansın şartları, sizin yaptığınız tüm materyallerin iletilmesinde geçerlidir
+Telif hakkını kontrol etmezler. Böylece kapsanan eserleri yapan veya yönetenler
+çünkü bunu yalnızca kendi adınıza, sizin yönetiminiz altında yapmalısınız
+ve kontrol, herhangi bir kopyasını yapmalarını yasaklayan şartlar altında
+sizinle olan ilişkilerinin dışında telif hakkına sahip olduğunuz materyal.
+
+ Herhangi başka bir koşul altında taşıma işlemine yalnızca aşağıdakiler uyarınca izin verilir:
+aşağıda belirtilen koşullar. Alt lisanslama yasaktır; bölüm 10
+gereksiz hale getiriyor.
+
+ 3. Kullanıcıların Yasal Haklarının Anti-Durdurma Yasasından Korunması.
+
+ Hiçbir kapsam dahilindeki çalışma, etkili bir teknolojik faaliyetin parçası olarak kabul edilmeyecektir.
+ Madde kapsamındaki yükümlülükleri yerine getiren herhangi bir geçerli yasa kapsamındaki önlem
20 Aralık 1996'da kabul edilen WIPO telif hakkı anlaşmasının +11'i veya
+bu tür ihlallerin önlenmesini yasaklayan veya kısıtlayan benzer yasalar
+önlemler.
+
+ Kapsanan bir eseri ilettiğinizde, bunu yasaklama konusunda herhangi bir yasal yetkiden feragat edersiniz.
+teknolojik önlemlerin, bu tür bir engellemenin mümkün olduğu ölçüde engellenmesi
+bu Lisans kapsamındaki hakların kullanılmasıyla gerçekleştirilir
+Kapsanan çalışma ve operasyonu veya
+ Eserin, eserin haklarına aykırı olarak, zorla uygulanmasının bir yolu olarak değiştirilmesi
+Kullanıcıların, sizin veya üçüncü tarafların, ihlalleri yasaklama konusundaki yasal hakları
+teknolojik önlemler.
+
+ 4. Kelimesi kelimesine kopyaların iletilmesi.
+
+ Programın kaynak kodunun birebir kopyalarını istediğiniz zaman iletebilirsiniz.
+herhangi bir ortamda, açıkça ve açıkça belli etmek şartıyla alabilirsiniz
+her kopyaya uygun bir telif hakkı bildirimi yayınlamak;
+Bu Lisansı ve herhangi bir Lisansı belirten tüm bildirimleri olduğu gibi muhafaza edin
+ 7. maddeye göre eklenen izin verilmeyen şartlar kanuna uygulanır;
+herhangi bir garantinin bulunmadığına dair tüm bildirimleri olduğu gibi muhafaza edin; ve tüm
+Alıcılara Programla birlikte bu Lisansın bir kopyası.
+
+ Devrettiğiniz her kopya için herhangi bir fiyat talep edebilir veya hiçbir fiyat talep etmeyebilirsiniz,
+Ve ücret karşılığında destek veya garanti koruması sunabilirsiniz.
+
+ 5. Değiştirilmiş Kaynak Sürümlerinin İletimi.
+
+ Programa dayalı bir eseri veya Programın değişikliklerini aktarabilirsiniz.
+Programdan, kaynak kodu biçiminde üretin
+4. bölümün şartları, ayrıca aşağıdaki şartların tümünü de karşılamanız koşuluyla:
+
+ a) Eserde, değişiklik yaptığınızı belirten belirgin bildirimler bulunmalıdır.
+ ve ilgili tarihi vererek.
+
+ b) Eserde, bunun bir eser olduğunu belirten belirgin bildirimler bulunmalıdır.
+ bu Lisans ve bölüm altında eklenen tüm koşullar altında yayımlanmıştır
+ 7. Bu gereklilik, 4. bölümdeki gerekliliği şu şekilde değiştirir:
+ "tüm bildirimleri olduğu gibi muhafaza edin".
+
+ c) Bu lisans kapsamında, tüm eseri bir bütün olarak lisanslamalısınız.
+ Bir kopyasını ele geçiren herkese lisans verilir. Bu
+ Lisans bu nedenle geçerli olacak ve geçerli herhangi bir 7. bölümle birlikte geçerli olacaktır.
+ Eserin tamamına ve tüm parçalarına ilişkin ek şartlar,
+ nasıl paketlendiklerine bakılmaksızın. Bu Lisans hiçbir
+ eseri başka bir şekilde lisanslama izni, ancak bu
+ Ayrı ayrı aldığınız bu izni geçersiz kılın.
+
+ d) Çalışmanın etkileşimli kullanıcı arayüzleri varsa, her biri
+ Uygun Yasal Bildirimler; ancak Programın etkileşimli olması durumunda
+ Uygun Yasal Bildirimleri görüntülemeyen arayüzler,
+ iş onları buna zorlamak zorunda değil.
+
+ Kapsanan bir çalışmanın diğer ayrı ve bağımsız çalışmalarla derlenmesi
+ doğası gereği kapsanan eserin uzantısı olmayan eserler,
+ve daha büyük bir program oluşturacak şekilde birleştirilmemiş olanlar,
+bir depolama veya dağıtım ortamının bir biriminde veya üzerinde bulunan, bir
+"toplam" eğer derleme ve bunun sonucunda ortaya çıkan telif hakkı değilse
+derlemenin kullanıcılarının erişimini veya yasal haklarını sınırlamak için kullanılır
+bireysel çalışmaların izin verdiğinin ötesinde. Kapsanan bir çalışmanın dahil edilmesi
+toplu olarak bu Lisansın diğerlerine uygulanmasına neden olmaz
+toplamın parçaları.
+
+ 6. Kaynak Dışı Biçimlerin İletimi.
+
+ Kapsanan bir çalışmayı, aşağıdaki şartlar altında nesne kodu biçiminde iletebilirsiniz:
+4 ve 5. bölümlerin, ayrıca aşağıdakileri de iletmeniz şartıyla
+Bu Lisansın şartları uyarınca makine tarafından okunabilen İlgili Kaynak,
+bu yollardan biriyle:
+
+ a) Nesne kodunu fiziksel bir üründe iletin veya bu üründe somutlaştırın
+ (fiziksel dağıtım ortamı dahil), aşağıdakilerle birlikte
+ Dayanıklı bir fiziksel ortama sabitlenmiş İlgili Kaynak
+ genellikle yazılım alışverişi için kullanılır.
+
+ b) Nesne kodunu fiziksel bir üründe iletin veya bu üründe somutlaştırın
+ (fiziksel dağıtım ortamı dahil), bir
+ en az üç yıl geçerli ve geçerliliği en az üç yıl olan yazılı teklif
+ o ürün için yedek parça veya müşteri desteği sunduğunuz sürece
+ model, nesne koduna sahip olan herkese (1) bir
+ Tüm yazılımlar için İlgili Kaynağın kopyası
+ bu Lisans kapsamındaki ürün, dayanıklı fiziksel bir ambalaj üzerinde
+ Yazılım alışverişi için genellikle kullanılan ortam, bir bedel karşılığında
+ bunu fiziksel olarak gerçekleştirmenin makul maliyetinden daha fazlası
+ kaynağın iletilmesi veya (2) kopyalamaya erişim
+ Ücretsiz olarak bir ağ sunucusundan İlgili Kaynak.
+
+ c) Nesne kodunun bireysel kopyalarını, nesne kodunun bir kopyasıyla birlikte iletin
+ İlgili Kaynağın sağlanması için yazılı teklif. Bu
+ alternatif yalnızca ara sıra ve ticari olmayan amaçlarla kullanılabilir ve
+ yalnızca böyle bir teklifle nesne kodunu aldıysanız,
+ 6b alt maddesiyle birlikte.
+
+ d) Belirlenen bir erişim noktasından erişim sağlayarak nesne kodunu iletin
+ yer (ücretsiz veya ücretli) ve eşdeğer erişim imkanı sunar
+ Aynı yerden aynı şekilde Kaynak'a karşılık gelen
+ ek ücret. Alıcıların kopyalamasını talep etmenize gerek yok
+ Nesne koduyla birlikte karşılık gelen Kaynak. Eğer yer
+ nesne kodunu kopyala bir ağ sunucusudur, İlgili Kaynak
+ farklı bir sunucuda olabilir (sizin veya üçüncü bir tarafın işlettiği)
+ eşdeğer kopyalama olanaklarını destekler, ancak bunu korumanız koşuluyla
+ nesne kodunun yanında, nesnenin nerede bulunacağını belirten net talimatlar
+ İlgili Kaynak. Hangi sunucunun barındırdığına bakılmaksızın
+ İlgili Kaynak, bunun sağlanmasını garantilemekle yükümlüsünüz
+ Bu gereksinimleri karşılamak için ihtiyaç duyulduğu sürece kullanılabilir.
+
+ e) Nesne kodunu, aşağıdaki koşullar sağlandığı takdirde, eşler arası iletim kullanarak iletin:
+ diğer akranlara nesne kodunun ve Karşılık gelenin nerede olduğunu bildirirsiniz
+ Çalışmanın kaynağı kamuoyuna hiçbir şekilde sunulmamaktadır.
+ 6d alt maddesi uyarınca ücret.
+
+ Kaynak kodu hariç tutulan nesne kodunun ayrılabilir bir bölümü
+Sistem Kütüphanesi olarak İlgili Kaynaktan, gerekmemektedir
+nesne kod işinin iletilmesinde yer alır.
+
+ Bir "Kullanıcı Ürünü" (1) bir "tüketici ürünü"dür, bu da herhangi bir
+normalde kişisel, ailevi,
+veya ev amaçlı veya (2) birleştirmek üzere tasarlanmış veya satılan herhangi bir şey
+bir konuta. Bir ürünün tüketici ürünü olup olmadığını belirlemede,
+şüpheli durumlar teminat lehine çözülecektir. Belirli bir
+Belirli bir kullanıcı tarafından alınan ürün, "normalde kullanılan" bir ürünü ifade eder
+ o ürün sınıfının, statüsünden bağımsız olarak, tipik veya yaygın kullanımı
+belirli kullanıcının veya belirli kullanıcının kullandığı yolun
+ürünü gerçekten kullanır, kullanması beklenir veya beklenir. Bir ürün
+Ürünün önemli bir ticari değeri olup olmadığına bakılmaksızın bir tüketici ürünüdür
+ticari, endüstriyel veya tüketici dışı kullanımlar, bu tür kullanımlar aşağıdaki durumları temsil etmediği sürece:
+Ürünün tek önemli kullanım şekli.
+
+ Bir Kullanıcı Ürünü için "Kurulum Bilgileri", herhangi bir yöntem anlamına gelir,
+Kurulum için gereken prosedürler, yetkilendirme anahtarları veya diğer bilgiler
+ve kapsanan bir çalışmanın değiştirilmiş sürümlerini o Kullanıcı Ürününde yürütün
+Karşılık Gelen Kaynağının değiştirilmiş bir versiyonu. Bilgiler,
+Değiştirilen nesnenin sürekli işlevselliğini sağlamak için yeterlidir
+kod hiçbir durumda yalnızca şu nedenle engellenmez veya müdahale edilmez:
+Değişiklik yapıldı.
+
+ Bu bölüm kapsamında bir nesne kodu çalışmasını, içinde veya ile birlikte veya
+özellikle bir Kullanıcı Ürünü'nde kullanım için ve aktarım şu şekilde gerçekleşir:
+sahip olma ve kullanma hakkının devredildiği bir işlemin parçası
+Kullanıcı Ürünü, alıcıya kalıcı olarak veya bir süreliğine devredilir.
+ sabit vadeli (işlemin nasıl nitelendirildiğine bakılmaksızın),
+Bu bölüm uyarınca iletilen İlgili Kaynak, aşağıdakilerle birlikte sunulmalıdır:
+Kurulum Bilgileri tarafından. Ancak bu gereklilik geçerli değildir
+ ne siz ne de herhangi bir üçüncü taraf kurulum yetkisine sahip değilse
+Kullanıcı Ürününde değiştirilmiş nesne kodu (örneğin, çalışma
+ROM'a yüklenmiş).
+
+ Kurulum Bilgilerinin sağlanması gerekliliği şunları içermez:
+destek hizmeti, garanti veya güncelleme sağlamaya devam etme gereksinimi
+alıcı tarafından değiştirilmiş veya kurulmuş bir eser için veya
+Değiştirildiği veya yüklendiği Kullanıcı Ürünü. Bir
+Ağ, değişikliğin kendisi önemli ölçüde ve
+ ağın işleyişini olumsuz etkiler veya kuralları ihlal eder ve
+Ağ genelinde iletişim için protokoller.
+
+ İlgili Kaynak iletildi ve Kurulum Bilgileri sağlandı,
+bu bölüme uygun olarak kamuya açık bir biçimde olmalıdır
+belgelenmiş (ve kamuya açık bir uygulama ile)
+kaynak kodu biçimi) ve özel bir parola veya anahtar gerektirmemelidir
+açma, okuma veya kopyalama.
+
+ 7. Ek Şartlar.
+
+ "Ek izinler" bu Sözleşmenin şartlarını tamamlayan şartlardır.
+Lisans, şartlarından bir veya birkaçından istisna yapılarak verilir.
+ Programın tamamına uygulanabilecek ek izinler
+bu Lisansa dahil oldukları ölçüde, bu Lisansa dahil edilmiş gibi kabul edilirler
+uygulanabilir yasa kapsamında geçerli oldukları. Ek izinler varsa
+ Programın yalnızca bir kısmına uygulanır, söz konusu kısım ayrı olarak kullanılabilir
+bu izinler altında, ancak Programın tamamı aşağıdakiler tarafından yönetilmeye devam ediyor:
+Bu Lisans ek izinlere bakılmaksızın geçerlidir.
+
+ Kapsanan bir eserin bir kopyasını ilettiğinizde, isteğinize bağlı olarak
+bu kopyadan veya herhangi bir bölümünden ek izinleri kaldırın
+it. (Ek izinler kendi izinlerini gerektirecek şekilde yazılabilir.
+bazı durumlarda çalışmayı değiştirdiğinizde kaldırma.)
+Kapsanan bir çalışmaya sizin tarafınızdan eklenen materyal üzerindeki ek izinler,
+Uygun telif hakkı iznine sahip olduğunuz veya verebileceğiniz.
+
+ Bu Lisansın diğer hükümlerine bakılmaksızın, sizin için geçerli olan materyal için
+Kapsanan bir çalışmaya, (telif hakkı sahipleri tarafından yetkilendirildiği takdirde) ekleyebilirsiniz.
+bu materyal) bu Lisansın şartlarını aşağıdaki şartlarla tamamlar:
+
+ a) Garantiyi reddetmek veya sorumluluğu farklı şekilde sınırlamak
+ bu Lisansın 15 ve 16. bölümlerinin şartları; veya
+
+ b) Belirtilen makul yasal bildirimlerin saklanmasını gerektiren veya
+ söz konusu materyaldeki veya Uygun Yasal Bilgilerdeki yazar atıfları
+ Bunu içeren eserler tarafından görüntülenen bildirimler; veya
+
+ c) Söz konusu materyalin kökeninin yanlış tanıtılmasının yasaklanması veya
+ bu tür materyalin değiştirilmiş sürümlerinin işaretlenmesini gerektiren
+ orijinal versiyondan farklı olarak makul yollar; veya
+
+ d) Lisans verenlerin veya lisans verenlerin adlarının tanıtım amaçlı kullanımının sınırlandırılması
+ materyalin yazarları; veya
+
+ e) Bazı markaların kullanımı için ticari marka yasası kapsamında hak verilmesinin reddedilmesi
+ ticari adlar, ticari markalar veya hizmet markaları; veya
+
+ f) Lisans verenlerin ve söz konusu eserin yazarlarının tazmin edilmesini talep etmek
+ materyali ileten herkes tarafından (veya değiştirilmiş versiyonları)
+ it) alıcıya karşı sözleşmesel sorumluluk varsayımlarıyla,
+ bu sözleşmesel varsayımların doğrudan yüklediği herhangi bir sorumluluk
+ bu lisans verenler ve yazarlar.
+
+ Diğer tüm izin verilmeyen ek şartlar "daha fazla" olarak kabul edilir
+10. madde anlamında "kısıtlamalar". Programı sizin için uygun şekilde kullanıyorsanız
+alındı ​​veya herhangi bir parçası, bunun alındığını belirten bir bildirim içeriyor
+bu Lisans ile yönetilen ve daha ileri bir terim olan
+kısıtlama, bu terimi kaldırabilirsiniz. Bir lisans belgesi şunları içeriyorsa
+daha fazla kısıtlama ancak bu kapsamda yeniden lisanslama veya taşımaya izin veriyor
+Lisans, kapsanan bir çalışmaya, şartlara tabi olan materyali ekleyebilirsiniz
+bu lisans belgesinin, daha fazla kısıtlamanın olmaması kaydıyla
+böyle bir yeniden lisanslama veya aktarmayı atlatamaz.
+
+ Bu bölüm uyarınca kapsanan bir çalışmaya terimler eklerseniz,
+İlgili kaynak dosyalarına, bir ifadenin yerleştirilmesi gerekir
+bu dosyalara uygulanacak ek şartlar veya bunu belirten bir bildirim
+uygulanabilir şartların nerede bulunacağı.
+
+ İzin verici veya izin vermeyen ek şartlar, sözleşmede belirtilebilir.
+ayrıca yazılı bir lisans biçimi veya istisnalar olarak belirtilmiş;
+Yukarıdaki şartlar her iki durumda da geçerlidir.
+
+ 8. Fesih.
+
+ Açıkça belirtildiği durumlar haricinde, kapsanan bir eseri yayamaz veya değiştiremezsiniz.
+bu Lisans kapsamında sağlanmıştır. Aksi takdirde yayma veya yayma girişimi
+Değiştirilmesi geçersizdir ve otomatik olarak haklarınızı sona erdirecektir
+bu Lisans (üçüncü tarafça verilen patent lisansları dahil)
+bölüm 11 paragrafı).
+
+ Ancak, bu Lisansın tüm ihlallerini durdurursanız, o zaman
+Belirli bir telif hakkı sahibinden alınan lisans yeniden yürürlüğe girer (a)
+geçici olarak, telif hakkı sahibi açıkça ve izin verene kadar
+sonunda lisansınızı sonlandırır ve (b) telif hakkı kalıcı olarak sona ererse
+sahibi, ihlali makul bir şekilde size bildirmede başarısız olur
+Kontraksiyonun sona ermesinden itibaren 60 güne kadar.
+
+ Ayrıca, belirli bir telif hakkı sahibinden aldığınız lisans,
+Telif hakkı sahibi sizi bilgilendirirse kalıcı olarak iade edilir
+ makul bir şekilde ihlal, bu ilk defa oluyor
+bu Lisansın (herhangi bir çalışma için) ihlaline ilişkin bildirimi o kişiden aldım
+telif hakkı sahibiyseniz ve ihlali 30 gün içinde düzeltirseniz
+tebligatın tarafınıza ulaşması.
+
+ Bu bölüm kapsamındaki haklarınızın sona ermesi, aşağıdakilere son vermez:
+Sizden kopya veya hak alan tarafların lisansları
+bu Lisans. Haklarınız sonlandırıldıysa ve kalıcı değilse
+yeniden etkinleştirildi, aynı lisans için yeni lisans almaya hak kazanmıyorsunuz
+10. madde kapsamındaki materyal.
+
+ 9. Kopyaların Bulundurulması İçin Kabul Gerekmez.
+
+ Bu Lisansı almak veya almak için bu Lisansı kabul etmeniz gerekmez.
+ Programın bir kopyasını çalıştırın. Kapsanan bir çalışmanın yardımcı yayılımı
+sadece eşler arası iletişimin kullanılması sonucu ortaya çıkan
+bir kopyasını almak da aynı şekilde kabul gerektirmez. Ancak,
+bu Lisans dışında hiçbir şey size çoğaltma veya yayma izni vermez
+herhangi bir kapsanan çalışmayı değiştirin. Bunu yaparsanız bu eylemler telif hakkını ihlal eder
+Bu Lisansı kabul etmeyin. Bu nedenle, bir Lisansı değiştirerek veya yayarak
+Kapsanan çalışmayı yapmak, bu Lisansı kabul ettiğinizi gösterir.
+
+ 10. Alt Alıcıların Otomatik Lisanslanması.
+
+ Her seferinde örtülü bir eseri ilettiğinizde, alıcı otomatik olarak
+ Orijinal lisans verenlerden çalıştırmak, değiştirmek ve kullanmak için lisans alır
+bu Lisansa tabi olarak bu eseri yaymak. Siz sorumlu değilsiniz
+Üçüncü tarafların bu Lisansa uymasını sağlamak için.
+
+ Bir "varlık işlemi", bir varlığın kontrolünün devredildiği bir işlemdir.
+bir kuruluşun veya esasen tüm varlıklarının veya bir kuruluşun alt bölümlerinin
+organizasyon veya birleşen organizasyonlar. Kapsanan bir organizasyonun yayılması
+bir varlık işleminden elde edilen iş sonuçları, bu işlemin taraflarının her biri
+işlem eserin bir kopyasını alan kişi aynı zamanda ne varsa onu da alır
+partinin ilgili selefinin sahip olduğu veya sahip olabileceği çalışmalara ilişkin lisanslar
+önceki paragraf uyarınca verilen, artı mülkiyet hakkı
+İlgili öncülden çalışmanın Karşılık Gelen Kaynağı, eğer varsa
+selefinde var veya makul çabalarla elde edilebilir.
+
+ Kullanım hakkının kullanılmasına ilişkin herhangi bir ek kısıtlama getiremezsiniz.
+Bu Lisans kapsamında verilen veya onaylanan haklar. Örneğin, şunları yapabilirsiniz:
+ lisans ücreti, telif hakkı veya başka bir ücret talep etmemek
+Bu Lisans kapsamında verilen haklar ve dava açamazsınız
+(bir davada çapraz talep veya karşı talep dahil) iddia ederek
+herhangi bir patent talebi, yapılması, kullanılması, satılması, teklif edilmesi yoluyla ihlal edilir.
+Programın veya herhangi bir bölümünün satışı veya ithalatı.
+
+ ## 11. Patentler.
+
+ "Katkıda bulunan", bu kapsamdaki kullanımları yetkilendiren bir telif hakkı sahibidir.
+ Programın veya Programın dayandığı bir eserin lisansı.
+Bu şekilde lisanslanan esere, katkıda bulunanın "katkıda bulunan sürümü" denir.
+
+ Bir katılımcının "temel patent iddiaları"nın hepsi patent iddialarıdır
+Katkıda bulunanın sahip olduğu veya kontrol ettiği, halihazırda satın alınmış olsun veya olmasın
+bundan sonra edinilen, bir şekilde ihlal edilecek olan, izin verilen
+bu Lisans ile, katkıda bulunan sürümünün yapılması, kullanılması veya satılması,
+ancak yalnızca ihlal edilebilecek iddiaları dahil etmeyin
+katkıda bulunan sürümün daha fazla değiştirilmesinin sonucu.
+Bu tanımın amaçları doğrultusunda, "kontrol", verme hakkını da içerir
+patent alt lisansları, gereklilikleriyle uyumlu bir şekilde
+bu Lisans.
+
+ Her katılımcı size dünya çapında, telifsiz, münhasır olmayan bir hak verir
+Katkıda bulunanın temel patent talepleri kapsamındaki patent lisansı,
+üretmek, kullanmak, satmak, satışa sunmak, ithal etmek ve başka şekillerde çalıştırmak, değiştirmek ve
+Katkıda bulunan sürümünün içeriğini yaymak.
+
+ Aşağıdaki üç paragrafta, "patent lisansı" herhangi bir açık ifadedir
+bir patenti uygulamamak için yapılan anlaşma veya taahhüt, her ne şekilde adlandırılırsa adlandırılsın
+(örneğin bir patenti uygulamaya yönelik açık bir izin veya bir sözleşmeyi uygulamama
+patent ihlali nedeniyle dava açmak). Böyle bir patent lisansını birine "vermek" için
+parti, bir sözleşmeyi uygulamamak için böyle bir anlaşma veya taahhütte bulunmak anlamına gelir
+partiye karşı patent.
+
+ Bir patent lisansına bilerek güvenerek, kapsanan bir eseri devrederseniz,
+ve eserin İlgili Kaynağı hiç kimse tarafından erişilebilir değildir
+bu Lisansın şartları uyarınca, ücretsiz olarak kopyalamak için
+kamuya açık ağ sunucusu veya diğer kolayca erişilebilir araçlar,
+o zaman (1) İlgili Kaynağın bu şekilde olmasını sağlamalısınız
+mevcut veya (2) kendinizi bu faydadan mahrum bırakmayı ayarlayın
+bu belirli çalışma için patent lisansı veya (3) bir şekilde düzenleme
+bu Lisansın gerekliliklerine uygun olarak, patenti uzatmak için
+Alt akış alıcılarına lisans. "Bilerek güvenmek", sahip olduğunuz anlamına gelir
+Patent lisansı olmasa bile, gerçek bilginin sizin tarafınızdan iletilmesi
+ ülkedeki kapsanan iş veya alıcınızın kapsanan işi kullanımı
+bir ülkede, o ülkedeki bir veya daha fazla tanımlanabilir patenti ihlal edecek
+geçerli olduğuna inanmak için sebebiniz olan ülke.
+
+ Tek bir işlem uyarınca veya bununla bağlantılı olarak veya
+düzenleme, bir şeyin iletilmesini sağlayarak iletir veya yayarsınız
+Kapsanan çalışma ve bazı taraflara patent lisansı verilmesi
+Kapsanan eserin alınması, kullanılması, yayılması ve değiştirilmesine yetki verilmesi
+veya kapsanan eserin belirli bir kopyasını iletirseniz, o zaman patent lisansı
+ hibeniz otomatik olarak kapsanan tüm alıcılara uzatılır
+iş ve ona dayalı işler.
+
+ Bir patent lisansı, aşağıdakileri içermiyorsa "ayrımcı"dır:
+kapsamının kapsamı, kullanımını yasaklıyorsa veya
+bir veya daha fazla hakkın kullanılmaması şartıyla
+bu Lisans kapsamında özel olarak verilmiştir. Kapsanan bir
+Üçüncü bir tarafla bir anlaşmaya tarafsanız çalışın
+yazılım dağıtımı işinde, ödeme yaptığınızda
+ Üçüncü tarafa, iletme faaliyetinizin kapsamına göre
+ Üçüncü tarafın, herhangi birine verdiği eser ve
+Sizden kapsanan işi alacak taraflar, ayrımcı bir
+patent lisansı (a) kapsanan eserin kopyalarıyla bağlantılı olarak
+sizin tarafınızdan iletilen (veya bu kopyalardan yapılan kopyalar) veya (b) öncelikli olarak
+belirli ürünler veya derlemelerle bağlantılı olarak ve bunlarla ilgili olarak
+ kapsanan işi içerir, eğer siz bu düzenlemeye girmediyseniz,
+veya patent lisansının 28 Mart 2007 tarihinden önce verilmiş olması.
+
+ Bu Lisans'taki hiçbir şey, hariç tutma veya sınırlama şeklinde yorumlanmayacaktır.
+ ihlale karşı herhangi bir zımni lisans veya diğer savunmalar
+aksi takdirde geçerli patent yasası uyarınca sizin kullanımınıza sunulabilir.
+
+ ## 12. Başkalarının özgürlüğünden vazgeçilmemesi.
+
+ Size şartlar empoze edilirse (ister mahkeme kararıyla, ister anlaşmayla veya
+aksi takdirde) bu Lisansın şartlarına aykırı olan,
+bu Lisansın şartlarını mazur görün. Eğer bir
+Bu kapsamdaki yükümlülüklerinizi aynı anda yerine getirebilmeniz için kapsanan iş
+Lisans ve diğer ilgili yükümlülükler, bunun sonucunda şunları yapabilirsiniz:
+hiçbir şekilde iletmeyin. Örneğin, sizi bağlayan şartları kabul ederseniz
+ devrettiğiniz kişilerden daha fazla devretmek için telif hakkı toplamak
+Program, hem bu şartları hem de bu şartı yerine getirebilmenin tek yoludur
+Lisans, Programın iletiminden tamamen kaçınmak anlamına gelir.
+
+ 13. GNU Affero Genel Kamu Lisansı ile kullanın.
+
+ Bu Lisansın diğer hükümlerine bakılmaksızın,
+herhangi bir kapsanan eseri lisanslı bir eserle bağlama veya birleştirme izni
+GNU Affero Genel Kamu Lisansı'nın 3. sürümü altında tek bir
+birleştirilmiş çalışma ve ortaya çıkan çalışmayı iletmek. Bu çalışmanın şartları
+Lisans, kapsanan işin olduğu kısım için geçerli olmaya devam edecektir,
+ancak GNU Affero Genel Kamu Lisansı'nın özel gereksinimleri,
+13. madde, bir ağ üzerinden etkileşimle ilgili olarak uygulanacaktır
+kombinasyon böyledir.
+
+ 14. Bu Lisansın Gözden Geçirilmiş Sürümleri.
+
+ Özgür Yazılım Vakfı, aşağıdakilerin gözden geçirilmiş ve/veya yeni sürümlerini yayınlayabilir:
+GNU Genel Kamu Lisansı zaman zaman. Bu tür yeni sürümler
+ruhsal olarak mevcut versiyona benzer olabilir, ancak ayrıntılarda farklılık gösterebilir
+yeni sorunlara veya endişelere değinmek.
+
+ Her versiyona ayırt edici bir versiyon numarası verilir.
+Program, GNU Genel'in belirli bir numaralı sürümünü belirtir
+Kamu Lisansı "veya daha sonraki bir sürüm" buna uygulanırsa,
+bu numaralandırılmış şartlar ve koşulların herhangi birini takip etme seçeneği
+Özgür Yazılım tarafından yayımlanan herhangi bir sonraki sürüm veya sürüm
+Vakıf. Program bir sürüm numarası belirtmiyorsa
+GNU Genel Kamu Lisansı, şimdiye kadar yayınlanmış herhangi bir sürümü seçebilirsiniz
+Özgür Yazılım Vakfı tarafından.
+
+ Program, bir vekilin gelecekteki hangi işlemlerin yapılacağına karar verebileceğini belirtiyorsa
+GNU Genel Kamu Lisansı'nın sürümleri kullanılabilir, bu proxy'nin
+bir sürümün kabulüne ilişkin kamu beyanı sizi kalıcı olarak yetkilendirir
+ Program için o versiyonu seçmek için.
+
+ Daha sonraki lisans sürümleri size ek veya farklı özellikler sağlayabilir
+izinler. Ancak, herhangi bir ek yükümlülük getirilmemiştir
+bir yazar veya telif hakkı sahibi, bir kişiyi takip etmeyi seçmeniz sonucunda
+sonraki versiyon.
+
+ 15. Garanti Reddi.
+
+ PROGRAM İÇİN, İZİN VERİLEN ÖLÇÜDE HİÇBİR GARANTİ YOKTUR
+UYGULANACAK HUKUK. YAZILI OLARAK AKSİ BELİRTİLMEDİKÇE TELİF HAKKI
+SAHİPLER VE/VEYA DİĞER TARAFLAR PROGRAMI GARANTİ OLMADAN "OLDUĞU GİBİ" SAĞLAR
+HERHANGİ BİR TÜRDE, AÇIKÇA BELİRTİLMİŞ YA DA ZIMNİ, BUNLARLA SINIRLI OLMAMAK ÜZERE,
+ SATILABİLİRLİK VE BELİRLİ BİR AMAÇ İÇİN UYGUNLUK İLE İLGİLİ ZIMNİ GARANTİLER
+AMAÇ. PROGRAMIN KALİTESİ VE PERFORMANSI İLE İLGİLİ TÜM RİSK
+SİZİNLEDİR. PROGRAMIN KUSURLU OLDUĞU ORTAYA ÇIKARSA, MALİYETİ SİZ ÜSTLENİRSİNİZ
+ GEREKLİ TÜM BAKIM, ONARIM VEYA DÜZELTME.
+
+ 16. Sorumluluğun Sınırlandırılması.
+
+ YÜRÜRLÜKTEKİ KANUNLARCA GEREKTİRİLMEDİĞİ VEYA YAZILI OLARAK ANLAŞILMADIĞI TAKDİRDE HİÇBİR DURUMDA
+HERHANGİ BİR TELİF HAKKI SAHİBİ VEYA BUNU DEĞİŞTİREN VE/VEYA İLETEN HERHANGİ BİR TARAF
+YUKARIDA İZİN VERİLEN PROGRAM, HERHANGİ BİR ZARAR DAHİL OLMAK ÜZERE, SİZE KARŞI SORUMLU TUTULACAKTIR
+GENEL, ÖZEL, ARIZİ VEYA SONUÇ OLARAK OLUŞAN ZARARLAR
+ PROGRAMIN KULLANILMASI VEYA KULLANILAMAMASI (BUNLARLA SINIRLI OLMAMAK ÜZERE)
+ VERİLERİN VEYA VERİLERİN YANLIŞ HALE GETİRİLMESİ VEYA SİZİN VEYA ÜÇÜNCÜ KİŞİLERİN ZARAR GÖRMESİ
+TARAFLAR VEYA PROGRAMIN DİĞER PROGRAMLARLA BİRLİKTE ÇALIŞMAMASI),
+BÖYLE BİR SAHİBE VEYA DİĞER TARAF, OLASILIKTAN HABERDAR EDİLMİŞ OLSA BİLE;
+BU TÜR ZARARLAR.
+
+ 17. 15 ve 16. Bölümlerin Yorumlanması.
+
+ Garanti reddi ve sorumluluk sınırlaması sağlanmışsa
+yukarıdaki hükümlere, kendi şartlarına göre yerel hukuki etki verilemez,
+İnceleme mahkemeleri, en yakın yerel yasayı uygulayacaktır
+ Bağlantılı tüm hukuki sorumluluklardan mutlak feragat
+Program, bir garanti veya sorumluluk üstlenimi eşlik etmediği sürece
+Ücret karşılığında Programın bir kopyası.
+
+ ŞARTLAR VE KOŞULLARIN SONU
+
+ Bu Şartları Yeni Programlarınıza Nasıl Uygularsınız
+
+ Yeni bir program geliştirirseniz ve bunun en iyilerden biri olmasını istiyorsanız
+halkın kullanımına sunulabilir, bunu başarmanın en iyi yolu onu
+Herkesin bu şartlar altında yeniden dağıtabileceği ve değiştirebileceği özgür yazılım.
+
+ Bunu yapmak için, programa aşağıdaki bildirimleri ekleyin. En güvenlisi
+bunları en etkili şekilde her kaynak dosyasının başına eklemek için
+garantinin hariç tutulduğunu belirtin; ve her dosya en azından şunları içermelidir:
+"telif hakkı" satırı ve tam bildirimin bulunduğu yere bir işaretçi.
+
+ <programın adını ve ne işe yaradığına dair kısa bir fikir veren bir satır.>
+ Telif Hakkı (C) <yıl> <yazarın adı>
+
+ Bu program özgür bir yazılımdır: onu yeniden dağıtabilir ve/veya değiştirebilirsiniz
+ GNU Genel Kamu Lisansı'nın yayınladığı şartlar uyarınca
+ Özgür Yazılım Vakfı, Lisansın 3. sürümü veya
+ (tercihinize göre) herhangi bir sonraki versiyon.
+
+ Bu program yararlı olacağı umuduyla dağıtılmaktadır,
+ ancak HERHANGİ BİR GARANTİ OLMADAN; hatta ima edilen garanti bile olmaksızın
+ SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK. Bkz.
+ Daha fazla ayrıntı için GNU Genel Kamu Lisansı'na bakın.
+
+ GNU Genel Kamu Lisansı'nın bir kopyasını almış olmalısınız
+ bu programla birlikte. Değilse, <http://www.gnu.org/licenses/> adresine bakın.
+
+Ayrıca elektronik ve kağıt posta yoluyla sizinle nasıl iletişime geçebileceğimize dair bilgileri de ekleyin.
+
+ Program terminal etkileşimi yapıyorsa, kısa bir çıktı verin
+Etkileşimli modda başlatıldığında buna benzer bir uyarı:
+
+ <program> Telif Hakkı (C) <yıl> <yazarın adı>
+ Bu program kesinlikle HİÇBİR GARANTİ ile gelmez; detaylar için `show w' yazın.
+ Bu özgür bir yazılımdır ve onu yeniden dağıtabilirsiniz
+ belirli koşullar altında; ayrıntılar için `show c' yazın.
+
+ Varsayımsal `w'yi göster' ve `c'yi göster' komutları uygun olanı göstermelidir
+Genel Kamu Lisansının parçaları. Elbette programınızın komutları
+farklı olabilir; bir GUI arayüzü için "hakkında kutusu" kullanırsınız.
+
+ Ayrıca işvereninizi (programcı olarak çalışıyorsanız) veya okulunuzu da almalısınız,
+eğer varsa, program için bir "telif hakkı feragatnamesi" imzalamak.
+Bu konuda daha fazla bilgi ve GNU GPL'yi nasıl uygulayacağınız ve takip edeceğiniz hakkında bilgi için bkz.
+<http://www.gnu.org/licenses/>.
+
+ GNU Genel Kamu Lisansı programınızı dahil etmenize izin vermez
+özel programlara. Programınız bir alt rutin kütüphanesiyse,
+Tescilli uygulamaların birbirine bağlanmasına izin verilmesinin daha yararlı olduğunu düşünebilir
+kütüphane. Eğer yapmak istediğiniz buysa, GNU Lesser General'ı kullanın
+Bu Lisans yerine Kamu Lisansı. Ama önce lütfen okuyun
+<http://www.gnu.org/philosophy/why-not-lgpl.html>.
+
+*/
 ```
 
 3. Kvrocks: Kullanıcı hesap ağacını depola
 
 ```Düz metin
- docker run -d --name zk-kvrocks -p 6666:6666 apache/kvrocks
+ docker run -d -[{"constant":true,"girdi":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true," girişler":[],"name":"toplamTedarik","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"sabit":false,"girişler":[{"name":"src","type":"adres"},{"name":"dst","type" :"adres"},{"name":"wad","type":"uint256"}],"name":"transferFrom","çıktılar":[{"name":"","type":"bool"}],"ödenebilir":false,"durumDeğişebilirliği":"ödenemez","type":"işlev tion"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"çekilme","outputs":[],"payable":false,"stateMutability":"ödenemez","type":"function"},{"constant":true,"inputs":[],"name":"decials","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"görünüm","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"b alanceOf","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"},{"sabit":true,"girdiler":[],"ad":"sembol","çıktılar":[{"name":"","type":"dize"}],"ödenebilir":false,"durum Değişebilirliği":"görünüm","type":"işlev"},{"sabit":false,"girdiler":[{"name":"dst","type":"adres"},{"name":"wad","type":"uint256"}],"ad":"aktarım","çıktılar":[{"name":"","type":"bool"}],"ödenebilir":false,"durumDeğişebilirliği":"ödenemez","type":"işlev"}, {"sabit":false,"girdiler":[],"name":"depozito","çıktılar":[],"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"işlev" },{"sabit":true,"girdiler":[{"name":"","type":"adres"},{"name":"","type":"adres"}]," n ame":"ödenek","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":" işlevi"},{"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"ad":"kaynak","type":"adres"},{"indexed":true,"ad" :"adam","type":"adres"}, {"indexed":false,"name":"wad","type":"uint256"}],"name":"Onay","type" :"olay"},{"anonymous":false,"girişler":[{"indexed":true,"name":"src","type":"adres"},{"indexed":true," name":"dst","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer"," tür":"olay"},{"anonim":fa lse,"inputs":[{"indexed":true,"name":"dst","type":"adres"},{"indexed":false,"name":"wad","type": "uint256"}],"name":"Para Yatırma","type":"olay"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src" ,"type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"olay" }]"adres"}],"name":"izinat","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":" görünüm","type":"işlev"},{"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","type":"adres"},{"indexed":true,"name":"adam","type":"adres"},{"indexed":false,"name":"wad","type":"uint256 "}],"name":"Onay","type":"olay"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","typ e":"adres"},{"indexed":true,"name":"dst","type":"adres"},{"indexed":false,"name":"wad","type" :"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst" ,"type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{" indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"event"}]"adres"}],"name": "izinat","çıktılar":[{"name":"","type":"uint256"}],"ödenebilir":false,"durumDeğişebilirliği":"görünüm","type":"işlev"}, {"ödenebilir":true,"durumDeğişebilirliği":"ödenebilir","type":"geri dönüş"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","type":"adres"},{"indexed":true,"name" :"adam","type":"adres"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Onay","type" :"olay"},{"anonim":false,"girdiler":[{"indexed":true,"name":"kaynak","typ e":"adres"},{"indexed":true,"name":"dst","type":"adres"},{"indexed":false,"name":"wad","type" :"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst" ,"type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event "},{"anonim":yanlış,"girişler":[{"indeksli":doğru,"ad":"kaynak","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekme","type":"event"}]"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Para Yatırma","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]"wad","type":"uint256"}],"name":"Çekilme","type":"event"}]
 ```
 
   > Kvrocks kurulumundan sonra bağlantı başarısız olursa:   
@@ -49,13 +788,9 @@ Programı derlemek için, kullanacağınız Go dil ortamını kullanmanız gerekir.
 Dışa aktarılan borsa kullanıcı varlığı .csv veri yapısı aşağıdaki gibidir:
 
 ```Düz metin
-- rn #dizi
-- id # borsadaki kullanıcının benzersiz tanımlayıcısı
-- e_xtoken #kullanıcının xtoken sermayesi, örneğin e_BTC
-- d_xtoken #kullanıcının xtoken borcu, örneğin d_BTC
-- x_token #kullanıcının net varlık değeri, x_token = e_xtoken - d_xtoken
-- xtoken_usdt_price #xtoken fiyatı
-- total_net_balance_usdt #tüm kullanıcıların tokenlerinin toplam USDT değeri
+"KanıtCsv": "./config/proof.csv",
+ "ZkKeyVKDirectoryAndPrefix": "./zkpor864",
+ "CexAssetsInfo": [{"ToplamÖzsermaye":10049232946,"ToplamBorç":0,"TemelFiyat":3960000000,"Sembol":"1inç","İndeks":0},{"ToplamÖzsermaye":421836,"ToplamBorç":0,"TemelFiyat":564000000000,"Sembol":"aave","İndeks":1},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelPr buz":79800000,"Sembol":"ach","İndeks":2},{"ToplamÖzsermaye":3040000,"ToplamBorç":0,"TemelFiyat":25460000000,"Sembol":"acm","İndeks":3},{"ToplamÖzsermaye":17700050162640,"ToplamBorç":0,"TemelFiyat":2784000000,"Sembol":"ada","İndeks":4}, {"ToplamSermaye":485400000,"ToplamBorç":0,"TemelFiyat":1182000000,"Sembol":"adx","İndeks":5},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":907000000,"Sembol":"aergo","İndeks":6},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":27200000 00,"Sembol":"agld","İndeks":7},{"ToplamÖzsermaye":1969000000,"ToplamBorç":0,"TemelFiyat":30500000,"Sembol":"akro","İndeks":8},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":141000000000,"Sembol":"alcx","İndeks":9},{"ToplamÖzsermaye":1548 3340912,"ToplamBorç":0,"TemelFiyat":1890000000,"Sembol":"algo","İndeks":10},{"ToplamÖzsermaye":3187400,"ToplamBorç":0,"TemelFiyat":11350000000,"Sembol":"alice","İndeks":11},{"ToplamÖzsermaye":1760000,"ToplamBorç":0,"TemelFiyat":2496000 000,"Sembol":"alpaca","İndeks":12},{"ToplamÖzsermaye":84596857600,"ToplamBorç":0,"TemelFiyat":785000000,"Sembol":"alfa","İndeks":13},{"ToplamÖzsermaye":3672090936,"ToplamBorç":0,"TemelFiyat":20849000000,"Sembol":"alpine","İndeks":14}, {"ToplamÖzsermaye":198200000,"ToplamBorç":0,"TemelFiyat":132600000,"Sembol":"amb","İndeks":15},{"ToplamÖzsermaye":53800000,"ToplamBorç":0,"TemelFiyat":32200000,"Sembol":"amp","İndeks":16},{"ToplamÖzsermaye":3291606210,"ToplamBorç":0,"TemelP pirinç":340300000,"Sembol":"anc","İndeks":17},{"ToplamÖzsermaye":192954000,"ToplamBorç":0,"TemelFiyat":166000000,"Sembol":"ankr","İndeks":18},{"ToplamÖzsermaye":2160000,"ToplamBorç":0,"TemelFiyat":20940000000,"Sembol":"karınca","İndeks":19},{"ToplamÖzsermaye":5995002000,"ToplamBorç":0,"TemelFiyat":40370000000,"Sembol":"ape","İndeks":20},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":11110000000,"Sembol":"api3","İndeks":21},{"ToplamÖzsermaye":53728000,"ToplamBorç":0,"TemelFiyat" :38560000000,"Sembol":"apt","İndeks":22},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":68500000000,"Sembol":"ar","İndeks":23},{"ToplamÖzsermaye":55400000,"ToplamBorç":0,"TemelFiyat":667648400,"Sembol":"ardr","İndeks":24},{"ToplamÖzsermaye" :8320000,"ToplamBorç":0,"TemelFiyat":266200000,"Sembol":"arpa","İndeks":25},{"ToplamÖzsermaye":18820000,"ToplamBorç":0,"TemelFiyat":401000000,"Sembol":"astr","İndeks":26},{"ToplamÖzsermaye":13205405410,"ToplamBorç":0,"TemelFiyat":934000000 ,"Sembol":"ata","İndeks":27},{"ToplamÖzsermaye":7016230960,"ToplamBorç":0,"TemelFiyat":102450000000,"Sembol":"atom","İndeks":28},{"ToplamÖzsermaye":2619441828,"ToplamBorç":0,"TemelFiyat":40900000000,"Sembol":"müzayede","İndeks":29},{"ToplamE quity":9640198,"ToplamBorç":0,"TemelFiyat":1432000000,"Sembol":"ses","İndeks":30},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":2306000000000,"Sembol":"otomatik","İndeks":31},{"ToplamÖzsermaye":886400,"ToplamBorç":0,"TemelFiyat":539000000 0,"Sembol":"ava","İndeks":32},{"ToplamÖzsermaye":2883562350,"ToplamBorç":0,"TemelFiyat":117800000000,"Sembol":"avax","İndeks":33},{"ToplamÖzsermaye":1864300912,"ToplamBorç":0,"TemelFiyat":68200000000,"Sembol":"axs","İndeks":34},{"ToplamÖzsermaye ity":843870,"ToplamBorç":0,"TemelFiyat":23700000000,"Sembol":"porsuk","İndeks":35},{"ToplamÖzsermaye":114869291528,"ToplamBorç":0,"TemelFiyat":1379000000,"Sembol":"pişir","İndeks":36},{"ToplamÖzsermaye":95400,"ToplamBorç":0,"TemelFiyat":541 10000000,"Sembol":"bal","İndeks":37},{"ToplamÖzsermaye":123113880,"ToplamBorç":0,"TemelFiyat":14610000000,"Sembol":"bant","İndeks":38},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":37100000000,"Sembol":"çubuk","İndeks":39},{"ToplamÖzsermaye":73090049578,"ToplamBorç":0,"TemelFiyat":1774000000,"Sembol":"bat","İndeks":40},{"ToplamÖzsermaye":28891300,"ToplamBorç":0,"TemelFiyat":1017000000000,"Sembol":"bch","İndeks":41},{"ToplamÖzsermaye":19889623294,"ToplamBorç":0,"TemelFiyat":41300 00000,"Sembol":"bel","İndeks":42},{"ToplamÖzsermaye":374840602180,"ToplamBorç":0,"TemelFiyat":699700000,"Sembol":"beta","İndeks":43},{"ToplamÖzsermaye":270294580,"ToplamBorç":0,"TemelFiyat":12290900000000,"Sembol":"beth","İndeks":44},{"Toplam lSermaye":35692901600,"ToplamBorç":0,"TemelFiyat":2730000000,"Sembol":"bico","İndeks":45},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":639000,"Sembol":"bidr","İndeks":46},{"ToplamSermaye":240200000,"ToplamBorç":0,"TemelFiyat":538000000, "Sembol":"blz","İndeks":47},{"ToplamÖzsermaye":83614634622,"ToplamBorç":0,"TemelFiyat":2599000000000,"Sembol":"bnb","İndeks":48},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3490000000,"Sembol":"bnt","İndeks":49},{"ToplamÖzsermaye":1560,"Toplam alDebt":0,"Temel Fiyat":592000000000,"Sembol":"bnx","İndeks":50},{"Toplam Özsermaye":2076000,"Toplam Borç":0,"Temel Fiyat":32630000000,"Sembol":"tahvil","İndeks":51},{"Toplam Özsermaye":44699589660,"Toplam Borç":0,"Temel Fiyat":1768000000,"Sembol":" bsw","İndeks":52},{"ToplamÖzsermaye":291716078,"ToplamBorç":0,"TemelFiyat":169453900000000,"Sembol":"btc","İndeks":53},{"ToplamÖzsermaye":15500321300000000,"ToplamBorç":0,"TemelFiyat":6300,"Sembol":"bttc","İndeks":54},{"ToplamÖzsermaye":7077154 6756,"ToplamBorç":0,"TabanFiyat":5240000000,"Symbol":"burger","Endeks":55},{"TotalEquity":12058907297354,"ToplamBorç":1476223055432,"BazFiyat":10000000000,"Sembol" :"busd","Index":56},{"TotalEquity":34716440000,"TotalBorç":0,"Bas ePrice":1647000000,"Sembol":"c98","İndeks":57},{"ToplamÖzsermaye":1541723702,"ToplamBorç":0,"TemelFiyat":33140000000,"Sembol":"kek","İndeks":58},{"ToplamÖzsermaye":2112000,"ToplamBorç":0,"TemelFiyat":5200000000,"Sembol":"celo","İndeks":59},{"ToplamÖzsermaye":317091540000,"ToplamBorç":0,"TemelFiyat":101000000,"Sembol":"celr","İndeks":60},{"ToplamÖzsermaye":137111365560,"ToplamBorç":0,"TemelFiyat":228000000,"Sembol":"cfx","İndeks":61},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat e":1820000000,"Sembol":"satranç","İndeks":62},{"ToplamÖzsermaye":258540000,"ToplamBorç":0,"TemelFiyat":1140000000,"Sembol":"chr","İndeks":63},{"ToplamÖzsermaye":289172288882,"ToplamBorç":0,"TemelFiyat":1099000000,"Sembol":"chz","İndeks":64} ,{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":25100000,"Sembol":"ckb","İndeks":65},{"ToplamÖzsermaye":1851135024806,"ToplamBorç":0,"TemelFiyat":535500000,"Sembol":"clv","İndeks":66},{"ToplamÖzsermaye":155010000,"ToplamBorç":0,"TemelFiyat": 5202000000,"Sembol":"cocos","İndeks":67},{"ToplamÖzsermaye":52093390,"ToplamBorç":0,"TemelFiyat":335800000000,"Sembol":"comp","İndeks":68},{"ToplamÖzsermaye":13991592000,"ToplamBorç":0,"TemelFiyat":44500000,"Sembol":"cos","İndeks":69},{"Kime talEquity":51240788068,"ToplamBorç":0,"TemelFiyat":557000000,"Sembol":"coti","İndeks":70},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":107900000000,"Sembol":"cream","İndeks":71},{"ToplamSermaye":15940224,"ToplamBorç":0,"TemelFiyat":5 470000000,"Sembol":"crv","İndeks":72},{"ToplamÖzsermaye":2336000,"ToplamBorç":0,"TemelFiyat":7450000000,"Sembol":"ctk","İndeks":73},{"ToplamÖzsermaye":88860000,"ToplamBorç":0,"TemelFiyat":1059000000,"Sembol":"ctsi","İndeks":74},{"ToplamÖzsermaye":74},{"ToplamÖzsermaye":740000000,"ToplamÖzsermaye":74 ... ity":440400000,"ToplamBorç":0,"TemelFiyat":1763000000,"Sembol":"ctxc","İndeks":75},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":3375000000,"Sembol":"cvp","İndeks":76},{"ToplamÖzsermaye":176202,"ToplamBorç":0,"TemelFiyat":30810000000,"S ymbol":"cvx","İndeks":77},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":9999000100,"Symbol":"dai","İndeks":78},{"ToplamÖzsermaye":90702266836,"ToplamBorç":0,"TemelFiyat":1293500000,"Symbol":"dar","İndeks":79},{"ToplamÖzsermaye":29386961406,"ToplamBorç":0,"TemelFiyat":458300000000,"Sembol":"tire","İndeks":80},{"ToplamÖzsermaye":1628888000,"ToplamBorç":0,"TemelFiyat":235500000,"Sembol":"veri","İndeks":81},{"ToplamÖzsermaye":0,"ToplamD ebt":0,"Temel Fiyat":186229836100,"Sembol":"dcr","İndeks":82},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat":15920000000,"Sembol":"dego","İndeks":83},{"Toplam Özsermaye":26105549312822,"Toplam Borç ":0,"TemelFiyat":6830000,"Sembol":"dent","İndeks":84},{"ToplamÖzsermaye":670658000,"ToplamBorç":0,"TemelFiyat":24000000000,"Sembol":"dexe","İndeks":85},{"ToplamÖzsermaye":517372774000,"ToplamBorç ":0,"Temel Fiyat":82200000,"Sembol":"dgb","İndeks":86},{"Toplam Özsermaye":1120000,"Toplam Borç":0,"Temel Fiyat":2970000000,"Sembol":"dia","İndeks":87},{"Toplam Özsermaye":0,"Toplam Borç":0,"Temel Fiyat": 151800000,"Sembol":"rıhtım","İndeks":88},{"ToplamÖzsermaye":19453393384,"ToplamBorç":0,"TemelFiyat":987000000,"Sembol":"dodo","İndeks":89},{"ToplamÖzsermaye":25526548451614,"ToplamBorç":0,"TemelFiyat ce":723900000,"Sembol":"doge","İndeks":90},{"ToplamÖzsermaye":466049240950,"ToplamBorç":0,"TemelFiyat":46820000000,"Sembol":"nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat e":3138000000,"Sembol":"drep","İndeks":92},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":45675816000,"ToplamBorç":0,"TemelFiyat":121200 00000,"Sembol":"dydx","İndeks":94},{"ToplamÖzsermaye":241920370,"ToplamBorç":0,"TemelFiyat":343400000000,"Sembol":"egld","İndeks":95},{"ToplamÖzsermaye":3640000,"ToplamBorç":0,"TemelFiyat":1691000{"TotalEquity":26105549312822,"TotalBorç":0,"BasePrice":6830000,"Symbol":"dent","Index":84},{"TotalEquity":670658000,"TotalBorç":0,"BasePrice" :24000000000,"Symbol":"dexe","Index":85},{"TotalEquity":517372774000,"TotalBorç":0,"BasePrice":82200000,"Symbol":"dgb","Index":86 },{"TotalEq uity":1120000,"ToplamBorç":0,"TemelFiyat":2970000000,"Sembol":"dia","İndeks":87},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":151800000 ,"Sembol":"rıhtım","İndeks":88},{"ToplamSermaye":19453393384,"ToplamBorç":0,"TemelFiyat":987000000,"Sembol":"dodo","İndeks":89}, {"ToplamSermaye":25526548451614," talDebt":0,"Temel Fiyat":723900000,"Sembol":"doge","İndeks":90},{"Toplam Özsermaye":466049240950,"Toplam Borç":0,"Temel Fiyat":46820000000,"Sembol":" nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat":3138000000,"Sembol":"drep","İndeks":92},{"ToplamÖzsermaye":0 ,"ToplamBorç":0,"TemelÖz ce":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":45675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","İndeks" :94},{"Toplam Özsermaye":241920370,"Toplam Borç":0,"Temel Fiyat":343400000000,"Sembol":"egld","İndeks":95},{"Toplam Özsermaye":3640000,"Toplam Borç":0 ,"Temel Fiyat":1691000{"TotalEquity":26105549312822,"TotalBorç":0,"BasePrice":6830000,"Symbol":"dent","Index":84},{"TotalEquity":670658000,"TotalBorç":0,"BasePrice" :24000000000,"Symbol":"dexe","Index":85},{"TotalEquity":517372774000,"TotalBorç":0,"BasePrice":82200000,"Symbol":"dgb","Index":86 },{"TotalEq uity":1120000,"ToplamBorç":0,"TemelFiyat":2970000000,"Sembol":"dia","İndeks":87},{"ToplamSermaye":0,"ToplamBorç":0,"TemelFiyat":151800000 ,"Sembol":"rıhtım","İndeks":88},{"ToplamSermaye":19453393384,"ToplamBorç":0,"TemelFiyat":987000000,"Sembol":"dodo","İndeks":89}, {"ToplamSermaye":25526548451614," talDebt":0,"Temel Fiyat":723900000,"Sembol":"doge","İndeks":90},{"Toplam Özsermaye":466049240950,"Toplam Borç":0,"Temel Fiyat":46820000000,"Sembol":" nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat":3138000000,"Sembol":"drep","İndeks":92},{"ToplamÖzsermaye":0 ,"ToplamBorç":0,"TemelÖz ce":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":45675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","İndeks" :94},{"Toplam Özsermaye":241920370,"Toplam Borç":0,"Temel Fiyat":343400000000,"Sembol":"egld","İndeks":95},{"Toplam Özsermaye":3640000,"Toplam Borç":0 ,"Temel Fiyat":169100046820000000,"Sembol":"nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat":3138000000,"Sembol":"drep","İndeks":92},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":4 5675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","İndeks":94},{"ToplamÖzsermaye":241920370,"ToplamBorç":0,"TemelFiyat":343400000000,"Sembol":"egld","İndeks":95},{"ToplamÖzsermaye":3640000,"ToplamBorç":0,"TemelFiyat":169100046820000000,"Sembol":"nokta","İndeks":91},{"ToplamÖzsermaye":69200000,"ToplamBorç":0,"TemelFiyat":3138000000,"Sembol":"drep","İndeks":92},{"ToplamÖzsermaye":0,"ToplamBorç":0,"TemelFiyat":870000000,"Sembol":"alacakaranlık","İndeks":93},{"ToplamÖzsermaye":4 5675816000,"ToplamBorç":0,"TemelFiyat":12120000000,"Sembol":"dydx","İndeks":94},{"ToplamÖzsermaye":241920370,"ToplamBorç":0,"TemelFiyat":343400000000,"Sembol":"egld","İndeks":95},{"ToplamÖzsermaye":3640000,"ToplamBorç":0,"TemelFiyat":1691000
 ```
 
 Ayrıntılar için `./example_data/example_users.csv` dosyasına bakın.
@@ -331,27 +1066,33 @@ ana
 Doğrulamayı başlatmak için aşağıdaki komutu çalıştırın
 
 ```Düz metin
-./main cex'i doğrula
+./main cex'i doğrula, [zkmerkle_cex_20240520.tar.gz](https://github.com/user-attachments/files/17051675/zkmerkle_cex_20240520.tar.gz)
+[zkmerkle_cex_20240520.tar.gz](https://github.com/user-attachments/files/17051675/zkmerkle_cex_20240520.tar.gz)
+
 ```
 
 Doğrulama başarılı olursa, çıktı olarak şu verilir:
 
 ```Düz metin
-Tüm kanıtlar doğrulandı!!!
+Hepsi , [Windows2022-Readme.md](https://github.com/user-attachments/files/17051708/Windows2022-Readme.md)
+[Windows2022-Readme.md](https://github.com/user-attachments/files/17051708/Windows2022-Readme.md)
+kanıtlar doğrula kaydet!!!
 ```
 
 ## Kullanıcı Kendi Varlıklarını Doğrular
 
 ```Düz metin
+[Gate.io PoR Uygulama güncellemesi.pdf](https://github.com/user-attachments/files/17051719/Gate.io.PoR.Implementation.upd.pdf)
+[Gate.io PoR Uygulama güncellemesi.pdf](https://github.com/user-attachments/files/17051719/Gate.io.PoR.Implementation.upd.pdf)
 ./main kullanıcıyı doğrula
 ```
 
 Doğrulama başarılı olursa, çıktı olarak şu verilir:
 
-```Düz metin
-merkle bırak karma: 164bc38a71b7a757455d93017242b4960cd1fea6842d8387b60c5780205858ce
-geçişinizi doğrulayın!!!
-```
+
+![cüzdan_20240511-231342_Gateio](https://github.com/user-attachments/assets/9aa7552c-2503-483b-a9c4-73d64f8ad741)
+![cüzdan_20240511-231342_Gateio](https://github.com/user-attachments/assets/9aa7552c-2503-483b-a9c4-73d64f8ad741)
+
 
 ## Katkı
 
@@ -361,4 +1102,4 @@ Merkezi olmayan borsalara ilgi duyan tüm dostlarımızı bekliyoruz, zk-SNARK,
 ## Lisans
 Telif Hakkı 2023 © Gate Technology Inc.. Tüm hakları saklıdır.
 
-GPLv3 lisansı altında lisanslanmıştır.
\ Dosyanın sonunda yeni satır yok
+GPLv3 lisansı altında lisanslanmıştır.
