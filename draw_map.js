//canvas setup
const canvas = document.getElementById("overview_map");
const ctx = canvas.getContext("2d");

//read json for lines
fetch("json/lines.json")
  .then(response => response.json())
  .then(data => {
    data.lines.forEach(line => {
      //console.log(`Linie: ${line.name}, Farbe: ${line.color}`);
      line.stations.forEach(station => {
        //console.log(`Station: ${station}`);
        
        fetch('json/haltestellen_2023.json')
            .then(response => response.json())
            .then(data => {
            let stations = data.find(stations => stations.triasID === station);
            if (stations) {
                //console.log(`Koordinaten: ${stations.coordPositionWGS84}`);
              } else {
                //console.log("Station nicht gefunden.");
                console.log(`Station: ${station}`);
              }
        });

      });
    });
  })
  .catch(error => console.error("Error: lines.json failed reading", error));