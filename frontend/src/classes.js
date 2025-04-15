class Package{
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

class DeliveryRobot{
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

    unloadPackage(currentStop){

        console.log("a")
    }
}