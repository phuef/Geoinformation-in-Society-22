<template>
  <div class="pt-8 pl-6 pr-1">
    <div class="body-1 text-xs-body-2">
    <p>Do you have the desire to <span class="highlight-gray">Find your Spot</span>?
    With this application you can search for a specific location that meets your interests. 
    <mark>Define the layers</mark> that you want, <mark>specify the distance</mark>, 
    and that`s it, congrats, you just found your Spot.<br /></p>
    <p><mark>Need help?</mark> For detailed information of the functionalities, <span class="highlight-yellow">use the information</span> buttons below.</p>
    </div>
    <v-divider></v-divider>
    <v-select
      v-model="activeSliders"
      :items="sliders"
      item-text="name"
      item-value="name"
      deletable-chips
      chips
      label="selected layers"
      multiple
      dense
      @input="changeActiveState()"
    >
    </v-select>
    <div v-for="slider in sliders" :key="slider.label">
      <!--<v-card-subtitle>{{slider.label}}</v-card-subtitle> -->
      <v-slider
        v-if="slider.active"
        v-model="slider.value"
        step="50"
        thumb-label="always"
        ticks
        max="1000"
        dense
        :label="slider.label + ':'"
        append-icon="mdi-close"
        prepend-icon="mdi-information-outline"
        @click:append="(slider.active = false), removeLayer(slider.name)"
      ></v-slider>
    </div>
    <v-divider></v-divider>
    <div v-for="configuration in configurations" :key="configuration.name">
      <v-btn
        width="100%"
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
  name: "MapView",
  data() {
    return {
      sliders: [
        //All availabe sliders
        {
          name: "Parks",
          label: "Distance to parks",
          value: 0,
          active: true,
          infoLabel:
            "Move the slider to remove all areas that have a certain distance to parks",
        },
        {
          name: "Water",
          label: "Distance to areas of water",
          value: 0,
          active: true,
          infoLabel:
            "Move the slider to remove all areas that have a certain distance to areas of water",
        },
        {
          name: "Trashcans",
          label: "Distance to trashcan",
          value: 0,
          active: true,
          infoLabel:
            "Move the slider to remove all areas that have a certain distance to trashcans",
        },
      ],
      activeSliders: ["Parks", "Water", "Trashcans"], //The currently active Sliders
      configurations: [
        //The pre-configurations
        {
          name: "Find your Park",
          activeSliders: ["Parks", "Water"],
          values: [200, 0],
        },
        {
          name: "Find your Trashcan",
          activeSliders: ["Trashcans"],
          values: [0],
        },
      ],
    };
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
  },
};
</script>


<style scoped>
  div {
    text-align: justify;
  }
  .highlight-gray {
  background-image: linear-gradient(to right, #e9e9e9, #e9e9e9);
  border-radius: 6px;
  padding: 3px 6px;
}
.highlight-yellow {
  border-radius: 1em 0 1em 0;
  background-image: linear-gradient(
    -100deg,
    rgba(255, 224, 0, 0.2),
    rgba(255, 224, 0, 0.7) 95%,
    rgba(255, 224, 0, 0.1)
  );
}

mark {
  -webkit-animation: 1.5s highlight 1.5s 1 normal forwards;
          animation: 1.5s highlight 1.5s 1 normal forwards;
  background-color: none;
  background: linear-gradient(90deg, #e9e9e9 50%, rgba(255, 255, 255, 0) 50%);
  background-size: 200% 100%;
  background-position: 100% 0;
}

@-webkit-keyframes highlight {
  to {
    background-position: 0 0;
  }
}

@keyframes highlight {
  to {
    background-position: 0 0;
  }
}
</style>