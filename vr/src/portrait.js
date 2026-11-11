/* Portre üretici (geliştirme aracı): filozof figürünün büst görüntüsünü PNG olarak verir. */
(function (root) {
  'use strict';
  const T = root.THREE, F = root.AgoraFigures;
  root.renderPortrait = (id, accent, size) => {
    const c = document.createElement('canvas'), R = new T.WebGLRenderer({ canvas: c, antialias: true, preserveDrawingBuffer: true });
    R.setSize(size, size, false);
    const scene = new T.Scene(), bg = document.createElement('canvas'); bg.width = bg.height = 256;
    const g = bg.getContext('2d'), grd = g.createRadialGradient(128, 110, 10, 128, 128, 190);
    grd.addColorStop(0, accent + 'cc'); grd.addColorStop(0.55, '#12254d'); grd.addColorStop(1, '#0a1530');
    g.fillStyle = grd; g.fillRect(0, 0, 256, 256); scene.background = new T.CanvasTexture(bg);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x8a7a60, 0.85));
    const key = new T.DirectionalLight(0xfff0d0, 0.9); key.position.set(-1.5, 2.2, 2.5); scene.add(key);
    const rim = new T.DirectionalLight(new T.Color(accent), 0.7); rim.position.set(2, 1.5, -1.5); scene.add(rim);
    const rig = F.makePhilosopher(F.SPECS[id]); scene.add(rig.group); rig.update(0.016, 0, new T.Vector3(0.0, 1.5, 3));
    const cam = new T.PerspectiveCamera(30, 1, 0.05, 20); cam.position.set(0.0, 1.48, 1.35); cam.lookAt(0, 1.36, 0);
    R.render(scene, cam); const url = c.toDataURL('image/png'); R.dispose(); return url;
  };
})(window);
