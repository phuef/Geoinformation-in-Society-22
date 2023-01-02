<template>
  <v-container id="mapContainer" fluid fill-height />
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import { GeoSearchControl, OpenStreetMapProvider } from "leaflet-geosearch";
import "leaflet-geosearch/dist/geosearch.css";
import "leaflet.locatecontrol";
import "leaflet.locatecontrol/dist/L.Control.Locate.min.css";

// Make marker icons available (icon itself and shadow)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "MapView",
  data() {
    return {
      map: null,
      tileLayer: null,
      colorblindLayer: null,
      drawLayer: new L.FeatureGroup(),
    };
  },
  props: {
    center: {
      required: true,
      type: Array,
    },
    zoom: {
      required: true,
      type: Number,
    },
    resultGeoJson: {
      type: Object,
    },
  },
  methods: {
    initMap: function () {
      this.map = L.map("mapContainer", {
        layers: this.tileLayer,
        zoomControl: false,
        attributionControl: false,
      }).setView(this.center, this.zoom);

      L.control.attribution({ prefix: false }).addTo(this.map);

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

      L.control.layers(basemaps).addTo(this.map);

      L.control
        .zoom({
          position: "topright",
        })
        .addTo(this.map);

      const searchProvider = new OpenStreetMapProvider();
      new GeoSearchControl({
        provider: searchProvider,
        style: "button",
        showMarker: false,
        autoCompleteDelay: 1000,
        autoClose: true,
      }).addTo(this.map);
      this.map.on("geosearch/showlocation", (event) => {
        const marker = event.marker;
        marker.on("move", () => {
          marker.off(); // remove address popup when marker is moved
        });
        marker.addTo(this.drawLayer);
      });

      L.control
        .locate({
          position: "topright",
          initialZoomLevel: 16,
          showPopup: false,
          strings: {
            title: "Show your location",
          },
        })
        .addTo(this.map);

      this.map.addLayer(this.drawLayer);
      const drawControl = new L.Control.Draw({
        draw: {
          polyline: false,
          circle: false,
          rectangle: false,
          circlemarker: false,
          polygon: {
            shapeOptions: {
              color: "#00ffdd",
            },
          },
        },
        edit: {
          featureGroup: this.drawLayer,
        },
      });
      this.map.addControl(drawControl);
      this.map.on(L.Draw.Event.CREATED, (event) => {
        this.drawLayer.addLayer(event.layer);
      });
      this.map.setMaxBounds([
        [52.060024427, 7.473785644],
        [51.840134598, 7.774359118],
      ]);
      this.map.setMinZoom(12);
    },
    updateResultLayer: function (newGeoJson) {
      newGeoJson = JSON.parse(JSON.stringify(newGeoJson));
      this.resultLayer.clearLayers();
      try {
        this.resultLayer.addData(newGeoJson);
      } catch (error) {
        console.warn(error);
      }
    },
    getMapBounds: function () {
      return this.map.getBounds();
    },
    getMapZoom: function () {
      return this.map.getZoom();
    },
    updateOnResize: function (pixelOffset = [0, 0]) {
      // Move the map so that it stays in the same place on the screen
      this.map.panBy(pixelOffset, { animate: false });
      // Load newly visible tiles
      this.map.invalidateSize({ pan: false });
    },
  },
  watch: {
    resultGeoJson: function (newGeoJson) {
      this.updateResultLayer(newGeoJson);
    },
  },
  mounted() {
    this.initMap();
    if (this.resultGeoJson) {
      this.updateResultLayer(this.resultGeoJson);
    }
  },
};
</script>

<style scoped></style>
