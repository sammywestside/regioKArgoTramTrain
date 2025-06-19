import { getAllLines } from "./communication_handler.js";
import { startRoboAnimation } from './animation.js';

const fullData  = await getAllLines();
const map = L.map('map').setView([48.95, 8.55], 11);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; OpenStreetMap & Carto'
}).addTo(map);

function linesOfStation(stationName) {
  const lines = new Set();

  for (const line of fullData) {
    for (const station of line.stations) {
      if (station.name === stationName) {
        lines.add(line.number);
      }
    }
  }

  return Array.from(lines).join(", ");
}

function drawMap() {
    for (const line of fullData) {
    const latlngs = [];

    for (const station of line.stations) {
      const lat = parseFloat(station.coordinates.lat);
      const lng = parseFloat(station.coordinates.long);
      const latlng = [lat, lng];
      latlngs.push(latlng);
     

      L.circleMarker(latlng, {
        radius: 3,
        color: line.color,
        fillColor: line.color,
        fillOpacity: 1
      })

      .addTo(map)
      .bindTooltip(
        `<div style="background:#e7e7e7; padding:5px; border-radius:4px; font-weight:bold;">
          Station: ${station.name} <br>
          Breitengrad: ${lat} <br>
          Längengrad: ${lng} <br>
          Linien: ${linesOfStation(station.name)} 
        </div>`,
        { sticky: true, direction: 'top' }
      );
    };
    
    L.polyline(latlngs, { color: line.color, weight: 2 })
    .addTo(map)
    .bindTooltip(
      `<div style="background:#d9d9d9; padding:5px; border-radius:4px; font-weight:bold;">
        Linie ${line.number}
      </div>`,
      { sticky: true, direction: 'center' }
    );
    
  };
}

drawMap();

const roboIcon = L.icon({
  iconUrl: '../../frontend/img/lieferroboter.png', 
  iconSize: [32, 32],
  iconAnchor: [16, 16]
});

//Testing of animation
const line = fullData[0];
const latlngs = line.stations.map(station => [
  parseFloat(station.coordinates.lat),
  parseFloat(station.coordinates.long)
]);

startRoboAnimation(map, latlngs, roboIcon);