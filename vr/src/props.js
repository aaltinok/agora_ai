/* Agora dekoru: döşeme, çeşme, heykeller, tezgâh, ağaçlar, bulutlar, kuşlar, uzak şehir. */
(function (root) {
  'use strict';
  const T = root.THREE;
  const C = root.AgoraCitizens;
  const { lamb, add, G } = C;
  const rand = (a, b) => a + Math.random() * (b - a);
  const phong = (color, o) => new T.MeshPhongMaterial(Object.assign({ color, shininess: 6, flatShading: true }, o || {}));
  const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

  function plazaTexture() {
    const S = 1024, c = canvas(S, S), g = c.getContext('2d');
    g.fillStyle = '#e8e0cc'; g.fillRect(0, 0, S, S);
    const n = 10, cell = (S - 128) / n;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const l = 88 + rand(-3, 3);
      g.fillStyle = `hsl(40,22%,${l}%)`; g.fillRect(64 + i * cell, 64 + j * cell, cell, cell);
      g.strokeStyle = 'rgba(120,100,70,.5)'; g.lineWidth = 2; g.strokeRect(64 + i * cell, 64 + j * cell, cell, cell);
      g.strokeStyle = 'rgba(150,130,100,.18)'; g.lineWidth = 1;
      for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(64 + i * cell + rand(0, cell), 64 + j * cell); g.bezierCurveTo(64 + i * cell + rand(0, cell), 64 + j * cell + 30, 64 + i * cell + rand(0, cell), 64 + j * cell + 70, 64 + i * cell + rand(0, cell), 64 + j * cell + cell); g.stroke(); }
    }
    g.fillStyle = '#234a7c'; g.fillRect(0, 0, S, 64); g.fillRect(0, S - 64, S, 64); g.fillRect(0, 0, 64, S); g.fillRect(S - 64, 0, 64, S);
    g.strokeStyle = '#d6b25a'; g.lineWidth = 5; g.lineJoin = 'miter';
    const key = () => { g.beginPath(); g.moveTo(4, 56); g.lineTo(4, 8); g.lineTo(52, 8); g.lineTo(52, 40); g.lineTo(20, 40); g.lineTo(20, 24); g.lineTo(36, 24); g.stroke(); };
    for (let side = 0; side < 4; side++) {
      g.save(); g.translate(side === 1 || side === 2 ? S : 0, side >= 2 ? S : 0); g.rotate(side * Math.PI / 2);
      for (let x = 0; x < S; x += 56) { g.save(); g.translate(x, 0); key(); g.restore(); }
      g.restore();
    }
    const t = new T.CanvasTexture(c); t.anisotropy = 8; return t;
  }
  function groundTexture() {
    const c = canvas(256, 256), g = c.getContext('2d');
    g.fillStyle = '#b9a276'; g.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 2200; i++) { g.fillStyle = `rgba(${100 + rand(0, 70) | 0},${85 + rand(0, 55) | 0},${55 + rand(0, 40) | 0},.22)`; g.fillRect(rand(0, 256), rand(0, 256), rand(1, 5), rand(1, 4)); }
    const t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(30, 30); return t;
  }

  const amphoraGeo = () => G('amphora', () => new T.LatheGeometry([[0.001, 0], [0.12, 0.05], [0.2, 0.28], [0.17, 0.5], [0.08, 0.62], [0.09, 0.72], [0.13, 0.76], [0.13, 0.78], [0.001, 0.78]].map(([x, y]) => new T.Vector2(x, y)), 12));
  function amphora(color, x, y, z, s) {
    const m = add(new T.Group(), amphoraGeo(), lamb(color || 0xb5553f), 0, 0, 0); const g = new T.Group(); g.add(m);
    g.position.set(x, y, z); g.scale.setScalar(s || 1); g.traverse((o) => { if (o.isMesh) o.castShadow = true; }); return g;
  }
  function bench(x, z, ry) {
    const g = new T.Group(); const m = phong(0xe6dfcb);
    add(g, new T.BoxGeometry(1.7, 0.1, 0.55), m, 0, 0.44, 0); add(g, new T.BoxGeometry(0.15, 0.4, 0.5), m, -0.7, 0.2, 0); add(g, new T.BoxGeometry(0.15, 0.4, 0.5), m, 0.7, 0.2, 0);
    g.position.set(x, 0, z); g.rotation.y = ry || 0; g.traverse((o) => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } }); return g;
  }
  function fountain(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); const m = phong(0xeee7d3);
    add(g, new T.CylinderGeometry(2.1, 2.2, 0.55, 24), m, 0, 0.275, 0);
    const water = add(g, new T.CircleGeometry(1.9, 24), new T.MeshPhongMaterial({ color: 0x5fb4d6, transparent: true, opacity: 0.78, shininess: 80 }), 0, 0.5, 0);
    water.rotation.x = -Math.PI / 2;
    add(g, new T.CylinderGeometry(0.25, 0.35, 1.5, 12), m, 0, 1.0, 0);
    add(g, new T.CylinderGeometry(0.8, 0.3, 0.2, 16), m, 0, 1.75, 0);
    const jet = add(g, new T.ConeGeometry(0.16, 0.9, 10), new T.MeshBasicMaterial({ color: 0xbfe9ff, transparent: true, opacity: 0.6 }), 0, 2.3, 0);
    g.traverse((o) => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } });
    return { group: g, update: (t) => { water.scale.setScalar(1 + Math.sin(t * 2) * 0.01); jet.scale.y = 1 + Math.sin(t * 5) * 0.12; jet.position.y = 2.3 + Math.sin(t * 5) * 0.05; } };
  }
  function statue(x, z, ry) {
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; const pm = phong(0xd9d2bf);
    add(g, new T.BoxGeometry(1.0, 0.25, 1.0), pm, 0, 0.125, 0); add(g, new T.BoxGeometry(0.75, 1.1, 0.75), pm, 0, 0.8, 0);
    const c = C.makeCitizen({ skin: 0xe9e4d6, cloth: 0xe4ded0, trim: 0xe4ded0, hair: 0xd8d2c4, beard: Math.random() < 0.6, cloak: 0xdcd6c6, height: 1.05 });
    c.group.position.y = 1.35; c.arms[1].sh.rotation.set(-0.5, 0, -0.1); c.arms[1].el.rotation.x = -0.9; g.add(c.group);
    g.traverse((o) => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } }); return g;
  }
  function brazier(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); const m = phong(0x3a3430);
    for (let i = 0; i < 3; i++) { const l = add(g, new T.CylinderGeometry(0.03, 0.03, 1.1, 5), m, Math.cos(i * 2.1) * 0.22, 0.52, Math.sin(i * 2.1) * 0.22); l.rotation.set(Math.sin(i * 2.1) * 0.2, 0, -Math.cos(i * 2.1) * 0.2); }
    add(g, new T.CylinderGeometry(0.4, 0.22, 0.2, 12), m, 0, 1.1, 0);
    const flame = add(g, new T.ConeGeometry(0.22, 0.6, 8), new T.MeshBasicMaterial({ color: 0xff8a2a }), 0, 1.5, 0);
    const core = add(g, new T.ConeGeometry(0.12, 0.4, 8), new T.MeshBasicMaterial({ color: 0xffd35a }), 0, 1.45, 0);
    return { group: g, update: (t) => { const f = 1 + Math.sin(t * 13 + x) * 0.18 + Math.sin(t * 7.3) * 0.1; flame.scale.set(1 / f, f, 1 / f); core.scale.set(1 / f, f * 1.1, 1 / f); } };
  }
  function stall(x, z, ry) {
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = ry || 0; const wood = lamb(0x7a5638);
    add(g, new T.BoxGeometry(2.2, 0.08, 0.9), wood, 0, 0.9, 0); add(g, new T.BoxGeometry(2.1, 0.85, 0.8), wood, 0, 0.45, 0);
    [-1, 1].forEach((sx) => [-1, 1].forEach((sz) => add(g, new T.CylinderGeometry(0.04, 0.04, 2.4, 6), wood, sx * 1.1, 1.2, sz * 0.5)));
    const shade = add(g, new T.BoxGeometry(2.6, 0.04, 1.5), lamb(0xece3cd), 0, 2.4, 0); shade.rotation.x = 0.1;      // düz keten güneşlik
    [0x6b2f54, 0xb5342b, 0x6b2f54, 0xb5342b, 0x8a9a4a].forEach((c, i) => add(g, new T.SphereGeometry(0.085, 8, 6), lamb(c), -0.7 + i * 0.16, 1.0, 0.05)); // incir, nar, üzüm
    g.add(amphora(0xb5553f, 0.7, 0.94, 0, 0.5), amphora(0x8d4a2b, 0.95, 0.94, 0.12, 0.45), amphora(0xc9703f, 1.2, 0, 0.55, 1.1), amphora(0xa94a2f, -1.3, 0, 0.6, 1.2));
    g.traverse((o) => { if (o.isMesh) { o.castShadow = true; } }); return g;
  }
  function olive(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z); g.rotation.y = rand(0, 6);
    const trunk = add(g, new T.CylinderGeometry(0.1, 0.22, 1.7, 7), lamb(0x6d5a43), 0, 0.85, 0); trunk.rotation.z = 0.12;
    add(g, new T.CylinderGeometry(0.07, 0.1, 1.0, 6), lamb(0x6d5a43), 0.25, 1.9, 0).rotation.z = -0.6;
    for (let i = 0; i < 6; i++) add(g, new T.IcosahedronGeometry(rand(0.6, 0.95), 0), lamb(i % 2 ? 0x8aa468 : 0x6f8f55), rand(-0.9, 0.9), rand(1.9, 2.7), rand(-0.9, 0.9));
    g.traverse((o) => { if (o.isMesh) o.castShadow = true; }); return g;
  }
  function cypress(x, z) {
    const g = new T.Group(); g.position.set(x, 0, z);
    add(g, new T.CylinderGeometry(0.1, 0.14, 0.8, 6), lamb(0x5a4632), 0, 0.4, 0);
    add(g, new T.ConeGeometry(0.75, 5.2, 8), lamb(0x35552f), 0, 3.2, 0);
    g.traverse((o) => { if (o.isMesh) o.castShadow = true; }); return g;
  }

  function sky(scene, sunDir) {
    const c = canvas(4, 256), g = c.getContext('2d'), grd = g.createLinearGradient(0, 0, 0, 256);
    grd.addColorStop(0, '#2f6bb8'); grd.addColorStop(0.5, '#8fc0ee'); grd.addColorStop(1, '#f6e8c8');
    g.fillStyle = grd; g.fillRect(0, 0, 4, 256);
    scene.add(new T.Mesh(new T.SphereGeometry(190, 24, 16), new T.MeshBasicMaterial({ map: new T.CanvasTexture(c), side: T.BackSide, fog: false })));
    const gc = canvas(128, 128), gg = gc.getContext('2d'), rg = gg.createRadialGradient(64, 64, 4, 64, 64, 64);
    rg.addColorStop(0, 'rgba(255,248,220,1)'); rg.addColorStop(0.25, 'rgba(255,236,170,.55)'); rg.addColorStop(1, 'rgba(255,230,160,0)');
    gg.fillStyle = rg; gg.fillRect(0, 0, 128, 128);
    const sun = new T.Sprite(new T.SpriteMaterial({ map: new T.CanvasTexture(gc), fog: false, blending: T.AdditiveBlending, depthWrite: false }));
    sun.scale.setScalar(70); sun.position.copy(sunDir).multiplyScalar(150); scene.add(sun);
    const clouds = [];
    const cm = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.92, fog: false });
    for (let i = 0; i < 9; i++) {
      const cl = new T.Group();
      for (let k = 0; k < 6; k++) add(cl, new T.SphereGeometry(rand(7, 13), 8, 6), cm, k * 9 - 22 + rand(-3, 3), rand(-2, 3), rand(-4, 4)).scale.y = 0.5;
      cl.position.set(rand(-150, 150), rand(55, 85), rand(-170, -40)); scene.add(cl); clouds.push(cl);
    }
    return (dt) => clouds.forEach((cl) => { cl.position.x += dt * 1.2; if (cl.position.x > 170) cl.position.x = -170; });
  }
  function birds(scene) {
    const bm = new T.MeshBasicMaterial({ color: 0x2b2b30, side: T.DoubleSide });
    const wingGeo = G('wing', () => { const gg = new T.BufferGeometry(); gg.setAttribute('position', new T.Float32BufferAttribute([0, 0, 0, 0.9, 0, 0.15, 0.25, 0, -0.3], 3)); return gg; });
    const list = Array.from({ length: 8 }, (_, i) => {
      const b = new T.Group(); const w1 = new T.Mesh(wingGeo, bm), w2 = new T.Mesh(wingGeo, bm); w2.scale.x = -1; b.add(w1, w2); scene.add(b);
      return { b, w1, w2, r: rand(22, 38), h: rand(18, 30), s: rand(0.12, 0.22) * (i % 2 ? 1 : -1), a: rand(0, 6), f: rand(7, 10) };
    });
    return (t, dt) => list.forEach((o) => {
      o.a += o.s * dt; o.b.position.set(Math.cos(o.a) * o.r, o.h + Math.sin(t * 0.5 + o.r) * 1.5, -30 + Math.sin(o.a) * o.r * 0.7);
      o.b.rotation.y = -o.a + (o.s > 0 ? 0 : Math.PI); const fl = Math.sin(t * o.f + o.r) * 0.6; o.w1.rotation.z = fl; o.w2.rotation.z = -fl;
    });
  }
  function city(scene, color) {
    const n = 70, mesh = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: color || 0xd9c7a1 }), n), m = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), p = new T.Vector3();
    for (let i = 0; i < n; i++) {
      const a = rand(-1.3, 1.3), r = rand(48, 78), h = rand(3, 7);
      p.set(Math.sin(a) * r * 1.6, h / 2, -Math.cos(a) * r - 30); q.setFromAxisAngle(new T.Vector3(0, 1, 0), rand(0, 3)); sc.set(rand(4, 8), h, rand(4, 8));
      mesh.setMatrixAt(i, m.compose(p, q, sc));
    }
    scene.add(mesh);
  }
  root.AgoraProps = { plazaTexture, groundTexture, amphora, bench, fountain, statue, brazier, stall, olive, cypress, sky, birds, city, phong };
})(window);
