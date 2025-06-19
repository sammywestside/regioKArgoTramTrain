export function initialFetch(){

  fetch('http://127.0.0.1:8000/', {
  method: 'GET',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

  
}


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

//Name, station, drain over time minutes, 
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


//todo: add url parameter robot name
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

//robot parameter
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

export async function getLines() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/lines');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error; 
  }
}


export async function getLineCoords(id) {
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/lines/coords/${encodeURIComponent(id)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error; 
  }
}


export async function getLineStations(id) {
  console.log(id); 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/line/stations/{lines_id}?line_id=${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error; 
  }
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
