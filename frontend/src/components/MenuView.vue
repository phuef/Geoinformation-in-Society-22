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
      v-if="resultAreasEmpty"
      text
      color="rgb(25,118,210)"
      colored-border
      type="info"
      class="py-2 px-2 mb-0 mt-3"
    >
      There is no spot that matches the current query. Adjust the sliders to
      find one.
    </v-alert>
    <v-alert
      v-if="resultAreasRequestFailed"
      text
      color="rgb(25,118,210)"
      colored-border
      type="info"
      class="py-2 px-2 mb-0 mt-3"
    >
      Request to the server failed.
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
                  data-v-step="4"
                  elevation="0"
                  dense
                  small
                  outlined
                  @click="
                    $emit('isMinOfSliderHasChanged', slider.name),
                      doResultAreasRequest()
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
              @end="doResultAreasRequest"
            ></v-slider>
          </div>
        </v-card>
      </v-col>
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
  emits: ["requestResultAreas", "clearResultAreas", "isMinOfSliderHasChanged"],
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
    };
  },
  props: {
    /* eslint-disable */
    sliders: {
      type: Array,
    },
    resultAreasEmpty: {
      type: Boolean,
    },
    resultAreasRequestFailed: {
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
      this.doResultAreasRequest();
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
        this.doResultAreasRequest();
      } else {
        this.$emit("clearResultAreas");
      }
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
      this.doResultAreasRequest();
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
     * @returns String
     */
    getSliderTuple(band, value, isMin) {
      let tupel = "(" + band + ",";
      if (isMin) {
        tupel += value + ",None)";
      } else {
        tupel += "0," + value + ")";
      }
      return tupel;
    },
    /**
     * Sends the query string for a request to the backend (e.g. [(0,250,None),(1,0,1000)])
     * @emits requestString to the parent component (MainPage)
     */
    doResultAreasRequest() {
      const requestTuples = [];
      for (const slider of this.sliders) {
        if (slider.active) {
          requestTuples.push(
            this.getSliderTuple(slider.band, slider.value, slider.isMin)
          );
        }
      }
      if (requestTuples.length < 1) {
        this.$emit("clearResultAreas");
        return;
      }
      const requestString = "[" + requestTuples.join() + "]";
      this.$emit("requestResultAreas", requestString);
    },
  },
  mounted() {
    // do request at mount with the initial configuration
    this.doResultAreasRequest();
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
