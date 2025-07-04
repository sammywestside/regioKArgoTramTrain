// Import all functions from the communication module
import * as communication from "./frontend_communication.js";

defaultInfo();

// show last clicked sim-panel button
// element: the button as HTML-Element
function activeButton(element) {
    document.querySelectorAll("#sim_panel button").forEach(button => {
        button.classList.remove("button_true");
    });
    element.classList.add("button_true");
}

// show package-panel an hide package button
function toggleConfigurePackage() {
    var add_package = document.getElementById("add_package");
    var package_panel = document.getElementById("package_panel");
    if (add_package.style.display === "none") {
        add_package.style.display = "flex";
        package_panel.style.display = "none";
    }
    else {
        add_package.style.display = "none";
        package_panel.style.display = "flex";
    }
}

// toggle dropdown in package-panel
// drop_id: id of div around dropdown-content (like span or input)
function toggleDropdown(drop_id) {
    document.getElementById(drop_id).classList.toggle("show");
    if (drop_id === "drop_content_start" || drop_id === "drop_content_end" || drop_id === "info_drop_content"|| drop_id === "info_drop_content") {
        updateStationsDrop(drop_id)
    }
}

// select from dropdown in package-panel and show selection
// item: text of selected element from dropdown
// input_id: id of input to show selection in
// drop_id: id of div around dropdown-content (like span or input)
async function selectFromDrop(item, input_id, drop_id) {
    document.getElementById(input_id).value = item;
    if(input_id === "input_info"){
        await communication.addCargoStationByName(item); 
    }else if(input_id === "input_info_robo"){
        const robots = await communication.getAllRobotInfo();
        if (!robots || robots.length === 0){
            await communication.addNewRobot(item,"Robot Nr. 1", 100, item) 
        }
        else{
            await communication.addNewRobot(item,"Robot Nr. 2", 100,item)
        }    
        location.reload();
    }
    
     toggleDropdown(drop_id); 
}



// update stations in dropdowns in package-panel
// drop_id: id of div around dropdown-content (like span or input)
async function updateStationsDrop(drop_id) {
    const stationsData = await communication.getAllStations();
    let allStations = []; 
    for (const station of stationsData) {
        allStations.push(station.name); 
    }

    const cargoStations = await communication.getCargoStations(); 
 
    let container;
    let stations;
    let package_type;

    if (drop_id != 'info_drop_content') {
        if (drop_id === 'drop_content_start') {
            container = document.getElementById("drop_content_start");
            stations = cargoStations;
            package_type = "package_start";
        } else if (drop_id === 'drop_content_end') {
            container = document.getElementById("drop_content_end");
            stations = allStations;
            package_type = "package_end";
        }

        const spans = container.querySelectorAll("span");
        spans.forEach(span => span.remove());

        stations.forEach(station => {
            const span = document.createElement("span");
            span.textContent = station;
            span.classList.add("pointer");
            span.onclick = () => selectFromDrop(span.textContent, package_type, drop_id);
            container.appendChild(span);
        });
    } else {
        container = document.getElementById("info_drop_content");
        stations = allStations;

        const spans = container.querySelectorAll("span");
        spans.forEach(span => span.remove());

        stations.forEach(station => {
            const span = document.createElement("span");
            span.textContent = station;
            span.classList.add("pointer");
            span.onclick = () => addStartStation(span.textContent, drop_id);
            container.appendChild(span);
        });
    }


}

// add configured package 
async function addPackage() {
    const weight = document.getElementById("package_weight").value;
    const size = document.getElementById("package_size").value;
    const start = document.getElementById("package_start").value;
    const end = document.getElementById("package_end").value;

    if (weight && weight != null && size && size != null && start && start != null && end && end != null) {
        communication.addNewPackage(start, end, size, weight)
        const robots = await communication.getAllRobotInfo();
          // Loop through each robot
          for (const robot of robots) {
            try {
                // Try to load packages into the robot
                await communication.addPackagesToRobot(robot.id);
            } catch (error) {
                console.warn("Package could not be added:");
            }
          }     
    }

   // toggleConfigurePackage();
     
}

