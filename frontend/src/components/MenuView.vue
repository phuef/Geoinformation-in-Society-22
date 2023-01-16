<template>
  <div class="pa-4 pt-8">
    <div id="intro-text" class="body-1 text-xs-body-2">
      <p
        style="
          font-size: 14px;
          line-height: 150%;
          font-family: 'Avenir', Helvetica, Arial, sans-serif;
          color: #000000de;
          text-align: justify;
        "
      >
        Do you have the desire to
        <span class="highlight-gray">Find your Spot</span>?<br /><br />
        With this application you can search for a location that meets your
        leisure interests.
        <span class="highlight-gray">Add the layers</span> that you want,
        <span class="highlight-gray">specify the distance</span> to your target
        location, and that`s it, congrats, you just found your Spot.<br /><br />
        <span class="highlight-gray">Need help?</span> Click
        <a class="start-demo-link" @click="startTour()">here</a> to find
        detailed information of the functionalities.
      </p>
    </div>
    <v-divider></v-divider>
    <v-select
      class="pt-7"
      v-model="activeSliders"
      :items="sliders"
      item-text="name"
      item-value="name"
      deletable-chips
      chips
      label="Selected layers:"
      multiple
      dense
      @input="doResultAreasRequest()"
      data-v-step="0"
    >
    </v-select>
    <p class="text pt-2 mb-0" style="color: #000000de; font-size: 14px" dense>
      Distance to ...
    </p>
    <br />
    <v-row v-for="slider in sliders" :key="slider.label" class="py-3 px-3">
      <v-col class="lessPadding">
        <v-card
          v-if="slider.active"
          width="100%"
          elevation="0"
          tile
          dense
          cols="12"
          data-v-step="6"
        >
          <div tile class="d-flex paddingTop">
            <v-row>
              <v-col cols="4">
                <p
                  color="black"
                  class="text-capitalize mb-0 d-flex"
                  dense
                  style="align-items: center"
                >
                  {{ slider.name }}
                  <v-tooltip right z-index="1000">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        dense
                        small
                        color="white"
                        elevation="0"
                        v-bind="attrs"
                        v-on="on"
                        class="bNoPadding"
                      >
                        <v-icon small style="color: #000000de"
                          >mdi-information-outline</v-icon
                        >
                      </v-btn>
                    </template>
                    <span v-html="slider.infoLabel"></span>
                  </v-tooltip>
                </p>
              </v-col>
              <v-col cols="3">
                <v-btn
                  data-v-step="4"
                  elevation="0"
                  dense
                  small
                  outlined
                  @click="toggleIsMin(slider)"
                  class="text-lowercase bNoPadding"
                >
                  {{ slider.isMin ? "at least" : "less than" }}
                </v-btn>
              </v-col>
              <v-col cols="4"> {{ slider.value }} m </v-col>
              <v-col cols="1">
                <div class="d-flex center-align justify-center bNoPadding">
                  <v-tooltip left z-index="1000">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        id="deleteBtn"
                        elevation="0"
                        small
                        class="bNoPadding"
                        color="white"
                        @click="deactivateSlider(slider)"
                      >
                        <v-icon
                          style="color: #000000de"
                          v-bind="attrs"
                          v-on="on"
                          >mdi-close</v-icon
                        >
                      </v-btn>
                    </template>
                    <span class="bNoPadding"
                      >Remove {{ slider.name }} layer</span
                    >
                  </v-tooltip>
                </div>
              </v-col>
            </v-row>
          </div>
          <div
            v-if="slider.active"
            cols="1"
            class="d-flex center-align justify-center"
          >
            <v-slider
              hide-details
              v-model="slider.value"
              step="10"
              :thumb-size="30"
              max="2000"
              dense
              @end="updateSliderValue(slider)"
            ></v-slider>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center">
      <v-col cols="2" class="d-flex justify-center">
        <v-switch
          class="mt-0 pt-0"
          color="primary"
          v-model="state_showBusStations"
          hide-details
          @change="$emit('setBusStationsVisibility', !showBusStations)"
        >
        </v-switch>
      </v-col>
      <v-col
        cols="10"
        class="pl-0"
        style="color: #000000de; align-items: center; display: flex"
        >Add bus stops
        <v-tooltip right z-index="1201">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              dense
              small
              color="white"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              class="bNoPadding"
            >
              <v-icon small style="color: #000000de"
                >mdi-information-outline</v-icon
              >
            </v-btn>
          </template>
          <span
            v-html="
              'Here you can add the </br><b>cities bus stations</b></br> to the map'
            "
          ></span> </v-tooltip
      ></v-col>
    </v-row>

    <br />
    <v-divider style="border-color: rgba(127, 127, 127)"></v-divider>
    <br />

    <v-expansion-panels flat data-v-step="1">
      <v-expansion-panel>
        <v-expansion-panel-header
          style="color: #000000de; padding-left: 0px; font-size: inherit"
          dense
        >
          Pre-configurated examples:
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row
            v-for="configuration in configurations"
            :key="configuration.name"
            align="center"
          >
            <v-col
              style="color: #000000de"
              cols="1"
              v-html="'<b>' + configuration.index + ')</b>'"
            ></v-col>
            <v-col
              style="color: #000000de"
              cols="6"
              class="p-0"
              v-html="configuration.name"
            ></v-col>
            <v-col class="d-flex justify-center" cols="5">
              <v-btn
                color="rgb(70,77,93)"
                class="white--text text-capitalize"
                elevation="0"
                height="50px"
                @click="applyConfiguration(configuration)"
                v-html="'Show this <br/>configuration'"
              ></v-btn>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
export default {
  name: "MenuView",
  emits: [
    "requestResultAreas",
    "clearResultAreas",
    "setSliderActiveState",
    "updateSliderValue",
    "updateSliderIsMin",
    "setBusStationsVisibility",
  ],
  data() {
    return {
      activeSliders: [],
      configurations: [
        // The pre-configurations that can be set upfront in the following form:
        {
          index: 1,
          name: "Find places that are at minimum one kilometer away from any museums", // name of the configuration - gets displayed
          activeSliders: ["Museums"], // the name(s) of the slider(s) that should be shown
          values: [1000], // values that the slider(s) should have
          isMin: [true], // isMin properties of the slider(s)
        },
        {
          index: 2,
          name: "Find places within 500 meters of a theater",
          activeSliders: ["Theaters"],
          values: [500],
          isMin: [false],
        },
      ],
      state_showBusStations: this.showBusStations,
    };
  },
  props: {
    sliders: {
      type: Array,
    },
    resultAreasEmpty: {
      type: Boolean,
    },
    resultAreasRequestFailed: {
      type: Boolean,
    },
    showBusStations: {
      required: true,
      type: Boolean,
    },
  },
  methods: {
    /**
     * Removes a layer with a given name
     */
    deactivateSlider(slider) {
      const i = this.activeSliders.indexOf(slider.name);
      if (i !== -1) {
        this.activeSliders.splice(i, 1);
      }
      this.doResultAreasRequest();
    },
    updateSliderValue(slider) {
      this.$emit("updateSliderValue", slider.name, slider.value);
      this.doResultAreasRequest();
    },
    toggleIsMin(slider) {
      this.$emit("updateSliderIsMin", slider.name, !slider.isMin);
      this.doResultAreasRequest();
    },
    /**
     * Adjusts the shown layers according to a given configuration
     */
    applyConfiguration(configuration) {
      const { activeSliders, values, isMin } = configuration;
      this.activeSliders = Array.from(activeSliders);
      for (let i = 0; i < activeSliders.length; i++) {
        this.$emit("updateSliderValue", activeSliders[i], values[i]);
        this.$emit("updateSliderIsMin", activeSliders[i], isMin[i]);
      }
      this.doResultAreasRequest();
    },
    /**
     * Sends the query string for a request to the backend (e.g. (0,250,None),(1,0,1000))
     * @emits requestString to the parent component (MainPage)
     */
    doResultAreasRequest() {
      if (this.activeSliders.length < 1) {
        this.$emit("clearResultAreas");
      } else {
        const requestString = this.sliders
          .filter((slider) => this.activeSliders.includes(slider.name))
          .map((slider) =>
            this.getSliderTuple(slider.band, slider.value, slider.isMin)
          )
          .join();
        this.$emit("requestResultAreas", requestString);
      }
    },
    /**
     * @returns String
     */
    getSliderTuple(band, value, isMin) {
      if (isMin) {
        return `(${band},${value},None)`;
      } else {
        return `(${band},0,${value})`;
      }
    },
    startTour() {
      this.$tours["myTour"].start();
    },
    stopTour() {
      this.$tours["myTour"].stop();
    },
  },
  watch: {
    activeSliders: function (value) {
      // Changes to activeSliders update the sliders active state in MainPage
      for (const slider of this.sliders) {
        if (value.includes(slider.name)) {
          this.$emit("setSliderActiveState", slider.name, true);
        } else {
          this.$emit("setSliderActiveState", slider.name, false);
        }
      }
    },
    showBusStations: function (value) {
      // Updates the state for the bus stations switch in the menu
      this.state_showBusStations = value;
    },
  },
  mounted() {
    // Set activeSliders according to the sliders active state in MainPage
    this.activeSliders = this.sliders
      .filter((slider) => slider.active)
      .map((slider) => slider.name);
    // Request with intitial configuration
    this.doResultAreasRequest();
  },
};
</script>

<style scoped>
.v-expansion-panel-content > .v-expansion-panel-content__wrap {
  padding: 0 !important;
}

.div {
  text-align: justify;
}
.highlight-gray {
  background-color: #c3c3c393;
  border-radius: 6px;
  padding: 3px 6px;
}

.bNoPadding {
  padding-left: 2px !important;
  padding-right: 2px !important;
  min-width: 0px !important;
}

.noMarginBottom {
  margin-bottom: 0px !important;
}

.lessPadding {
  padding-left: 2px !important;
  padding-right: 2px !important;
  padding-top: 2px !important;
  padding-bottom: 2px !important;
}

.paddingTop {
  padding-top: 2px !important;
}

.start-demo-link:hover {
  text-decoration: underline;
  font-weight: bold;
}
</style>
