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
import "leaflet.markercluster/dist/leaflet.markercluster.js";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

// Make marker icons available (icon itself and shadow)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});
import busMarker from "@/assets/alpha-b-circle-outline-dark-grey.png";

export default {
  name: "MapView",
  emits: ["setBusStationsVisibility"],
  data() {
    return {
      map: null,
      tileLayer: null,
      colorblindLayer: null,
      busLayer: null,
      busLayerMarkerCluster: null,
      resultLayer: null,
      drawLayer: new L.FeatureGroup(),
      layerControl: null,
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
    resultAreas: {
      type: Object,
    },
    busStations: {
      type: Object,
    },
    showBusStations: {
      required: true,
      type: Boolean,
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

      this.layerControl = L.control.layers(basemaps).addTo(this.map);

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
          position: "topleft",
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
          polygon: false,
        },
        edit: {
          featureGroup: this.drawLayer,
          edit: false,
        },
      });
      this.map.addControl(drawControl);
      this.map.on(L.Draw.Event.CREATED, (event) => {
        this.drawLayer.addLayer(event.layer);
      });
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
    addBusLayer: function () {
      const busIcon = L.icon({
        iconUrl: busMarker,
        iconSize: [15, 15],
      });
      this.busLayer = L.geoJSON(undefined, {
        pointToLayer: function (_feature, latlng) {
          return L.marker(latlng, { icon: busIcon });
        },
      });
      this.busLayerMarkerCluster = L.markerClusterGroup({
        polygonOptions: {
          fillColor: "#245fb3", // polygon color
          color: "#245fb3", // line color
          opacity: 1, // opacity of line
          weight: 3, // line thickness
          fillOpacity: 0.2, // opacity inside polygon
        },
      }).addLayer(this.busLayer);
      this.layerControl.addOverlay(this.busLayerMarkerCluster, "Bus stations");
      this.map.on("overlayadd", (event) => {
        if (event.name === "Bus stations")
          this.$emit("setBusStationsVisibility", true);
      });
      this.map.on("overlayremove", (event) => {
        if (event.name === "Bus stations")
          this.$emit("setBusStationsVisibility", false);
      });
    },
    updateBusLayer: function (newGeoJson) {
      // Refresh bus layer
      newGeoJson = JSON.parse(JSON.stringify(newGeoJson));
      this.busLayer.clearLayers();
      this.busLayer.addData(newGeoJson);
      // Refresh marker cluster layer
      this.busLayerMarkerCluster.clearLayers();
      this.busLayerMarkerCluster.addLayer(this.busLayer);
    },
    updateOnResize: function (pixelOffset = [0, 0]) {
      // Move the map so that it stays in the same place on the screen
      this.map.panBy(pixelOffset, { animate: false });
      // Load newly visible tiles
      this.map.invalidateSize({ pan: false });
    },
  },
  watch: {
    resultAreas: function (value) {
      if (value) {
        this.updateResultLayer(value);
      } else {
        this.resultLayer.clearLayers();
      }
    },
    busStations: function (newBusGeoJson) {
      if (newBusGeoJson) {
        this.updateBusLayer(newBusGeoJson);
      }
    },
    showBusStations: function (value) {
      if (value) {
        if (!this.map.hasLayer(this.busLayerMarkerCluster))
          this.map.addLayer(this.busLayerMarkerCluster);
      } else {
        if (this.map.hasLayer(this.busLayerMarkerCluster))
          this.map.removeLayer(this.busLayerMarkerCluster);
      }
    },
  },
  mounted() {
    // Initialization
    this.initMap();
    this.addBusLayer();

    if (this.resultAreas) {
      this.updateResultLayer(this.resultAreas);
    }
  },
};
</script>

<style scoped></style>
