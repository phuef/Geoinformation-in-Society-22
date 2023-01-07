<template>
  <div class="pa-4 pt-8">
    <v-select
      v-model="activeSliders"
      :items="sliders"
      item-text="name"
      item-value="name"
      deletable-chips
      chips
      label="Selected layers:"
      multiple
      dense
      @input="changeActiveState()"
      data-v-step="0"
    >
    </v-select>
    <p class="text-capitalize pt-2 mb-0" style="color: #000000de" dense>
      Distance to ...
    </p>
    <v-alert
      v-if="isResponseEmpty"
      text
      color="rgb(25,118,210)"
      colored-border
      type="info"
      class="py-2 px-2 mb-0 mt-3"
    >
      There is no spot that matches the current query. Adjust the sliders to
      find one.
    </v-alert>
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
                  @click="
                    $emit('isMinOfSliderHasChanged', slider.name), doRequest()
                  "
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
                        @click="
                          (slider.active = false), removeLayer(slider.name)
                        "
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
              @end="doRequest"
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
          style="color: #000000de; padding-left: 0px; font-size: 16px"
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
                @click="
                  (activeSliders = configuration.activeSliders),
                    adjustSliders(
                      configuration.activeSliders,
                      configuration.values,
                      configuration.isMin
                    )
                "
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
  emits: ["newRequest", "isMinOfSliderHasChanged", "setBusStationsVisibility"],
  data() {
    return {
      activeSliders: ["Museums", "Theaters"], //The currently active Sliders
      configurations: [
        // The pre-configurations that can be set upfront in the following form:
        {
          index: 1,
          name: "Find museums with a minimum distance of 1000 m.", // name of the configuration - gets displayed
          activeSliders: ["Museums"], // the name(s) of the slider(s) that should be shown
          values: [1000], // the values that the slider(s) should have
          isMin: true,
        },
        {
          index: 2,
          name: "Find theaters with a maximum distance of 500 m.",
          activeSliders: ["Theaters"],
          values: [500],
          isMin: false,
        },
      ],
      response: "",
      state_showBusStations: this.showBusStations,
    };
  },
  props: {
    /* eslint-disable */
    sliders: {
      type: Array,
    },
    showBusStations: {
      required: true,
      type: Boolean,
    },
  },
  methods: {
    /**
     * Changes the active state of the sliders according to the currently active sliders
     */
    changeActiveState() {
      for (var h in this.sliders) {
        this.sliders[h].active = false;
      }
      for (var i in this.sliders) {
        for (var j in this.activeSliders) {
          if (this.sliders[i].name == this.activeSliders[j]) {
            this.sliders[i].active = true;
          }
        }
      }
      this.doRequest();
    },
    /**
     * Removes a layer with a given name
     */
    removeLayer(name) {
      for (var j in this.activeSliders) {
        if (this.activeSliders[j] == name) {
          this.activeSliders.splice(j, 1);
        }
      }
      if (this.activeSliders.length != 0) {
        this.doRequest();
      } else {
        this.clearMap();
      }
    },
    // returns a string in the following form:
    // "(bandId, sliderValue)"

    /**
     * @returns String
     */
    getTupelForRequest(band, value, isMin) {
      var tupel = "(" + band + ",";
      if (isMin) {
        tupel += value + ",None)";
      } else {
        tupel += "0," + value + ")";
      }
      return tupel;
    },
    /**
     * @returns String in the following form:"[(bandId, sliderValue), (bandId, sliderValue)]"
     * this String can be put together with <serverUrl>/request/<this string> to make the request to the backend
     */
    requestString() {
      // outcome should look like this: [(0, 1000),(1,1500)]
      var a = [];
      a = this.getBandValueArray(); //returns an array with the bandIds and the corresponding values
      var b = "[";
      for (var i in a) {
        if (i > 0) {
          b += ",";
        }
        b += this.getTupelForRequest(a[i].band, a[i].value, a[i].isMin);
      }
      b += "]";
      return b;
    },
    /**
     * Gathers the bandId and current value for each active layer
     * @returns Array in the following form: [{band:0,value:50},{band:1,value:100}]
     */
    getBandValueArray() {
      // for each active layer add the bandId and its current value in an array
      var helpArray = [];
      for (var i in this.sliders) {
        if (this.sliders[i].active) {
          helpArray.push({
            band: this.sliders[i].band,
            value: this.sliders[i].value,
            isMin: this.sliders[i].isMin,
          });
        }
      }
      return helpArray;
    },
    /**
     * Adjusts the shown layers according to a given configuration
     */
    adjustSliders(activeSliders, values, isMin) {
      for (var h in this.sliders) {
        this.sliders[h].active = false;
      }
      for (var i in activeSliders) {
        for (var j in this.sliders) {
          if (this.sliders[j].name == activeSliders[i]) {
            this.sliders[j].active = true;
            this.sliders[j].value = values[i];
            console.log(this.sliders[i].isMin);
            this.sliders[i].isMin = isMin;
          }
        }
      }
      this.removeNotActiveLayers();
      this.doRequest();
    },
    /**
     * Removes all layers that are currently not active
     */
    removeNotActiveLayers() {
      for (var i in this.activeSliders) {
        for (var j in this.sliders)
          if (
            this.activeSliders[i] == this.sliders[j].name &&
            this.sliders[j].active == false
          ) {
            this.activeSliders.splice(i, 1);
          }
      }
    },
    /**
     * sends a request to the backend with the current parameters (e.g. http://localhost:5050/request/[(0,0),(1,50)])
     * @emits response of the server to the parent component (MainPage), so it can be added to the map component
     */
    async doRequest() {
      // the request to the backend to retrieve the areas that meet the current conditions (configured by the user)
      const response = await fetch(
        "http://localhost:5050/request/" + this.requestString()
      );
      const geojson = await response.json();
      this.response = geojson;

      // sends an event, that the parent component (in this case Mainpage) can listen to
      this.$emit("newRequest", this.response);
    },
    async clearMap() {
      this.$emit("clearMap", null);
    },
  },
  watch: {
    showBusStations: function (value) {
      // Updates the state for the bus stations switch in the menu
      this.state_showBusStations = value;
    },
  },
  mounted() {
    // do request at mount with the initial configuration
    this.doRequest();
  },
  computed: {
    isResponseEmpty() {
      return this.response.features == "" ? true : false;
    },
  },
};
</script>

<style scoped>
.v-expansion-panel-content > .v-expansion-panel-content__wrap {
  padding: 0 !important;
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
</style>
