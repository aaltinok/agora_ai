/* Türkçe ses: konuşma okuma (TTS) ve konuşma tanıma (STT) — yalnızca tarayıcı API'leri, anahtar gerekmez. */
(function (root) {
  'use strict';
  const fold = (s) => s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLowerCase()
    .replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ç/g, 'c').replace(/ğ/g, 'g')
    .replace(/ö/g, 'o').replace(/ü/g, 'u').replace(/[âîû]/g, (c) => ({ â: 'a', î: 'i', û: 'u' })[c]);

  // Sesli komut anahtar kelimeleri (katlanmış/aksansız). En uzun eşleşme kazanır.
  const KEYWORDS = {
    evet: ['evet', 'tabii', 'tabi', 'kesinlikle', 'elbette', 'olur'],
    hayir: ['hayir', 'yok', 'olmaz', 'degil'],
    kararsizim: ['kararsizim', 'bilmiyorum', 'emin degilim', 'belki', 'bilemiyorum', 'kararsiz'],
    experience: ['yasadigim', 'yasadiklarim', 'deneyim', 'tecrube', 'kendi hayat', 'gozlem'],
    reasoning: ['akil yurut', 'cikarim', 'mantiksal'],
    principle: ['ilke', 'inandigim', 'deger'],
    example: ['ornek', 'somut'],
    heard: ['duydum', 'ogrendim', 'duyduk'],
    unsure: ['emin degilim', 'daha cok dusun', 'dusunmeliyim', 'bilmiyorum'],
    changed: ['degisti', 'degistirdi'],
    same: ['degismedi', 'ayni'],
    undecided: ['karar veremedim', 'henuz', 'bilemiyorum'],
    bilgi: ['bilgelik', 'bilgi'], erdem: ['iyi insan', 'erdem'], adalet: ['adalet'],
    dostluk: ['dostluk', 'dost'], mantik: ['mantik'], siyaset: ['siyaset', 'toplum', 'devlet'], sehir: ['erdemli sehir', 'sehir'],
    akil: ['akil'], ilimler: ['bilimler', 'ilim'], muzik: ['muzik', 'ruh'],
    mutluluk: ['mutluluk', 'mutlu'], 'yapay-zeka': ['yapay zeka', 'yapay', 'makine'],
  };
  const COMMANDS = {
    early: ['konuyu degistir', 'baska konu', 'konu degistir'],
    repeat: ['tekrar', 'bir daha', 'tekrar soyle'],
    stop: ['sus', 'dur', 'sessiz'],
  };

  function matchOption(transcript, options) {
    const t = fold(transcript);
    let best = null, bestLen = 0;
    for (const o of options) {
      for (const k of KEYWORDS[o.id] || []) {
        if (t.includes(k) && k.length > bestLen) { best = o; bestLen = k.length; }
      }
      const lab = fold(o.label);          // etiketin kendisi de söylenebilir
      if (t.includes(lab) && lab.length > bestLen) { best = o; bestLen = lab.length; }
    }
    return best;
  }
  function matchCommand(transcript) {
    const t = fold(transcript);
    for (const [cmd, ks] of Object.entries(COMMANDS)) if (ks.some((k) => t.includes(k))) return cmd;
    return null;
  }

  const synth = root.speechSynthesis || null;
  const Rec = root.SpeechRecognition || root.webkitSpeechRecognition || null;
  const state = { voice: null, enabled: true, rate: 0.95, pitch: 0.8, speaking: false, token: 0 };

  function pickVoice() {
    if (!synth) return;
    const vs = synth.getVoices();
    state.voice = vs.find((v) => v.lang === 'tr-TR') || vs.find((v) => v.lang.toLowerCase().startsWith('tr')) || null;
  }
  if (synth) { pickVoice(); synth.onvoiceschanged = pickVoice; }

  const ttsAvailable = () => !!synth && !!state.voice;

  function stop() {
    state.token += 1; state.speaking = false;
    if (synth) synth.cancel();
  }
  /** Metinleri sırayla okur. onState(true/false): konuşuyor mu. Bitince Promise çözülür. */
  function speakAll(texts, onState) {
    stop();
    const token = state.token;
    return new Promise((resolve) => {
      if (!state.enabled || !ttsAvailable()) { resolve(false); return; }
      let i = 0;
      const next = () => {
        if (token !== state.token || i >= texts.length) { state.speaking = false; onState && onState(false); resolve(token === state.token); return; }
        const u = new root.SpeechSynthesisUtterance(texts[i++]);
        u.lang = 'tr-TR'; u.voice = state.voice; u.rate = state.rate; u.pitch = state.pitch;
        u.onstart = () => { state.speaking = true; onState && onState(true); };
        u.onend = next; u.onerror = next;
        synth.speak(u);
      };
      next();
    });
  }

  let rec = null;
  const sttAvailable = () => !!Rec;
  function listen({ onResult, onError, onEnd }) {
    if (!Rec) { onError && onError('unsupported'); return null; }
    stop();                                  // Sokrates konuşurken mikrofon açılmasın
    rec = new Rec();
    rec.lang = 'tr-TR'; rec.interimResults = false; rec.maxAlternatives = 3; rec.continuous = false;
    rec.onresult = (e) => {
      const alts = Array.from(e.results[0]).map((a) => a.transcript);
      onResult && onResult(alts);
    };
    rec.onerror = (e) => onError && onError(e.error);
    rec.onend = () => onEnd && onEnd();
    try { rec.start(); } catch (err) { onError && onError('start-failed'); }
    return rec;
  }
  function stopListening() { if (rec) { try { rec.stop(); } catch (e) { /* zaten durmuş */ } } }

  const api = { fold, matchOption, matchCommand, speakAll, stop, listen, stopListening, ttsAvailable, sttAvailable, state, KEYWORDS };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.AgoraSpeech = api;
})(typeof window !== 'undefined' ? window : globalThis);
