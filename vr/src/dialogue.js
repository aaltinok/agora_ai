/* Diyalog durum makinesi — services/dialogue.py ile birebir aynı mantık (parite testi var). */
(function (root) {
  'use strict';
  const STANCES = [['evet', 'Evet'], ['hayir', 'Hayır'], ['kararsizim', 'Kararsızım']];

  function fromJSON(data) {
    const topics = {};
    for (const t of data.topics) {
      if (!t.questions.length || !t.opening || !t.closing) throw new Error(t.id + ': eksik alan');
      for (const q of t.questions) {
        const ok = STANCES.every(([k]) => q.branches[k]);
        if (!ok) throw new Error(q.id + ': dallar eksik');
      }
      topics[t.id] = t;
    }
    return {
      id: data.id, philosopher: data.philosopher, scene: data.scene, title: data.title, setting: data.setting,
      disclaimer: data.disclaimer, welcome: data.welcome, topics, order: data.topics.map((t) => t.id),
      reasonPrompt: data.reason_prompt, reasons: data.reasons, bridges: data.bridges,
      reflection: data.reflection,
    };
  }
  const say = (s, who, text) => s.log.push({ who, text });

  function newState(script, topicId) {
    const topic = script.topics[topicId];
    if (!topic) throw new Error('Bilinmeyen konu');
    const s = { topic: topicId, q: 0, phase: 'stance', log: [], answers: [], bridge: 0, reflection: '' };
    say(s, 'philosopher', topic.opening);
    say(s, 'philosopher', topic.questions[0].text);
    return s;
  }
  function options(script, s) {
    if (s.phase === 'stance') return STANCES.map(([id, label]) => ({ id, label }));
    if (s.phase === 'reason') return script.reasons.map((r) => ({ id: r.id, label: r.label }));
    if (s.phase === 'reflection') return script.reflection.options.map((o) => ({ id: o.id, label: o.label }));
    return [];
  }
  function close(script, s) {
    say(s, 'philosopher', script.topics[s.topic].closing);
    say(s, 'philosopher', script.reflection.question);
    s.phase = 'reflection';
  }
  function choose(script, s, optionId) {
    const opt = options(script, s).find((o) => o.id === optionId);
    if (!opt) throw new Error('Bu adımda geçersiz seçim');
    const topic = script.topics[s.topic];
    const question = topic.questions[s.q];
    say(s, 'student', opt.label);
    if (s.phase === 'stance') {
      s.answers.push({ question: question.text, stance: opt.label, reason: '' });
      say(s, 'philosopher', question.branches[optionId]);
      say(s, 'philosopher', script.reasonPrompt);
      s.phase = 'reason';
    } else if (s.phase === 'reason') {
      s.answers[s.answers.length - 1].reason = opt.label;
      say(s, 'philosopher', script.reasons.find((r) => r.id === optionId).reply);
      if (s.q + 1 < topic.questions.length) {
        say(s, 'philosopher', script.bridges[s.bridge % script.bridges.length]);
        s.bridge += 1; s.q += 1;
        say(s, 'philosopher', topic.questions[s.q].text);
        s.phase = 'stance';
      } else close(script, s);
    } else {
      s.reflection = opt.label;
      say(s, 'philosopher', script.reflection.final);
      s.phase = 'done';
    }
    return s;
  }
  function finishEarly(script, s) {
    if (s.phase === 'stance' || s.phase === 'reason') {
      say(s, 'student', 'Konuyu değiştirmek istiyorum.');
      const last = s.answers[s.answers.length - 1];
      if (s.phase === 'reason' && last && !last.reason) last.reason = '(gerekçe verilmedi)';
      if (s.answers.length) close(script, s);
      else { say(s, 'philosopher', script.reflection.final); s.phase = 'done'; }
    }
    return s;
  }
  function summaryMarkdown(script, s) {
    const lines = ['# ' + script.title + ' — ' + script.topics[s.topic].title, ''];
    s.answers.forEach((a, i) => lines.push(`**${i + 1}. ${a.question}**`, `- Seçim: ${a.stance}`, `- Gerekçe: ${a.reason || '—'}`, ''));
    lines.push('**Düşünce değişimi:** ' + (s.reflection || '—'));
    return lines.join('\n');
  }
  const api = { fromJSON, newState, options, choose, finishEarly, summaryMarkdown, STANCES };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.AgoraDialogue = api;
})(typeof window !== 'undefined' ? window : globalThis);