// display info in default info-panel (also, when clicked on part of map that is not robot, line, station or other special)
async function defaultInfo() {
    let robot = await communication.getAllRobotInfo();
    let start_station = await communication.getCargoStations(); 
    const info_panel = document.getElementById("info_panel");
    info_panel.innerHTML = "";

    let rspan = document.createElement("span");
    rspan.classList.add("headline");
    rspan.innerHTML = "Paketroboter:";
    info_panel.appendChild(rspan);

    if (robot != null) {
        let rtable1 = document.createElement("table");
        let rtr1 = document.createElement("tr");
        rtr1.id = "robot_1";
        let rtd1 = document.createElement("td");
        rtd1.innerHTML = robot[0].id; //id = name for robot
        let rtd2 = document.createElement("td");
        let ri1 = document.createElement("i");
        ri1.id = "robot_trash_1";
        ri1.classList.add("fas", "fa-trash", "pointer");
        ri1.onclick = () => deleteRobot(rtd1.innerHTML);

        info_panel.appendChild(rtable1);
        rtable1.appendChild(rtr1);
        rtr1.appendChild(rtd1);
        rtr1.appendChild(rtd2);
        rtd2.appendChild(ri1);

        if (robot.length >= 2) {
            let rtr2 = document.createElement("tr");
            rtr2.id = "robot_2";
            let rtd3 = document.createElement("td");
            rtd3.innerHTML = robot[1].id; //id = name for robot
            let rtd4 = document.createElement("td");
            let ri2 = document.createElement("i");
            ri2.id = "robot_trash_2";
            ri2.classList.add("fas", "fa-trash", "pointer");
            ri2.onclick = () => deleteRobot(rtd3.innerHTML);


            rtable1.appendChild(rtr2);
            rtr2.appendChild(rtd3);
            rtr2.appendChild(rtd4);
            rtd4.appendChild(ri2);
        }
        else {
            let ri_add = document.createElement("i");
            ri_add.id = "add_robot";
            ri_add.classList.add("fas", "fa-plus", "pointer");
            ri_add.onclick = () => addRobot();

            info_panel.appendChild(ri_add);
        }
    }
    else {
        let ri_add = document.createElement("i");
        ri_add.id = "add_robot";
        ri_add.classList.add("fas", "fa-plus", "pointer");
        ri_add.onclick = () => addRobot();

        info_panel.appendChild(ri_add);
    }

    let sspan = document.createElement("span");
    sspan.classList.add("headline");
    sspan.innerHTML = "Beladestationen:";
    info_panel.appendChild(sspan);

    if (start_station != null) {
        let stable1 = document.createElement("table");
        let str1 = document.createElement("tr");
        str1.id = "start_station_1";
        let std1 = document.createElement("td");
        std1.innerHTML = start_station[0]; //name of startstation
        let std2 = document.createElement("td");
        let si1 = document.createElement("i");
        si1.id = "station_trash_1";
        si1.classList.add("fas", "fa-trash", "pointer");
        si1.onclick = () => deleteStart(start_station[0]);

        info_panel.appendChild(stable1);
        stable1.appendChild(str1);
        str1.appendChild(std1);
        str1.appendChild(std2);
        std2.appendChild(si1);

        if (start_station.length >= 2) {
            let str2 = document.createElement("tr");
            str2.id = "start_station_2";
            let std3 = document.createElement("td");
            std3.innerHTML = start_station[1]; //name of startstation
            let std4 = document.createElement("td");
            let si2 = document.createElement("i");
            si2.id = "station_trash_2";
            si2.classList.add("fas", "fa-trash", "pointer");
            si2.onclick = () => deleteStart(start_station[1]);


            stable1.appendChild(str2);
            str2.appendChild(std3);
            str2.appendChild(std4);
            std4.appendChild(si2);
        }
        if (start_station.length >= 3) {
            let str3 = document.createElement("tr");
            str3.id = "start_station_3";
            let std5 = document.createElement("td");
            std5.innerHTML = start_station[2]; //name of startstation
            let std6 = document.createElement("td");
            let si3 = document.createElement("i");
            si3.id = "station_trash_3";
            si3.classList.add("fas", "fa-trash", "pointer");
            si3.onclick = () => deleteStart(start_station[2]);


            stable1.appendChild(str3);
            str3.appendChild(std5);
            str3.appendChild(std6);
            std6.appendChild(si3);
        }
        if (start_station.length >= 4) {
            let str4 = document.createElement("tr");
            str4.id = "start_station_4";
            let std7 = document.createElement("td");
            std7.innerHTML = start_station[3]; //name of startstation
            let std8 = document.createElement("td");
            let si4 = document.createElement("i");
            si4.id = "station_trash_4";
            si4.classList.add("fas", "fa-trash", "pointer");
            si4.onclick = () => deleteStart(start_station[3]);


            stable1.appendChild(str4);
            str4.appendChild(std7);
            str4.appendChild(std8);
            std8.appendChild(si4);
        }
        else {
            let si_add = document.createElement("i");
            si_add.id = "open_add_start";
            si_add.classList.add("fas", "fa-plus", "pointer");
            si_add.onclick = () => addCargoStationInInfobox(); 

            info_panel.appendChild(si_add);
        }
    }
    else {
        let si_add = document.createElement("i");
        si_add.id = "open_add_start";
        si_add.classList.add("fas", "fa-plus", "pointer");
        si_add.onclick = () => toggleDropdown('info_drop_content');

        info_panel.appendChild(si_add);
    }
}

