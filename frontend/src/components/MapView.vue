<template>
  <div class="container d-flex align-stretch bg-light" style="flex: 1">
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
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 10,
      center: [51.966, 7.633],
      markerLatLng: [51.504, -0.159],
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
  props: {
    geojson: {
      type: Object,
      default() {
        return {
          crs: {
            properties: {
              name: "urn:ogc:def:crs:EPSG::3857",
            },
            type: "name",
          },
          features: [
            {
              geometry: {
                coordinates: [
                  [
                    [7.62451171875, 51.96288477548509],
                    [7.595750026234441, 51.96942882531462],
                  ],
                ],
                type: "Polygon",
              },
              properties: {
                DN: 0.0,
              },
              type: "Feature",
            },
          ],
          name: "test",
          type: "FeatureCollection",
        };
      },
    },
  },
  mounted() {
    this.initMap();
    console.log(this.map);
  },
  watch: {
    geojson: function (newGeojson) {
      // TODO: when the object changes add it to the map
      var geojsonColl = JSON.parse(JSON.stringify(newGeojson));
      //var geojsonColl = JSON.parse(JSON.stringify(this.geojsonFeature));
      console.log(geojsonColl);
      console.log(this.geojsonFeature);
      //this.map.createPane("results");
      //this.map.getPane("results").style.zIndex = 15;
      this.resultLayer = L.geoJSON().addTo(this.map);
      this.resultLayer.addData(geojsonColl);

      // TOmaybeDO: adjust the bounds to the size of the geojson
      //this.map.fitBounds(geoLayer.getBounds());
    },
  },
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
