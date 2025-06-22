import * as frontendComms from './frontend_communication.js';

let robots = []; 

//returns all filtered data for all lines. Data includes color as hexcode, name, number and an array of all stations.
export async function getAllLines() {
  try {
    const rawData = await frontendComms.getLines();

    //console.log("raw: ", rawData); 

    const filteredLines = rawData.map(line => ({
      color: line.color,
      name: line.name,
      number: line.number,
      stations: []
    }));


    await Promise.all(
    filteredLines.map(async line => {
      let fullStations = await frontendComms.getLineStations(line.number);
      line.stations = fullStations.stations; 
    })
  );

     const rawLines = rawData.map(line => ({
        stations: line.stations 
    }));

    //console.log("rawLines: ", rawLines); 

    //console.log("look ", filteredLines); 

    return filteredLines;
  } catch (error) {
    //console.error("Error fetching lines:", error);
    return []; 
  }
}


export async function getRobotInfo(id){

  if(robots.length != 0){


  }

  try {
    const rawData = await frontendComms.getLines();

    
  } catch (error) {
    console.error("Error fetching lines:", error);
    return []; 
  }
}
