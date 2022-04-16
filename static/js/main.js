//main.js
//This is the front end of Station Keeper
//Patrick Pragman
//Ciego Services
//January 31, 2018

//this is the div that contains the list of stations
//these globals (gross I know) control the page
var sld = document.getElementById('station_list_div');
var wld = document.getElementById('watch_list_div');
var sl = [];
var wl = [];
var time_interval = 1000*60*5; //default refresh interval is 5 minutes

//generic function to GET json from the server
function getJSON(callback, target, payload=null, rtype="GET"){
    var xhr = new XMLHttpRequest;
    xhr.overrideMimeType("application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(JSON.parse(xhr.responseText));
        }
    };

    xhr.open(rtype,target,true);
    if (rtype == "POST"){
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }
    xhr.send(payload)
};


function populate(station_list){
    //load station list into the sl list

    for (var i = 0; i< station_list.length; i++){

        if (station_list[i] != ""){
            sl.push(station_list[i])
        }

    };

    //populate the station_list_div

    sld.innerHTML = ""; //clear out the HTML in there, which on page load should only be a loading message

    for (var i = 0; i < sl.length; i++) {
        sld.appendChild(make_station(sl[i]));
    };

};

//makes a station div
function make_station(STA){

    var name = STA.NAME;
    var ICAO = STA.ICAO;
    var IATA = STA.IATA;

    var station = document.createElement("div")
    station.id = ICAO;
    station.innerText = name + " " + ICAO + " " + IATA;
    station.name = name + " " + ICAO + " " + IATA;
    station.onclick = function(){getJSON(build_report,"get_metar","code=" + ICAO, rtype="POST")};
    station.setAttribute('class',"list-group-item list-group-item-action")

    return station;

};

function build_report(response){
    //add a metar to the watch list

    wl = wl.filter(report => report.ICAO != response.ICAO);
    

    if (!response.ERROR){
        //if the server doesn't send back an error, build a a report
        //and push it to the watch list (wl)
        var report = {
            "ICAO": response.ICAO,
            "RAW" : response.RAW,
            "CX" : response.CX,
            "VIS": response.VIS,
            "WIND": response.WIND,
            "timer": setTimeout(function() {
                                    //refresh the report every "time interval"
                                    getJSON(build_report,"get_metar","code=" + response.ICAO, rtype="POST")
                                            
                                        },time_interval),
            "last_called" : new Date().toUTCString()
        }

        wl.push(report); //now push it to the watch list
        populate_wld();

    } else {
        //If you get an error, change the station div to indicate something didn't go right
        //Then tell the user.
        var station = document.getElementById(response.ICAO);

        station.setAttribute('class', "list-group-item list-group-item-action list-group-item-danger");
        station.innerText = "Report unavailable. " + response.ERROR_TYPE;
        
        setTimeout(function(){ 
                station.setAttribute('class', "list-group-item list-group-item-action");
                station.innerText = station.name;                
            }, 1000); //getting the perfect timing right for this is kind of funny - I'm not sure what i want to do here yet
    };
}

function populate_wld(){
    //populate the watch_list_div

    wld.innerHTML = ""; //clear out the HTML in there

    for (var i = 0; i < wl.length; i++) {
        wld.appendChild(make_metar(wl[i]));
    };

}

function make_metar(RPT){
    //this is kind of mess, I could probably make this cleaner and refactor some of this code


    //make a metar div

    var report = document.createElement("div");
    var raw_container = document.createElement("div");
    var flight_rules_container = document.createElement("div");
    var flight_rules_h3 = document.createElement("h3");
    var last_refresh = document.createElement("p");
    var x = document.createElement("a") //this will be what closes the box on click
    x.innerText = "close"; //close button
    x.setAttribute("href","#");
    x.setAttribute("class", "btn btn-outline-dark btn-sm");
    raw_container.setAttribute("class","list-group-item")
    flight_rules_container.setAttribute("class", "list-group-item")

    report.appendChild(x)
    report.appendChild(flight_rules_container);
    flight_rules_container.appendChild(flight_rules_h3);
    flight_rules_container.appendChild(last_refresh);
    report.appendChild(raw_container);


    //this whole section is just...the worst.  I apologize.  I guess it works right now.
    //clean this shit up.
    var name = RPT.NAME;
    var ICAO = RPT.ICAO;
    var RAW = RPT.RAW;
    var CX = RPT.CX;
    var VIS = RPT.VIS;
    var WIND = RPT.WIND;
    var FLIGHT_RULES = "UNAVAILABLE";
    last_refresh.innerText = "Last Refresh:  " + RPT.last_called;


    if (CX > 3000 && VIS > 5){
        FLIGHT_RULES = "VFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-success")

    }

    if (CX <= 3000 || VIS <= 5){
        FLIGHT_RULES = "MVFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-primary")

    }

    if (CX < 1000 || VIS <3){
        FLIGHT_RULES = "IFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-warning")

    }

    if (CX < 500 || VIS <= 2 ){
        FLIGHT_RULES = "LIFR";
        report.setAttribute('class',"list-group-item list-group-item-action list-group-item-danger") 
    }
    
    report.id = ICAO + "_metar";
    flight_rules_h3.innerText = "Flight Rules:  " + FLIGHT_RULES;
    raw_container.innerText = RAW;


    x.onclick = function(){
                                //get rid of the timer
                                clearTimeout(RPT.timer);
                                delete RPT.timer; //be extra sure
                                
                                //remove the object, then repopulate the list
                                wl = wl.filter(report => report.ICAO != ICAO);
                                populate_wld();
                            };


    return report;

};

function unhide(){
    //unhide stations on change
    
    var input = document.getElementById("search_box");
    var filter = input.value.toUpperCase();
    var div;
    station_list = sld.getElementsByTagName('div');

    // Loop through all list items, and hide those who don't match the search query

    for (var i = 0; i < station_list.length; i++) {
        div = station_list[i];
        if (div.name.toUpperCase().indexOf(filter) > -1) {
            div.style.display = "";
        } else {

            div.style.display = "none";}
    }
    
    input.focus();
    input.scrollIntoView();
}

//first query the server for the station list
getJSON(populate,'get_stations');