// display info of clicked item from map in info-panel
// id: id of clicked item
export function showInfo(id, name, lat, long, battery_level, stop) {
    const info_panel = document.getElementById("info_panel");

    // Prüfe, ob der Container für alle Roboterinfos schon existiert
    let robotsContainer = document.getElementById("robots-info-container");
    if (!robotsContainer) {
        robotsContainer = document.createElement("div");
        robotsContainer.id = "robots-info-container";
        info_panel.appendChild(robotsContainer);
    }

    // Falls schon ein Info-Panel für diesen Roboter existiert, löschen
    const existing = document.getElementById("robot-info-" + id);
    if (existing) existing.remove();

    // Neuen Container pro Roboter
    const container = document.createElement("div");
    container.id = "robot-info-" + id;
    container.classList.add("robot-info-box");

    // Headline
    const headline = document.createElement("span");
    headline.classList.add("headline");
    headline.innerText = "Informationen zu " + name;
    container.appendChild(headline);

    // Datenliste
    const info = [
        { label: "ID", value: id },
        { label: "Batterie", value: battery_level + "%" },
        { label: "Breitengrad", value: lat },
        { label: "Längengrad", value: long },
        { label: "Stops bis Ziel", value: stop }
    ];

    for (const entry of info) {
        const row = document.createElement("div");
        row.classList.add("info-row");

        const label = document.createElement("span");
        label.classList.add("info-label");
        label.innerText = entry.label + ":";

        const value = document.createElement("span");
        value.classList.add("info-value");
        value.innerText = entry.value;

        row.appendChild(label);
        row.appendChild(value);
        container.appendChild(row);
    }

    // Einfügen nach Sortierung – Robot 1 oben, Robot 2 unten
    if (name.includes("1")) {
        robotsContainer.prepend(container);
    } else if (name.includes("2")) {
        robotsContainer.appendChild(container);
    } else {
        robotsContainer.appendChild(container);
    }
}





async function addCargoStationInInfobox() {
    //build dropdown
    const info_panel = document.getElementById("info_panel");
    const container = document.createElement("div");
    container.id = "info_drop_content";
    container.classList.add("dropdown-content", "show");

    const searchInput = document.createElement("input");
    searchInput.type = "text";
    searchInput.placeholder = "Suchen...";
    searchInput.classList.add("search_input");
    searchInput.id = "input_info";

    container.appendChild(searchInput);   
   
    const stations =  await communication.getAllStations(); 
     stations.forEach(station => {
            const span = document.createElement("span");
            span.textContent = station.name;
            span.classList.add("pointer");
            span.onclick = () => selectFromDrop(span.textContent, "input_info", "info_drop_content");
            container.appendChild(span);
        });

    info_panel.appendChild(container);

    searchInput.addEventListener("keyup", function() {
    searchStation(this, "info_drop_content");   
    });

    
}

// add new robot
async function addRobot() {
    //build dropdown
    const info_panel = document.getElementById("info_panel");
    const container = document.createElement("div");
    container.id = "info_drop_content";
    container.classList.add("dropdown-content", "show");

    const searchInput = document.createElement("input");
    searchInput.type = "text";
    searchInput.placeholder = "Suchen...";
    searchInput.classList.add("search_input");
    searchInput.id = "input_info_robo";

    container.appendChild(searchInput);   
   
    const stations =  await communication.getCargoStations(); 
     stations.forEach(station => {
            const span = document.createElement("span");
            span.textContent = station;
            span.classList.add("pointer");
            span.onclick = () => selectFromDrop(span.textContent, "input_info_robo", "info_drop_content");
            container.appendChild(span);
        });

    info_panel.appendChild(container);

    searchInput.addEventListener("keyup", function() {
    searchStation(this, "info_drop_content");   
    });
}


//delete robot
// id: id of robot
async function deleteRobot(id) {
    await communication.removeRobotById(id);
    location.reload(); 
}

// add station as start station
// station: name of station
// drop_id: id of div around dropdown-content (like span or input)
function addStartStation(station, drop_id) {
    toggleDropdown(drop_id);
}

// delete start station
async function deleteStart(stationName) {
    await communication.deleteCargoStationByName(stationName); 
}


// package panel
document.getElementById("add_package").addEventListener("click", () => {
    toggleConfigurePackage();
});
document.getElementById("close_package").addEventListener("click", () => {
    toggleConfigurePackage();
});
document.getElementById("toggle_dropdown_start").addEventListener("click", () => {
    toggleDropdown('drop_content_start');
});
document.getElementById("toggle_dropdown_size").addEventListener("click", () => {
    toggleDropdown('drop_content_size');
});
document.getElementById("select_from_drop_s").addEventListener("click", () => {
    selectFromDrop('S', 'package_size', 'drop_content_size');
});
document.getElementById("select_from_drop_m").addEventListener("click", () => {
    selectFromDrop('M', 'package_size', 'drop_content_size');
});
document.getElementById("select_from_drop_l").addEventListener("click", () => {
    selectFromDrop('L', 'package_size', 'drop_content_size');
});
document.getElementById("select_from_drop_xl").addEventListener("click", () => {
    selectFromDrop('XL', 'package_size', 'drop_content_size');
});
document.getElementById("toggle_dropdown_end").addEventListener("click", () => {
    toggleDropdown('drop_content_end');
});
document.getElementById("addpackage_button").addEventListener("click", () => {
    addPackage();
});


// map
document.getElementById("map").addEventListener("click", (event) => {
    defaultInfo();
});


