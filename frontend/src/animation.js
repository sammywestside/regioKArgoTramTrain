export function startRoboAnimation(map, latlngs, roboIcon) {
  const marker = L.marker(latlngs[0], { icon: roboIcon }).addTo(map);

  let currentIndex = 0;
  const speed = 0.05; // kleiner Wert = langsamer

  function moveToNextPoint() {
    if (currentIndex >= latlngs.length - 1) return;

    const [startLat, startLng] = latlngs[currentIndex];
    const [endLat, endLng] = latlngs[currentIndex + 1];

    let t = 0;

    function animateStep() {
      t += speed;

      if (t >= 1) {
        marker.setLatLng([endLat, endLng]);
        console.log("Hier update funktion um aktuelle inforamtionen von Robo anzeigen zu lassen ");
        currentIndex++;
        moveToNextPoint(); // move to next segment
        return;
      }

      const currentLat = startLat + (endLat - startLat) * t;
      const currentLng = startLng + (endLng - startLng) * t;
      marker.setLatLng([currentLat, currentLng]);

      requestAnimationFrame(animateStep);
    }

    animateStep();
  }

  moveToNextPoint();
}
