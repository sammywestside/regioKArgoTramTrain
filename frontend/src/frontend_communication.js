export function sendNewParcel(station, destination, weight, volume){

station = setNullOnEmptyVar(station); 
destination = setNullOnEmptyVar(destination);
weight= setNullOnEmptyVar(destination);
volume = setNullOnEmptyVar(destination); 

  fetch('http://127.0.0.1:8000/newParcel', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    station: station,
    destination: destination,
    weight: weight,
    volume: volume
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});


}

export function sendRobotConfig(batteryCapcity, drainPerUnitTraveled, cargoCapacity, weightCapacity){

  batteryCapcity = setNullOnEmptyVar(batteryCapcity);
  drainPerUnitTraveled = setNullOnEmptyVar (drainPerUnitTraveled);
  cargoCapacity = setNullOnEmptyVar(cargoCapacity);
  weightCapacity = setNullOnEmptyVar(weightCapacity); 

  fetch('http://127.0.0.1:8000/robotConfig', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    batteryCapcity: batteryCapcity,
    drainPerUnitTraveled: drainPerUnitTraveled,
    cargoCapacity: cargoCapacity,
    weightCapacity: weightCapacity
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});


}

export function sendSimulationSpeed(simulationSpeed){

  simulationSpeed = setNullOnEmptyVar(simulationSpeed); 

  fetch('http://127.0.0.1:8000/simSpeed', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    simulationSpeed: simulationSpeed
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});

  
}

export function sendStopRequest(){

  fetch('http://127.0.0.1:8000/stop', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    request: 'stop'
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});

  
}

export function sendStartRequest(){

  fetch('http://127.0.0.1:8000/start', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    request: 'start'
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});

  
}

export function sendPauseRequest(){

  fetch('http://127.0.0.1:8000/pause', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    request: 'pause'
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});

  
}

export function sendRestartRequest(){

  fetch('http://127.0.0.1:8000/restart', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    request: 'restart'
  })
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log('Success:', data);
})
.catch(error => {
  console.error('Error:', error);
});

  
}

export function getAllRobotInfo(){

  fetch('http://127.0.0.1:8000/allRobotInfo', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data)) 
.catch(error => console.error('Error:', error));

  
}

export function getCurrentBatterieCapacity(){

  fetch('http://127.0.0.1:8000/batterieCapacity', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data)) 
.catch(error => console.error('Error:', error));

  
}

export function getCurrentBatterieCharge(){
  
  fetch('http://127.0.0.1:8000/batterieCharge', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

}

export function getCurrentLoadCapcity(){

  fetch('http://127.0.0.1:8000/loadCapacity', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getCargo(){

  fetch('http://127.0.0.1:8000/api/cargo', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getRoute(){

  fetch('http://127.0.0.1:8000/route', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

 
}

export function getFastestRoute(){

  fetch('http://127.0.0.1:8000/route/steps', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getLines(){

  fetch('http://127.0.0.1:8000/lines', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getNextStop(){

  fetch('http://127.0.0.1:8000/nextStop', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getRobotId(){

  fetch('http://127.0.0.1:8000/robotId', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

export function getCargoStations(){

  fetch('http://127.0.0.1:8000/cargoStations', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}

function setNullOnEmptyVar(a) {
  return (a === undefined || a === null || a === '') ? null : a;
}
