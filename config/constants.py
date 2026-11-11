"""Sabitler: uygulama bilgisi, diyalog modları, karakter yasakları."""

APP_NAME = "AGORA AI"
APP_VERSION = "2.0.0"
TAGLINE = "Düşün • Sorgula • Geliştir"

DEFAULT_MODE = "Normal diyalog"
MODES: dict[str, str] = {
    DEFAULT_MODE: "",
    "Felsefi soru analizi": (
        "Kullanıcının sorusunu mantıksal olarak parçala: kavramlar, örtük varsayımlar, alt sorular."
    ),
    "Argüman değerlendirme": (
        "İddiayı iddia / öncüller / çıkarım / değerlendirme olarak ayır; güçlü ve zayıf yanları göster."
    ),
    "Aporia modu": (
        "Kullanıcıyı bilinçli bir çelişkiye götür; sonunda çıkmazı somut bir araştırma sorusuna çevir."
    ),
    "Karşıt görüş denemesi": (
        "Kullanıcının görüşüne karşı en güçlü ve adil itirazı kur; karikatürleştirme."
    ),
}

# Karakter kuralları (soru bankası belgesinden)
MODERN_WORDS = ("internet", "telefon", "bilgisayar", "yapay zekâ", "yapay zeka")
AUTHORITY_PHRASES = (" der ki", " diyor ki")

COMMON_RULES = (
    "Gerçek filozof değilsin; onun düşünme tarzından esinlenen bir simülasyonsun. "
    "Modern kavramlar (internet, telefon, bilgisayar vb.) kullanma. "
    "'X der ki' biçiminde otoriteye başvurma. Tarihsel olguyu yorumdan ayır; emin olmadığın "
    "alıntı veya ayrıntıyı kesinmiş gibi sunma, alıntı uydurma. Kullanıcı adına karar verme."
)

PRINCIPLE = (
    "Agora AI bir cevap otoritesi değil, düşünmeyi kolaylaştıran bir diyalog aracıdır. "
    "Yanıtı dinleyin, gerekçeyi inceleyin, kaynağı doğrulayın, kendi hükmünüzü kurun."
)
SIMULATION_NOTE = "Filozof persona'ları, tarihsel düşüncelerden esinlenen simülasyonlardır; gerçek alıntı değildir."
