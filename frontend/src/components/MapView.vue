<template>
  <div class="container d-flex align-stretch bg-light" style="flex: 1">
    <div id="mapContainer"></div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
//import 'leaflet';
export default {
  name: "MapView",
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 10,
      center: [51.966, 7.633],
      markerLatLng: [51.504, -0.159],
      map: null,
      tileLayer: null,
      colorblindLayer: null,
    };
  },
  methods: {
    initMap: function () {
      this.map = L.map("mapContainer", {
        layers: this.tileLayer,
        zoomControl: false,
      }).setView(this.center, this.zoom);

      // To make sure, that the two basement options lie underneath the outputlayers which should be visualized,
      // a Pane with a z-Index gets created, which makes sure they will always lie underneath.
      //this.map.createPane("basemap");
      //this.map.getPane("basemap").style.zIndex = 10;
      // To keep sure the tiles are not able to grab this line gets added.
      //this.map.getPane("basemap").style.pointerEvents = "none";

      const osmUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
      const osmAttr =
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

      const colorblindUrl =
        "https://tile.jawg.io/e05fd39a-c48d-4fe7-865e-75b940afcb34/{z}/{x}/{y}{r}.png?access-token=f8JszPWTpbAxBEKElUVA7DJcC7Rrzg8hm36s98r2dV7SFWWvoP6v0E9BTxGttjZZ";
      const colorblindAttr =
        '<a href="https://www.jawg.io" target="_blank">&copy; Jawg</a> - <a href="https://www.openstreetmap.org" target="_blank">&copy; OpenStreetMap</a>&nbsp;contributors';

      this.tileLayer = L.tileLayer(osmUrl, {
        attribution: osmAttr,
        //pane: "basemap", // Both layers are added to the basemap-pane.
      }).addTo(this.map);

      this.colorblindLayer = L.tileLayer(colorblindUrl, {
        attribution: colorblindAttr,
        //subdomains: "abcd",
      });

      const basemaps = {
        "Open Street Map": this.tileLayer,
        "Colorblind map": this.colorblindLayer,
      };
      L.control.layers(basemaps).addTo(this.map);
      
      L.control
        .zoom({
          position: "topright",
        })
        .addTo(this.map);

      
    },
  },
  props:{
    geojson:{type:Object,
    default(){return{
      "crs": {
        "properties": {
          "name": "urn:ogc:def:crs:EPSG::3857"
        },
        "type": "name"
      },
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  831978.0122,
                  6810985.9256
                ],
                [
                  831978.0122,
                  6771275.9256
                ],
                [
                  865438.0122,
                  6771275.9256
                ],
                [
                  865438.0122,
                  6810985.9256
                ],
                [
                  831978.0122,
                  6810985.9256
                ]
              ]
            ],
            "type": "Polygon"
          },
          "properties": {
            "DN": 0.0
          },
          "type": "Feature"
        }
      ],
      "name": "test",
      "type": "FeatureCollection"
    }}}
  },
  mounted() {
    this.initMap();
  },
  watch:{
    geojson: function(newGeojson){ // TODO: when the object changes add it to the map
      var a=JSON.parse(JSON.stringify(newGeojson))
      console.log(a);
      //L.geoJSON(a).addTo(this.map); // add the geojson object to the map
      // TOmaybeDO: adjust the bounds to the size of the geojson
      // this.map.fitBounds(geoLayer.getBounds())
    }
  }
  
};
</script>

<style scoped>
#mapContainer {
  width: 100%;
  height: 350px;
}
@media (min-width: 1264px) {
  .wrapper {
    flex: 1;
    min-height: 0;
  }
  #mapContainer {
    width: 100%;
    height: 100%;
  }
}
</style>
