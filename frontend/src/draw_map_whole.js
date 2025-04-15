//canvas setup
const canvas = document.getElementById("overview_map");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const ctx = canvas.getContext("2d");

//max values lat/lng
const minLat = 48.5, maxLat = 49.4; 
const minLng = 7.9, maxLng = 9.2;

//spherical coordinates for 2d coordinates matching the canvas
function latLngToCanvas(lat, lng) {
  const x = (((lng - minLng) / (maxLng - minLng)) * canvas.width);
  const y = canvas.height - ((lat - minLat) / (maxLat - minLat)) * canvas.height;
  return { x, y };
}

let last_point = [0,0]; 
let last_line_color = ""; 

//read json for lines
fetch("../../backend/src/main/json/lines_v2.json") //changes to correct file path
  .then(response => response.json())
  .then(data => {
    data.lines.forEach(line => {
      //console.log(`Linie: ${line.name}, Farbe: ${line.color}`);
        line.stations.forEach(station => {
          //console.log(`Station: ${station}`);
          fetch('../../backend/src/main/json/lines_v2.json')
              .then(response => response.json())
              .then(data => {
              let stations = data.find(stations => stations.triasID === station);
              if (stations) {
                let point = latLngToCanvas(stations.coordPositionWGS84.lat, stations.coordPositionWGS84.long);
                //scale by 1.3 to enlarge the map, then move it back into the visible canvas 
                point.x = point.x*1.3-(canvas.width*.18); 
                point.y = point.y*1.3-(canvas.height*.18);
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
      
    });
  })
  .catch(error => console.error("Error: lines.json failed reading", error));

