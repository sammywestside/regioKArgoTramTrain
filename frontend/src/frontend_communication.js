import { Route, Station } from './presets.js';

export const headersCollection = {

  routeCalc: {
      "Content-Type": "application/json",
      "X-Request-Type": "routeCalculation"
  }
};


export function stationNameHandler(id) {

  let element = document.getElementById(id);

  if (!element) return {};

  let stationName = element.options[element.selectedIndex].value;

  if (id === "start") {
      return { start: stationName };
  } else if (id === "destination") {
      return { destination: stationName };
  }

  return {};
};


export function selectedStationToJson(start = "start", destination= "destination") { 

  let startObject = stationNameHandler(start); 
  let destinationObject = stationNameHandler(destination);

  return JSON.stringify([startObject, destinationObject]);
};


/* function packageAnalyzer(incomingData) {

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
  } */
  

export function sendData(jsonPackage, header) {
    fetch("http://127.0.0.1:8000/api/route", {
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
        const route = Route.fromJSON(data);
        
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
};

/* This might be useful in the future

let timeoutId;
const search = document.getElementById("search");
const suggestions = document.getElementById("suggestions");

let options = []; // to be loaded

// Load data once
fetch('/data/options.json')
  .then(res => res.json())
  .then(data => options = data);

search.addEventListener("input", () => {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    const input = search.value.toLowerCase();
    const matches = options.filter(option =>
      option.toLowerCase().includes(input)
    );
    
    suggestions.innerHTML = matches
      .slice(0, 10)
      .map(match => `<li>${match}</li>`)
      .join("");

    document.querySelectorAll("#suggestions li").forEach(li => {
      li.onclick = () => {
        search.value = li.textContent;
        suggestions.innerHTML = "";
      };
    });
  }, 200); // debounce delay
});

*/



