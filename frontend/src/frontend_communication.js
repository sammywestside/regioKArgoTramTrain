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


//working. Start station needs to be a cargo station that has been added with func addCargoStationByName before. All arguments are passed as strings except weight, this is passed as number. 
export function addNewPackage(startStationName, destinationStationName, size, weight){

  fetch('http://127.0.0.1:8000/api/addPackage', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    start: startStationName,
    weight: weight,
    size: size, 
    destination: destinationStationName
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


//functional. add a Cargo station. Pass the station name as a string for it to work. 
export function addCargoStationByName(stationName){

  fetch(`http://127.0.0.1:8000/api/addCargoStations?station_name=${encodeURIComponent(stationName)}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
  
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

//working
export function initBasicRobots(){

  fetch('http://127.0.0.1:8000/api/init_basic_robots', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
 
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


//working. id is passed as string. 
export function addPackagesToRobot(id){

  fetch(`http://127.0.0.1:8000/api/addPackagesToRobot?robot_id=${id}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
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


//working. All arguments are passed as strings except battery_level, this is passed as number. Passing an id as "1" did not work. id "a" did work. 
export function addNewRobot(id, name, battery_level, position){

  console.log('Type of id:', typeof id);
  console.log('Type of name:', typeof name);
  console.log('Type of battery_level:', typeof battery_level);
  console.log('Type of position:', typeof position);

  fetch('http://127.0.0.1:8000/api/addRobot', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    id: id,
    name: name,
    battery_level: battery_level,
    position: position
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


//working. Id is passed as string, batterie_level as number, status as string
export function sendRobotConfig(id, batterie_level, status){

  fetch(`http://127.0.0.1:8000/api/robotConfig`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    robot_id: id,
    batterie_level: batterie_level,
    status: status
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


//working. name is passed as string. 
export function deleteCargoStationByName(stationName){

  fetch(`http://127.0.0.1:8000/api/deleteCargoStation?station_name=${stationName}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({

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


//working. 
export async function getAllStations() { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/stations`);
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


//working.
export async function getStationById(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/station/${id}`);
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


//not working
export async function getLineByStationId(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/station?id=${id}/line`);
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

//working. id is passed as string. returns number
export async function getBatterieChargeById(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/batterieCharge?id=${id}`);
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


//working. id is passed as string. returns data package that contains. available_capacity, current_num_packages, max_packages, robot_id, total_weight

export async function getLoadCapacityById(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/loadCapacity?id=${id}`);
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



//working. id gets passes as string. returns a data package that contains: battery_level, id, name, num_packages, packages (array of the packages in the robot and the info about them.), position, route and status. 
export async function getRobotInfoByIdAndCoords(id, lat, long) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/RobotInfo?id=${id}&lat=${lat}&long=${long}`);
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


//working. returns an array of all existing robots, each index in the array is a robot with all their information. 
export async function getAllRobotInfo() { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/AllRobotInfo`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
  }
}


//not working. 
export async function getCargo() { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/cargoOnDelivery`);
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


export async function getRoute() { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/route`);
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


//working. id is passed as string. returns array of all station along a delivery route of a robot. Each index contains the station id and the line name
export async function getRouteSteps(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/route/steps?robot_id=${id}`);
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


//working. Returns all lines. 
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


//working. returns all coordinates related to the line with the id that is given. 
export async function getLineCoords(id) {
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/line/coords/${encodeURIComponent(id)}`);
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


//working. returns all information related to to station with the given id
export async function getLineStations(id) {
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


//working. id is passed as string. Returns a data package that contains: 1. segments, this is an array of arrays. These arrays describe the stations a robot travels along one tram line. Each array = a line. 2. stations, an array of all stations that the robot travels to. 3. stops the number os stops. 4. transfers, an array of the stations where a robot has to swap to a different line. 5. transfer_time, time it takes the robot to transfer at a line swap. 6. travel_time, the amount of time the robot needs to travel 
export async function getDeliveryRoute(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/deliveryRoute?robot_id=${id}`);
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


//working. id is passed as string. returns a data package like in getDeliveryRoute. 
export async function reloadRoute(id) { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reloadRoute?robot_id=${id}`);
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

//working. Returns array of Cargo Stations 
export async function getCargoStations() { 
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/cargoStations`);
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

//working. id is passed as string. 
export function removeRobotById(id){

  fetch(`http://127.0.0.1:8000/api/removeRobot?id=${id}`, {
  method: 'DELETE',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
 
}


//working. 
export function removeAllRobot(){

  fetch(`http://127.0.0.1:8000/api/removeAllRobots`, {
  method: 'DELETE',
  headers: {
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
 
}


