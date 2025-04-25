

function readDropdownValue(id){
    let dropdownValue = document.getElementById(id).value; 
    return dropdownValue;
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
    console.log("Starting"); 
    const startDropdownID = "start_content";
    const destinationDropdownID = "destination_content"; 
    let startID = readDropdownValue(startDropdownID); 
    let destinationID = readDropdownValue(destinationDropdownID); 
    console.log("Start ID: ", startID);
    console.log("Destination ID: ", destinationID);
    fillDeliveryRobotInfo(startID, destinationID, "None", 10, "This cargo"); 

    const DeliveryRobot = new DeliveryRobot(startID, destinationID, 10); 

    console.log("Delivery Robot: ", DeliveryRobot);

};

document.getElementById("submit_button").addEventListener("click", handleUiInput); 

