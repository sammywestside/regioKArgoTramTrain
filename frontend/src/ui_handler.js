import { Route, Station, Parcel, DeliveryRobot } from "./presets.js";
import * as communication from "./frontend_communication.js"

function readDropdownValue(id){
    let dropdownValue = document.getElementById(id).value; 
    return dropdownValue;
}; 

function readDropdownName(id){
    let select = document.getElementById(id);
    let selectedText = select.options[select.selectedIndex].text; 
    return selectedText; 
};

function fillDeliveryRobotInfo(start, destination, deliveryRoute, maxNumberOfPackages, cargo){
    
    fillStart(start);
    fillDestination(destination); 
    fillDeliveryRoute(deliveryRoute); 
    fillMaxNumberOfPackages(maxNumberOfPackages)
    fillCargo(cargo); 
};

function fillStart(value){
    let element = document.getElementById("robot_info_start");
    element.innerText = "Start: " + value; 
};

function fillDestination(value){
    let element = document.getElementById("robot_info_destination");
    element.innerText = "Destination: " + value; 
};

function fillDeliveryRoute(value){
    let element = document.getElementById("robot_info_deliveryRoute");
    element.innerText = "Delivery Route: " + value; 
};

function fillMaxNumberOfPackages(value){
    let element = document.getElementById("robot_info_maxNumberOfPackages");
    element.innerText = "Max Number of Packages: " + value; 
};

function fillCargo(value){
    let element = document.getElementById("robot_info_cargo");
    element.innerText = "Cargo: " + value; 
};


function handleUiInput(){
    //console.log("Starting"); 
    const startDropdownID = "start_content";
    const destinationDropdownID = "destination_content"; 
    let startID = readDropdownValue(startDropdownID); 
    let destinationID = readDropdownValue(destinationDropdownID); 
    let startName = readDropdownName(startDropdownID);
    let destinationName = readDropdownName(destinationDropdownID); 
    //console.log("Start ID: ", startID);
    //console.log("Destination ID: ", destinationID);
    //console.log("Start Name: ", startName);
    //console.log("Destination Name: ", destinationName); 
    fillDeliveryRobotInfo(startName, destinationName, "None", 10, "This cargo"); 
    let startDestinationJSON = communication.selectedStationToJson(startName, destinationName);  
    let route = communication.sendData(startDestinationJSON, communication.headersCollection.routeCalc); 
    //console.log("Route: ", route); 

};

//document.getElementById("submit_button").addEventListener("click", handleUiInput); 

