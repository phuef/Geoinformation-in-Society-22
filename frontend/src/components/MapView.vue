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
// For the marker clustering
import "leaflet.markercluster/dist/leaflet.markercluster.js";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
// Extension to support multiple layers
import "leaflet.markercluster.layersupport"; ///leaflet.markercluster.layersupport-src.js";
import "@gnatih/leaflet.legend/src/leaflet.legend.css";
import "@gnatih/leaflet.legend/src/leaflet.legend.js";

// Make marker icons available (icon itself and shadow)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});
import busMarker from "@/assets/haltestellen_icon.png";
import trainMarker from "@/assets/train_icon.png";
import trainJson from "@/data/trains.json";
import locationMarker from "@/assets/marker-icon.png";

export default {
  name: "MapView",
  emits: ["setBusStationsVisibility"],
  data() {
    return {
      map: null,
      tileLayer: null,
      mapLegend: null,
      legendElements: [],
      colorblindLayer: null,
      sliderFeaturesLayers: new Map(),
      busLayer: null,
      trainLayer: null,
      trainJson: null,
      busLayerMarkerCluster: null,
      trainLayerMarkerCluster: null,
      resultLayer: null,
      drawLayer: new L.FeatureGroup(),
      layerControl: null,
      busStationInfo: null,
      colorblindMode: false,
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
    sliderFeatures: {
      type: Map,
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

      // Required to use this in the event listeners:
      const ref = this;

      this.tileLayer = L.tileLayer(osmUrl, {
        attribution: osmAttr,
        pane: "basemap", // Both layers are added to the basemap-pane.
      })
        .on("add", function () {})
        .addTo(this.map);

      this.colorblindLayer = L.tileLayer(colorblindUrl, {
        attribution: colorblindAttr,
      })
        .on("add", function () {
          ref.resultLayer.setStyle({
            fillColor: "red",
            color: "red",
          });
          ref.colorblindMode = true;
        })
        .on("remove", function () {
          ref.resultLayer.setStyle({
            fillColor: "rgb(51,136,255)",
            color: "rgb(51,136,255)",
          });
          ref.colorblindMode = false;
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
        this.legendElements.push({
          label: "Location marker",
          type: "image",
          url: locationMarker,
          weight: 2,
        });
      });
      this.map.on(L.Draw.Event.DELETED, () => {
        if (this.drawLayer.getLayers().length == 0) {
          const i = this.legendElements.findIndex(
            (legendElement) => legendElement.label === "Location marker"
          );
          this.legendElements.splice(i, 1);
        }
      });

      this.map.setMaxBounds([
        [52.060024427, 7.473785644],
        [51.840134598, 7.774359118],
      ]);
      this.map.setMinZoom(12);

      this.legendElements.push({
        label: "Area matching your desires",
        type: "rectangle",
        color: "rgb(51,136,255)",
        fillColor: "rgb(51,136,255)",
        fillOpacity: 0.5,
        weight: 3,
      });
    },
    updateResultLayer: function (newGeoJson) {
      newGeoJson = JSON.parse(JSON.stringify(newGeoJson));
      this.resultLayer.clearLayers();
      try {
        this.resultLayer.addData(newGeoJson);
        if (this.colorblindMode) {
          this.resultLayer.setStyle({
            fillColor: "red",
            color: "red",
          });
        } else {
          this.resultLayer.setStyle({
            fillColor: "rgb(51,136,255)",
            color: "rgb(51,136,255)",
          });
        }
      } catch (error) {
        console.warn(error);
      }
    },
    updateSliderFeatures: function () {
      // Because there is no easy way to watch changes of Map data structures with Vue 2
      // this function needs to be called manually
      const newKeys = Array.from(this.sliderFeatures.keys());
      const previousKeys = Array.from(this.sliderFeaturesLayers.keys());
      const addedKeys = newKeys.filter((key) => !previousKeys.includes(key)); // Newly added keys
      const deletedKeys = previousKeys.filter((key) => !newKeys.includes(key)); // Deleted keys
      // Add layers for new keys and geoJSON features
      for (const key of addedKeys) {
        const iconUrl = `map_icons/${key}_icon.png`;
        const featureLayer = L.geoJSON(this.sliderFeatures.get(key), {
          pointToLayer: function (_geoJsonPoint, latlng) {
            return L.marker(latlng, {
              icon: L.icon({
                iconUrl,
                iconSize: [16, 16],
              }),
              alt: `${key} point`,
              keyboard: false,
            });
          },
          interactive: false,
        });
        this.sliderFeaturesLayers.set(key, featureLayer);
        this.map.addLayer(featureLayer);
      }
      // Remove layers for deleted keys
      for (const key of deletedKeys) {
        this.map.removeLayer(this.sliderFeaturesLayers.get(key));
        this.sliderFeaturesLayers.delete(key);
      }
    },
    addBusLayer: function () {
      const busIcon = L.icon({
        iconUrl: busMarker,
        iconSize: [20, 20],
      });
      this.trainJson = JSON.parse(JSON.stringify(trainJson));
      const trainIcon = L.icon({
        iconUrl: trainMarker,
        iconSize: [30, 30],
      });
      this.trainLayer = L.geoJSON(this.trainJson, {
        pointToLayer: function (_feature, latlng) {
          return L.marker(latlng, { icon: trainIcon }).on(
            "click",
            async function () {
              let popup = `<h1>Train station: ${_feature.properties.name}</h1>`;
              this.bindPopup(popup);
            }
          );
        },
        onEachFeature: function (_feature, layer) {
          layer.bindPopup();
        },
      });

      this.busLayer = L.geoJSON(undefined, {
        pointToLayer: function (_feature, latlng) {
          return L.marker(latlng, { icon: busIcon }).on(
            "click",
            async function () {
              const stationResponse = await fetch(
                "https://rest.busradar.conterra.de/prod/haltestellen/" +
                  _feature.properties.nr +
                  "/abfahrten"
              );
              this.busStationInfo = await stationResponse.json();
              let popup =
                `<h1>${_feature.properties.lbez}</h1>` +
                `<p><h4>Direction (german): </h4>${_feature.properties.richtung}` +
                `</br></br><h4>Next departures:</h4>`;

              if (this.busStationInfo.length == 0) {
                popup += "There are <b>no departures</b> the next time.</p>";
              } else {
                popup += "<br>";
              }
              for (let i = 0; i < this.busStationInfo.length; i++) {
                const plannedDeparture = new Date(
                  this.busStationInfo[i].ankunftszeit * 1000
                );
                let plannedAM_PM;
                if (plannedDeparture.getHours() > 12) {
                  plannedAM_PM = "pm";
                } else {
                  plannedAM_PM = "am";
                }
                let plannedDepartureMinute;
                if (plannedDeparture.getMinutes() < 10) {
                  plannedDepartureMinute = "0" + plannedDeparture.getMinutes();
                } else {
                  plannedDepartureMinute = plannedDeparture.getMinutes();
                }

                const actualDeparture = new Date(
                  this.busStationInfo[i].tatsaechliche_ankunftszeit * 1000
                );
                let actualAM_PM;
                if (actualDeparture.getHours() > 12) {
                  actualAM_PM = "pm";
                } else {
                  actualAM_PM = "am";
                }
                let actualDepartureMinute;
                if (actualDeparture.getMinutes() < 10) {
                  actualDepartureMinute = "0" + actualDeparture.getMinutes();
                } else {
                  actualDepartureMinute = actualDeparture.getMinutes();
                }
                popup +=
                  `<li> ${this.busStationInfo[i].linienid} ${this.busStationInfo[i].richtungstext}:` +
                  `<br> Planned: <b> ${plannedDeparture.getHours()}:${plannedDepartureMinute} ${plannedAM_PM} </b>` +
                  `| Actually: <b>${actualDeparture.getHours()}:${actualDepartureMinute} ${actualAM_PM}</b></li>`;
              }
              this.bindPopup(popup);
            }
          );
        },
        onEachFeature: function (_feature, layer) {
          layer.bindPopup();
        },
      });

      this.busLayerMarkerCluster = L.markerClusterGroup.layerSupport({
        polygonOptions: {
          fillColor: "#245fb3", // polygon color
          color: "#245fb3", // line color
          opacity: 1, // opacity of line
          weight: 3, // line thickness
          fillOpacity: 0.2, // opacity inside polygon
        },
      });
      this.busLayerMarkerCluster.checkIn([this.busLayer, this.trainLayer]);
      this.trainLayer.addTo(this.map);
      this.busLayer.addTo(this.map);

      this.layerControl.addOverlay(
        this.busLayerMarkerCluster,
        "Public transport"
      );
      this.map.on("overlayadd", (event) => {
        if (event.name === "Public transport")
          this.$emit("setBusStationsVisibility", true);
      });
      this.map.on("overlayremove", (event) => {
        if (event.name === "Public transport")
          this.$emit("setBusStationsVisibility", false);
      });
    },
    updateBusLayer: function (newGeoJson) {
      // Refresh bus layer
      newGeoJson = JSON.parse(JSON.stringify(newGeoJson));
      this.busLayer.clearLayers();
      this.busLayer.addData(newGeoJson);
      // Refresh marker cluster layer
      this.busLayerMarkerCluster.checkIn([this.busLayer, this.trainLayer]);
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
        this.legendElements.push({
          label: "Bus stations",
          type: "image",
          url: busMarker,
          weight: 2,
        });
      } else {
        if (this.map.hasLayer(this.busLayerMarkerCluster))
          this.map.removeLayer(this.busLayerMarkerCluster);
        const i = this.legendElements.findIndex(
          (legendElement) => legendElement.label === "Bus stations"
        );
        this.legendElements.splice(i, 1);
      }
    },
    legendElements: function (value) {
      try {
        this.mapLegend.remove();
      } catch {
        //pass
      }
      this.mapLegend = L.control
        .Legend({
          position: "bottomright",
          legends: value,
          symbolWidth: 20,
          symbolHeight: 20,
          collapsed: true,
        })
        .addTo(this.map);
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

<style>
.leaflet-legend-item i {
  display: flex;
  justify-content: center;
  padding-right: 10px;
}
.leaflet-legend-item img {
  position: unset;
}
.leaflet-legend-column {
  margin-left: 5px;
}
</style>
