"""Aristoteles ve Farabi senaryoları ile Sokrates taslağına eklenen içerik (kaynak metin).

Bu dosya senaryoların KAYNAĞIDIR; `python scripts/build_dialogues.py` ile data/dialogues/*.json üretilir.
Tüm içerik taslaktır ve tarihsel/felsefi doğruluk açısından bir uzman tarafından gözden geçirilmelidir.
Konu yapısı: her konuda 6 soru; her soru için (soru, evet-karşı sorusu, hayır-karşı sorusu, kararsızım-basit örnek).
"""

STOP = "Henüz karar veremedim"
REFLECTION_OPTIONS = [
    {"id": "changed", "label": "Düşüncem değişti"},
    {"id": "same", "label": "Düşüncem değişmedi"},
    {"id": "undecided", "label": STOP},
]
REASON_LABELS = [
    ("experience", "Kendi gözlem ve deneyimime dayanıyor"),
    ("example", "Aklımda somut bir örnek var"),
    ("heard", "Böyle duydum ya da öğrendim"),
    ("reasoning", "Bir akıl yürütmeye dayanıyor"),
    ("principle", "İnandığım bir ilkeye dayanıyor"),
    ("unsure", "Emin değilim, daha çok düşünmeliyim"),
]

# --------------------------------------------------------------------------- SOKRATES (ek içerik)
SOKRATES_REASON_REPLIES = {
    "experience": "Kendi deneyiminden yola çıkman değerli. Peki, başka birinin yaşadıkları farklı olsaydı o da aynı sonuca varır mıydı?",
    "example": "Örnekler düşünmeyi somutlaştırır. Bu örnek her durum için geçerli mi, yoksa yalnızca belirli bir durum için mi?",
    "heard": "Duyduklarımızı hemen reddetmemize gerek yok, ama onları sınamadan da benimsemeyelim. Bu düşünceyi kendi sözlerinle gerekçelendirmeyi dener misin?",
    "reasoning": "Bir akıl yürütmeden söz ediyorsun; güzel. Öncüllerini tek tek saysak, hangisinden en az eminsin?",
    "principle": "İlkelerimiz yaşamımızı yönlendirir. Bu ilkeyi sana kim ya da ne öğretti ve onu hiç sınadın mı?",
    "unsure": "Bunu söylemek cesaret ister; bilmediğimizi fark etmek araştırmanın başlangıcıdır. Gel, daha basit bir örnekten ilerleyelim.",
}
SOKRATES_EXTRA_QUESTIONS = {
    "bilgi": (
        "Bilgi ile doğru sanı (kanaat) aynı şey midir?",
        "Tesadüfen doğru bir tahmin yapan biri o şeyi biliyor sayılır mı? Bilmek için doğruya nasıl ulaştığımızı da açıklayabilmemiz gerekmez mi?",
        "Öyleyse bilgiyi doğru sanıdan ayıran nedir? Gerekçe göstermek ya da nedenini açıklayabilmek bu farkı yaratır mı?",
        "Daha basit bir örnek düşünelim: Bir öğrenci sınavda bir soruyu tahminle doğru cevaplıyor. Sence o öğrenci cevabı bilmiş mi oldu?",
    ),
    "erdem": (
        "Erdem öğretilebilir mi?",
        "Öyleyse erdemi öğretecek öğretmenler kimlerdir? Doğru davranmayı öğretmek, bir zanaatı öğretmek gibi midir?",
        "Erdem öğretilemezse insanlar iyi olmayı nasıl kazanır? Doğuştan mı, alıştırmayla mı, yoksa başka bir yolla mı?",
        "Daha basit bir örnek düşünelim: Birine yüzmeyi öğretebiliriz. Peki cesur olmayı bir ders gibi anlatarak öğretebilir miyiz?",
    ),
    "adalet": (
        "Haksızlık yapmak, haksızlığa uğramaktan daha mı kötüdür?",
        "Öyleyse bir insan haksızlığa uğramayı, haksızlık yapmaya tercih etmeli midir? Bunun nedeni ne olabilir?",
        "Haksızlık yapan kişinin kendi ruhunda ne olur? Başkasına yapılan haksızlık, yapan kişiyi de etkiler mi?",
        "Daha basit bir örnek düşünelim: Bir çocuk arkadaşının oyuncağını gizlice alıyor. Sence en çok kim zarar görür: oyuncağı kaybeden mi, yoksa alan mı?",
    ),
    "mutluluk": (
        "Mutlu olmak için önce erdemli olmak gerekir mi?",
        "Erdemli olduğu hâlde acı çeken bir insan mutlu sayılabilir mi?",
        "Öyleyse erdemsiz biri de gerçekten mutlu olabilir mi? Mutluluğu neye bağlıyorsun?",
        "Daha basit bir örnek düşünelim: Dürüst çalışan bir öğrenci ile kopya çeken bir öğrenci aynı notu alsa, hangisi daha huzurlu olur?",
    ),
    "yapay-zeka": (
        "Bir makine soru sorabiliyorsa, düşünüyor sayılabilir mi?",
        "Öyleyse düşünmek yalnızca soru sorabilmek midir? Soru sormakla anlayarak soru sormak arasında fark var mıdır?",
        "Peki düşünmeyi nasıl tanımlıyorsun? Bir insanın ezberlediği bir soruyu sorması düşünmek midir?",
        "Daha basit bir örnek düşünelim: Bir papağan günaydın diyebilir. Sence papağan bunun ne demek olduğunu bilerek mi söyler?",
    ),
}

