/* Uygulama: senaryo seçimi + 3B sahne + diyalog + ses + masaüstü paneli + VR paneli. */
(function () {
  'use strict';
  const D = window.AgoraDialogue, S = window.AgoraSpeech, T = window.THREE;
  const $ = (id) => document.getElementById(id);
  const raw = window.AGORA_SCRIPTS;
  const ORDER = ['sokrates', 'aristoteles', 'farabi'].filter((k) => raw[k]);
  const scripts = {};
  ORDER.forEach((k) => { scripts[k] = D.fromJSON(raw[k]); });

  const renderer = new T.WebGLRenderer({ canvas: $('c'), antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.xr.enabled = true;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = T.PCFSoftShadowMap;
  const lite = /[?&]lite\b/.test(window.location.search);

  let curId = ORDER[0], script = scripts[curId], world = null, scene = null, camera = null, phil = null;
  let dstate = null, mark = 0, notice = '';
  const talkFallback = { until: 0 };

  /* ------------------------------------------------------------ VR paneli (ortak nesne) */
  const PW = 1024, PH = 768;
  const pc = document.createElement('canvas'); pc.width = PW; pc.height = PH;
  const pctx = pc.getContext('2d'); const ptex = new T.CanvasTexture(pc);
  const panel = new T.Mesh(new T.PlaneGeometry(1.3, 0.975), new T.MeshBasicMaterial({ map: ptex, transparent: true }));
  panel.position.set(0, 0.95, -0.9); panel.rotation.x = -0.55; panel.visible = false;
  const controllers = [0, 1].map((i) => {
    const c = renderer.xr.getController(i);
    c.add(new T.Line(new T.BufferGeometry().setFromPoints([new T.Vector3(), new T.Vector3(0, 0, -2)]), new T.LineBasicMaterial({ color: 0x9fb8ff })));
    c.addEventListener('selectstart', () => {
      const k = panelHit(c); if (k < 0) return;
      const id = hits[k].id; if (id === '__early') early(); else choose(id);
    });
    return c;
  });

  function loadWorld(id) {
    S.stop(); curId = id; script = scripts[id]; dstate = null; mark = 0; notice = '';
    world = window.AgoraScenes.build(script.scene); scene = world.scene; camera = world.camera; phil = world.philosopher;
    scene.add(panel); controllers.forEach((c) => scene.add(c));
    if (lite || renderer.xr.isPresenting) world.setXR(true);
    resize(); refresh(false);
    document.querySelectorAll('#who button').forEach((b) => b.classList.toggle('on', b.dataset.id === id));
    $('title').textContent = script.title; $('setting').textContent = script.setting + '. ' + script.disclaimer;
  }

  /* ----------------------------------------------------------- diyalog görünümü */
  const topicOptions = () => script.order.map((id) => ({ id, label: script.topics[id].menu }));
  function view() {
    if (!dstate) return { title: '', text: script.welcome, options: topicOptions(), early: false, done: false, lines: [script.welcome] };
    const lines = dstate.log.slice(mark).filter((l) => l.who === 'philosopher').map((l) => l.text);
    const done = dstate.phase === 'done';
    return {
      title: script.topics[dstate.topic].title, text: lines.join('\n\n'), lines, done,
      options: done ? [{ id: '__new', label: 'Yeni konu seç' }] : D.options(script, dstate),
      early: dstate.phase === 'stance' || dstate.phase === 'reason',
    };
  }
  function choose(id) {
    if (!dstate) { dstate = D.newState(script, id); mark = 0; }
    else if (id === '__new') { dstate = null; mark = 0; }
    else { mark = dstate.log.length; D.choose(script, dstate, id); }
    notice = ''; refresh(true);
  }
  function early() { if (dstate) { mark = dstate.log.length; D.finishEarly(script, dstate); notice = ''; refresh(true); } }

  /* ----------------------------------------------------------------- HUD */
  function drawHud(v) {
    $('topic').textContent = v.title;
    $('subtitle').textContent = v.text;
    const box = $('options'); box.textContent = '';
    v.options.forEach((o) => { const b = document.createElement('button'); b.textContent = o.label; b.onclick = () => choose(o.id); box.appendChild(b); });
    $('early').hidden = !v.early; $('note').textContent = notice; $('dl').hidden = !(dstate && dstate.phase === 'done');
  }
  $('early').onclick = early;
  $('dl').onclick = () => {
    const blob = new Blob([D.summaryMarkdown(script, dstate)], { type: 'text/markdown' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'yuz_yuze_ozet.md'; a.click();
  };
  ORDER.forEach((id) => {
    const b = document.createElement('button'); b.textContent = scripts[id].philosopher; b.dataset.id = id; b.onclick = () => loadWorld(id); $('who').appendChild(b);
  });

  /* ----------------------------------------------------------------- ses */
  function speak(lines) {
    talkFallback.until = performance.now() + lines.join(' ').length * 55;
    S.speakAll(lines, (on) => { if (phil) phil.talking = on; });
  }
  function setTts(on) { S.state.enabled = on; $('tts').textContent = on ? 'Ses: Açık' : 'Ses: Kapalı'; if (!on) S.stop(); }
  $('tts').onclick = () => setTts(!S.state.enabled);
  $('stop').onclick = () => { S.stop(); if (phil) phil.talking = false; talkFallback.until = 0; };
  if (!S.ttsAvailable()) $('tts').title = 'Bu cihazda Türkçe ses bulunamadı; yalnızca altyazı gösterilir.';
  const mic = $('mic');
  if (!S.sttAvailable()) { mic.disabled = true; mic.title = 'Bu tarayıcıda ses tanıma yok (Chrome veya Edge önerilir). Düğmeleri kullan.'; }
  function onTranscript(alts) {
    const v = view();
    for (const a of alts) {
      const cmd = S.matchCommand(a);
      if (cmd === 'stop') { $('stop').click(); return; }
      if (cmd === 'early' && v.early) { early(); return; }
      if (cmd === 'repeat') { speak(v.lines); return; }
      const opt = S.matchOption(a, v.options);
      if (opt) { choose(opt.id); return; }
    }
    notice = 'Anlayamadım: “' + alts[0] + '”. Tekrar söyler misin?'; $('note').textContent = notice; drawVrPanel();
  }
  mic.onclick = () => {
    mic.classList.add('on'); mic.textContent = 'Dinliyorum...';
    S.listen({
      onResult: onTranscript,
      onError: (e) => { notice = e === 'not-allowed' ? 'Mikrofon izni verilmedi.' : 'Ses tanınamadı (' + e + ').'; $('note').textContent = notice; },
      onEnd: () => { mic.classList.remove('on'); mic.textContent = 'Konuş'; },
    });
  };

  /* ------------------------------------------------------------ VR paneli çizimi */
  let hits = [], hover = -1;
  function wrap(ctx, text, x, y, maxW, lh, maxY) {
    for (const para of text.split('\n')) {
      let line = '';
      for (const w of para.split(' ')) {
        const test = line ? line + ' ' + w : w;
        if (ctx.measureText(test).width > maxW && line) { ctx.fillText(line, x, y); y += lh; line = w; } else line = test;
        if (y > maxY) return;
      }
      ctx.fillText(line, x, y); y += lh * 1.5;
    }
  }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function drawVrPanel() {
    const v = view(); const c = pctx;
    c.clearRect(0, 0, PW, PH); c.fillStyle = 'rgba(11,23,48,.94)'; rr(c, 0, 0, PW, PH, 36); c.fill();
    c.fillStyle = '#9fb8ff'; c.font = 'bold 30px sans-serif'; c.fillText(v.title || script.title, 36, 56);
    c.fillStyle = '#fff'; c.font = '34px sans-serif'; wrap(c, v.text, 36, 112, PW - 72, 44, 430);
    const opts = v.options.slice(); if (v.early) opts.push({ id: '__early', label: 'Konuyu değiştirmek istiyorum' });
    hits = []; const bh = 64, gap = 12; let y = PH - 36 - opts.length * (bh + gap) + gap;
    opts.forEach((o, i) => {
      c.fillStyle = i === hover ? '#4f8cff' : '#24407a'; rr(c, 36, y, PW - 72, bh, 18); c.fill();
      c.fillStyle = '#fff'; c.font = '30px sans-serif'; c.fillText(o.label, 64, y + 43);
      hits.push({ id: o.id, x: 36, y, w: PW - 72, h: bh }); y += bh + gap;
    });
    ptex.needsUpdate = true;
  }
  const ray = new T.Raycaster(), tmpM = new T.Matrix4();
  function panelHit(ctrl) {
    tmpM.identity().extractRotation(ctrl.matrixWorld);
    ray.ray.origin.setFromMatrixPosition(ctrl.matrixWorld); ray.ray.direction.set(0, 0, -1).applyMatrix4(tmpM);
    const h = ray.intersectObject(panel)[0]; if (!h || !h.uv) return -1;
    const px = h.uv.x * PW, py = (1 - h.uv.y) * PH;
    return hits.findIndex((b) => px >= b.x && px <= b.x + b.w && py >= b.y && py <= b.y + b.h);
  }
  function refresh(doSpeak) { const v = view(); drawHud(v); drawVrPanel(); if (doSpeak) speak(v.lines); }

  /* ----------------------------------------------- masaüstü bakış (sürükle) */
  let yaw = 0, pitch = -0.16, drag = null;
  const cv = $('c');
  cv.addEventListener('pointerdown', (e) => { drag = { x: e.clientX, y: e.clientY }; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointerup', () => { drag = null; });
  cv.addEventListener('pointermove', (e) => {
    if (!drag || renderer.xr.isPresenting) return;
    yaw -= (e.clientX - drag.x) * 0.005; pitch = Math.max(-0.8, Math.min(0.8, pitch - (e.clientY - drag.y) * 0.005));
    drag = { x: e.clientX, y: e.clientY };
  });
  function resize() { renderer.setSize(window.innerWidth, window.innerHeight); if (camera) { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); } }
  window.addEventListener('resize', resize);

  /* -------------------------------------------------------------- VR girişi */
  const vrBtn = $('vrBtn'); let session = null;
  if (navigator.xr && navigator.xr.isSessionSupported) navigator.xr.isSessionSupported('immersive-vr').then((ok) => { vrBtn.hidden = !ok; }).catch(() => {});
  vrBtn.onclick = async () => {
    if (session) { session.end(); return; }
    try {
      session = await navigator.xr.requestSession('immersive-vr', { optionalFeatures: ['local-floor', 'bounded-floor'] });
      renderer.xr.setReferenceSpaceType('local-floor'); await renderer.xr.setSession(session);
      world.setXR(true); panel.visible = true; $('hud').style.display = 'none'; vrBtn.textContent = 'VR’den çık';
      session.addEventListener('end', () => { session = null; if (!lite) world.setXR(false); panel.visible = false; $('hud').style.display = ''; vrBtn.textContent = 'VR’ye gir'; });
      drawVrPanel();
    } catch (err) { notice = 'VR başlatılamadı: ' + err.message; $('note').textContent = notice; }
  };

  /* ------------------------------------------------------------------ döngü */
  const clock = new T.Clock();
  renderer.setAnimationLoop(() => {
    const dt = Math.min(clock.getDelta(), 0.1), t = clock.elapsedTime;
    if (!renderer.xr.isPresenting) camera.rotation.set(pitch, yaw, 0, 'YXZ');
    if (!S.state.speaking) phil.talking = performance.now() < talkFallback.until;
    world.update(dt, t);
    if (renderer.xr.isPresenting) {
      const h = controllers.map(panelHit).find((i) => i >= 0); const nh = h === undefined ? -1 : h;
      if (nh !== hover) { hover = nh; drawVrPanel(); }
    }
    renderer.render(scene, camera);
  });

  loadWorld(curId);
  window.AGORA = { choose, early, view, load: loadWorld, state: () => dstate, scripts, speech: S, matchOption: S.matchOption, renderer, panel, look: (y, p) => { yaw = y; pitch = p; } };
})();
