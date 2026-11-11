/* Filozof figürleri: tek bir iskelet, her filozof için ayrı dönem giysisi ve yüz. */
(function (root) {
  'use strict';
  const T = root.THREE, C = root.AgoraCitizens;
  const lamb = (c, o) => new T.MeshLambertMaterial(Object.assign({ color: c }, o || {}));
  const add = C.add;

  /* Giysiler dönemine göre genelleştirilmiş tasvirlerdir (belgelenmiş portre yoktur). */
  const SPECS = {
    sokrates: { style: 'greek', skin: 0xd9a77e, robe: 0xe9dcbc, drape: 0xb79d6e, hair: 0xc4c2bb, bald: true, sideHair: true, beard: 'full', beardColor: 0xc4c2bb, snub: true, barefoot: true },
    platon: { style: 'greek', skin: 0xd6a47c, robe: 0xf1ead8, drape: 0x4f6fa5, hair: 0xbdb7ab, hairStyle: 'wavy', beard: 'full', beardColor: 0xbdb7ab },
    aristoteles: { style: 'greek', skin: 0xdcae88, robe: 0xf0e8d2, drape: 0x7a3b34, hair: 0x7a6a55, hairStyle: 'receding', beard: 'short', beardColor: 0x8a8378, holds: 'scroll' },
    epiktetos: { style: 'greek', skin: 0xc99a72, robe: 0xd8cdb4, drape: 0x8f8468, hair: 0xa8a39a, bald: true, sideHair: true, beard: 'short', beardColor: 0xa8a39a },
    farabi: { style: 'abbasid', skin: 0xd3a27a, robe: 0x2f5f6b, drape: 0xe8e0cc, sash: 0xc9a24b, hair: 0x9a9a98, turban: 0xf2eee4, beard: 'pointed', beardColor: 0xc8c8c4, holds: 'book' },
  };

  function makePhilosopher(spec) {
    const skin = lamb(spec.skin), robe = lamb(spec.robe), drape = lamb(spec.drape, { side: T.DoubleSide });
    const hairM = lamb(spec.hair || 0x888888), beardM = lamb(spec.beardColor || spec.hair || 0x888888), dark = lamb(0x2a1c14);
    const abb = spec.style === 'abbasid';
    const g = new T.Group(), body = new T.Group(); g.add(body);

    add(body, new T.CylinderGeometry(0.23, 0.42, 1.15, 18), robe, 0, 0.575, 0);
    if (abb) {
      add(body, new T.CylinderGeometry(0.262, 0.28, 0.07, 18), lamb(spec.sash), 0, 0.78, 0);                // kuşak
      add(body, new T.CylinderGeometry(0.27, 0.33, 0.3, 18, 1, true), drape, 0, 1.06, 0);                   // omuz şalı
    } else {
      add(body, new T.CylinderGeometry(0.3, 0.37, 0.8, 18, 1, true), drape, 0, 0.84, 0);                    // himation: bel-omuz arası sarılı kumaş
    }
    add(body, new T.SphereGeometry(0.3, 14, 10), robe, 0, 1.17, 0).scale.set(1, 0.42, 0.7);
    add(body, new T.CylinderGeometry(0.06, 0.075, 0.12, 10), skin, 0, 1.3, 0);
    [-0.1, 0.1].forEach((x) => {
      if (spec.barefoot) add(body, new T.BoxGeometry(0.1, 0.045, 0.22), skin, x, 0.025, 0.08);
      else add(body, new T.BoxGeometry(0.11, 0.06, 0.24), lamb(abb ? 0x6b4a2b : 0x5a3a22), x, 0.03, 0.08);
    });

    const head = new T.Group(); head.position.set(0, 1.45, 0); body.add(head);
    add(head, new T.SphereGeometry(0.125, 18, 14), skin, 0, 0, 0).scale.set(1, 1.15, 1.05);
    add(head, new T.SphereGeometry(0.034, 10, 8), skin, 0, -0.012, 0.125).scale.set(spec.snub ? 1.25 : 0.9, spec.snub ? 1.1 : 1.35, 1.2);
    [-0.045, 0.045].forEach((x) => {
      add(head, new T.SphereGeometry(0.013, 8, 6), dark, x, 0.025, 0.112);
      add(head, new T.BoxGeometry(0.06, 0.012, 0.02), beardM, x, 0.055, 0.112).rotation.z = x > 0 ? -0.15 : 0.15;
      add(head, new T.SphereGeometry(0.03, 8, 6), skin, x * 2.8, 0, 0).scale.set(0.5, 1, 0.8);
    });
    if (spec.turban) {
      const tm = lamb(spec.turban);
      add(head, new T.TorusGeometry(0.128, 0.05, 8, 18), tm, 0, 0.08, 0).rotation.x = Math.PI / 2;
      add(head, new T.SphereGeometry(0.128, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2), tm, 0, 0.085, 0);
      add(head, new T.BoxGeometry(0.05, 0.28, 0.012), tm, 0.06, -0.08, -0.13);                              // sarığın ucu
    } else if (spec.hairStyle === 'wavy') {
      add(head, new T.SphereGeometry(0.135, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.55), hairM, 0, 0.015, -0.02).rotation.x = -0.2;
      add(head, new T.SphereGeometry(0.11, 10, 8), hairM, 0, -0.04, -0.07).scale.set(1.1, 1.1, 0.7);
    } else if (spec.hairStyle === 'receding') {
      add(head, new T.SphereGeometry(0.13, 14, 8, 0, Math.PI * 2, Math.PI * 0.3, Math.PI * 0.3), hairM, 0, 0.0, -0.02);
    } else if (spec.sideHair) {
      add(head, new T.SphereGeometry(0.13, 16, 6, 0, Math.PI * 2, Math.PI * 0.42, Math.PI * 0.22), hairM, 0, 0.005, -0.012);
    }
    if (spec.beard) {
      const bl = spec.beard === 'short' ? 0.18 : spec.beard === 'pointed' ? 0.34 : 0.3, br = spec.beard === 'pointed' ? 0.075 : 0.105;
      add(head, new T.ConeGeometry(br, bl, 12), beardM, 0, -0.07 - bl / 2, 0.045).rotation.x = Math.PI;
      add(head, new T.SphereGeometry(0.095, 10, 8), beardM, 0, -0.085, 0.045).scale.set(1, 0.7, 0.95);
      [-0.03, 0.03].forEach((x) => add(head, new T.SphereGeometry(0.03, 8, 6), beardM, x, -0.04, 0.115).scale.set(1.4, 0.6, 0.8));
    }
    const mouth = add(head, new T.BoxGeometry(0.05, 0.012, 0.02), dark, 0, -0.072, 0.118);

    function arm(side) {
      const sh = new T.Group(); sh.position.set(0.3 * side, 1.2, 0); body.add(sh);
      add(sh, new T.CylinderGeometry(0.05, 0.045, 0.3, 8), robe, 0, -0.15, 0);
      const el = new T.Group(); el.position.set(0, -0.3, 0); sh.add(el);
      add(el, new T.CylinderGeometry(0.042, 0.036, 0.27, 8), abb ? robe : skin, 0, -0.135, 0);
      add(el, new T.SphereGeometry(0.045, 8, 6), skin, 0, -0.29, 0);
      return { sh, el };
    }
    const armL = arm(-1), armR = arm(1);
    if (spec.holds === 'scroll') {
      const r = add(armR.el, new T.CylinderGeometry(0.026, 0.026, 0.32, 8), lamb(0xe6d9b0), 0, -0.3, 0.05); r.rotation.z = Math.PI / 2;
      [-0.16, 0.16].forEach((x) => add(armR.el, new T.CylinderGeometry(0.03, 0.03, 0.02, 8), lamb(0x8a6a3a), x, -0.3, 0.05).rotation.z = Math.PI / 2);
    } else if (spec.holds === 'book') {
      add(armR.el, new T.BoxGeometry(0.17, 0.23, 0.04), lamb(0x5a3a22), 0, -0.3, 0.06);
      add(armR.el, new T.BoxGeometry(0.15, 0.21, 0.03), lamb(0xefe6cf), 0.005, -0.3, 0.065);
    }
    const blob = add(g, new T.CircleGeometry(0.55, 20), new T.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.22 }), 0, 0.01, 0);
    blob.rotation.x = -Math.PI / 2;
    g.traverse((m) => { if (m.isMesh && m.material.opacity === 1) m.castShadow = true; });

    const S = { group: g, head, talking: false, _v: 0, _yaw: 0 };
    S.update = (dt, t, cam) => {
      const target = Math.atan2(cam.x - g.position.x, cam.z - g.position.z);
      let d = target - S._yaw; d = Math.atan2(Math.sin(d), Math.cos(d));
      S._yaw += d * Math.min(1, dt * 3); g.rotation.y = S._yaw;
      body.scale.y = 1 + Math.sin(t * 1.6) * 0.004;
      head.rotation.set(Math.sin(t * 0.7) * 0.03 + (S.talking ? Math.sin(t * 3) * 0.04 : 0), Math.sin(t * 0.4) * 0.05, 0);
      S._v += ((S.talking ? 1 : 0) - S._v) * Math.min(1, dt * 8);
      mouth.scale.y = 1 + S._v * Math.abs(Math.sin(t * 13)) * 5;
      const wave = S._v * (0.55 + 0.25 * Math.sin(t * 2.1));
      armR.sh.rotation.set(-wave * 1.3, 0, -0.12 - wave * 0.3); armR.el.rotation.x = -wave * 0.9 - (spec.holds ? 0.5 : 0);
      armL.sh.rotation.set(-S._v * 0.25, 0, 0.12); armL.el.rotation.x = -S._v * 0.35;
    };
    return S;
  }
  root.AgoraFigures = { SPECS, makePhilosopher };
})(window);
