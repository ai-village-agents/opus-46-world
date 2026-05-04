// The Liminal Archive - 3D Landmark Module
// A towering dark obelisk with floating golden glyphs and orbiting fog wisps
// Export: mountLandmark(THREE, scene, position) 

export function mountLandmark(THREE, scene, position = [0, 0, 0]) {
  const group = new THREE.Group();
  group.position.set(position[0], position[1], position[2]);

  // === OBELISK (main body) ===
  const obeliskGeo = new THREE.CylinderGeometry(1.2, 2.0, 18, 6);
  const obeliskMat = new THREE.MeshStandardMaterial({
    color: 0x0a0a0e,
    emissive: 0x1a150a,
    emissiveIntensity: 0.3,
    roughness: 0.8,
    metalness: 0.2
  });
  const obelisk = new THREE.Mesh(obeliskGeo, obeliskMat);
  obelisk.position.y = 9;
  group.add(obelisk);

  // === OBELISK CAP (pyramid top) ===
  const capGeo = new THREE.ConeGeometry(1.2, 3, 6);
  const capMat = new THREE.MeshStandardMaterial({
    color: 0xc9a96e,
    emissive: 0xc9a96e,
    emissiveIntensity: 0.6,
    roughness: 0.3,
    metalness: 0.5
  });
  const cap = new THREE.Mesh(capGeo, capMat);
  cap.position.y = 19.5;
  group.add(cap);

  // === GOLDEN GLOW (point light from within) ===
  const innerGlow = new THREE.PointLight(0xc9a96e, 2, 40);
  innerGlow.position.y = 12;
  group.add(innerGlow);

  // === AMBIENT BEACON (upward light beam) ===
  const beamGeo = new THREE.CylinderGeometry(0.3, 0.8, 30, 8, 1, true);
  const beamMat = new THREE.MeshBasicMaterial({
    color: 0xc9a96e,
    transparent: true,
    opacity: 0.15,
    side: THREE.DoubleSide
  });
  const beam = new THREE.Mesh(beamGeo, beamMat);
  beam.position.y = 30;
  group.add(beam);

  // === FLOATING GLYPHS (orbiting golden symbols) ===
  const glyphCount = 12;
  const glyphs = [];
  for (let i = 0; i < glyphCount; i++) {
    const glyphGeo = new THREE.BoxGeometry(0.4, 0.6, 0.05);
    const glyphMat = new THREE.MeshBasicMaterial({
      color: 0xc9a96e,
      transparent: true,
      opacity: 0.7
    });
    const glyph = new THREE.Mesh(glyphGeo, glyphMat);
    const angle = (i / glyphCount) * Math.PI * 2;
    const radius = 4 + Math.sin(i * 1.7) * 1.5;
    const height = 5 + (i / glyphCount) * 14;
    glyph.position.set(Math.cos(angle) * radius, height, Math.sin(angle) * radius);
    glyph.rotation.y = angle;
    glyph.userData = { angle, radius, height, speed: 0.3 + Math.random() * 0.2 };
    group.add(glyph);
    glyphs.push(glyph);
  }

  // === FOG WISPS (orbiting translucent spheres) ===
  const wispCount = 8;
  const wisps = [];
  for (let i = 0; i < wispCount; i++) {
    const wispGeo = new THREE.SphereGeometry(0.5 + Math.random() * 0.5, 8, 8);
    const wispMat = new THREE.MeshBasicMaterial({
      color: 0x7a6b4a,
      transparent: true,
      opacity: 0.2
    });
    const wisp = new THREE.Mesh(wispGeo, wispMat);
    const angle = (i / wispCount) * Math.PI * 2;
    const radius = 5 + Math.random() * 3;
    const height = 2 + Math.random() * 16;
    wisp.position.set(Math.cos(angle) * radius, height, Math.sin(angle) * radius);
    wisp.userData = { angle, radius, height, speed: 0.1 + Math.random() * 0.15, drift: Math.random() * Math.PI * 2 };
    group.add(wisp);
    wisps.push(wisp);
  }

  // === BASE PLATFORM (hexagonal) ===
  const baseGeo = new THREE.CylinderGeometry(4, 4.5, 0.5, 6);
  const baseMat = new THREE.MeshStandardMaterial({
    color: 0x1a150a,
    emissive: 0xc9a96e,
    emissiveIntensity: 0.1,
    roughness: 0.9
  });
  const base = new THREE.Mesh(baseGeo, baseMat);
  base.position.y = 0.25;
  group.add(base);

  // === LABEL ===
  // Create a sprite label
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'transparent';
  ctx.fillRect(0, 0, 512, 128);
  ctx.font = 'bold 36px Georgia, serif';
  ctx.fillStyle = '#c9a96e';
  ctx.textAlign = 'center';
  ctx.fillText('The Liminal Archive', 256, 50);
  ctx.font = '22px Georgia, serif';
  ctx.fillStyle = '#7a6b4a';
  ctx.fillText('4,420+ Chambers', 256, 85);
  const labelTexture = new THREE.CanvasTexture(canvas);
  const labelMat = new THREE.SpriteMaterial({ map: labelTexture, transparent: true });
  const label = new THREE.Sprite(labelMat);
  label.position.y = 24;
  label.scale.set(10, 2.5, 1);
  group.add(label);

  scene.add(group);

  // === ANIMATION FUNCTION ===
  function animate(time) {
    const t = time * 0.001;
    // Rotate glyphs
    glyphs.forEach(g => {
      const d = g.userData;
      const newAngle = d.angle + t * d.speed;
      g.position.x = Math.cos(newAngle) * d.radius;
      g.position.z = Math.sin(newAngle) * d.radius;
      g.position.y = d.height + Math.sin(t * 0.5 + d.angle) * 0.5;
      g.rotation.y = newAngle + Math.PI / 2;
      g.material.opacity = 0.5 + Math.sin(t * 2 + d.angle) * 0.3;
    });
    // Drift wisps
    wisps.forEach(w => {
      const d = w.userData;
      const newAngle = d.angle + t * d.speed;
      w.position.x = Math.cos(newAngle) * d.radius;
      w.position.z = Math.sin(newAngle) * d.radius;
      w.position.y = d.height + Math.sin(t * 0.3 + d.drift) * 2;
      w.material.opacity = 0.15 + Math.sin(t + d.drift) * 0.1;
    });
    // Pulse inner glow
    innerGlow.intensity = 1.5 + Math.sin(t * 0.8) * 0.5;
    // Pulse beam opacity
    beamMat.opacity = 0.1 + Math.sin(t * 0.5) * 0.05;
  }

  return { group, animate };
}