# --------------------------------------------------------------------------- ARISTOTELES
ARISTOTELES = {
    "id": "aristoteles",
    "philosopher": "Aristoteles",
    "scene": "lykeion",
    "title": "Aristoteles ile Yüz Yüze",
    "setting": "Lykeion (Atina), MÖ 4. yüzyıl",
    "disclaimer": "Mekân ve giysiler dönem bilgisine dayanan yaklaşık bir canlandırmadır; belgelenmiş bir görüntü değildir.",
    "welcome": (
        "Hoş geldin. Ben Aristoteles. Lykeion'un yürüyüş yolunda öğrencilerimle doğa, insan ve toplum üzerine "
        "araştırma yaparız. Bir konuyu önce gözlemler, sonra nedenlerini ararız. Bugün hangi konuyu inceleyelim?"
    ),
    "reason_prompt": "Bu görüşün neye dayanıyor?",
    "reasons": {
        "experience": "Gözlem iyi bir başlangıçtır. Peki, aynı gözlemi yapan başka birçok kişi de aynı sonuca varır mıydı?",
        "example": "Örnek, genel ilkeye giden yoldur. Ama tek bir örnek bir ilkeyi kanıtlar mı, yoksa yalnızca düşündürür mü?",
        "heard": "Yaygın görüşler araştırmaya başlamak için değerlidir; ama onları sınamadan benimsemeyiz. Bu görüşün gerekçesini bulabilir misin?",
        "reasoning": "Öncülleri ve sonucu ayıralım. Öncüllerinden hangisine en az güveniyorsun?",
        "principle": "İlkeler araştırmanın başlangıcıdır; yine de ilkenin kendisini neyin desteklediğini sormak gerekir. Bu ilkeyi nereden edindin?",
        "unsure": "Bu yadırganacak bir şey değil; araştırma şaşırmakla başlar. Daha basit bir durumdan ilerleyelim.",
    },
    "bridges": [
        "Şimdi aynı konuya başka bir yönden bakalım.",
        "Bunu bir ayrımla netleştirelim.",
        "Şimdi bir sonraki soruya geçelim.",
        "Buradan yeni bir soru çıkıyor.",
        "Bu konuyu başka bir örnekle düşünelim.",
        "Şimdi konunun bir başka yanına bakalım.",
    ],
    "reflection_question": "Bu konuşmanın başındaki düşüncenle şimdiki düşüncen arasında bir fark var mı?",
    "final": (
        "İnsanlar doğaları gereği bilmek ister. Bugün birlikte sorduğumuz soruları tek başına da sürdür: "
        "gözlemle, ayır, gerekçelendir. Öğrenmeye devam et."
    ),
    "topics": [
        {
            "id": "mutluluk",
            "menu": "Mutluluk",
            "title": "Mutluluk (Eudaimonia)",
            "opening": (
                "Her insan mutlu olmak ister; ama mutluluğun ne olduğunda anlaşamayız. Kimi onu hazda, kimi onurda, kimi de "
                "düşüncede arar. Önce bu görüşleri ayıralım."
            ),
            "closing": (
                "Mutluluğu yalnızca hazza ya da şansa değil, erdemle yapılan etkinliğe bağlamak, onu büyük ölçüde kendi "
                "çabamıza bağlamaktır. Bu görüşü birlikte sınadık; sınamaya devam etmek sana kalmış."
            ),
            "questions": [
                (
                    "Mutluluk yalnızca haz almaktan mı ibarettir?",
                    "Öyleyse bir hayvanın hazzı ile bir insanın hazzı aynı değerde midir? İnsana özgü olan nedir?",
                    "Haz mutluluğun bir parçası olabilir mi? Hazzı tamamen dışarıda bıraktığımızda mutluluk eksik kalır mı?",
                    "Basit bir örnek düşünelim: Bir öğrenci oyun oynarken haz alır, çalışırken ise zorlanır ama sonunda bir şey öğrenir. Hangisi onun için daha kalıcı bir iyidir?",
                ),
                (
                    "Mutluluk, bir anlık bir durum değil de bütün bir hayat boyunca süren bir durum mudur?",
                    "Öyleyse bir kişinin mutlu olduğunu söylemek için hayatının sonunu beklemek gerekir mi? Yoksa her gün mutlu olunabilir mi?",
                    "Bir anlığına mutlu olan biri, ömrünün geri kalanını mutsuz geçirse mutlu sayılır mı?",
                    "Bir kırlangıç gelince yaz gelmiş olur mu, yoksa yaz uzun bir mevsim midir? Mutluluk hangisine benziyor?",
                ),
                (
                    "Sağlık, dostlar ve geçim gibi dış koşullar mutluluk için gerekli midir?",
                    "Peki bu dış koşullar yeterli midir? Hepsine sahip olup erdemsiz yaşayan biri mutlu olur mu?",
                    "Aç, hasta ve yalnız bir insanın erdemli etkinlikte bulunması ne kadar kolaydır? Bu koşullar hiç mi önemli değil?",
                    "Basit bir örnek düşünelim: İyi bir koşucu sakatsa yeteneğini gösterebilir mi? Dış koşullar buna benzer mi?",
                ),
                (
                    "İnsana özgü işlev, düşünme yetisini kullanmak mıdır?",
                    "O hâlde iyi bir insan, düşünme yetisini iyi kullanan insan mıdır? Düşünmeyi iyi kullanmak ne demektir?",
                    "İnsanı diğer canlılardan ayıran başka bir işlev önerebilir misin? Bu işlev yalnızca insana mı özgü olur?",
                    "Gözün işlevi görmektir, bıçağın işlevi kesmek. İnsan için de böyle bir işlev var mıdır, sence?",
                ),
                (
                    "Düşünceyle yapılan etkinlik, en yüksek mutluluk biçimi olabilir mi?",
                    "Peki herkes bütün zamanını düşünmeye ayırabilir mi? Gündelik yaşam ve erdemli eylemler bu hayatta nerede durur?",
                    "O hâlde en yüksek mutluluğu hangi etkinlikte buluyorsun? Bu etkinlik yalnızca insana mı özgüdür?",
                    "Bir bilmeceyi çözmenin verdiği doyumu düşün. Bu doyum başka hazlardan farklı mı?",
                ),
                (
                    "Mutluluk herkes için aynı şeylerden mi oluşur?",
                    "O hâlde bir çiftçi, bir asker ve bir hekim için mutluluk aynı etkinlik midir? Ortak olan nedir?",
                    "Eğer herkes için farklıysa, mutluluk sözcüğüyle hepimiz aynı şeyi mi kastediyoruz? Ortak bir ölçüt olabilir mi?",
                    "Basit bir örnek düşünelim: İki öğrenciden biri resim yapmayı, diğeri koşmayı seviyor. İkisinin de iyi bir hayatı olabilir mi? Aralarında ortak ne var?",
                ),
            ],
        },
        {
            "id": "erdem",
            "menu": "Erdem",
            "title": "Erdem ve Altın Orta",
            "opening": (
                "Karakter erdemleri, doğuştan gelmez; alışkanlıkla kazanılır. Cesaret, ölçülülük, cömertlik gibi erdemleri "
                "iki aşırılık arasındaki bir orta nokta olarak ele alırım. Bu fikri birlikte sınayalım."
            ),
            "closing": (
                "Erdem, bir kez edinilip bırakılan şey değil, her gün sürdürülen bir alışkanlıktır. Bugün sınadığın fikirleri "
                "gündelik yaşamında da sına."
            ),
            "questions": [
                (
                    "Erdem, doğuştan gelen bir özellik midir?",
                    "O hâlde bir insan iyi alışkanlıklar edinmeden de erdemli olabilir mi? Çocukluktaki eğitim bu durumda ne işe yarar?",
                    "Öyleyse erdem nasıl kazanılır? Alışkanlık ve tekrarın erdemde nasıl bir yeri olabilir?",
                    "Bir çalgıcı çalarak çalgıcı olur. İnsan da adil işler yaparak adil olabilir mi?",
                ),
                (
                    "Cesaret, hiç korkmamak demek midir?",
                    "Hiç korkmayan biri tehlikenin ne olduğunu anlamıyor olabilir mi? Bu durumda ona cesur mu, pervasız mı deriz?",
                    "O hâlde cesaret, korkunun ne zaman ve ne kadar yerinde olduğunu bilmek midir? Korkaklık ve pervasızlık nerede başlar?",
                    "Basit bir örnek düşünelim: Bir itfaiyeci yanan binaya girer. Korkmuyor mu, yoksa korkusuna rağmen mi giriyor? Hangisi daha cesurca?",
                ),
                (
                    "Doğru davranış her insan için ve her durumda aynı mıdır?",
                    "Bir kişiye yetecek kadar yemek, bir güreşçi için de yeterli midir? Orta nokta herkes için aynı mıdır?",
                    "Öyleyse doğru davranışı neye göre belirleyeceğiz? Bu işte pratik bilgelik (phronesis) bir rol oynar mı?",
                    "Bir arkadaşına sert ya da yumuşak davranmak durumuna göre değişir mi? Hangi durumda hangisi yerinde olur?",
                ),
                (
                    "Bazı eylemler, ortası aranamayacak kadar baştan kötü müdür?",
                    "Öyleyse her eylemde altın orta aramak doğru mu? Hangi eylemler bu kuralın dışında kalır?",
                    "Bir hırsızlığın ölçülüsü olabilir mi? Bir eylemin kendisi kötüyse ölçüsünü aramak ne anlama gelir?",
                    "Basit bir örnek düşünelim: Başkasının malını kasten almak için uygun bir miktar var mıdır?",
                ),
                (
                    "Neyin doğru olduğunu bilmek, doğru davranmak için yeterli midir?",
                    "Biz buna akrasia, yani irade zayıflığı deriz. Doğruyu bildiği hâlde arzusuna yenilen birini hiç görmedin mi?",
                    "Öyleyse bilginin yanında ne gerekir? Alışkanlık ve arzularımızı terbiye etmek bunun bir parçası mıdır?",
                    "Basit bir örnek düşünelim: Sağlıklı beslenmenin iyi olduğunu bilen herkes sağlıklı mı besleniyor? Bilgi ile uygulama arasında ne var?",
                ),
                (
                    "Erdemli olmak, erdemli eylemden haz almayı da içerir mi?",
                    "Peki cesur eylemi zorlukla yapan biri ile onu isteyerek yapan biri arasında bir fark var mıdır?",
                    "Doğru olanı yapmaktan hiç haz almayan biri erdemli sayılır mı, yoksa kendini zorlayan biri mi?",
                    "Basit bir örnek düşünelim: Bir çocuk ödevini isteksizce, diğeri isteyerek yapıyor. Hangisinin alışkanlığı daha sağlam olur?",
                ),
            ],
        },
        {
            "id": "dostluk",
            "menu": "Dostluk",
            "title": "Dostluk (Philia)",
            "opening": (
                "Dostluk, erdemden sonra yaşamın en gerekli şeylerinden biridir; başka bütün iyilere sahip olsa bile hiç kimse "
                "dostsuz yaşamak istemez. Dostluğun türlerini birlikte ayıralım."
            ),
            "closing": (
                "Dostluk yalnızca bir duygu değil, birlikte yapılan iyi etkinliktir. Dostlarını seçerken hangi tür dostluğu "
                "kurduğunu düşün."
            ),
            "questions": [
                (
                    "Yararına olan biriyle kurulan ilişki gerçek bir dostluk sayılabilir mi?",
                    "Yarar ortadan kalkınca ilişki de sona ererse, bu ilişki ne kadar kalıcıdır?",
                    "Birbirine yararı dokunan iki tüccara hiç mi dost diyemeyiz? Dostluğun daha düşük bir türü olabilir mi?",
                    "Basit bir örnek düşünelim: Ders çalışmak için bir araya gelen iki öğrenciden biri sınav bitince uzaklaşırsa bu ne tür bir arkadaşlıktı?",
                ),
                (
                    "Eğlenceye dayanan bir dostluk kalıcı olabilir mi?",
                    "Eğlendiren şeyler değişirse ilişki de değişir mi? Bunu gençlerde sıkça görmez miyiz?",
                    "Güven ve ortak değerler olmadan yalnızca eğlenceye dayalı bir dostluk zamanla neden çözülür?",
                    "Basit bir örnek düşünelim: Aynı oyunu seven iki arkadaş oyunu bırakınca ne konuşur? Ortak olan yalnızca oyun muydu?",
                ),
                (
                    "Gerçek dostluk için dostların iyi karakterli olması gerekir mi?",
                    "Dostun iyiliğini, dostun kendisi için istemek bu tür dostlukta nasıl görünür?",
                    "Kötü karakterli iki kişi birbirine güvenerek uzun süre dost kalabilir mi? Birbirlerine ne kadar iyilik isterler?",
                    "Basit bir örnek düşünelim: Sürekli yalan söyleyen biriyle sırlarını paylaşır mıydın? Güven ile karakter arasında ne ilişki var?",
                ),
                (
                    "İnsan dostlarının sayısını istediği kadar artırabilir mi?",
                    "Zamanı ve ilgiyi herkesle paylaşırsak, her birine ne kadar yakın olabiliriz?",
                    "Neden sınırlı olsun? Birbirini tanımak ve birlikte vakit geçirmek için ne kadar zaman gerekir?",
                    "Basit bir örnek düşünelim: Bir doğum gününe yüz kişi davet etsen hepsiyle tek tek konuşabilir misin?",
                ),
                (
                    "İnsan kendisiyle de dost olabilir mi?",
                    "Kendini sevmek ile bencillik aynı şey midir? İyi bir insan kendini nasıl sever?",
                    "Kendisiyle çatışan biri başkalarıyla sağlıklı bir dostluk kurabilir mi?",
                    "Basit bir örnek düşünelim: Yaptığı bir şeyden pişman olan biri kendine kızgınsa, bu kendisiyle dostluğun bozulması mıdır?",
                ),
                (
                    "Mutlu bir insan için dostlar gerekli midir?",
                    "Peki kendi başına yeten biri neden yine de dost ister? Dostlar ona ne verir?",
                    "Hiç dostu olmayan bir insanın en güzel etkinliklerini kiminle paylaşacağını düşündün mü?",
                    "Basit bir örnek düşünelim: Önemli bir şey keşfettiğinde onu kimseyle paylaşamasaydın sevincin aynı olur muydu?",
                ),
            ],
        },
        {
            "id": "mantik",
            "menu": "Mantık",
            "title": "Mantık ve Akıl Yürütme",
            "opening": (
                "Bir akıl yürütmenin sağlam olup olmadığını anlamak için önce öncülleri ve sonucu ayırmamız gerekir. Bu amaçla, "
                "sonucun öncüllerden zorunlu olarak çıktığı çıkarımları inceledim; buna syllogismos diyoruz. Birlikte deneyelim."
            ),
            "closing": (
                "Doğru düşünmenin yolu, kavramları net kullanmak ve çıkarımları adım adım sınamaktır. Bu yöntemi hem "
                "benim sözlerime hem kendi sözlerine uygula."
            ),
            "questions": [
                (
                    "Sonuç, öncüllerden zorunlu olarak çıkıyorsa bu akıl yürütme sağlam mıdır?",
                    "Öncüller yanlışsa, bu tür bir akıl yürütme yine de doğru bir sonuca götürür mü? Çıkarımın sağlamlığı ile öncüllerin doğruluğu aynı şey midir?",
                    "Sonucun öncüllerden çıkmasını başka hangi ölçütle güvence altına alırdın?",
                    "Basit bir örnek düşünelim: Bütün kuşların kanadı vardır. Serçe bir kuştur. Bundan serçenin kanadı olduğu sonucu zorunlu olarak çıkar mı?",
                ),
                (
                    "Öncülleri doğru olmayan bir akıl yürütmenin sonucuna güvenilebilir mi?",
                    "Yanlış öncüllerden hareketle doğru bir sonuca rastlantıyla ulaşılabilir mi? O sonuca gerekçeli bir bilgi diyebilir miyiz?",
                    "O hâlde bilimsel bir kanıt için öncüllerin nasıl olması gerekir? Doğru ve daha temel olmaları yeter mi?",
                    "Basit bir örnek düşünelim: Bütün kuşlar balıktır, serçe bir kuştur, o hâlde serçe balıktır. Biçim düzgün, öncül yanlış. Sonuç güvenilir mi?",
                ),
                (
                    "Bütün bilgilerimiz kanıtlanabilir mi?",
                    "Her kanıt bir önceki öncüle dayanırsa bu zincir nerede biter? Sonsuza kadar sürebilir mi?",
                    "Kanıtlanamayan ama doğru bildiğimiz ilkelere nasıl ulaşırız? Gözlem ve sezgi bu işte bir rol oynar mı?",
                    "Basit bir örnek düşünelim: Bir şeyin aynı anda hem var hem yok olamayacağını nasıl kanıtlarsın? Bu bir kanıta mı dayanır, yoksa her kanıttan önce mi gelir?",
                ),
                (
                    "Aynı şey, aynı anda ve aynı bakımdan hem var hem yok olabilir mi?",
                    "Böyle olduğunu savunan biriyle nasıl konuşuruz? Anlaşma neye dayanır?",
                    "Bu ilkeyi inkâr eden birine karşı onu nasıl savunursun? Konuşabilmek için bile bu ilkeyi kabul etmek gerekmez mi?",
                    "Basit bir örnek düşünelim: Bir kapı aynı anda hem açık hem kapalı olabilir mi? Aynı bakımdan sözü burada ne işe yarıyor?",
                ),
                (
                    "Birkaç gözlemden bütün için bir sonuç çıkarmak güvenilir midir?",
                    "Peki kaç gözlem yeterlidir? Bir kuğuyu beyaz görmek bütün kuğuların beyaz olduğunu kanıtlar mı?",
                    "Öyleyse genel ilkelere nasıl ulaşırız? Tümevarım (epagoge) bu konuda bize nasıl yardım eder?",
                    "Basit bir örnek düşünelim: Üç gün üst üste güneşin doğduğunu görürsün. Yarın da doğacağından neye dayanarak emin olursun?",
                ),
                (
                    "Aynı sözcüğü farklı anlamlarda kullanmak bir tartışmayı yanıltabilir mi?",
                    "Bunu önlemek için tartışmaya başlarken ne yapmalıyız? Terimleri tanımlamak yeter mi?",
                    "İyi sözcüğü, iyi bir at için ve iyi bir insan için kullanıldığında anlamı aynı mıdır? Fark nerede?",
                    "Basit bir örnek düşünelim: Kol sözcüğü hem vücudun bir parçası hem de bir kuruluşun bölümü olabilir. Hangisini kastettiğimizi belirtmesek ne olur?",
                ),
            ],
        },
        {
            "id": "siyaset",
            "menu": "Toplum ve Siyaset",
            "title": "Toplum ve Siyaset",
            "opening": (
                "İnsan, doğası gereği toplumsal bir canlıdır; kentte (polis) yaşar, çünkü yalnızca yaşamak için değil, iyi yaşamak "
                "için bir araya geliriz. Yönetim biçimlerini ve adalet ölçütlerini birlikte inceleyelim."
            ),
            "closing": (
                "Siyaset, ortak iyiyi arama sanatıdır. Yaşadığın toplulukta neyin iyi yaşamayı desteklediğini sormaya devam et."
            ),
            "questions": [
                (
                    "İnsan, tek başına da iyi bir hayat yaşayabilir mi?",
                    "Dili, hukuku ve işbölümünü nereden edindik? Kendi kendine yeten ancak bir tanrı ya da bir hayvan olabilir mi?",
                    "Öyleyse topluluk içinde yaşamak bizim doğamızın bir gereği midir, yoksa bir alışkanlık mı?",
                    "Basit bir örnek düşünelim: Hiç konuşacak kimsesi olmayan biri düşünme yetisini ne kadar geliştirebilir?",
                ),
                (
                    "Bir devletin amacı yalnızca güvenliği ve ticareti sağlamak mıdır?",
                    "Peki iyi bir hayat için gerekli olan erdemi ve eğitimi kim sağlar? Yalnızca bir ittifaktan farkı ne olurdu?",
                    "O hâlde devletin asıl amacı iyi yaşamak olmalı mı? Bu amacı gerçekleştirmek için neler gerekir?",
                    "Basit bir örnek düşünelim: Bir okulun amacı yalnızca öğrencileri sınıfta tutmak mıdır, yoksa onlara bir şey öğretmek mi?",
                ),
                (
                    "Yönetimin kim tarafından yapıldığı, yönetimin iyi olup olmadığını belirler mi?",
                    "Öyleyse bir kişi, birkaç kişi ve çoğunluk arasında hangisi her zaman daha iyi yönetir?",
                    "Peki yönetimi ne zaman iyi, ne zaman bozulmuş sayarız? Ortak yararı gözetmek burada bir ölçüt olabilir mi?",
                    "Basit bir örnek düşünelim: Bir takımı yalnızca kendi çıkarını düşünen bir kaptan ile bütün takımı düşünen bir kaptan yönetse sonuç aynı olur mu?",
                ),
                (
                    "Orta halli yurttaşların çoğunlukta olduğu bir toplum daha kararlı olur mu?",
                    "Çok zengin ile çok yoksulun karşı karşıya geldiği bir toplumda ne olur? Orta halli yurttaşlar bu dengeyi nasıl etkiler?",
                    "Peki servetin çok az kişide toplandığı toplumlarda istikrar nasıl sağlanır?",
                    "Basit bir örnek düşünelim: Bir sınıfta öğrenciler ya çok başarılı ya çok başarısız olsa, o sınıfı yönetmek kolay mı olur?",
                ),
                (
                    "Yasalar, yönetenlerin kişisel kararlarından daha güvenilir midir?",
                    "Peki yasa her özel durumu önceden görebilir mi? Yasanın bıraktığı boşluğu kim, nasıl doldurur?",
                    "Bir yöneticinin tutkusu ve çıkarı kararlarını etkileyebilir mi? Yasa bu etkiyi nasıl sınırlar?",
                    "Basit bir örnek düşünelim: Bir oyunda hakem kuralları uygulamasa, kendi kararına göre davransa oyuncular ona güvenir mi?",
                ),
                (
                    "Eğitim, devletin ilgilenmesi gereken bir konu mudur?",
                    "Öyleyse bütün yurttaşlar için ortak bir eğitim mi olmalı, yoksa ailelere mi bırakılmalı?",
                    "Peki yurttaşları ortak iyiye hazırlayacak olan kimdir? Yalnızca aileler yeterli olur mu?",
                    "Basit bir örnek düşünelim: Herkesin farklı kurallar öğrettiği bir kentte insanlar ortak kurallara nasıl uyar?",
                ),
            ],
        },
    ],
}

