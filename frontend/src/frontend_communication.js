const headersCollection = {

  routeCalc: {
      "Content-Type": "application/json",
      "X-Request-Type": "routeCalculation"
  }
};


function stationNameHandler(id) {

  let element = document.getElementById(id);

  if (!element) return {};

  let stationName = element.options[element.selectedIndex].value;

  if (id === "start") {
      return { start: stationName };
  } else if (id === "destination") {
      return { destination: stationName };
  }

  return {};
}


function selectedStationToJson(start = "start", destination= "destination") { 

  let startObject = stationNameHandler(start); 
  let destinationObject = stationNameHandler(destination);

  return JSON.stringify([startObject, destinationObject]);
}


function packageAnalyzer(incomingData) {

    const idType = incomingData?.metadata?.type;
  
    switch (idType) {
      case "1":

        console.log("Works");
        return "1";
  
      case "2":
        return "2";
  
      case "...":
        return "...";
  
      default:
        return incomingData;
    }
  }
  

function sendData(jsonPackage, header) {
    fetch("http://127.0.0.1:8000/transfer", {
        method: "POST",
        headers: header,
        body: jsonPackage
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        let a = packageAnalyzer(data);
        
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
}
 
function testRun(){

  console.log("Starting progress...")

  let stations = selectedStationToJson();

  console.log(stations);

  sendData(stations, headersCollection.routeCalc);

  console.log("End");
}



