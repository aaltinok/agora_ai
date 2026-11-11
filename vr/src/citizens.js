/* Antik Atina vatandaşları: uzuvlu, yürüyen / konuşan / oturan insan figürleri (düşük poligon, paylaşılan geometri). */
(function (root) {
  'use strict';
  const T = root.THREE;
  const lamb = (color, o) => new T.MeshLambertMaterial(Object.assign({ color }, o || {}));
  const cache = {};
  const G = (key, make) => cache[key] || (cache[key] = make());
  const add = (parent, geo, mat, x, y, z) => {
    const m = new T.Mesh(geo, mat); m.position.set(x || 0, y || 0, z || 0); parent.add(m); return m;
  };
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const SKINS = [0xf0c8a0, 0xd9a77e, 0xc08a62, 0xa8744f, 0x8a5a3c];
  const CLOTH = [0xf1e9d6, 0xe3d3a8, 0xc9a24b, 0xb5553f, 0x4f6fa5, 0x6f8f5f, 0x8d5ea0, 0xd98f4e, 0x3f6f7a, 0xa63d40];
  const TRIM = [0x1f3f7a, 0xa4352b, 0x2f6b4f, 0x3a3a3a, 0xc9a24b];
  const HAIR = [0x2b1d14, 0x4a3222, 0x1c1c1c, 0x7a5a3a, 0xb9b4aa];
  const SANDAL = lamb(0x5a3a22);
  const ABB_CLOTH = [0xf1e9d6, 0xcdbf9a, 0x3f5f7a, 0x6f5a3f, 0x4f6f55, 0x8a4b3c, 0x5a4a6a, 0xd9b36a];

  /** opts: female, long, height, skin, cloth, trim, hair, beard, hat, cloak, bald, child */
  function makeCitizen(o) {
    o = o || {};
    const abb = o.style === 'abbasid';
    const long = abb ? !o.child : o.long !== undefined ? o.long : !!o.female;
    const skin = lamb(o.skin || pick(SKINS)), clothHex = o.cloth || pick(abb ? ABB_CLOTH : CLOTH), cloth = lamb(clothHex), trim = lamb(o.trim || pick(TRIM));
    const hairM = lamb(o.hair || pick(HAIR));
    const g = new T.Group(); const body = new T.Group(); g.add(body);
    const hipY = 0.88;

    function leg(side) {
      const hip = new T.Group(); hip.position.set(0.085 * side, hipY, 0); body.add(hip);
      add(hip, G('thigh', () => new T.CylinderGeometry(0.055, 0.045, 0.44, 7)), skin, 0, -0.22, 0);
      const knee = new T.Group(); knee.position.y = -0.44; hip.add(knee);
      add(knee, G('shin', () => new T.CylinderGeometry(0.042, 0.035, 0.42, 7)), skin, 0, -0.21, 0);
      add(knee, G('foot', () => new T.BoxGeometry(0.075, 0.035, 0.17)), SANDAL, 0, -0.43, 0.04);
      return { hip, knee };
    }
    const legs = [leg(-1), leg(1)];

    const torso = new T.Group(); torso.position.y = hipY; body.add(torso);
    add(torso, G('torso', () => new T.CylinderGeometry(0.15, 0.17, 0.56, 10)), cloth, 0, 0.28, 0);
    add(torso, G('belt', () => new T.CylinderGeometry(0.178, 0.178, 0.05, 10)), trim, 0, 0.04, 0);
    add(torso, G('shoulder', () => new T.SphereGeometry(0.17, 10, 6)), cloth, 0, 0.54, 0).scale.set(1.1, 0.34, 0.72);

    const skH = long ? 0.78 : 0.3, skR = long ? 0.31 : 0.245;
    const skirt = new T.Group(); skirt.position.y = hipY + 0.05; body.add(skirt);
    add(skirt, G('skirt' + long, () => new T.CylinderGeometry(0.17, skR, skH, 12)), cloth, 0, -skH / 2, 0);
    add(skirt, G('hem' + long, () => new T.CylinderGeometry(skR + 0.004, skR + 0.004, 0.045, 12)), trim, 0, -skH + 0.022, 0);

    function arm(side) {
      const sh = new T.Group(); sh.position.set(0.2 * side, 0.5, 0); torso.add(sh);
      add(sh, G('uarm', () => new T.CylinderGeometry(0.04, 0.034, 0.28, 7)), abb ? cloth : skin, 0, -0.14, 0);
      const el = new T.Group(); el.position.y = -0.28; sh.add(el);
      add(el, G('farm', () => new T.CylinderGeometry(0.033, 0.028, 0.26, 7)), abb ? cloth : skin, 0, -0.13, 0);
      add(el, G('hand', () => new T.SphereGeometry(0.036, 7, 5)), skin, 0, -0.28, 0);
      return { sh, el };
    }
    const arms = [arm(-1), arm(1)];

    add(torso, G('neck', () => new T.CylinderGeometry(0.045, 0.05, 0.1, 7)), skin, 0, 0.62, 0);
    const head = new T.Group(); head.position.y = 0.74; torso.add(head);
    add(head, G('head', () => new T.SphereGeometry(0.1, 12, 9)), skin, 0, 0, 0).scale.set(0.95, 1.12, 1);
    add(head, G('nose', () => new T.SphereGeometry(0.02, 6, 5)), skin, 0, -0.005, 0.1);
    if (abb) {
      const wm = lamb(o.female ? clothHex : o.turban || pick([0xf3efe6, 0xe9e1cc, 0xcdbf9a, 0x3f5f7a]));
      if (o.female) {
        add(head, G('scarf', () => new T.SphereGeometry(0.116, 12, 9, 0, Math.PI * 2, 0, Math.PI * 0.62)), wm, 0, 0.01, -0.01);
        add(head, G('scarfback', () => new T.CylinderGeometry(0.1, 0.13, 0.3, 10, 1, true)), wm, 0, -0.12, -0.05).scale.z = 0.8;
      } else {
        add(head, G('tring', () => new T.TorusGeometry(0.105, 0.04, 7, 14)), wm, 0, 0.06, 0).rotation.x = Math.PI / 2;
        add(head, G('tdome', () => new T.SphereGeometry(0.105, 10, 7, 0, Math.PI * 2, 0, Math.PI / 2)), wm, 0, 0.07, 0);
      }
    }
    if (!abb && !o.bald) {
      const cap = add(head, G('hair', () => new T.SphereGeometry(0.108, 12, 8, 0, Math.PI * 2, 0, Math.PI * 0.55)), hairM, 0, 0.012, -0.012);
      cap.rotation.x = -0.25;
    }
    if (!abb && o.female) {
      add(head, G('bun', () => new T.SphereGeometry(0.06, 8, 6)), hairM, 0, 0.02, -0.11);
      add(head, G('hairback', () => new T.SphereGeometry(0.1, 8, 6)), hairM, 0, -0.04, -0.05).scale.set(1, 1.25, 0.8);
    }
    if (o.beard) add(head, G('beard', () => new T.ConeGeometry(0.07, 0.17, 8)), hairM, 0, -0.14, 0.045).rotation.x = Math.PI;
    if (!abb && o.hat) {
      const hatM = lamb(0xcdb27a);
      add(head, G('brim', () => new T.CylinderGeometry(0.2, 0.2, 0.012, 14)), hatM, 0, 0.085, 0);
      add(head, G('dome', () => new T.SphereGeometry(0.095, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2)), hatM, 0, 0.09, 0);
    }
    if (o.cloak) {
      const cm = lamb(o.cloak, { side: T.DoubleSide });
      const c = add(torso, G('cloak', () => new T.CylinderGeometry(0.2, 0.26, 0.72, 12, 1, true, Math.PI * 0.25, Math.PI * 1.5)), cm, 0, 0.18, 0);
      c.rotation.y = Math.PI;
    }
    g.scale.setScalar(o.height || 1);
    g.traverse((m) => { if (m.isMesh) m.castShadow = true; });
    return { group: g, body, torso, head, legs, arms, skirt, long, phase: Math.random() * 6 };
  }

  /** Yürüme döngüsü: phase ilerler, amp 0..1. */
  function walk(c, dt, speed) {
    c.phase += dt * speed * 4.4;
    const s = Math.sin(c.phase), amp = Math.min(1, speed);
    c.legs[0].hip.rotation.x = s * 0.62 * amp; c.legs[1].hip.rotation.x = -s * 0.62 * amp;
    c.legs[0].knee.rotation.x = Math.max(0, -Math.cos(c.phase)) * 0.7 * amp;
    c.legs[1].knee.rotation.x = Math.max(0, Math.cos(c.phase)) * 0.7 * amp;
    c.arms[0].sh.rotation.x = -s * 0.5 * amp; c.arms[1].sh.rotation.x = s * 0.5 * amp;
    c.arms[0].el.rotation.x = -0.2 * amp; c.arms[1].el.rotation.x = -0.2 * amp;
    c.body.position.y = Math.abs(Math.cos(c.phase)) * 0.028 * amp;
    c.torso.rotation.y = s * 0.07 * amp; c.skirt.rotation.z = s * 0.025 * amp * (c.long ? 1.5 : 0.5);
  }
  /** Durağan konuşma: el hareketi, baş sallama. */
  function talk(c, t, seed) {
    const k = 0.5 + 0.5 * Math.sin(t * 1.3 + seed);
    c.arms[1].sh.rotation.set(-0.7 - 0.5 * Math.sin(t * 2.2 + seed), 0, -0.15);
    c.arms[1].el.rotation.x = -0.9 * k;
    c.arms[0].sh.rotation.x = -0.15 * k;
    c.head.rotation.set(0.04 * Math.sin(t * 2.6 + seed), 0.12 * Math.sin(t * 0.8 + seed), 0);
    c.torso.rotation.y = 0.08 * Math.sin(t * 0.6 + seed);
  }
  function sit(c) {
    c.body.position.y = -0.4;
    c.legs.forEach((l) => { l.hip.rotation.x = -1.5; l.knee.rotation.x = 1.45; });
    c.arms.forEach((a) => { a.sh.rotation.x = -0.5; a.el.rotation.x = -0.9; });
  }
  function sitFloor(c) {
    c.body.position.y = -0.62;
    c.legs.forEach((l, i) => { l.hip.rotation.set(-1.1, 0, i ? -0.75 : 0.75); l.knee.rotation.x = 2.1; });
    c.arms.forEach((a) => { a.sh.rotation.x = -0.35; a.el.rotation.x = -0.7; });
  }
  root.AgoraCitizens = { makeCitizen, walk, talk, sit, sitFloor, lamb, add, G };
})(window);
