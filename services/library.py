"""Kütüphane (kavramlar sözlüğü, filozof künyeleri) ve Felsefe Atölyesi planı.

Tarihler ve eser adları standart kaynaklara dayanan kısa künyelerdir; yaklaşık değerler "yaklaşık" ile belirtilmiştir.
"""

from __future__ import annotations

GLOSSARY = {
    "Aporia": "Bir soruda veya argümanda ortaya çıkan düşünsel çıkmaz ya da çözümsüzlük.",
    "Elenkhos": "Sokratik sorgulama yoluyla bir iddianın tutarsızlıklarını sınama yöntemi.",
    "Maieutik": "Soru sorarak kişinin düşüncesini açığa çıkarmasına yardım etme; düşünce ebeliği benzetmesi.",
    "Eidos (idea)": "Platon felsefesinde tek tek örneklerin ötesindeki biçim; bağlama göre dikkatle açıklanmalıdır.",
    "Phronesis": "Aristoteles'te pratik bilgelik; somut durumlarda iyi yargıda bulunma yetisi.",
    "Eudaimonia": "Aristoteles'te mutluluk ya da iyi yaşam; erdemle uyumlu etkinlik.",
    "Saadet": "Farabi'de insanın kendi uğruna istenen en yüksek iyisi; bilgi ve erdemli eylemle kazanılır.",
    "Faal akıl": "Farabi'nin düşüncesinde, insan aklını imkândan gerçek bilgiye geçiren ilke.",
    "Prohairesis": "Epiktetos'ta iradenin seçme gücü; bize bağlı olan şeylerin merkezi.",
    "Argüman": "Bir sonucu desteklemek üzere sunulan öncüller ve çıkarım ilişkisi.",
    "Öncül": "Bir argümanda sonucu desteklemek için kullanılan önerme.",
    "Karşı örnek": "Bir iddianın her durumda geçerli olduğu savını sınayan örnek.",
    "Varsayım": "Açıkça savunulmadan doğru kabul edilen düşünce veya koşul.",
    "Tutarlılık": "İddialar arasında çelişki bulunmaması; tek başına doğruluk garantisi değildir.",
}

PROFILES = {
    "Sokrates": {
        "dönem": "yaklaşık MÖ 470–399, Atina",
        "yöntem": "Elenkhos ve maieutik",
        "kaynak": "Kendisi yazmamıştır; Platon (Savunma, Kriton, Phaidon), Ksenophon ve Aristophanes aracılığıyla bilinir.",
    },
    "Platon": {
        "dönem": "yaklaşık MÖ 428/427–348/347, Atina",
        "yöntem": "Diyalog biçiminde felsefe, diyalektik",
        "kaynak": "Devlet, Şölen, Menon, Phaidon, Timaios; Akademia'yı kurmuştur.",
    },
    "Aristoteles": {
        "dönem": "MÖ 384–322, Stageira ve Atina",
        "yöntem": "Gözlem, sınıflandırma, mantıksal çıkarım",
        "kaynak": "Nikomakhos'a Etik, Politika, Metafizik, Fizik, Poetika ve mantık yazıları (Organon); Lykeion'u kurmuştur.",
    },
    "Epiktetos": {
        "dönem": "yaklaşık MS 50–135, Hierapolis ve Nikopolis",
        "yöntem": "Bize bağlı olan ve olmayanı ayırma",
        "kaynak": "Kendisi yazmamıştır; öğrencisi Arrianos'un derlediği Söylevler ve El Kitabı (Enkheiridion).",
    },
    "Farabi": {
        "dönem": "yaklaşık 870–950, Orta Asya, Bağdat ve Şam",
        "yöntem": "Mantık, ilimlerin sınıflandırılması, uzlaştırma",
        "kaynak": "Erdemli Şehir Halkının Görüşleri, İlimlerin Sayımı, Mutluluğa Ulaşma, Büyük Müzik Kitabı, Akıl Üzerine Risale.",
    },
}


def workshop_plan(topic: str, groups: int, minutes: int) -> str:
    """Rehberdeki Felsefe Atölyesi akışını süreye göre bölen plan (Markdown)."""
    groups = max(2, min(groups, 10))
    unit = max(5, minutes // 5)
    steps = [
        (
            "Ortak soru",
            unit,
            f'Herkese aynı soru verilir: "{topic}" üzerine tek bir ana soru yazılır.',
        ),
        (
            "Gruplar çalışır",
            unit * 2,
            f"{groups} grup, her biri bir filozofun yaklaşımıyla iddia, gerekçe ve karşı örnek geliştirir.",
        ),
        ("Paylaşım", unit, "Gruplar iddia, gerekçe ve karşı örneklerini kısaca sunar."),
        (
            "Değerlendirme",
            unit,
            "Filozof yanıtları değil, katılımcıların argüman kalitesi değerlendirilir (öncüller açık mı, karşı örnek ele alındı mı).",
        ),
        (
            "Kapanış",
            max(5, minutes - unit * 5),
            "Hangi düşüncenin değiştiği ve hangi sorunun açık kaldığı yazılır.",
        ),
    ]
    lines = [f"# Felsefe Atölyesi: {topic}", f"Süre: {minutes} dk, grup sayısı: {groups}", ""]
    lines += [f"{i}. **{t}** ({m} dk): {d}" for i, (t, m, d) in enumerate(steps, 1)]
    return "\n".join(lines)
