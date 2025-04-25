export class Package{
    constructor(destination, weight){
        this.destination = destination; 
        this.weight = weight; 
    }

    getDestination(){
        return this.destination; 
    }

    getWeight(){
        return this.weight; 
    }
}

export class DeliveryRobot{
    constructor(start, destination, maxNumberOfPackages){
        this.start = start;
        this.destination = destination
        this.deliveryRoute = []
        this.maxNumberOfPackages = maxNumberOfPackages; 
        this.cargo = []; 
    }

    getCurrentNumberOfPackagesCarried(){
        return this.cargo.length; 
    }

    getStart(){
        return this.start; 
    }

    getDestination(){
        return this.destination; 
    }

    getMaxNumberOfPackagesCarried(){
        return this.maxNumberOfPackages; 
    }

    setDeliveryRoute(route){
        this.deliveryRoute = route; 
    }

    loadPackage(package){

        if(this.cargo.length < this.maxNumberOfPackages){
            this.cargo.push(package); 
            console.log(`Package ${package} loaded. Current cargo;`, this.cargo); 

        } else {  
            console.log("Cannot load cargo. Cargo is full.");
        }
    }

    unloadPackage(currentStop) {
        for (let i = 0; i < this.cargo.length; i++) {
            if (this.cargo[i].destination === currentStop) {
                
                console.log(`Unloading package for ${currentStop}`);
                this.cargo.splice(i, 1);
                i--; 
            }
        }
    }
    
};

export class Route {
    constructor(stations, stops, transfer, travel_time, transfer_time) {
      this.stations = stations; // List of Station instances
      this.stops = stops;
      this.transfer = transfer; // List of Station instances
      this.travel_time = travel_time;
      this.transfer_time = transfer_time;
    }; 
  
    static fromJSON(json) {
      const stations = json.stations.map(Station.fromJSON);
      const transfer = json.transfer.map(Station.fromJSON);
      return new Route(
        stations,
        json.stops,
        transfer,
        json.travel_time,
        json.transfer_time
      );
    }
  };
  
  export class Station {
    constructor(id, name, coordinates ) {
      this.id = id;
      this.name = name;
      this.coordinates = coordinates;
    }
  
    static fromJSON(json) {
      return new Station(json.id, json.name, json.coordinates);
    }
  };