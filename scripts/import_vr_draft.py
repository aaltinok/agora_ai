"""VR etkinlik taslağı (.docx) → diyalog JSON + soru-cevap bankası dönüştürücü.

Kullanım:  python scripts/import_vr_draft.py "VR_ETKINLIK_TASLAGI.docx"
Word belgesini düzenleyip komutu yeniden çalıştırmak yeterlidir (python-docx gerekir).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "dialogues" / "sokrates.json"
OUT_QA = ROOT / "data" / "texts" / "qa_sokrates_vr.md"

TOPICS = {  # belgedeki başlık → (id, menü etiketi, görünen başlık); sıra menü sırasıdır
    "BİLGİ VE BİLGELİK": ("bilgi", "Bilgi", "Bilgi ve Bilgelik"),
    "ERDEM VE İYİ İNSAN": ("erdem", "Erdem", "Erdem ve İyi İnsan"),
    "ADALET": ("adalet", "Adalet", "Adalet"),
    "MUTLULUK": ("mutluluk", "Mutluluk", "Mutluluk"),
    "YAPAY ZEKÂ VE DÜŞÜNME": ("yapay-zeka", "Yapay Zekâ", "Yapay Zekâ ve Düşünme"),
}
STANCES = {"Evet": "evet", "Hayır": "hayir", "Kararsızım": "kararsizim"}
REFLECTION_OPTIONS = [
    {"id": "changed", "label": "Düşüncem değişti"},
    {"id": "same", "label": "Düşüncem değişmedi"},
    {"id": "undecided", "label": "Henüz karar veremedim"},
]
# --- Belgede yazılı OLMAYAN, taslak olarak eklenen içerik (öğretmen gözden geçirmeli) ---
AUTHORED_REASONS = [
    {
        "id": "experience",
        "label": "Kendi yaşadıklarıma dayanıyor",
        "reply": "Kendi deneyiminden yola çıkman değerli. Peki, başka birinin yaşadıkları farklı olsaydı o da aynı sonuca varır mıydı?",
    },
    {
        "id": "example",
        "label": "Aklımda somut bir örnek var",
        "reply": "Örnekler düşünmeyi somutlaştırır. Bu örnek her durum için geçerli mi, yoksa yalnızca belirli bir durum için mi?",
    },
    {
        "id": "heard",
        "label": "Böyle duydum ya da öğrendim",
        "reply": "Duyduklarımızı hemen reddetmemize gerek yok, ama onları sınamadan da benimsemeyelim. Bu düşünceyi kendi sözlerinle gerekçelendirmeyi dener misin?",
    },
    {
        "id": "unsure",
        "label": "Emin değilim, daha çok düşünmeliyim",
        "reply": "Bunu söylemek cesaret ister; bilmediğimizi fark etmek araştırmanın başlangıcıdır. Gel, daha basit bir örnekten ilerleyelim.",
    },
]
AUTHORED_BRIDGES = ["Şimdi konuya başka bir yönden bakalım.", "Bu bizi yeni bir soruya götürüyor."]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2019", "'").replace("\t", " ")).strip()


def unquote(text: str) -> str:
    return clean(text).strip('"“”').strip()


def read_paragraphs(path: Path) -> list[str]:
    return [clean(p.text) for p in docx.Document(str(path)).paragraphs]


def index_of(ps: list[str], pred, start: int = 0) -> int:
    for i in range(start, len(ps)):
        if pred(ps[i]):
            return i
    raise ValueError("Belgede beklenen bölüm bulunamadı.")


def parse_qa(ps: list[str], end: int) -> list[dict]:
    qa, section = [], ""
    for i, t in enumerate(ps[:end]):
        if m := re.match(r"^([A-E])\. (.+)$", t):
            section = m.group(2)
        elif (
            (m := re.match(r"^(\d+)\. (.+\?)$", t))
            and i + 1 < end
            and ps[i + 1].startswith("Sokrates:")
        ):
            qa.append(
                {
                    "question": m.group(2),
                    "answer": unquote(ps[i + 1][len("Sokrates:") :]),
                    "section": section,
                    "hypothetical": section.startswith("Sokrates Günümüzde"),
                }
            )
    return qa


def parse_topics(ps: list[str], start: int, end: int) -> list[dict]:
    heads = [i for i in range(start, end) if ps[i].endswith(" DİYALOĞU") and ps[i][:-9] in TOPICS]
    topics = []
    for n, h in enumerate(heads):
        stop = heads[n + 1] if n + 1 < len(heads) else end
        title = ps[h][: -len(" DİYALOĞU")]
        tid, menu, display = TOPICS[title]
        first_q = index_of(ps, lambda t: re.match(r"^\d+\. Soru:", t) is not None, h)
        opening = " ".join(
            unquote(t)
            for t in ps[h + 1 : first_q]
            if t and t not in ("Sokrates:", "Sokrates'in açılışı:")
        )
        questions, i = [], first_q
        while i < stop:
            if m := re.match(r"^(\d+)\. Soru:\s*(.+)$", ps[i]):
                branches, j = {}, i + 1
                while j < stop and not re.match(r"^\d+\. Soru:|^Kapanış", ps[j]):
                    if b := re.match(r"^(Evet|Hayır|Kararsızım):\s*(.+)$", ps[j]):
                        branches[STANCES[b.group(1)]] = unquote(b.group(2))
                    j += 1
                questions.append(
                    {"id": f"{tid}-{m.group(1)}", "text": m.group(2), "branches": branches}
                )
                i = j
            elif ps[i].startswith("Kapanış"):
                break
            else:
                i += 1
        closing = unquote(ps[index_of(ps, lambda t: t.startswith("Kapanış"), first_q) + 1])
        topics.append(
            {
                "id": tid,
                "menu": menu,
                "title": display,
                "opening": opening,
                "questions": questions,
                "closing": closing,
            }
        )
    order = [v[0] for v in TOPICS.values()]
    return sorted(topics, key=lambda t: order.index(t["id"]))


def build(path: Path) -> tuple[dict, list[dict]]:
    ps = read_paragraphs(path)
    pool_end = index_of(ps, lambda t: t.startswith("Öğrencinin Sokrates'in cevabına"))
    vr = index_of(ps, lambda t: t == "VR DENEYİMİNİN TASLAK SENARYOSU")
    flow = index_of(ps, lambda t: t.startswith("VR UYGULAMASINDA SORULAR"))
    w = index_of(ps, lambda t: t == "Sokrates:", vr) + 1
    welcome = []
    while True:
        welcome.append(unquote(ps[w]))
        if ps[w].endswith('"'):
            break
        w += 1
    tail = [
        t
        for t in ps[pool_end + 1 : vr]
        if t
        and not t.startswith("Ayrı bir soru havuzunu")
        and not t.startswith("Ayrı bir soru havuzunda")
    ]
    student_q = [t for t in tail if not t.startswith('"')]
    sok_lines = [unquote(t) for t in tail if t.startswith('"')]
    refl_q = unquote(ps[index_of(ps, lambda t: "konuşmamızın başındaki düşüncenle" in t, flow)])
    final = unquote(ps[index_of(ps, lambda t: t.startswith('"Önemli olan benimle'), flow)])
    bridges = [
        s for s in sok_lines if s.startswith(("Söylediklerini biraz", "Öyleyse bu konuda"))
    ] + AUTHORED_BRIDGES
    script = {
        "version": 1,
        "title": "Sokrates'le Yüz Yüze",
        "source": path.name,
        "welcome": " ".join(welcome),
        "topics": parse_topics(ps, vr, flow),
        "reason_prompt": "Neden böyle düşünüyorsun?",
        "reflection": {"question": refl_q, "options": REFLECTION_OPTIONS, "final": final},
        "student_questions": student_q,
        "sokrates_lines": sok_lines,
        "bridges": bridges,
        "reasons": AUTHORED_REASONS,
        "authored_note": "reasons ve bridges içindeki son iki satır belgede yoktur; taslak olarak eklenmiştir, gözden geçirin.",
    }
    return script, parse_qa(ps, pool_end)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    from scripts.build_dialogues import augment_sokrates

    script, qa = build(Path(argv[1]))
    script = augment_sokrates(script)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Sokrates VR taslağı — soru havuzu (import_vr_draft.py ile üretildi; elle düzenlemeyin)",
        "",
    ]
    for n, e in enumerate(qa, 1):
        lines += [f'{n}. "{e["question"]}"', f'Sokrates: "{e["answer"]}"', ""]
    OUT_QA.write_text("\n".join(lines), encoding="utf-8")
    nq = sum(len(t["questions"]) for t in script["topics"])
    print(
        f"{len(script['topics'])} konu, {nq} soru, {len(qa)} soru-cevap → {OUT_JSON.name}, {OUT_QA.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
