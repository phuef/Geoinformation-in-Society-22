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
    >
    </v-select>
    <p class="text-capitalize pt-2 mb-0" style="color: #000000de" dense>
      Distance to ...
    </p>
    <br />
    <v-row v-for="slider in sliders" :key="slider.label" class="py-3 px-3">
      <v-col class="lessPadding"
        ><v-card
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
                <p color="black" class="text-capitalize mb-0" dense>
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
                  elevation="0"
                  dense
                  small
                  outlined
                  @click="$emit('isMinOfSliderHasChanged', slider.name)"
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
    <br />
    <v-divider></v-divider>
    <br />
    <div v-for="configuration in configurations" :key="configuration.name">
      <v-btn
        width="100%"
        small
        @click="
          (activeSliders = configuration.activeSliders),
            adjustSliders(configuration.activeSliders, configuration.values)
        "
        >{{ configuration.name }}</v-btn
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "MenuView",
  emits: ["newRequest", "isMinOfSliderHasChanged"],
  data() {
    return {
      activeSliders: ["Museums", "Theaters"], //The currently active Sliders
      configurations: [
        // The pre-configurations that can be set upfront in the following form:
        {
          name: "Find your Museum", // name of the configuration - gets displayed
          activeSliders: ["Museums"], // the name(s) of the slider(s) that should be shown
          values: [100], // the values that the slider(s) should have
        },
        {
          name: "Find your Theater",
          activeSliders: ["Theaters"],
          values: [0],
        },
      ],
      response: "",
    };
  },
  props: {
    /* eslint-disable */
    sliders: {
      type: Array,
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
    adjustSliders(activeSliders, values) {
      for (var h in this.sliders) {
        this.sliders[h].active = false;
      }
      for (var i in activeSliders) {
        for (var j in this.sliders) {
          if (this.sliders[j].name == activeSliders[i]) {
            this.sliders[j].active = true;
            this.sliders[j].value = values[i];
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
  mounted() {
    // do request at mount with the initial configuration
    this.doRequest();
  },
};
</script>
<style>
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
