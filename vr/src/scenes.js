/* Üç senaryo: Atina Agorası (Sokrates), Lykeion (Aristoteles), Abbasi ilim meclisi (Farabi). */
(function (root) {
  'use strict';
  const T = root.THREE, C = root.AgoraCitizens, P = root.AgoraProps, F = root.AgoraFigures;
  const { lamb, add } = C, phong = P.phong;
  const rand = (a, b) => a + Math.random() * (b - a);
  const wrapAngle = (d) => Math.atan2(Math.sin(d), Math.cos(d));
  const marble = phong(0xf0e9d8), marbleDark = phong(0xd6cdb6), terracotta = phong(0xb5532f), blue = lamb(0x1f4f8f), red = lamb(0xa63d36), ochre = lamb(0xd9b36a);

  /* Dor düzeni: kaide (stylobate) üzerinde, tabansız, sivrilen yivli gövde, ekinus + abaküs; triglif/metop frizi. */
  function doric(n, spacing, h, roof) {
    const g = new T.Group(), w = (n - 1) * spacing + 1.8, base = 0.32, top = base + h + 0.38;
    add(g, new T.BoxGeometry(w + 1.4, 0.16, 2.6), marbleDark, 0, 0.08, 0); add(g, new T.BoxGeometry(w + 0.8, 0.16, 2.1), marbleDark, 0, 0.24, 0);
    for (let i = 0; i < n; i++) {
      const c = new T.Group(); c.position.x = (i - (n - 1) / 2) * spacing; g.add(c);
      add(c, new T.CylinderGeometry(0.36, 0.5, h, 16), marble, 0, base + h / 2, 0);
      add(c, new T.CylinderGeometry(0.58, 0.38, 0.22, 16), marbleDark, 0, base + h + 0.11, 0);
      add(c, new T.BoxGeometry(1.2, 0.16, 1.2), marbleDark, 0, base + h + 0.3, 0);
    }
    add(g, new T.BoxGeometry(w, 0.5, 1.3), marble, 0, top + 0.25, 0);                                // arhitrav
    add(g, new T.BoxGeometry(w, 0.5, 1.3), red, 0, top + 0.75, 0.02);                                 // metoplar
    for (let x = -w / 2 + 0.45; x < w / 2 - 0.2; x += 0.85) add(g, new T.BoxGeometry(0.28, 0.5, 1.34), blue, x, top + 0.75, 0.02);  // trigliflar
    add(g, new T.BoxGeometry(w + 0.5, 0.2, 1.8), marbleDark, 0, top + 1.1, 0);                        // korniş
    if (roof) { const r = add(g, new T.CylinderGeometry(1.5, 1.5, w + 0.8, 3), terracotta, 0, top + 1.75, -0.2); r.rotation.set(0, 0, Math.PI / 2); r.scale.set(0.62, 1, 1.05); }
    return g;
  }
  function acropolis(solid, z) {
    add(solid, new T.CylinderGeometry(34, 50, 22, 10), phong(0x9d8d6c), 0, 2, z);
    const g = new T.Group(); g.position.set(0, 13.2, z);
    for (let s = 0; s < 3; s++) add(g, new T.BoxGeometry(26 - s * 1.6, 0.4, 13 - s * 1.2), marbleDark, 0, 0.2 + s * 0.4, 0);
    [5, -5].forEach((zz) => { const f = doric(8, 2.4, 6, false); f.position.set(0, 1.0, zz); g.add(f); });
    add(g, new T.BoxGeometry(20, 0.5, 11.5), marble, 0, 10.4, 0);
    const ped = add(g, new T.CylinderGeometry(4.4, 4.4, 19.8, 3), marble, 0, 11.5, 5); ped.rotation.set(0, 0, Math.PI / 2); ped.scale.set(0.45, 1, 1);
    solid.add(g);
  }

  /* ---------------------------------------------------------------- ortak iskelet */
  function begin(o) {
    const scene = new T.Scene(); scene.fog = new T.Fog(o.fog || 0xf2e4c6, 55, 200);
    const sunDir = new T.Vector3(-0.45, 0.7, 0.35).normalize();
    const ups = [P.sky(scene, sunDir)], bu = P.birds(scene);
    scene.add(new T.HemisphereLight(0xdfeaff, 0xa88f60, 0.66));
    const sun = new T.DirectionalLight(0xfff0cc, 0.78); sun.position.copy(sunDir).multiplyScalar(50); sun.target.position.set(0, 0, -4);
    sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0006;
    Object.assign(sun.shadow.camera, { left: -24, right: 24, top: 24, bottom: -24, near: 5, far: 120 });
    scene.add(sun, sun.target);
    const gmat = o.groundMap ? new T.MeshLambertMaterial({ map: o.groundMap }) : new T.MeshLambertMaterial({ map: P.groundTexture(), color: o.groundColor || 0xe0cfa8 });
    const ground = new T.Mesh(new T.PlaneGeometry(420, 420), gmat); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
    const solid = new T.Group(); scene.add(solid);
    return { scene, solid, sun, ups, bu, walkers: [], talkers: [], updaters: [], t: 0 };
  }
  function walkers(ctx, loops, counts, mk) {
    loops.forEach((loop, li) => {
      const path = loop.map(([x, z]) => new T.Vector3(x, 0, z));
      for (let k = 0; k < counts[li]; k++) {
        const c = mk(li, k), i = Math.floor(rand(0, path.length));
        ctx.solid.add(c.group);
        ctx.walkers.push({ c, path, i, dir: k % 2 ? -1 : 1, speed: rand(0.6, 1.0), yaw: 0, pos: path[i].clone().add(new T.Vector3(rand(-0.6, 0.6), 0, rand(-0.6, 0.6))) });
      }
    });
  }
  function talkerPair(ctx, x, z, mk) {          // karşılıklı konuşan iki kişi
    [[-0.45, Math.PI / 2 + 0.25], [0.45, -Math.PI / 2 - 0.25]].forEach(([dx, ry]) => {
      const c = mk(); c.group.position.set(x + dx, 0, z); c.group.rotation.y = ry; ctx.solid.add(c.group); ctx.talkers.push({ c, seed: Math.random() * 6 });
    });
  }
  function finish(ctx, rig, pos, eye) {
    rig.group.position.set(pos[0], pos[1], pos[2]); ctx.solid.add(rig.group);
    ctx.solid.traverse((m) => { if (m.isMesh && !m.userData.noShadow) { m.castShadow = true; m.receiveShadow = true; } });
    const camera = new T.PerspectiveCamera(70, 1, 0.05, 500); camera.position.set(0, eye, 0);
    const camPos = new T.Vector3();
    function update(dt, t) {
      ctx.ups.forEach((u) => u(dt)); ctx.bu(t, dt); ctx.updaters.forEach((u) => u(t, dt));
      ctx.walkers.forEach((w) => {
        if (!w.c.group.visible) return;
        const tg = w.path[w.i], dx = tg.x - w.pos.x, dz = tg.z - w.pos.z;
        if (Math.hypot(dx, dz) < 0.5) w.i = (w.i + w.dir + w.path.length) % w.path.length;
        w.yaw += wrapAngle(Math.atan2(dx, dz) - w.yaw) * Math.min(1, dt * 3.5);
        w.pos.x += Math.sin(w.yaw) * w.speed * dt; w.pos.z += Math.cos(w.yaw) * w.speed * dt;
        C.walk(w.c, dt, w.speed); w.c.group.position.set(w.pos.x, 0, w.pos.z); w.c.group.rotation.y = w.yaw;
      });
      ctx.talkers.forEach((k) => C.talk(k.c, t, k.seed));
      camera.getWorldPosition(camPos); rig.update(dt, t, camPos);
    }
    function setXR(on) { ctx.sun.castShadow = !on; ctx.walkers.forEach((w, i) => { w.c.group.visible = !on || i < 5; }); }
    return { scene: ctx.scene, camera, philosopher: rig, update, setXR };
  }
  const cloak = () => [0xe9dfc4, 0x8a3b34, 0x37557e, 0xbf9a4d][Math.floor(Math.random() * 4)];
  const greek = (extra) => { const female = Math.random() < 0.35; return C.makeCitizen(Object.assign({ female, height: rand(0.94, 1.06), beard: !female && Math.random() < 0.5, hat: !female && Math.random() < 0.15, bald: !female && Math.random() < 0.12, cloak: !female && Math.random() < 0.4 ? cloak() : 0 }, extra || {})); };
  const arab = (extra) => { const female = Math.random() < 0.3; return C.makeCitizen(Object.assign({ style: 'abbasid', female, height: rand(0.95, 1.05), beard: !female && Math.random() < 0.6 }, extra || {})); };

  /* ------------------------------------------------------------ 1) Atina Agorası */
  function agora() {
    const ctx = begin({ groundColor: 0xd9c49a }), S = ctx.solid, scene = ctx.scene;
    P.city(scene, 0xd9c7a1); acropolis(S, -112);
    const stoa = doric(9, 3.0, 4.2, true); stoa.position.set(0, 0, -14.2); S.add(stoa);
    add(S, new T.BoxGeometry(29.5, 5.6, 0.5), ochre, 0, 2.8, -15.1);
    [[-13.2, Math.PI / 2], [13.2, -Math.PI / 2]].forEach(([x, ry]) => { const s = doric(6, 3.0, 4.2, true); s.position.set(x, 0, -1); s.rotation.y = ry; S.add(s); });
    S.add(P.tholos(-24, -8), P.altar(5, -7.5), P.well(-7.5, -4.4), P.herm(-9, -12.2, 0), P.herm(-6.4, -12.2, 0), P.herm(3.4, -12.2, 0));
    S.add(P.statue(8.6, -4.6, -0.5), P.statue(10.1, -4.2, -0.8), P.stall(9.6, -1.0, -0.9));
    const br = [P.brazier(-4.2, -11.4), P.brazier(4.2, -11.4)]; br.forEach((b) => S.add(b.group)); ctx.updaters.push((t) => br.forEach((b) => b.update(t)));
    S.add(P.bench(-5, -12.2, 0), P.bench(6, -12.2, 0));
    [[-8.5, -10.8], [-12, 6], [12, 6]].forEach(([x, z]) => S.add(P.plane(x, z)));
    [[10.5, -11.2], [-11.5, -2]].forEach(([x, z]) => S.add(P.olive(x, z)));
    [[-14.2, -9], [14.2, -9]].forEach(([x, z]) => S.add(P.cypress(x, z)));
    [[-10.2, -13.2], [3.2, -13.2], [8.2, -13.2]].forEach(([x, z], i) => S.add(P.amphora([0xb5553f, 0x8d4a2b, 0xc9703f][i % 3], x, 0, z, 1.25)));
    const loops = [[[-11, -9.6], [-4, -10.2], [4, -9.6], [11, -10.2], [11, -8], [4, -7.6], [-4, -8], [-11, -7.6]], [[-10, 1.5], [-10, 6], [-7, 6], [-7, 1.5]], [[10, 1.5], [10, 6], [7, 6], [7, 1.5]]];
    walkers(ctx, loops, [6, 2, 2], (li, k) => greek(li === 1 && k === 1 ? { height: 0.62, female: false, beard: false, hat: false, cloak: 0 } : {}));
    talkerPair(ctx, -2.4, -6.0, greek); talkerPair(ctx, 3.6, -5.6, greek);
    [[-5, -12.2], [6.4, -12.2]].forEach(([x, z]) => { const c = greek({ female: false, long: false }); c.group.position.set(x, 0, z + 0.05); C.sit(c); S.add(c.group); });
    const rig = F.makePhilosopher(F.SPECS.sokrates);
    return finish(ctx, rig, [0, 0, -2.1], 1.6);
  }

  /* ------------------------------------------------------------ 2) Lykeion */
  function lykeion() {
    const ctx = begin({ groundColor: 0xf0e2bd, fog: 0xf0e6cc }), S = ctx.solid, scene = ctx.scene;
    P.city(scene, 0xd9c7a1); acropolis(S, -118);
    const hill = add(S, new T.ConeGeometry(30, 34, 10), phong(0x8c8068), -90, 15, -70); hill.userData.noShadow = true;     // Likabettos benzeri kayalık tepe
    const back = doric(10, 3.0, 3.8, true); back.position.set(0, 0, -14.5); S.add(back);                                      // peripatos (örtülü yürüyüş yolu)
    add(S, new T.BoxGeometry(34, 5, 0.5), lamb(0xe3cfa0), 0, 2.5, -15.4);
    [[-14, Math.PI / 2], [14, -Math.PI / 2]].forEach(([x, ry]) => { const s = doric(7, 3.0, 3.8, true); s.position.set(x, 0, -4); s.rotation.y = ry; S.add(s); });
    S.add(P.statue(-6.5, -7.5, 0.4), P.altar(6.5, -8), P.herm(-3.5, -12.4, 0), P.herm(3.5, -12.4, 0), P.scrollShelf(9.5, -13.6, 0));
    [[-10, -9], [11, -10], [-11, 6], [11.5, 6], [-4, 9], [4, 9]].forEach(([x, z]) => S.add(P.plane(x, z)));
    [[-12, -11], [12.5, -2], [-12.5, -1]].forEach(([x, z]) => S.add(P.olive(x, z)));
    S.add(P.bench(-5.5, -4.8, 0.5), P.bench(5.5, -4.6, -0.5), P.bench(0, -9.2, 0));
    const loops = [[[-11, -12.2], [11, -12.2], [11, -10.6], [-11, -10.6]], [[-11.5, 2], [-11.5, -9.5], [-10, -9.5], [-10, 2]], [[11.5, 2], [11.5, -9.5], [10, -9.5], [10, 2]]];
    walkers(ctx, loops, [4, 2, 2], () => greek({ cloak: Math.random() < 0.7 ? cloak() : 0 }));
    talkerPair(ctx, -3.8, -7.2, greek); talkerPair(ctx, 3.0, -6.8, greek);
    [[-5.5, -4.8], [5.5, -4.6], [-0.4, -9.2], [0.5, -9.2]].forEach(([x, z]) => { const c = greek({ long: false }); c.group.position.set(x, 0, z + 0.05); c.group.rotation.y = x < 0 ? 0.5 : -0.5; C.sit(c); S.add(c.group); });
    return finish(ctx, F.makePhilosopher(F.SPECS.aristoteles), [0, 0, -2.1], 1.6);
  }

  /* ------------------------------------------------------------ 3) Abbasi ilim meclisi */
  function majlis() {
    const ctx = begin({ groundMap: P.brickTexture(), fog: 0xf0dcb4 }), S = ctx.solid, scene = ctx.scene;
    P.city(scene, 0xcdb88a); P.river(scene);
    for (let i = 0; i < 16; i++) S.add(P.palm(rand(-70, 70), rand(-90, -52)));
    const back = P.archRow(4, 7, 8.2); back.position.set(-10, 0, -15); S.add(back);
    const back2 = P.archRow(4, 7, 8.2); back2.position.set(10, 0, -15); S.add(back2);
    const iw = P.iwan(7.6, 10.5); iw.position.set(0, 0, -15); S.add(iw);                                                 // iwan: üç yanı kapalı, bir yanı açık kemerli salon
    [[-14, Math.PI / 2], [14, -Math.PI / 2]].forEach(([x, ry]) => { const s = P.archRow(5, 5, 6.2); s.position.set(x, 0, -3); s.rotation.y = ry; S.add(s); });
    const pool = P.pool(0, -8.2, 6.5, 2.6); S.add(pool); ctx.updaters.push((t) => { pool.userData.water.material.opacity = 0.8 + Math.sin(t * 1.4) * 0.03; });
    S.add(P.palm(-10.5, -8), P.palm(10.5, -8), P.palm(-10.5, 6), P.palm(10.5, 6));
    scene.add(P.rug(3.4, 5.0, 0, -2.3, '#7a2f2a', '#23406e'));
    const dais = add(S, new T.BoxGeometry(2.6, 0.3, 2.2), lamb(0xb58b5a), 0, 0.15, -2.2); dais.userData.noShadow = false;
    [[-0.9, 0.3, -2.9, 0x2f5f6b], [0.9, 0.3, -2.9, 0x8a3b34]].forEach(([x, y, z, c]) => S.add(P.cushion(x, y, z, c, 0.1)));
    S.add(P.rahle(-1.7, -2.6, 0.6), P.rahle(1.8, -2.6, -0.6), P.oud(2.4, 0.0, -1.2, 2.3));
    const tbl = add(S, new T.BoxGeometry(0.5, 0.5, 0.5), lamb(0x6f4c2e), -2.4, 0.25, -1.2); S.add(P.astrolabe(-2.4, 0.62, -1.2));
    S.add(P.amphora(0xb5553f, -6.5, 0, -12.5, 1.3), P.amphora(0x8d4a2b, 6.5, 0, -12.5, 1.3), P.amphora(0xc9703f, -11, 0, 3, 1.2));
    const loops = [[[-11, -11.5], [-4, -12.2], [4, -12.2], [11, -11.5], [11, -10], [4, -10.6], [-4, -10.6], [-11, -10]], [[-11.5, 3], [-11.5, -8.5], [-10, -8.5], [-10, 3]], [[11.5, 3], [11.5, -8.5], [10, -8.5], [10, 3]]];
    walkers(ctx, loops, [3, 2, 2], () => arab());
    [[-3.6, -3.4, 0.6], [-3.9, -1.4, 1.1], [3.6, -3.4, -0.6], [3.9, -1.2, -1.1], [-2.6, 0.8, 0.3], [2.6, 0.8, -0.3]].forEach(([x, z, ry], i) => {
      const c = arab({ female: false, beard: i % 3 !== 0 }); c.group.position.set(x, 0, z); c.group.rotation.y = ry; C.sitFloor(c); S.add(c.group);
    });
    const rig = F.makePhilosopher(F.SPECS.farabi);
    return finish(ctx, rig, [0, 0.3, -2.2], 1.6);
  }

  const BUILD = { agora, lykeion, majlis };
  root.AgoraScenes = { build: (id) => BUILD[id]() , ids: Object.keys(BUILD) };
})(window);
