<template>
  <div>
    <Header />
    <div class="main-div">
      <div id="map" class="map-div">
        <!-- map will be injected here :) -->
      </div>
      <div class="info-div">
        <div class="my-obj-div">
          <label class="label-heading">Your data</label>
          <div class="my-info-card card">
              <!-- oops! same code repeated, why dont you use a function ? -->
              <!-- yeah i'm lazy, Sorry! "dont argue just modify"-->
             <!--  make a list and iterate -->
            <p>
              <label class="label-inside">LAT {{ myFlyingObject.latitude }}</label>
            </p>
            <p>
              <label class="label-inside">LON {{ myFlyingObject.longitude }}</label>
            </p>
            <p>
              <label class="label-inside">ALT {{ myFlyingObject.altitude }}</label>
            </p>
            <p>
              <label class="label-inside">SPEED {{ myFlyingObject.speed }}</label>
            </p>
            <p>
              <label class="label-inside">ATM {{ myFlyingObject.pressure }}</label>
            </p>
          </div>
        </div>
        <div class="other-obj-div">
          <label class="label-heading">Nearby data</label>
          <div class="other-info-card card" v-bind:key="obj.id" v-for="obj in allOtherFlyingObjects">
            <p>
              <label class="label-inside">LAT {{ obj.latitude }}</label>
            </p>
            <p>
              <label class="label-inside">LON {{ obj.longitude }}</label>
            </p>
            <p>
              <label class="label-inside">ALT {{ obj.altitude }}</label>
            </p>
            <p>
              <label class="label-inside">SPEED {{ obj.speed }}</label>
            </p>
            <p>
              <label class="label-inside">ATM {{ obj.pressure }}</label>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

import mapboxgl from "mapbox-gl/dist/mapbox-gl.js";
import axios from 'axios';

import Header from "./Header"

import redDrone from "../assets/drones/redDrone.png";
import blackDrone from "../assets/drones/blackDrone.png";
import blueDrone from "../assets/drones/blueDrone.png";
import yellowDrone from "../assets/drones/yellowDrone.png";
import greenDrone from "../assets/drones/greenDrone.png";
import whiteDrone from "../assets/drones/whiteDrone.png";

mapboxgl.accessToken =
  "pk.eyJ1Ijoic2F1cmF2bmlyYXVsYSIsImEiOiJja2F5eHd2Y3AwOGMzMnNxYno3M2xmMXdkIn0.QeVxe4rfaHG4KsgQ7FbZqA";

var map = null;

