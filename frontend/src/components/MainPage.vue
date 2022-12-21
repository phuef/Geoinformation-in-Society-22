<template>
  <v-container
    id="mainContainer"
    class="fill-height"
    fluid
    style="height: 100vh"
  >
    <v-row no-gutters class="fill-height" style="height: 100%">
      <v-col cols="12" xs="12" sm="6" v-if="showMenu">
        <MenuView
          @newRequest="processNewRequest"
          @isMinOfSliderHasChanged="changeSlidersIsMinState"
          @clearMap="processNewRequest"
          :sliders="sliders"
        />
      </v-col>
      <v-col cols="12" xs="12" :sm="mapViewSize">
        <div id="mapContainer" :key="mapViewSize">
          <div class="d-none d-sm-flex align-items-center" id="iconContainer">
            <v-icon v-if="showMenu" @click="handleClick" id="collapseIcon">
              mdi-menu-left</v-icon
            >
            <v-icon v-if="!showMenu" @click="handleClick" id="openIcon">
              mdi-menu-right</v-icon
            >
          </div>
          <MapView
            :geojson="requestResponse"
            :center="mapCenterPoint"
            :zoom="mapZoom"
            ref="map"
            :busGeojson="busGeojson"
          />
          <div
            class=""
            style="
              z-index: 9999;
              position: absolute;
              padding-left: 12px;
              padding-top: 12px;
            "
          >
            <v-tooltip right z-index="1000">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  elevation="0"
                  style="
                    background-color: white;
                    border: 2px solid rgba(150, 150, 150, 0.5);
                    -webkit-background-clip: padding-box; /* for Safari */
                    width: 54px;
                    height: 54px;
                    padding: 0px;
                  "
                  v-bind="attrs"
                  v-on="on"
                  @click="doBusRequest()"
                >
                  <v-icon> mdi-bus-stop </v-icon>
                </v-btn>
              </template>
              <span v-html="'Show / Remove<br\>bus stops'"></span>
            </v-tooltip>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MapView from "./MapView.vue";
// eslint-disable-next-line
import MenuView from "./MenuView.vue";

export default {
  name: "MainPage",
  components: {
    MapView,
    // eslint-disable-next-line
    MenuView,
  },
  data() {
    return {
      showMenu: true,
      requestResponse: null,
      sliders: [
        // All availabe sliders
        // TODO: add new layers to this list, when new layers are added to the backend.
        //       The layers need to have the structure shown and explained below
        {
          name: "Museums", // the layer name that gets displayed at the layer selection
          label: "Distance to museums", // the label that gets shown at the slider
          value: 250, // the value the slider has
          band: 0, // the corresponding band ID the layer has in the backend
          active: true, // wether the layer is currently selected by the user
          // the text that shall be displayed when the user hovers over the info button
          infoLabel:
            "Move the slider to remove all areas <br/>that have a certain <b>distance to museums</b>.",
          icon: "mdi-bank",
          isMin: true,
        },
        {
          name: "Theaters",
          label: "Distance to theaters",
          value: 1000,
          band: 1,
          active: true,
          infoLabel:
            "Move the slider to remove all areas <br/>that have a certain <b>distance to theaters</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
        },
      ],
      mapBounds: null,
      mapCenterPoint: [51.96229626341511, 7.6256090207326395],
      mapZoom: 10,
      busGeojson: null,
    };
  },
  computed: {
    mapViewSize: function () {
      // makes sure that the map is displayed on the full screen when the menu is not shown
      return this.showMenu ? "6" : "12";
    },
  },
  methods: {
    processNewRequest: function (response) {
      this.requestResponse = response;
    },
    changeSlidersIsMinState: function (sliderName) {
      for (var i in this.sliders) {
        if (this.sliders[i].name == sliderName) {
          this.sliders[i].isMin = !this.sliders[i].isMin;
        }
      }
    },
    handleClick: function () {
      this.calculateCenterPoint();
      this.getMapZoom();
      this.showMenu = !this.showMenu;
    },
    calculateCenterPoint: function () {
      this.mapBounds = this.$refs.map.getMapBounds();
      if (this.showMenu) {
        this.mapCenterPoint = [
          this.mapBounds.getSouth() +
            (this.mapBounds.getNorth() - this.mapBounds.getSouth()) / 2,
          this.mapBounds.getWest(),
        ];
      } else {
        this.mapCenterPoint = [
          this.mapBounds.getSouth() +
            (this.mapBounds.getNorth() - this.mapBounds.getSouth()) / 2,
          this.mapBounds.getWest() +
            (3 * (this.mapBounds.getEast() - this.mapBounds.getWest())) / 4,
        ];
      }
    },
    getMapZoom: function () {
      this.mapZoom = this.$refs.map.getMapZoom();
    },
    async doBusRequest() {
      // the request to the backend to retrieve the areas that meet the current conditions (configured by the user)
      const busResponse = await fetch(
        "https://rest.busradar.conterra.de/prod/haltestellen"
      );
      this.busGeojson = await busResponse.json();
      this.busResponse = this.busGeojson;
      //console.log(JSON.parse(JSON.stringify(this.busGeojson)));
    },
  },
  mounted() {
    this.calculateCenterPoint();
    this.getMapZoom();
  },
};
</script>

<style scoped>
#iconContainer {
  margin: 0;
  position: absolute;
  top: 45%;
}
#mainContainer {
  padding: 0px;
  width: 100%;
}
#mapContainer {
  height: 100%;
}
#collapseIcon,
#openIcon {
  padding: 0px;
  margin: left;
  border-radius: 4px;
  width: 15px;
  height: 80px;
  background-color: white;
  opacity: 0.8;
  border: 1px solid grey;
  z-index: 9999;
}
</style>
