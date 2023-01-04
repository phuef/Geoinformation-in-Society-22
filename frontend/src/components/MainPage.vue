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
          <v-btn class="ms-3" @click="startTour()"> Start Demo </v-btn>
          <MenuView
            ref="menu"
            @newRequest="processNewRequest"
            @isMinOfSliderHasChanged="changeSlidersIsMinState"
            @clearMap="processNewRequest"
            :sliders="sliders"
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
          <div
            id="menuButton"
            data-v-step="3"
            @click="toggleMenu"
            :style="menuButtonStyle"
          >
            <v-icon v-show="showMenu">mdi-menu-left</v-icon>
            <v-icon v-show="!showMenu">mdi-menu-right</v-icon>
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
      mapCenterPoint: [51.96229626341511, 7.6256090207326395],
      mapZoom: 10,
      steps: [
        {
          target: '[data-v-step="0"]', // We're using document.querySelector() under the hood
          header: {
            title: "Switch Layers",
          },
          content:
            "Click here to change the <strong>selected layers </strong>.",
        },
        {
          target: '[data-v-step="4"]',
          header: {
            title: "Min or max distance",
          },
          content:
            "Here you can decide if the choosen distance should be understood as <b>at least or less than</b>.  ",
        },
        {
          target: '[data-v-step="1"]',
          header: {
            title: "Examples",
          },
          content:
            "Here are some <strong>examples</strong> to get an idea about the results.",
        },
        {
          target: '[data-v-step="2"]',
          header: {
            title: "Map",
          },
          content:
            "In the map you can see the <br><strong>visualised results</strong>.",
          params: {
            placement: "left", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="2"]',
          header: {
            title: "Add location",
          },
          content:
            "Here you can add a <strong>marker</strong> to the map. <br> E.g. to mark a certain position.",
          params: {
            placement: "left-start", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: '[data-v-step="3"]',
          header: {
            title: "Hide and elapse",
          },
          content:
            "With this button you can <b>hide the menu</b> or elapse it, if it's hidden.",
          params: {
            placement: "right", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
      ],
    };
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
  mounted() {
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
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  border: 2px solid lightgrey;
  border-left: 0;
  z-index: 1200;
  display: flex;
  place-content: center;
  cursor: pointer;
}
</style>