export default {
  name: "Map",

  components: {
    Header
  },

  data() {
    return {
      channel_id: "",
      mapStyle: "mapbox://styles/mapbox/streets-v11",
      // center: [this.myFlyingObject.longitude, this.myFlyingObject.latitude],  // look at mounted
      zoom: 14, // mounted
      maxZoom: 19, // mounted
      offset: 0.01, // mounted  1 long ~= 110km
      droneColors: [
        // at returnFeatures
        "match",
        ["get", "eachColor"],
        "White",
        "whiteDrone",
        "Black",
        "blackDrone",
        "Blue",
        "blueDrone",
        "Green",
        "greenDrone",
        "Red",
        "redDrone",
        "Yellow",
        "yellowDrone",
        "#ccc", // but why ? > for declaring the type
      ],
      droneSize: ["match", ["get", "eachSize"], "others", 0.03, "mine", 0.05, 0], // at returnFeatures
    };
  },

  methods: {
    MapMain() {
      map.on("load", () => {
        // drones layer

        map.addSource("drones", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: this.returnDroneFeatures(this.allOtherFlyingObjects, this.myFlyingObject),
          },
        });

        map.addLayer({
          id: "drones",
          type: "symbol",
          source: "drones",
          layout: {
            "icon-image": this.droneColors,
            "icon-size": this.droneSize,
            "icon-allow-overlap": true,
          },
        });

        // restricted ares layer

        map.addSource("resAreas", {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: this.returnRestrictedAreasFeatures(this.restrictedAreas),
          },
        });
        map.addLayer({
          id: "resArea",
          type: "fill",
          source: "resAreas",
          layout: {},
          paint: {
            "fill-color": "#ff5500",
            "fill-opacity": 0.8,
          },
        });
      });
    },

    // when mouse enter event is called

    onMouseEnter() {

      var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: true,
      });



      var mouseEnter = (enterOn) => {
        
        map.on("mouseenter", enterOn, function(e) {
                    
          // Change the cursor style as a UI indicator.
        // map.getCanvas().style.cursor = "pointer";    // really ? aren't u kidding ? 
        
          // Change the cursor style as a UI indicator.
        // map.getCanvas().style.cursor = "pointer";    // really ? aren't u kidding ? 
        
        var coordinates = []

        if (enterOn == "drones") {     // ohh not again "extra code for handling two types of coords"
          coordinates = e.features[0].geometry.coordinates.slice();

        }
        else if(enterOn == "resArea") {
          let coordsList = e.features[0].geometry.coordinates[0]


          // to put popup on center of resarea "just ignore"

          let getLong = (coordsList[0][0] + coordsList[2][0]) / 2
          let getLat = (coordsList[0][1] + coordsList[2][1]) / 2

          coordinates = [getLong, getLat]

        }

        let description = e.features[0].properties.description;



        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup
          .setLngLat(coordinates)
          .setHTML(description)
          .addTo(map);
      });
      }

      mouseEnter("drones")
      mouseEnter("resArea")


    },

    // returns features according given allOtherFlyingObjects and myFlyingObjects

    returnDroneFeatures(objs, myobj) {
      var features = [];

      // other objects feature

      objs.forEach((obj) => {
        features.push({
          type: "Feature",
          properties: {
            eachColor: this.returnColor(obj.altitude),
            eachSize: "others",
            description: this.returnDroneDescription(obj),
          },
          geometry: {
            type: "Point",
            coordinates: [obj.longitude, obj.latitude],
          },
        });
      });

      // my obj feature

      features.push({
        type: "Feature",
        properties: {
          eachColor: this.returnColor(myobj.altitude),
          eachSize: "mine",
          description: this.returnDroneDescription(myobj),
        },
        geometry: {
          type: "Point",
          coordinates: [myobj.longitude, myobj.latitude],
        },
      });

      return features;
    },

    returnRestrictedAreasFeatures(areas) {
      var features = [];

      areas.forEach((area) => {
        features.push({
          type: "Feature",
          properties: {
            description: this.returnRestrictedAreasDescription(area),
          },
          geometry: {
            type: "Polygon",
            coordinates: [area.coordinates],
          },
        });
      });

      return features;
    },

    // returns color according to altitude

    returnColor(altitude) {
      if (altitude < 0) return "Black";
      else if (altitude >= 0 && altitude < 100) return "Blue";
      else if (altitude >= 100 && altitude < 200) return "Green";
      else if (altitude >= 200 && altitude < 300) return "Yellow";
      else return "Red";
    },

    // popUp message on hover

    returnDroneDescription(obj) {
      return `<strong>
                ${obj.name}
              </strong>
              <p>
                <strong>LAT</strong> ${obj.latitude}
              </p>
              <p>
                <strong>LON</strong> ${obj.longitude}
              </p>
              <p>
                <strong>ALT</strong> ${obj.altitude}
              </p>
              `;
    },

    returnRestrictedAreasDescription(obj) {
      return `<strong>
                Restricted Area
              </strong>
              <p>
                ${obj.type}
              </p>
              <p>
                ${obj.name}
              </p>
              `;
    },

    // loads image in mapbox

    loadImage(imageName, giveThisName) {
      map.loadImage(imageName, function(error, image) {
        if (error) throw error;
        map.addImage(giveThisName, image);
      });
    },
    socket_work(data){
      this.channel_id = data["_id"]
      console.log("Channel Id: "+data["_id"])
      var channel = new WebSocket('ws://' 
                                  + "68.183.89.213"
                                  + '/ws/connection/'
                                  + this.channel_id
                                  + '/')

      channel.onopen = function(){
        channel.send(JSON.stringify({"status": 20, "_id": this.channel_id, "latitude": 23.23232, "longitude": 23.23434234, "altitude": 234, "temperature": 34}))
      }

      channel.onmessage = function(e){
        console.log("message received");
        const data = JSON.parse(e.data);
        console.log(data)
      }
      
    }
  },

  computed: {
    ...mapGetters(["allOtherFlyingObjects", "myFlyingObject", "restrictedAreas"]),
  },

  created() {},

  mounted() {
    map = new mapboxgl.Map({
      container: "map",
      style: this.mapStyle,
      zoom: this.zoom,
      maxZoom: this.maxZoom,
      center: [this.myFlyingObject.longitude, this.myFlyingObject.latitude],
    });

    // boundary of map according to my drone center

    this.bounds = [   
      [this.myFlyingObject.longitude - this.offset, this.myFlyingObject.latitude - this.offset], // [west, south]
      [this.myFlyingObject.longitude + this.offset, this.myFlyingObject.latitude + this.offset], // [east, north]
    ];

    // this should be called every time socket sends data
    map.setMaxBounds(this.bounds); // just setting the boundaries (:

    // calls loadImage method and load Image giving a name "used in features"

    this.loadImage(redDrone, "redDrone");
    this.loadImage(whiteDrone, "whiteDrone");
    this.loadImage(blueDrone, "blueDrone");
    this.loadImage(greenDrone, "greenDrone");
    this.loadImage(blackDrone, "blackDrone");
    this.loadImage(yellowDrone, "yellowDrone");

    // calls Map on Load function

    this.MapMain();

    // calls Map onmouseenter

    this.onMouseEnter()


    axios
      .get('http://68.183.89.213/id')
      .then(response => (this.socket_work(response.data))) 
  },
};
</script>

<style scoped>
/* mapbox css */

.mapboxgl-popup {
  max-width: 400px;
  font: 12px/20px "Helvetica Neue", Arial, Helvetica, sans-serif;
}

.main-div {
  font-family: "Poppins", sans-serif;
  display: grid;
  grid-template-columns: 5fr 1fr;
  grid-column-gap: 10px;
  max-width: 100%;
  /* max-height: 90vh; */
  margin: 10px 10px 0 10px;
}

.map-div {
  max-height: 90vh;
}

.my-obj-div {
  margin: 10px 0 10px 0;
}

.info-div {
  background-color: rgb(255, 255, 255);
  border-radius: 5px;
  color: rgb(68, 68, 68);
  padding: 1px 1px 1px 1px;
  text-align: center;
}

.label-heading {
  color: black;
  font-size: 30px;
  font-weight: bold;
}

.card {
  padding: 10px 0 10px 0;
  border-radius: 5px;
}

.my-info-card {
  background-color: rgb(202, 202, 202);
  color: black;
  font-weight: 400;
  font-size: 18px;
}

.other-info-card {
  border: 1px solid rgb(255, 255, 255);
  background-color: rgb(228, 228, 228);
  margin: 2px;
  margin-bottom: 5px;
}

@media screen and (max-width: 1000px) {
  .main-div {
    display: block;
  }
  .map-div {
    max-height: 85vh;
    min-height: 80vh;
    margin-bottom: 10px;
  }
}

</style>
