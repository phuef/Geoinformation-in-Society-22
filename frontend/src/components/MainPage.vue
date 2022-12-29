<template>
  <v-container
    id="mainContainer"
    class="fill-height"
    fluid
    style="height: 100vh"
  >
    <v-row no-gutters class="fill-height" style="height: 100%">
      <v-col cols="12" xs="12" sm="6" v-show="showMenu">
        <v-btn class="ms-3" @click="startTour()"> Start Demo </v-btn>
        <MenuView
          ref="menu"
          @newRequest="processNewRequest"
          @isMinOfSliderHasChanged="changeSlidersIsMinState"
          @clearMap="processNewRequest"
          :sliders="sliders"
        />
      </v-col>
      <v-col cols="12" xs="12" :sm="mapViewSize">
        <div data-v-step="2" id="mapContainer" :key="mapViewSize">
          <div class="d-none d-sm-flex align-items-center" id="iconContainer">
            <v-icon v-if="showMenu" @click="toggleMenu" id="collapseIcon">
              mdi-menu-left
            </v-icon>
            <v-icon v-if="!showMenu" @click="toggleMenu" id="openIcon">
              mdi-menu-right
            </v-icon>
          </div>
          <MapView
            ref="map"
            :center="mapCenterPoint"
            :zoom="mapZoom"
            :result-geo-json="requestResponse"
          />
        </div>
      </v-col>
    </v-row>
    <v-tour name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>

<script>
import MapView from "./MapView.vue";
import MenuView from "./MenuView.vue";

export default {
  name: "MainPage",
  components: {
    MapView,
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
      steps: [
        {
          target: '[data-v-step="0"]', // We're using document.querySelector() under the hood
          header: {
            title: "Switch Layers",
          },
          content: `Click her to change the <strong>selected layers </strong>`,
        },
        {
          target: '[data-v-step="1"]',
          content: "Here are preconfigurations which you can choose from",
        },
        {
          target: '[data-v-step="2"]',
          content: "In the map you can see the visualised results ",
          params: {
            placement: "left", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
      ],
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
      for (const i in this.sliders) {
        if (this.sliders[i].name == sliderName) {
          this.sliders[i].isMin = !this.sliders[i].isMin;
        }
      }
    },
    toggleMenu: function () {
      const menuDim = [
        this.$refs.menu.$el.clientWidth,
        this.$refs.menu.$el.clientHeight,
      ];
      // Change menu visibility
      this.showMenu = !this.showMenu;
      this.$nextTick(() => {
        // When the menu visibility has changed, calculate the change in size
        const newMenuDim = [
          this.$refs.menu.$el.clientWidth,
          this.$refs.menu.$el.clientHeight,
        ];
        const menuDimChange = [
          newMenuDim[0] - menuDim[0],
          newMenuDim[1] - menuDim[1],
        ];
        // Get offset depending on menu position
        const requiredOffset = this.getMenuOffset(menuDimChange);
        // Update map
        this.$refs.map.updateOnResize(requiredOffset);
      });
    },
    getMenuOffset: function (dimChange) {
      let pixelOffset; // Here x, y coordinates!
      // TODO Set offset depending on menu position
      // this.$vuetify.breakpoint.sm
      const horizontalLayout = false;
      if (horizontalLayout) {
        // Menu on top
        pixelOffset = [0, dimChange[0]];
      } else {
        // Menu on the left side
        pixelOffset = [dimChange[0], 0];
      }
      return pixelOffset;
    },
    startTour() {
      this.$tours["myTour"].start();
    },
  },
};
</script>

<style scoped>
#iconContainer {
  margin: 0;
  position: absolute;
  top: 50%;
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
