<template>
  <div
    class="container d-flex align-stretch bg-light"
    style="flex: 1; padding: 0px"
  >
    <div id="mapContainer"></div>
  </div>
</template>

<script>
// eslint-disable-next-line
import L, { featureGroup } from "leaflet";
import "leaflet/dist/leaflet.css";
delete L.Icon.Default.prototype._getIconUrl;
// required, cause otherwise the marker icons (icon itself and shadow) are not available
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "MapView",
  data() {
    return {
      //zoom: 10,
      //center: [51.96229626341511, 7.6256090207326395], // changed from the center coords from münster to some coords in the eastside because of map width 100 vw
      map: null,
      tileLayer: null,
      colorblindLayer: null,
      resultLayer: null,
      resultPane: null,
      geojsonFeature: {
        type: "Feature",
        properties: {
          name: "Coors Field",
          amenity: "Baseball Stadium",
          popupContent: "This is where the Rockies play!",
        },
        geometry: {
          type: "Point",
          coordinates: [7.62451171875, 51.96288477548509],
        },
      },
      resultJson: null,
      //busGeojsonParsed: null,
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
      this.map.createPane("basemap");
      this.map.getPane("basemap").style.zIndex = 10;
      // To keep sure the tiles are not able to grab this line gets added.
      this.map.getPane("basemap").style.pointerEvents = "none";

      const osmUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
      const osmAttr =
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

      const colorblindUrl =
        "https://tile.jawg.io/e05fd39a-c48d-4fe7-865e-75b940afcb34/{z}/{x}/{y}{r}.png?access-token=f8JszPWTpbAxBEKElUVA7DJcC7Rrzg8hm36s98r2dV7SFWWvoP6v0E9BTxGttjZZ";
      const colorblindAttr =
        '<a href="https://www.jawg.io" target="_blank">&copy; Jawg</a> - <a href="https://www.openstreetmap.org" target="_blank">&copy; OpenStreetMap</a>&nbsp;contributors';

      this.tileLayer = L.tileLayer(osmUrl, {
        attribution: osmAttr,
        pane: "basemap", // Both layers are added to the basemap-pane.
      }).addTo(this.map);

      this.colorblindLayer = L.tileLayer(colorblindUrl, {
        attribution: colorblindAttr,
      });

      const basemaps = {
        "Open Street Map": this.tileLayer,
        "Colorblind map": this.colorblindLayer,
      };

      this.resultLayer = L.geoJSON().addTo(this.map);
      if (this.resultJson != null) {
        this.resultLayer.addData(this.resultJson);
      }

      L.control.layers(basemaps).addTo(this.map);

      L.control
        .zoom({
          position: "topright",
        })
        .addTo(this.map);
    },
    changeGeojson: function (newGeojson) {
      this.resultJson = JSON.parse(JSON.stringify(newGeojson));
      try {
        this.map.removeLayer(this.resultLayer);
        this.resultLayer = L.geoJSON().addTo(this.map);
        this.resultLayer.addData(this.resultJson);
      } catch (error) {
        //pass
      }
    },
    getMapBounds: function () {
      return this.map.getBounds();
    },
    getMapZoom: function () {
      return this.map.getZoom();
    },
    showBusStations: function (geojsonString) {
      this.busGeojsonParsed = console.log(
        JSON.parse(JSON.stringify(geojsonString))
      );
    },
  },
  props: {
    geojson: {
      type: Object,
      default() {
        return {
          crs: "urn:ogc:def:crs:EPSG::3857",
          features: [],
          name: "test",
          type: "FeatureCollection",
        };
      },
    },
    center: {
      required: true,
      type: Array,
    },
    zoom: {
      required: true,
      type: Number,
    },
    busGeojson: {
      type: Object,
      default() {
        return {
          features: [],
          type: "FeatureCollection",
        };
      },
    },
  },
  mounted() {
    // Some error occurred by re-saving this file. The error said that the map was already initialized but this try-catch block solves it.
    try {
      this.initMap();
    } catch {
      // pass
    }

    this.changeGeojson(this.geojson);
    this.showBusStations(this.busGeojson);
  },
  watch: {
    geojson: function (newGeojson) {
      this.changeGeojson(newGeojson);
    },
    busGeojsonString: function (newBusGeojson) {
      this.showBusStations(newBusGeojson);
    },
  },
};
</script>

<style scoped>
#mapContainer {
  width: 100%;
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
