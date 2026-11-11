/* Ek dekor: Atina/Lykeion (Dor düzeni, çınar, hermes) ve Abbasi meclisi (sivri kemer, hurma, rahle, usturlap, ud). */
(function (root) {
  'use strict';
  const T = root.THREE, C = root.AgoraCitizens, P = root.AgoraProps;
  const { lamb, add, G } = C, phong = P.phong;
  const rand = (a, b) => a + Math.random() * (b - a);
  const cv = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  const shadowAll = (g) => { g.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };

  function plane(x, z) {            // çınar: açık renkli gövde, geniş taç
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = rand(0, 6);
    add(g, new T.CylinderGeometry(0.28, 0.45, 3.0, 8), lamb(0xb9ae98), 0, 1.5, 0);
    for (let i = 0; i < 6; i++) add(g, new T.IcosahedronGeometry(rand(1.3, 2.0), 0), lamb(i % 2 ? 0x77a24f : 0x6a9544), rand(-1.6, 1.6), rand(3.6, 4.8), rand(-1.6, 1.6));
    return shadowAll(g);
  }
  function well(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); const m = phong(0xd8cdb4);
    add(g, new T.CylinderGeometry(0.75, 0.8, 0.8, 16), m, 0, 0.4, 0);
    add(g, new T.CircleGeometry(0.58, 16), lamb(0x1d2a33), 0, 0.81, 0).rotation.x = -Math.PI / 2;
    return shadowAll(g);
  }
  function herm(x, z, ry) {
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; const m = phong(0xe6dfcb);
    add(g, new T.BoxGeometry(0.38, 1.25, 0.32), m, 0, 0.625, 0); add(g, new T.SphereGeometry(0.17, 10, 8), m, 0, 1.45, 0);
    add(g, new T.ConeGeometry(0.1, 0.2, 8), m, 0, 1.28, 0.1).rotation.x = Math.PI;
    return shadowAll(g);
  }
  function tholos(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z);
    add(g, new T.CylinderGeometry(5, 5.2, 4.6, 18), phong(0xd8cdb0), 0, 2.3, 0);
    add(g, new T.ConeGeometry(5.6, 3, 18), phong(0xb5532f), 0, 6.1, 0);
    add(g, new T.BoxGeometry(1.6, 2.6, 0.4), lamb(0x3a2a1c), 0, 1.3, 5.0);
    return shadowAll(g);
  }
  function altar(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); const m = phong(0xe6dfcb);
    add(g, new T.BoxGeometry(4, 0.35, 4), m, 0, 0.175, 0); add(g, new T.BoxGeometry(3.2, 0.5, 3.2), m, 0, 0.6, 0);
    return shadowAll(g);
  }
  function scrollShelf(x, z, ry) {   // papirüs rulolar için gözlü dolap
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; const wood = lamb(0x7a5638);
    add(g, new T.BoxGeometry(2.4, 0.06, 0.5), wood, 0, 0.03, 0); add(g, new T.BoxGeometry(2.4, 0.06, 0.5), wood, 0, 1.6, 0);
    for (let i = 0; i < 4; i++) add(g, new T.BoxGeometry(0.05, 1.6, 0.5), wood, -1.2 + i * 0.8, 0.8, 0);
    for (let r = 0; r < 3; r++) { add(g, new T.BoxGeometry(2.4, 0.04, 0.5), wood, 0, 0.55 + r * 0.5, 0);
      for (let k = 0; k < 9; k++) add(g, new T.CylinderGeometry(0.045, 0.045, 0.4, 8), lamb(0xe6d9b0), -1.05 + (k % 3) * 0.8 + (k / 3 | 0) * 0.2 - 0.2, 0.34 + r * 0.5, 0.0).rotation.x = Math.PI / 2; }
    return shadowAll(g);
  }

  /* ---- Abbasi mimarisi: sivri kemerli revak, iwan */
  function archWall(w, h, depth, openW, openH, mat) {
    const s = new T.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, h); s.lineTo(-w / 2, h); s.closePath();
    const hole = new T.Path(), a = openH + openW * 0.55;
    hole.moveTo(-openW / 2, 0); hole.lineTo(-openW / 2, openH); hole.quadraticCurveTo(-openW / 2, openH + openW * 0.3, 0, a);
    hole.quadraticCurveTo(openW / 2, openH + openW * 0.3, openW / 2, openH); hole.lineTo(openW / 2, 0); hole.closePath();
    s.holes.push(hole);
    const m = new T.Mesh(new T.ExtrudeGeometry(s, { depth, bevelEnabled: false }), mat); m.position.z = -depth / 2; return m;
  }
  function archRow(n, w, h) {
    const g = new T.Group(), mat = lamb(0xdcc9a0);
    for (let i = 0; i < n; i++) { const b = archWall(w, h, 0.9, w * 0.66, h * 0.52, mat); b.position.x = (i - (n - 1) / 2) * w; g.add(b); }
    add(g, new T.BoxGeometry(n * w + 0.4, 0.3, 1.4), lamb(0xcdb98c), 0, h + 0.15, 0);
    for (let i = 0; i < n * 2; i++) add(g, new T.BoxGeometry(0.5, 0.45, 0.5), mat, (i - (n * 2 - 1) / 2) * (w / 2), h + 0.5, 0);   // parapet
    return shadowAll(g);
  }
  function iwan(w, h) {
    const g = new T.Group(), mat = lamb(0xd8c394);
    g.add(archWall(w, h, 1.2, w * 0.66, h * 0.55, mat));
    add(g, new T.BoxGeometry(w * 0.66, h * 0.8, 4), lamb(0x4a3b2c), 0, h * 0.4, -2.3);
    add(g, new T.CylinderGeometry(w * 0.33, w * 0.33, 4, 14, 1, false, 0, Math.PI), lamb(0x5a4838), 0, h * 0.55, -2.3).rotation.set(Math.PI / 2, 0, Math.PI / 2);
    return shadowAll(g);
  }
  function palm(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); const h = rand(5.5, 7.5);
    const trunk = add(g, new T.CylinderGeometry(0.22, 0.34, h, 8), lamb(0x7a5e3c), 0, h / 2, 0); trunk.rotation.z = rand(-0.05, 0.05);
    const crown = new T.Group(); crown.position.y = h; g.add(crown);
    for (let i = 0; i < 10; i++) { const pv = new T.Group(); pv.rotation.y = i * 0.63; crown.add(pv);
      const f = add(pv, new T.BoxGeometry(2.8, 0.03, 0.35), lamb(i % 2 ? 0x5f8a3c : 0x6c9a45), 1.3, 0, 0); f.rotation.z = -0.35; f.position.y = -0.1; }
    for (let i = 0; i < 6; i++) add(crown, new T.SphereGeometry(0.1, 6, 5), lamb(0x9a5a2a), Math.cos(i) * 0.3, -0.35, Math.sin(i) * 0.3);
    return shadowAll(g);
  }
  function brickTexture() {
    const c = cv(256, 256), g = c.getContext('2d'); g.fillStyle = '#9c7a55'; g.fillRect(0, 0, 256, 256);
    for (let r = 0; r < 16; r++) for (let k = 0; k < 8; k++) { g.fillStyle = `hsl(${28 + rand(-4, 4)},${32 + rand(-5, 5)}%,${50 + rand(-6, 6)}%)`; g.fillRect(k * 32 + (r % 2) * 16, r * 16 + 1, 30, 14); }
    const t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(14, 14); return t;
  }
  function rug(w, d, x, z, c1, c2) {
    const c = cv(256, 384), g = c.getContext('2d'); g.fillStyle = c1; g.fillRect(0, 0, 256, 384);
    g.fillStyle = '#e8dcc0'; g.fillRect(14, 14, 228, 356); g.fillStyle = c2; g.fillRect(28, 28, 200, 328);
    g.fillStyle = '#e8dcc0'; for (let y = 60; y < 340; y += 70) { g.beginPath(); g.moveTo(128, y - 28); g.lineTo(168, y); g.lineTo(128, y + 28); g.lineTo(88, y); g.closePath(); g.fill(); }
    const m = new T.Mesh(new T.PlaneGeometry(w, d), new T.MeshLambertMaterial({ map: new T.CanvasTexture(c) }));
    m.rotation.x = -Math.PI / 2; m.position.set(x, 0.025, z); m.receiveShadow = true; return m;
  }
  const cushion = (x, y, z, color, ry) => { const m = add(new T.Group(), new T.BoxGeometry(0.75, 0.2, 0.75), lamb(color), 0, 0, 0); const g = new T.Group(); g.add(m); g.position.set(x, y + 0.1, z); g.rotation.y = ry || 0; return shadowAll(g); };
  function rahle(x, z, ry) {          // katlanır kitap rahlesi + kodeks (kâğıt)
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; const w = lamb(0x6f4c2e);
    [-1, 1].forEach((s) => add(g, new T.BoxGeometry(0.05, 0.62, 0.34), w, 0, 0.3, 0).rotation.set(0, 0, s * 0.45));
    const b = add(g, new T.BoxGeometry(0.34, 0.03, 0.46), w, 0, 0.5, 0); b.rotation.x = -0.35;
    const cod = add(g, new T.BoxGeometry(0.3, 0.05, 0.4), lamb(0xefe6cf), 0, 0.54, 0.0); cod.rotation.x = -0.35;
    return shadowAll(g);
  }
  function astrolabe(x, y, z) {
    const g = new T.Group(); g.position.set(x, y, z); const br = phong(0xb8903a, { shininess: 60 });
    add(g, new T.CylinderGeometry(0.16, 0.16, 0.014, 28), br, 0, 0, 0).rotation.x = Math.PI / 2;
    add(g, new T.TorusGeometry(0.16, 0.012, 6, 28), br, 0, 0, 0); add(g, new T.TorusGeometry(0.06, 0.008, 6, 20), br, 0, 0.02, 0.01);
    add(g, new T.TorusGeometry(0.03, 0.01, 6, 12), br, 0, 0.19, 0); add(g, new T.BoxGeometry(0.3, 0.015, 0.02), br, 0, 0, 0.012).rotation.z = 0.5;
    return g;
  }
  function oud(x, y, z, ry) {
    const g = new T.Group(); g.position.set(x, y, z); g.rotation.y = ry || 0; const w = lamb(0x8a5a32), d = lamb(0x2a1c14);
    add(g, new T.SphereGeometry(0.22, 14, 10), w, 0, 0.09, 0).scale.set(0.85, 0.42, 1.1);
    add(g, new T.CircleGeometry(0.05, 12), d, 0, 0.2, 0.04).rotation.x = -Math.PI / 2;
    add(g, new T.BoxGeometry(0.06, 0.03, 0.55), lamb(0x3a2a1c), 0, 0.12, -0.5);
    add(g, new T.BoxGeometry(0.09, 0.04, 0.16), w, 0, 0.14, -0.82).rotation.x = 0.35;
    return shadowAll(g);
  }
  function pool(x, z, w, d) {
    const g = new T.Group(); g.position.set(x, 0, z); const m = phong(0xe0d3b4);
    add(g, new T.BoxGeometry(w + 0.8, 0.35, d + 0.8), m, 0, 0.175, 0);
    const water = add(g, new T.PlaneGeometry(w, d), new T.MeshPhongMaterial({ color: 0x4f9fb0, transparent: true, opacity: 0.82, shininess: 90 }), 0, 0.33, 0);
    water.rotation.x = -Math.PI / 2; shadowAll(g); g.userData.water = water; return g;
  }
  function river(scene) {
    const m = new T.Mesh(new T.PlaneGeometry(500, 40), new T.MeshLambertMaterial({ color: 0x5b8fa3 })); m.rotation.x = -Math.PI / 2; m.position.set(0, 0.03, -78); scene.add(m);
  }
  Object.assign(P, { plane, well, herm, tholos, altar, scrollShelf, archWall, archRow, iwan, palm, brickTexture, rug, cushion, rahle, astrolabe, oud, pool, river });
})(window);
