<template>
  <v-container id="mainContainer" fluid fill-height>
    <v-row no-gutters class="fill-height" fluid>
      <v-col
        cols="12"
        sm="6"
        md="5"
        lg="4"
        xl="3"
        v-show="showMenu"
        :style="{
          height: menuHeight,
          maxHeight: menuHeight,
        }"
      >
        <div id="menuContainer" ref="menuContainer" fill-height fluid>
          <MenuView
            ref="menu"
            :resultAreasEmpty="resultAreasEmpty"
            :resultAreasRequestFailed="resultAreasRequestFailed"
            :sliders="sliders"
            :showBusStations="showBusStations"
            @requestResultAreas="requestResultAreas"
            @clearResultAreas="clearResultAreas"
            @setSliderActiveState="setSliderActiveState"
            @updateSliderValue="updateSliderValue"
            @updateSliderIsMin="updateSliderIsMin"
            @setSliderDisplay="setSliderDisplay"
            @setBusStationsVisibility="setBusStationsVisibility"
          />
        </div>
      </v-col>
      <v-col
        cols="12"
        :sm="showMenu ? 6 : 12"
        :md="showMenu ? 7 : 12"
        :lg="showMenu ? 8 : 12"
        :xl="showMenu ? 9 : 12"
        :style="{ height: menuHeight }"
      >
        <div id="mapViewContainer" data-v-step="2">
          <button
            id="menuButton"
            data-v-step="3"
            @click="toggleMenu"
            :style="menuButtonStyle"
          >
            <v-icon v-show="showMenu">mdi-menu-left</v-icon>
            <v-icon v-show="!showMenu">mdi-menu-right</v-icon>
          </button>
          <div
            data-v-step="6"
            style="position: absolute; z-index: 9999; right: 60px; height: 70px"
          ></div>
          <div
            data-v-step="7"
            style="
              position: absolute;
              right: 0;
              bottom: 0;
              margin: 25px;
              z-index: 9999;
              height: 40px;
            "
          ></div>
          <MapView
            ref="map"
            :center="mapCenterPoint"
            :zoom="mapZoom"
            :busStations="busStations"
            :resultAreas="resultAreas"
            :sliderFeatures="sliderFeatures"
            :showBusStations="showBusStations"
            @setBusStationsVisibility="setBusStationsVisibility"
          />
        </div>
      </v-col>
    </v-row>
    <v-tour z-index="1500" name="myTour" :steps="steps"></v-tour>
  </v-container>
</template>

