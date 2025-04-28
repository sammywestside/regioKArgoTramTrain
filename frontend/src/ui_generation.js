
let stations_line4 = [
      "de:08212:611",
      "de:08212:610",
      "de:08212:609",
      "de:08212:608",
      "de:08212:607",
      "de:08212:606",
      "de:08212:605",
      "de:08212:604",
      "de:08212:603",
      "de:08212:602",
      "de:08212:40",
      "de:08212:39",
      "de:08212:37",
      "de:08212:37:4",
      "de:08212:61",
      "de:08212:71",
      "de:08212:85",
      "de:08212:3",
      "de:08212:401",
      "de:08212:402",
      "de:08212:403",
      "de:08212:404",
      "de:08212:405",
      "de:08212:406",
      "de:08212:407",
      "de:08212:408",
      "de:08212:409",
      "de:08212:3017",
      "de:08212:411",
      "de:08212:3012"
    ];


let stations_line_5 = [
      "de:08212:501",
      "de:08212:58",
      "de:08212:51",
      "de:08212:503",
      "de:08212:504",
      "de:08212:505",
      "de:08212:603",
      "de:08212:507",
      "de:08212:508",
      "de:08212:62",
      "de:08212:61",
      "de:08212:71",
      "de:08212:85",
      "de:08212:622",
      "de:08212:623",
      "de:08212:624",
      "de:08212:7",
      "de:08212:9",
      "de:08212:10",
      "de:08212:802"
    ];

async function loadHaltestellenData() { 
  
  try {

    const response = await fetch('/backend/src/main/json/haltestellen_v2-1.json');

    if (!response.ok) {

      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Data loaded:', data);
    return data;

  } catch (error) {

    console.error('Failed to load JSON:', error);
  }
}

function discardIrrelevantInfo(locations) {
  return locations.map(location => ({
    name: location.name,
    triasID: location.triasID
  }));
}

function filterByMatchingIds(namesAndIDs, onlyIDs) {
  // Convert secondArray to a Set for faster lookups
  const secondArraySet = new Set(onlyIDs);

  // Filter firstArray to only keep elements whose triasID exists in secondArray
  return namesAndIDs.filter(element => secondArraySet.has(element.triasID));
}

function populateDropdown(dropdownId, data) {
  const dropdownContent = document.getElementById(dropdownId);
  dropdownContent.innerHTML = ''; // Clear existing content

  data.forEach(item => {
      const link = document.createElement('option');
      link.textContent = item.name;
      link.setAttribute('value', item.triasID);
      dropdownContent.appendChild(link);
  });
}


(async () => {
  const data = await loadHaltestellenData();
  let onlyStationIDsOnLineFourAndFive = stations_line4.concat(stations_line_5); 
  console.log("File 1: ", stations_line4);
  console.log("File 2: ", stations_line_5)
  console.log("Joined files: ", onlyStationIDsOnLineFourAndFive); 
  let strippedArrayNamesAndIDs = discardIrrelevantInfo(data); 
  console.log("Stripped data: ", strippedArrayNamesAndIDs); 
  let finalSet = filterByMatchingIds(strippedArrayNamesAndIDs, onlyStationIDsOnLineFourAndFive); 
  console.log("Final refined data: ", finalSet);
  populateDropdown('start_content', finalSet);
  populateDropdown('destination_content', finalSet); 
})();