# --------------------------------------------------------------------------- FARABİ
FARABI = {
    "id": "farabi",
    "philosopher": "Farabi",
    "scene": "majlis",
    "title": "Farabi ile Yüz Yüze",
    "setting": "Abbasi dönemi bir ilim meclisi, 10. yüzyıl",
    "disclaimer": "Mekân ve giysiler dönem bilgisine dayanan genel bir canlandırmadır; Farabi'nin belgelenmiş bir portresi yoktur.",
    "welcome": (
        "Selam sana, ey hakikat arayıcısı. Ben Farabi. Mantık, akıl ve erdemli toplum üzerine düşünür, farklı görüşleri "
        "bir araya getirmeye çalışırım. Bugün seninle hangi konuyu inceleyelim?"
    ),
    "reason_prompt": "Bu görüşünü neye dayandırıyorsun?",
    "reasons": {
        "experience": "Kendi deneyiminden söz ediyorsun; deneyim bilginin kaynaklarından biridir. Aynı deneyimi başkaları da yaşasaydı hepsi aynı sonuca mı varırdı?",
        "example": "Örnek, genel hükmü anlamaya yardım eder. Ama bir örnek, genel bir hükmü kanıtlamaya yeter mi?",
        "heard": "Aktarılan bilgiyi dikkate almak gerekir; ama doğruluğunu sınamadan kabul etmek akıl yolu değildir. Bunun dayanağını birlikte arayalım mı?",
        "reasoning": "Akıl yürütmeye dayanman güzel. Öncülleri ve sonucu ayıralım: Öncüllerinden hangisini en az sağlam buluyorsun?",
        "principle": "İlkelerimiz davranışlarımızı yönlendirir. Peki bu ilkeyi hangi gerekçeyle benimsedin?",
        "unsure": "Bilmediğini kabul etmek öğrenmenin ilk adımıdır. Konuyu daha küçük parçalara ayırıp basit bir yerden başlayalım.",
    },
    "bridges": [
        "Şimdi konunun başka bir yönüne geçelim.",
        "Bunu bir ayrımla netleştirelim.",
        "Buradan yeni bir soru çıkıyor.",
        "Şimdi sıradaki soruya bakalım.",
        "Bunu bir örnekle somutlaştıralım.",
        "Şimdi başka bir açıdan bakalım.",
    ],
    "reflection_question": "Bu konuşmanın başındaki düşüncenle şimdiki düşüncen arasında bir fark var mı?",
    "final": (
        "Bilgiyi sevmek, ona saygıyla ve sabırla yaklaşmayı gerektirir. Öğrendiklerini düzenle, aralarındaki bağları ara ve "
        "bilgiyi toplumuna da fayda sağlayacak biçimde kullan. Bu yolda ilerlemeye devam et."
    ),
    "topics": [
        {
            "id": "mutluluk",
            "menu": "Mutluluk",
            "title": "Mutluluk (Saadet)",
            "opening": (
                "Saadet, insanın nihai amacıdır; yani başka bir şey için değil, kendi uğruna istenen en yüksek iyidir. İnsan ona "
                "bilgi ve erdemli eylemle ulaşır. Bunu birlikte inceleyelim."
            ),
            "closing": (
                "Saadet, yalnızca bilmekle değil, bildiğini erdemle yaşamakla kazanılır. Bunu bir ömür boyu sürdürülen bir çaba olarak düşün."
            ),
            "questions": [
                (
                    "Mutluluk, başka bir şey için değil kendi uğruna istenen en yüksek iyi midir?",
                    "Para, haz ve şöhret de mutluluk için istenen şeyler olabilir mi? Bunlar kendi uğruna mı istenir, yoksa başka bir şey için mi?",
                    "Peki her şeyin ardından ne için diye sorduğumuzda sonunda nerede duracağız?",
                    "Basit bir örnek düşünelim: İnsan ilaç içer, sağlıklı olmak için; sağlıklı olmak ister, işini yapabilmek için. Bu zincir nerede biter?",
                ),
                (
                    "Mutluluğa ulaşmak için yalnızca bilgi yeter mi?",
                    "Doğruyu bilen ama kötü alışkanlıkları olan biri mutlu olur mu? Bilgi ile eylem arasında nasıl bir bağ var?",
                    "Öyleyse bilgiye ek olarak ne gerekir? Ahlaki erdemler ve doğru eylem bu yolda hangi rolü oynar?",
                    "Basit bir örnek düşünelim: Yüzmenin kurallarını okuyan herkes iyi yüzer mi? Bilgi ile uygulama arasında ne var?",
                ),
                (
                    "İnsan, mutluluğa tek başına ulaşabilir mi?",
                    "Dili, bilgiyi ve zanaatları kimden öğrendik? Tek başına yaşayan biri bunların hangisine ulaşabilirdi?",
                    "Öyleyse insanın toplumda yaşaması, mutluluğuna ulaşmanın bir koşulu mudur? Bu neden böyledir?",
                    "Basit bir örnek düşünelim: Bir çiftçi ekmeğini, giysisini ve ilacını tek başına yapabilir mi?",
                ),
                (
                    "Herkes, mutluluk dediği şeyin gerçekten mutluluk olup olmadığını doğru bilir mi?",
                    "Bazı kentler yalnızca zenginliği ya da hazzı amaç edinir. Hepsi aynı oranda haklı olabilir mi?",
                    "Öyleyse insan neye mutluluk dediğinde yanılabilir. Gerçek mutluluğu, sanılan mutluluktan nasıl ayırırız?",
                    "Basit bir örnek düşünelim: Çok tatlı yemeyi seven bir çocuk bunun kendisine iyi geldiğini sanabilir. İyi gelen şey ile iyi görünen şey aynı mıdır?",
                ),
                (
                    "Erdemli davranışlar alışkanlıkla kazanılabilir mi?",
                    "Peki bir alışkanlığı kazanmak için eğitim, örnek ve yasa gibi şeyler ne kadar gereklidir?",
                    "Öyleyse erdemi nasıl edinirsin? Hiç alıştırma yapmadan bir davranışı özümseyebilir misin?",
                    "Basit bir örnek düşünelim: Bir çalgıyı hiç çalışmadan öğrenmek mümkün mü? Erdem buna benzer mi?",
                ),
                (
                    "Gençken edinilen alışkanlıklar, ileride mutluluğumuzu etkiler mi?",
                    "Öyleyse çocukluk ve gençlikteki eğitim, mutluluğa ulaşmanın ne kadar önemli bir parçası olur?",
                    "Kötü alışkanlıklar edinmiş birinin sonradan değişebilmesi için ne gerekir? Bu kolay mıdır?",
                    "Basit bir örnek düşünelim: Küçükken düzenli kitap okuyan biri büyüyünce kitapla nasıl bir ilişki kurar?",
                ),
            ],
        },
        {
            "id": "sehir",
            "menu": "Erdemli Şehir",
            "title": "Erdemli Şehir",
            "opening": (
                "Şehir, insanların bir arada yaşayarak mutluluğa ulaşmak için kurduğu topluluktur. Ben sağlıklı bir bedene benzeyen bir "
                "şehri düşünürüm: Bütün organlar, bir yöneticinin önderliğinde uyum içinde çalışır. Bu fikri birlikte inceleyelim."
            ),
            "closing": (
                "Şehir, tıpkı bir beden gibi, parçaların uyumuyla sağlıklı olur. Yaşadığın topluluğu bu gözle değerlendirmeyi dene."
            ),
            "questions": [
                (
                    "Bir şehrin amacı, halkını mutluluğa ulaştırmak mı olmalıdır?",
                    "Peki şehir yalnızca zenginlik ya da güç peşinde koşarsa halk mutluluğa ulaşır mı?",
                    "Öyleyse bir şehrin asıl amacı ne olmalıdır? Güvenlik, ticaret ya da güç mü?",
                    "Basit bir örnek düşünelim: Bir hastanenin amacı yalnızca binayı işletmek midir, yoksa hastaları iyileştirmek mi?",
                ),
                (
                    "Bir şehirde herkes aynı işi yapmalı mıdır?",
                    "Herkes aynı işi yaparsa ihtiyaçlarımızın hepsi nasıl karşılanır?",
                    "Farklı işleri yapan insanlar birbirine nasıl bağlanır? Organların uyumu burada nasıl bir benzetme olur?",
                    "Basit bir örnek düşünelim: Bir takımda herkes kaleci olsa maç oynanabilir mi?",
                ),
                (
                    "Şehri yönetecek kişi, bilgi ve erdemde en olgun kişi olmalı mıdır?",
                    "Peki böyle bir kişiyi nasıl tanırız? Yönetici olmak için hangi nitelikler aranmalıdır?",
                    "O hâlde yönetimi kime vermeliyiz? Bilgisizliği ya da çıkarı olan birinin yönetmesi şehre ne yapar?",
                    "Basit bir örnek düşünelim: Bir gemiyi denizi ve yıldızları iyi bilen mi, yoksa yalnızca yüksek sesle konuşan mı yönetmeli?",
                ),
                (
                    "Bir şehir, yanlış şeyleri mutluluk sanan bir yönetim yüzünden yanılabilir mi?",
                    "Böyle şehirlerde halk neyi amaç edinir? Servet ve haz gibi şeyler gerçek mutluluk mudur?",
                    "Hiçbir şehir yanılmaz mı? Yöneticilerinin yanlış amaçların peşinde koştuğu toplumlar hiç olmadı mı?",
                    "Basit bir örnek düşünelim: Bir kaptan yanlış harita kullanırsa bütün yolcular nereye varır?",
                ),
                (
                    "İnsanlar birbirine yardım etmeden mutlu olabilir mi?",
                    "Kendi ihtiyaçlarını başkalarına bağlı olmadan karşılayabilen biri var mıdır? Bunu hangi örnekle açıklarsın?",
                    "Öyleyse yardımlaşmayı sağlayan nedir: zorunluluk mu, sevgi mi, yoksa ortak amaç mı?",
                    "Basit bir örnek düşünelim: Köprü kuran işçiler arasında işbirliği olmasa köprü ayakta durur mu?",
                ),
                (
                    "Farklı kültürlerden ve inançlardan insanlar aynı şehirde birlikte yaşayabilir mi?",
                    "Peki bu insanları birleştiren ortak değerler ya da amaçlar neler olabilir?",
                    "Aynı şehirde yaşamak için ortak bir dil, ortak kurallar ve karşılıklı saygı yeterli olmaz mı?",
                    "Basit bir örnek düşünelim: Farklı mahallelerden çocuklar aynı okulda oynarken hangi ortak şeyler onları bir araya getirir?",
                ),
            ],
        },
        {
            "id": "akil",
            "menu": "Akıl ve Bilgi",
            "title": "Akıl ve Bilgi",
            "opening": (
                "İnsanı diğer canlılardan ayıran şey akıldır. Aklın, imkândan gerçek bilgiye uzanan basamakları olduğunu düşünürüm: "
                "Önce yalnızca bilme imkânı vardır, sonra öğrenilen kavramlar, en sonunda da bilgiyi bütünüyle kavrama. Bunu birlikte inceleyelim."
            ),
            "closing": (
                "Akıl, geliştirildikçe bilgiye ve olgunluğa yol açan bir imkândır. Her öğrendiğinde bu imkânın bir parçasını gerçekleştirmiş olursun."
            ),
            "questions": [
                (
                    "Akıl, doğuştan hazır bir bilgi deposu mudur?",
                    "Peki bir çocuk hiç öğrenmeden hangi bilgileri bilir? Dil bile öğrenilmez mi?",
                    "O hâlde akıl, bilgiyi alma yeteneği olarak mı düşünülmeli? Bu yeteneğin gelişmesi için ne gerekir?",
                    "Basit bir örnek düşünelim: Bir tohum doğuştan ağaç mıdır, yoksa ağaç olma imkânı mı taşır? Akıl buna benzer mi?",
                ),
                (
                    "Bir şeyi öğrenmek, var olan bir imkânı gerçekleştirmek midir?",
                    "Öyleyse bu imkânı gerçekleştirmek için dışarıdan neye ihtiyaç duyarız? Öğretmene, kitaba, gözleme?",
                    "Peki öğrenmeden önce ve sonra insanın zihninde ne değişir? Bu değişim bir şey eklemek midir?",
                    "Basit bir örnek düşünelim: Bir çocuk okumayı öğrenmeden önce okuyabilir miydi? Öğrenince ne oldu?",
                ),
                (
                    "Duyularla algıladığımız şeyler, akılla kavradığımız kavramlarla aynı şey midir?",
                    "Bir üçgeni çizdiğimizde çizgiler kusurlu çıkar. Aklımızdaki üçgen kavramı da kusurlu mudur?",
                    "Peki akıl kavramları duyulardan mı çıkarır, yoksa başka bir kaynaktan mı alır?",
                    "Basit bir örnek düşünelim: İki ağacı görüyorsun, ama ağaç dediğimiz genel kavramı nasıl görüyorsun?",
                ),
                (
                    "Aklın bir şeyi kavrayabilmesi için, gözün ışığa ihtiyacı gibi, dışarıdan bir etkiye ihtiyacı var mıdır?",
                    "O hâlde bu etki nedir? Ben bunu faal akıl diye adlandırırım; sen bu fikri nasıl yorumlarsın?",
                    "Öyleyse akıl, kendi başına, imkân hâlinden gerçek bilgiye nasıl geçer?",
                    "Basit bir örnek düşünelim: Karanlık bir odada gözün açık olsa da bir şey görebilir misin? Işık ne işe yarıyor?",
                ),
                (
                    "Düşünmek, öğrendiklerimizi düzenlemeyi ve birbirine bağlamayı da içerir mi?",
                    "Peki kavramları birleştirip ayırarak yeni bilgilere nasıl ulaşırız? Bu işlemin kuralları var mıdır?",
                    "Düzensiz bir bilgi yığını bir insanı bilge yapar mı? Bilgiyi bilgelikten ayıran şey nedir?",
                    "Basit bir örnek düşünelim: Bir çekmecedeki bütün kitaplar karışık dururken aradığın kitabı bulabilir misin? Düzen ne sağlar?",
                ),
                (
                    "Akıl, insanın duygularını yönetmesine yardımcı olabilir mi?",
                    "Peki öfke gibi güçlü bir duygu anında aklın söz geçirmesi için ne gerekir? Alışkanlık burada nasıl bir rol oynar?",
                    "Duygular akıldan tamamen bağımsız mıdır? Duygularımızı hiç yönlendiremez miyiz?",
                    "Basit bir örnek düşünelim: Çok kızdığında bir an durup düşünmek seni nasıl etkiler?",
                ),
            ],
        },
        {
            "id": "ilimler",
            "menu": "Bilimler ve Mantık",
            "title": "Bilimler ve Mantık",
            "opening": (
                "Bilimler, doğru bilgiye ulaşmanın düzenli yollarıdır. İlimleri dil, mantık, matematik, doğa bilimleri ve metafizik, "
                "siyaset bilimi ile fıkıh ve kelam gibi başlıklar altında sınıflandırdım. Mantığı ise ilimlerin ortak aracı olarak gördüm. "
                "Bu düşünceyi birlikte sınayalım."
            ),
            "closing": (
                "İlimleri tanımak ve aralarındaki bağları görmek, bilgiyi dağınık bir yığın olmaktan kurtarır. Öğrendiklerini bir düzen içinde yerleştirmeyi dene."
            ),
            "questions": [
                (
                    "Mantık, bütün ilimlerin ortak bir aracı olabilir mi?",
                    "Bir marangozun aletleri ağacı işlemeye yarar. Mantığın işlediği şey nedir?",
                    "Öyleyse her ilmin kendi yöntemi ayrı mı olmalı? Ortak bir doğruluk ölçütü olamaz mı?",
                    "Basit bir örnek düşünelim: Tartı hem şekeri hem unu ölçer. Mantık da farklı ilimlerin ürünlerini ölçebilir mi?",
                ),
                (
                    "Dilbilgisi ile mantık aynı şeyi mi inceler?",
                    "Peki Arapça, Yunanca ve Türkçe'nin dilbilgisi kuralları farklıyken, doğru düşünmenin kuralları da farklı mıdır?",
                    "Öyleyse biri belirli bir dilin ifade kurallarını, diğeri bütün insanlarda ortak düşünme kurallarını incelemiş olabilir mi?",
                    "Basit bir örnek düşünelim: Bütün insanlar ölümlüdür cümlesi hangi dilde söylenirse söylensin çıkarım kuralları değişir mi?",
                ),
                (
                    "Matematik, doğa bilimlerinden daha kesin sonuçlar verir mi?",
                    "Peki bu kesinlik neden kaynaklanır? Soyut nesnelerle uğraşmasından mı?",
                    "Doğa bilimlerinin kesinliği neye dayanır? Gözlem yeterli olur mu?",
                    "Basit bir örnek düşünelim: İki artı iki dörttür. Yarın yağmur yağar mı? İkisi aynı kesinlikte midir?",
                ),
                (
                    "Siyaset ve ahlak ilimleri de diğer ilimler kadar sistemli incelenebilir mi?",
                    "Öyleyse bu ilimlerin konusu nedir? İnsanın eylemleri ve toplumsal düzenin ilkeleri mi?",
                    "Peki bir şehrin yönetimi ve insanın erdemi hakkında sağlam bilgiye nasıl ulaşırız?",
                    "Basit bir örnek düşünelim: İyi bir yöneticinin sahip olması gereken özellikleri sıralamak bir tür bilgi midir?",
                ),
                (
                    "Farklı düşünürlerin görüşleri arasında uzlaşma aramak, hakikati bulmaya yardım eder mi?",
                    "Ben Platon ile Aristoteles'in görünürde farklı konuşsalar da asıl amaçta birleştiklerini göstermeye çalıştım. Sen bir uzlaşmayı hangi koşulda doğru bulurdun?",
                    "Öyleyse çelişen iki görüşten birinin yanlış olduğunu nasıl gösterirsin? Uzlaşma aramak burada zarar verir mi?",
                    "Basit bir örnek düşünelim: İki arkadaş bir yol tarifini farklı sözcüklerle anlatıyor. Aynı yeri mi tarif ediyorlar? Nasıl anlarız?",
                ),
                (
                    "Bilgiyi başkalarına öğretmek, onu daha iyi kavramamıza yardım eder mi?",
                    "Öğretirken karşılaştığımız soruları cevaplayamazsak bu bize bilgimiz hakkında ne söyler?",
                    "Hiç öğretmeden de bir konuyu derinlemesine kavrayabilir miyiz? Sorular bu işte bir rol oynamaz mı?",
                    "Basit bir örnek düşünelim: Bir arkadaşına oyunun kurallarını anlattığında kuralları sen de daha iyi anlamış olur musun?",
                ),
            ],
        },
        {
            "id": "muzik",
            "menu": "Müzik ve Ruh",
            "title": "Müzik ve Ruh",
            "opening": (
                "Müziği hem bir sanat hem de aralıkları ve oranları olan bir ilim olarak inceledim. Sesler arasındaki ilişkiler sayılarla "
                "ifade edilebilir; aynı zamanda müzik ruhu etkiler. Bu iki yüzü birlikte düşünelim."
            ),
            "closing": (
                "Müzik hem sayıların hem ruhun diliyle konuşur. Dinlediğin bir ezgide hem düzeni hem duyguyu fark etmeye çalış."
            ),
            "questions": [
                (
                    "Müzik yalnızca bir eğlence midir?",
                    "Peki ağıt, marş ve ninni aynı duyguyu mu uyandırır? Her birinin farklı bir etkisi yok mudur?",
                    "Öyleyse müziğin ruhta uyandırdığı etkiler nelerdir? Bunları nasıl gözlemleyebiliriz?",
                    "Basit bir örnek düşünelim: Bir ninni bir çocuğu sakinleştirir. Bu yalnızca eğlence midir?",
                ),
                (
                    "Seslerin birbirine oranı, müziğin güzelliğinde rol oynar mı?",
                    "Bir telin boyunu yarıya indirdiğinde çıkan ses ile asıl ses arasındaki ilişki nasıl bir oran verir?",
                    "Peki bir ezginin güzelliğini yalnızca zevke bırakırsak, iki insanın bir ezgi hakkında anlaşmasını nasıl açıklarız?",
                    "Basit bir örnek düşünelim: Aynı tel biri uzun, biri kısa iki parçaya ayrıldığında çıkan seslerin farkı oranlarla anlatılabilir mi?",
                ),
                (
                    "Bir çalgının perdelerini ölçerek belirlemek gerekir mi?",
                    "Peki ölçmek için neyi esas alırız: kulağı mı, telin boyunu mu, yoksa ikisini birden mi?",
                    "Kulaklarımız farklıysa bir çalgıyı herkes aynı biçimde nasıl akort eder?",
                    "Basit bir örnek düşünelim: İki kişi aynı ud'u kendi kulağına göre akort etse sesleri uyuşur mu?",
                ),
                (
                    "Müzik, insanın ruh hâlini ve karakterini etkileyebilir mi?",
                    "O hâlde bazı ezgiler eğitimde kullanılmalı mı? Hangi ezgiler hangi duyguları besler?",
                    "Bir ezgiyi dinlerken kimimiz neşelenip kimimiz hüzünlenirsek bu farkı neyle açıklarız?",
                    "Basit bir örnek düşünelim: Hızlı bir marş ile yavaş bir ağıt aynı ruh hâlini uyandırır mı?",
                ),
                (
                    "Bir müzisyenin hem kuramı hem uygulamayı bilmesi gerekir mi?",
                    "Yalnızca çalan ama nedenini bilmeyen biri ile nedenini bilen ama çalamayan biri arasında hangisi müziği daha iyi kavrar?",
                    "Kuramı bilmeden iyi çalabilen biri bunu nasıl başarır? Başkasına öğretirken zorlanmaz mı?",
                    "Basit bir örnek düşünelim: Futbol oynamayı bilen ama kuralları bilmeyen biri hakem olabilir mi?",
                ),
                (
                    "Aynı ezgi, farklı toplumlarda aynı etkiyi uyandırır mı?",
                    "O hâlde müziğin evrensel bir yanı olduğunu mu düşünüyoruz? Bunun nedeni ne olabilir?",
                    "Öyleyse alışkanlıklar ve kültür müziğin etkisini nasıl biçimlendirir?",
                    "Basit bir örnek düşünelim: Bildiğin bir ninniyi başka bir kültürden biri dinlese aynı anıları hisseder mi?",
                ),
            ],
        },
    ],
}