<script>
import polygonSmooth from "@turf/polygon-smooth";
import simplify from "@turf/simplify";

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
      resultAreas: null,
      resultAreasEmpty: false,
      resultAreasRequestFailed: false,
      mapCenterPoint: [51.96229626341511, 7.6256090207326395],
      mapZoom: 13,
      sliderFeatures: new Map(),
      busStations: null,
      showBusStations: false,
      sliders: [
        // All available sliders
        // TODO: add new layers to this list, when new layers are added to the backend.
        //       The layers need to have the structure shown and explained below
        {
          id: "museums",
          name: "Museums", // the layer name that gets displayed at the layer selection
          label: "Distance to museums", // the label that gets shown at the slider
          value: 250, // the value the slider has
          band: 1, // the corresponding band ID the layer has in the backend
          active: true, // wether the layer is currently selected by the user
          // the text that shall be displayed when the user hovers over the info button
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around museums</b>.",
          icon: "mdi-bank",
          isMin: false,
          displayFeatures: true,
        },
        {
          id: "theaters",
          name: "Theaters",
          label: "Distance to theaters",
          value: 1000,
          band: 0,
          active: true,
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around theaters</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
          displayFeatures: true,
        },
        {
          id: "playgrounds",
          name: "Playgrounds",
          label: "Distance to playgrounds",
          value: 1000,
          band: 2,
          active: false,
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around playgrounds</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
          displayFeatures: false,
        },
        {
          id: "sportsplaces",
          name: "Sports facilities",
          label: "Distance to sports facilities",
          value: 1000,
          band: 3,
          active: false,
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around sports facilities</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
          displayFeatures: false,
        },
        {
          id: "baths",
          name: "Baths",
          label: "Distance to baths",
          value: 1000,
          band: 4,
          active: false,
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around baths</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
          displayFeatures: false,
        },
        {
          id: "cinemas",
          name: "Cinemas",
          label: "Distance to cinemas",
          value: 1000,
          band: 5,
          active: false,
          infoLabel:
            "Move the slider to include areas inside or outside<br/> a certain <b>distance around cinemas</b>.",
          icon: "mdi-drama-masks",
          isMin: false,
          displayFeatures: false,
        },
      ],
      steps: [
        {
          target: '[data-v-step="0"]', // We're using document.querySelector() under the hood
          header: {
            title: "Switch Layers",
          },
          content: "Click here to change the <b>selected layers</b>.",
        },
        {
          target: '[data-v-step="8"]',
          header: {
            title: "Dataset",
          },
          content:
            "Click the slider's name to get directed to the data's <b>source</b>.",
        },
        {
          target: '[data-v-step="4"]',
          header: {
            title: "Min or max distance",
          },
          content:
            "Here you can decide if the chosen distance should be understood as <b>at least</b> or <b>less than</b>.",
        },
        {
          target: '[data-v-step="9"]',
          header: {
            title: "Source features",
          },
          content:
            "Here you can activate the <b>source features</b> on the map.",
        },
        {
          target: '[data-v-step="1"]',
          header: {
            title: "Examples",
          },
          content:
            "Here are some <b>examples</b> to get an idea about the results.",
        },
        {
          target: '[data-v-step="2"]',
          header: {
            title: "Map",
          },
          content: "In the map you can see the <br><b>visualized results</b>.",
          params: {
            placement: "left", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="2"]',
          header: {
            title: "Add location markers",
          },
          content:
            "Here you can add a <b>marker</b> to the map,<br>e.g. to mark a certain position.",
          params: {
            placement: "left-start", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="6"]',
          header: {
            title: "Layer control & zoom",
          },
          content:
            "Here it's possible to switch to a <b>colorblind baselayer</b>. You can also activate an overlay of the town's <b>bus and train stations</b>.<br>The buttons below let you <b>zoom</b> in or out.",
          params: {
            placement: "left-start", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="6"]',
          header: {
            title: "Colorblind mode",
          },
          content:
            "When turning on the <b>colorblind mode</b> the basemap and the color of the result layer polygons changes. This mode is modified for <b>blue-blindness/Tritanopia</b>.",
          params: {
            placement: "left-start", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="7"]',
          header: {
            title: "Legend",
          },
          content:
            "On hover, a legend will expand. It changes dynamically depending on the features visible on the map.",
          params: {
            placement: "top", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="3"]',
          header: {
            title: "Expand and minimize menu",
          },
          content:
            "With this button you can <b>hide the menu</b> or expand it, if it's hidden.",
          params: {
            placement: "right", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
      ],
    };
  },
  methods: {
    requestResultAreas: async function (requestString) {
      // Request to the backend to retrieve areas that meet the current conditions
      // (e.g. http://localhost:5050/request/[(0,250,None),(1,0,1000)])
      try {
        const response = await fetch(
          `http://localhost:5050/request/[${requestString}]`
        );
        const result = await response.json();
        // Smoothing
        simplify(result, {
          tolerance: 0.00029,
          highQuality: true,
          mutate: true,
        });
        this.resultAreas = polygonSmooth(result, { iterations: 3 });
        // Check if areas are empty
        this.resultAreasEmpty =
          Array.isArray(result.features) && result.features.length < 1;
        // Request successful
        this.resultAreasRequestFailed = false;
      } catch {
        this.resultAreas = null;
        this.resultAreasEmpty = false;
        this.resultAreasRequestFailed = true;
      }
    },
    clearResultAreas: function () {
      this.resultAreas = null;
      this.resultAreasEmpty = true;
      this.resultAreasRequestFailed = false;
    },
    setSliderActiveState: function (id, active) {
      for (const slider of this.sliders) {
        if (slider.id === id) {
          slider.active = active;
          if (active) {
            if (slider.displayFeatures && !this.sliderFeatures.has(slider.id))
              this.addSliderFeatures(slider);
          } else {
            this.sliderFeatures.delete(slider.id);
          }
          return;
        }
      }
    },
    updateSliderValue: function (id, value) {
      for (const slider of this.sliders) {
        if (slider.id === id) {
          slider.value = value;
          return;
        }
      }
    },
    updateSliderIsMin: function (id, isMin) {
      for (const slider of this.sliders) {
        if (slider.id === id) {
          slider.isMin = isMin;
          return;
        }
      }
    },
    setSliderDisplay: function (id, value) {
      for (const slider of this.sliders) {
        if (slider.id === id) {
          slider.displayFeatures = value;
          if (value && slider.active) this.addSliderFeatures(slider);
          else this.removeSliderFeatures(slider);
          return;
        }
      }
    },
    async addSliderFeatures(slider) {
      try {
        const response = await fetch(
          `http://localhost:5050/features/${slider.id}`
        );
        this.sliderFeatures.set(slider.id, await response.json());
        this.$refs.map.updateSliderFeatures();
      } catch (error) {
        console.log("Fetching features failed: ", error);
      }
    },
    removeSliderFeatures(slider) {
      this.sliderFeatures.delete(slider.id);
      this.$refs.map.updateSliderFeatures();
    },
    setBusStationsVisibility: function (value) {
      this.showBusStations = value;
    },
    toggleMenu: function () {
      const menuDim = [
        this.$refs.menuContainer.offsetWidth,
        this.$refs.menuContainer.offsetHeight,
      ];
      // Change menu visibility
      this.showMenu = !this.showMenu;
      this.stopTour();
      this.$nextTick(() => {
        // When the menu visibility has changed, calculate the change in size
        const menuDimChange = [
          this.$refs.menuContainer.offsetWidth - menuDim[0],
          this.$refs.menuContainer.offsetHeight - menuDim[1],
        ];
        // Get offset depending on menu position
        const requiredOffset = this.getMenuOffset(menuDimChange);
        // Update map
        this.$refs.map.updateOnResize(requiredOffset);
      });
    },
    getMenuOffset: function (dimChange) {
      let pixelOffset; // here x, y coordinates!
      const horizontalLayout = this.$vuetify.breakpoint.xs;
      if (horizontalLayout) {
        // Menu on top
        pixelOffset = [0, dimChange[1]];
      } else {
        // Menu on the left side
        pixelOffset = [dimChange[0], 0];
      }
      return pixelOffset;
    },
    onResize() {
      this.$refs.map.updateOnResize();
    },
    startTour() {
      this.$tours["myTour"].start();
    },
    stopTour() {
      this.$tours["myTour"].stop();
    },
    debounce(func, timeout = 200) {
      let timer;
      return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
          func.apply(this, args);
        }, timeout);
      };
    },
    async doBusRequest() {
      // the request to the backend to retrieve the areas that meet the current conditions (configured by the user)
      const busResponse = await fetch(
        "https://rest.busradar.conterra.de/prod/haltestellen"
      );
      this.busStations = await busResponse.json();
    },
  },
  computed: {
    menuHeight() {
      if (this.$vuetify.breakpoint.xs && this.showMenu) {
        return "50%";
      } else {
        return "100%";
      }
    },
    menuButtonStyle() {
      if (this.$vuetify.breakpoint.xs) {
        return "left: 50%; transform-origin: left; transform: translate(0, -40px) rotate(90deg)";
      } else {
        return "top: 50%; transform: translate(0, -50%);";
      }
    },
  },
  async mounted() {
    this.doBusRequest();

    // Update map size when resizing window
    window.addEventListener("resize", this.debounce(this.onResize, 500), {
      passive: true,
    });
  },
};
</script>

<style scoped>
#mainContainer {
  padding: 0px;
  width: 100%;
  max-height: 100%;
}

#mapViewContainer {
  height: 100%;
  overflow: hidden;
}

.v-step[data-v-54f9a632] {
  background-color: #5b7683;
}

.highlight-gray {
  background-color: #c3c3c393;
  border-radius: 6px;
  padding: 3px 6px;
}

#menuContainer {
  overflow-y: auto;
  scrollbar-width: thin;
  height: 100%;
}

#menuButton {
  position: absolute;
  margin: 0;
  width: 16px;
  height: 80px;
  background-color: white;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border: 2px solid lightgrey;
  border-left: 0;
  z-index: 1200;
  display: grid;
  place-content: center;
  overflow: hidden;
  cursor: pointer;
  transition: background-color 200ms;
}

#menuButton .v-icon {
  font-size: 28px;
}

#menuButton:hover {
  background-color: #eeeeee;
}
</style>
