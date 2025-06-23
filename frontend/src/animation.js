// Import all functions from the communication module
import * as communication from "./frontend_communication.js";
import * as ui from "./script.js";

// Animation speed for robot movement
let animationSpeed = 0.01; 
const speedSlider = document.getElementById("sim_speed");

// Listener für Änderung während des Ziehens
speedSlider.addEventListener("input", () => {
    const speedValue = parseInt(speedSlider.value);
    animationSpeed = 0.01; 
    animationSpeed = animationSpeed*speedValue+0.0001; 
});


document.getElementById("active_button_pause").addEventListener("click", (event) => {
    animationSpeed = 0;
});
document.getElementById("active_button_stop").addEventListener("click", (event) => {
    animationSpeed = 0; 
});


//**********************************************
// MAIN FUNCTION TO START AND MANAGE ROBOTS
//**********************************************
export async function startRobotManager(map, roboIcon) {
  // Get information about all robots
  const robots = await communication.getAllRobotInfo();
    

  // Loop through each robot
  for (const robot of robots) {
    animateRobotOnce(robot, robot.id, map, roboIcon);
  }
}

//**********************************************
// FUNCTION TO ANIMATE A ROUTE 
//**********************************************
async function animateRobotOnce(robot, robotId, map, roboIcon) {
  // Place a marker on the map at the robot's current position
  const marker = L.marker([robot.position.lat, robot.position.long], { icon: roboIcon }).addTo(map);

  // Add a click event to the marker (for opening a popup or details)
  marker.on('click', () => {
    console.log("Marker clicked");
    //HIER FEHLT DIE VERLINKUNG ZUM MENU
  });

  // Get the robot's delivery route
  let route = await communication.getDeliveryRoute(robotId);

 

  // If route is available and has stations
  if (route && route.stations.length > 0) {
    // Convert station coordinates into an array of [lat, lng]
    const latlngs = route.stations.map(station => [
      station.coordinates.lat,
      station.coordinates.long
    ]);

    travel_time = route.travel_time

    // Identify transfer points between route segments
    const transferPoints = [];
    if (robot.route.segments.length > 1) {
      for (let i = 0; i < robot.route.segments.length - 1; i++) {
        const segmentLength = robot.route.segments[i].length;
        transferPoints.push(segmentLength - 1);
      }
    }

    // Animate from current position to the first station
    await animateSegment(marker, [robot.position.lat, robot.position.long], latlngs[0], robot.id);
    communication.getRobotInfoByIdAndCoords(robotId, latlngs[0][0], latlngs[0][1])
    .then(info => {
      ui.showInfo(info.id, info.name, info.position.lat, info.position.long, info.battery_level, info.route.stops)
    });
    // Animate the robot along the entire route
    await animateRoute(robotId, latlngs, marker, transferPoints);
  }
}

//**********************************************
// FUNCTION TO ANIMATE A SINGLE SEGMENT
//**********************************************
function animateSegment(marker, startLatLng, endLatLng){
  return new Promise(resolve => {
    let t = 0;

    function animateStep() {
      t += animationSpeed;

      // Stop animation when end point is reached
      if (t >= 1) {
        marker.setLatLng(endLatLng);
        resolve();
        return;
      }

      // Calculate intermediate position
      const currentLat = startLatLng[0] + (endLatLng[0] - startLatLng[0]) * t;
      const currentLng = startLatLng[1] + (endLatLng[1] - startLatLng[1]) * t;
      marker.setLatLng([currentLat, currentLng]);

      requestAnimationFrame(animateStep);
    }

    animateStep();
  });
}

//**********************************************
// FUNCTION TO ANIMATE THE COMPLETE ROUTE
//**********************************************
async function animateRoute(robotId, latlngs, marker, transferPoints) {
  let currentIndex = 0;
  let transferPointsIndex = 0;

  return new Promise(resolve => {
    function moveToNextPoint() {
      // If we've reached the end of the route, stop
      if (currentIndex >= latlngs.length - 1) {
        resolve();
        return;
      }

      const [startLat, startLng] = latlngs[currentIndex];
      const [endLat, endLng] = latlngs[currentIndex + 1];
      let t = 0;

      function animateStep() {
        t += animationSpeed;

        // Once we reach the target point
        if (t >= 1) {
          marker.setLatLng([endLat, endLng]);

          // Fetch and log robot info at current station
          communication.getRobotInfoByIdAndCoords(robotId, endLat, endLng)
              .then(info => {
                console.log(info)
                ui.showInfo(info.id, info.name, endLat, endLng, info.battery_level, (info.route.stops-currentIndex))
              });

          currentIndex++;

          // If it's a transfer point, wait before moving on
          if (currentIndex == transferPoints[transferPointsIndex]) {
            transferPointsIndex++;
            setTimeout(() => moveToNextPoint(), 2000); // wait 2 seconds
          } else {
            moveToNextPoint();
          }
          return;
        }

        // Calculate current intermediate position
        const currentLat = startLat + (endLat - startLat) * t;
        const currentLng = startLng + (endLng - startLng) * t;
        marker.setLatLng([currentLat, currentLng]);

        // Continue animation
        requestAnimationFrame(animateStep);
      }

      animateStep();
    }

    moveToNextPoint();
  });
}
