//canvas setup
const canvas = document.getElementById("overview_map");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext("2d");

//canvas setup
const canvasRobo = document.getElementById("robo_map");
canvasRobo.width = window.innerWidth;
canvasRobo.height = window.innerHeight;
const ctxRobo = canvasRobo.getContext("2d");

//max values lat/lng
const minLat = 48.5, maxLat = 49.4; 
const minLng = 7.9, maxLng = 9.2;

//spherical coordinates for 2d coordinates matching the canvas
function latLngToCanvas(lat, lng, canvas) {
  const x = (((lng - minLng) / (maxLng - minLng)) * canvas.width);
  const y = canvas.height - ((lat - minLat) / (maxLat - minLat)) * canvas.height;
  return { x, y };
}

let last_point = [0,0]; 
let last_line_color = ""; 

const roboStations = [
  "de:08212:611", "de:08212:610", "de:08212:609", "de:08212:608",
  "de:08212:607", "de:08212:606", "de:08212:605", "de:08212:604",
  "de:08212:603", "de:08212:602", "de:08212:40",  "de:08212:39",
  "de:08212:37",  "de:08212:37:4", "de:08212:61", "de:08212:71",
  "de:08212:85",  "de:08212:622", "de:08212:623", "de:08212:624",
  "de:08212:7",   "de:08212:9",   "de:08212:10",  "de:08212:802"
];

//read json for lines
function drawMap(){
  fetch("../../backend/src/main/json/lines_v2.json") //changes to correct file path
  .then(response => response.json())
  .then(data => {
    data.lines.forEach(line => {
      //console.log(`Linie: ${line.name}, Farbe: ${line.color}`);
      if(line.number == "4" || line.number == "5"){ //FÜR PROTOTYP NUR LINE 4 und 5
        line.stations.forEach(station => {
          //console.log(`Station: ${station}`);
          fetch('../../backend/src/main/json/haltestellen_v2-1.json')
              .then(response => response.json())
              .then(data => {
              let stations = data.find(stations => stations.triasID === station);
              if (stations) {
                let point = latLngToCanvas(stations.coordPositionWGS84.lat, stations.coordPositionWGS84.long, canvas);
                //scale by 1.3 to enlarge the map, then move it back into the visible canvas  //KOMPLETTE MAP WERTE point.x*1.3-(canvas.width*.18)
                point.x = point.x*6-(canvas.width*1.9); 
                point.y = point.y*6-(canvas.height*2.1);
                //draw station
                ctx.fillStyle = line.color;
                ctx.fillRect( point.x-1.5, point.y-1.5, 3, 3);  
                if(last_line_color == "" || last_line_color != line.color ){
                  last_point = point;
                  last_line_color = line.color; 
                }else{
                  ctx.beginPath(); 
                  ctx.strokeStyle = line.color;
                  ctx.lineWidth = 1;        
                  ctx.moveTo(last_point.x,last_point.y); 
                  ctx.lineTo(point.x, point.y); 
                  ctx.stroke(); 
                  last_point = point;
                }
              }else{
                console.log("Station nicht gefunden.");
              }
          });

        });
      }
    });
  })
  .catch(error => console.error("Error: lines.json failed reading", error));

  return; 
}

const roboStationCoords = [];

function loadRoboStationCoords(callback) {
  fetch('../../backend/src/main/json/haltestellen_v2-1.json')
    .then(response => response.json())
    .then(data => {
      roboStations.forEach(id => {
        const station = data.find(s => s.triasID === id);
        if (station) {
          let point = latLngToCanvas(station.coordPositionWGS84.lat, station.coordPositionWGS84.long, canvasRobo);
          point.x = point.x * 6 - (canvasRobo.width * 1.9);
          point.y = point.y * 6 - (canvasRobo.height * 2.1);
          roboStationCoords.push(point);
        }
      });
      callback(); // Starte Animation wenn Koordinaten geladen
    });
}


function animateTrain(stations, index = 0, t = 0) {
  if (index >= stations.length - 1) return;

  const start = stations[index];
  const end = stations[index + 1];

  const x = start.x + (end.x - start.x) * t;
  const y = start.y + (end.y - start.y) * t;
 
  ctxRobo.clearRect(0, 0, canvasRobo.width, canvasRobo.height);

  // Neuen Kreis zeichnen
  ctxRobo.beginPath();
  ctxRobo.arc(x, y, 6, 0, Math.PI * 2);
  ctxRobo.fillStyle = "white";
  ctxRobo.fill();

  if (t < 1) {
    requestAnimationFrame(() => animateTrain(stations, index, t + 0.015));
  
  } else {
    requestAnimationFrame(() => animateTrain(stations, index + 1, 0));
  }
}




//Start 
drawMap(); // Zuerst Karte zeichnen
loadRoboStationCoords(() => {
  animateTrain(roboStationCoords);
});
