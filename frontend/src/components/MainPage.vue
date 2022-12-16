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
          <MapView :geojson="requestResponse" ref="map" />
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
          value: 2000, // the value the slider has
          band: 0, // the corresponding band ID the layer has in the backend
          active: true, // wether the layer is currently selected by the user
          // the text that shall be displayed when the user hovers over the info button
          infoLabel:
            "Move the slider to remove all areas <br/>that have a certain <b>distance to museums</b>.",
        },
        {
          name: "Theaters",
          label: "Distance to theaters",
          value: 2000,
          band: 1,
          active: true,
          infoLabel:
            "Move the slider to remove all areas <br/>that have a certain <b>distance to theaters</b>.",
        },
      ],
      mapBounds: null,
      mapCenterPoint: [51.96229626341511, 7.6256090207326395],
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

    handleClick: function () {
      this.calculateCenterPoint();
      this.showMenu = !this.showMenu;
    },
    calculateCenterPoint: function () {
      this.mapBounds = this.$refs.map.getMapBounds();
      console.log(this.mapBounds);
      console.log(this.mapBounds.getSouth());
      console.log(this.mapBounds.getNorth());
      console.log(this.mapBounds.getEast());
      console.log(this.mapBounds.getWest());
      if (this.showMenu) {
        this.mapCenterPoint = [
          this.mapBounds.getSouth() +
            (this.mapBounds.getNorth() - this.mapBounds.getSouth()) / 2,
          this.mapBounds.getWest(),
        ];
        console.log("with menu ");
      } else {
        this.mapCenterPoint = [
          this.mapBounds.getSouth() +
            (this.mapBounds.getNorth() - this.mapBounds.getSouth()) / 2,
          this.mapBounds.getWest() +
            (3 * (this.mapBounds.getEast() - this.mapBounds.getWest())) / 4,
        ];
        console.log("without menu ");
      }

      // should be the middle height of left border or middle hight of right halfs middle. depending on mapviewsize

      console.log(this.mapCenterPoint);
    },
  },
  mounted() {
    this.calculateCenterPoint();
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
