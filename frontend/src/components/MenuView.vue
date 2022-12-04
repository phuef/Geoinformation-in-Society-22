<template>
  <div class="pt-8 pl-6 pr-1">
    <!-- TODO: the line below is for developing purposes and needs to be deleted later.
               It shows the current request url -->
    current request url: localhost:5050/request/{{requestString()}}
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
      <v-slider
        v-if="slider.active"
        v-model="slider.value"
        step="10"
        thumb-label="always"
        max="2000"
        dense
        :label="slider.label + ':'"
        append-icon="mdi-close"
        prepend-icon="mdi-information-outline"
        @click:append="(slider.active = false), removeLayer(slider.name)"
        @input="doRequest()"
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
  name: "MenuView",
  emits: ['newRequest'],
  data() {
    return {
      sliders: [
        // All availabe sliders
        // TODO: add new layers to this list, when new layers are added to the backend.
        //       The layers need to have the structure shown and explained below 
        {
          name: "Museums", // the layer name that gets displayed at the layer selection 
          label: "Distance to museums", // the label that gets shown at the slider
          value: 0, // the value the slider has 
          band:0, // the corresponding band ID the layer has in the backend
          active: true, // wether the layer is currently selected by the user  
          infoLabel: // the text that shall be displayed when the user hovers over the info button
            "Move the slider to remove all areas that have a certain distance to museums",
        },
        {
          name: "Theaters",
          label: "Distance to theaters",
          value: 0,
          band: 1,
          active: true,
          infoLabel:
            "Move the slider to remove all areas that have a certain distance to theaters",
        },
      ],
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
      response:""
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
    // returns a string in the following form:
    // "(bandId, sliderValue)" 

    /**
     * @returns String in the following form:"[(bandId, sliderValue), (bandId, sliderValue)]" 
     * this String can be put together with <serverUrl>/request/<this string> to make the request to the backend 
     */
    requestString(){ // outcome should look like this: [(0, 1000),(1,1500)]
      var a=[{band:0,value:50},{band:1,value:100}];
      a=this.getBandValueArray() //returns an array with the bandIds and the corresponding values
      var b="["
      for (var i in a){
        if (i>0){b+=","}
        b+= "(" +a[i].band.toString() +"," +a[i].value.toString() +")"
      } 
      b+="]"
      return b
    },
    /**
     * Gathers the bandId and current value for each active layer
     * @returns Array in the following form: [{band:0,value:50},{band:1,value:100}]
     */
    getBandValueArray(){
      // for each active layer add the bandId and its current value in an array
      var helpArray=[]
      for (var i in this.sliders){
        if (this.sliders[i].active){
          helpArray.push({"band":this.sliders[i].band, "value":this.sliders[i].value})
        }
      }
      return helpArray
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
    /**
     * sends a request to the backend with the current parameters (e.g. http://localhost:5050/request/[(0,0),(1,50)])
     * @emits response of the server to the parent component (MainPage), so it can be added to the map component 
     */
    doRequest(){
      // TODO: uncomment the fetch function below, after cross-origin requests are allowed in the backend    

      // the request to the backend to retrieve the areas that meet the current conditions configured by the user
      /*fetch('http://localhost:5050/request/' +this.requestString(), {
          method: 'GET',
          headers:{
            "Access-Control-Allow-Origin":"*"}
          }).then((response) => this.response=response.json())
      .then((data) => console.log(data));
    */

   // for developing purposes the response gets set to an example response 
   // TODO: delete this part after the cross-origin requests are working   
   this.response={
      "crs": {
        "properties": {
          "name": "urn:ogc:def:crs:EPSG::3857"
        },
        "type": "name"
      },
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  848678.0122,
                  6793325.9256
                ],
                [
                  848688.0122,
                  6793325.9256
                ],
                [
                  848688.0122,
                  6793315.9256
                ],
                [
                  848718.0122,
                  6793315.9256
                ],
                [
                  848718.0122,
                  6793305.9256
                ],
                [
                  848728.0122,
                  6793305.9256
                ],
                [
                  848728.0122,
                  6793275.9256
                ],
                [
                  848738.0122,
                  6793275.9256
                ],
                [
                  848738.0122,
                  6793295.9256
                ],
                [
                  848748.0122,
                  6793295.9256
                ],
                [
                  848748.0122,
                  6793305.9256
                ],
                [
                  848778.0122,
                  6793305.9256
                ],
                [
                  848778.0122,
                  6793315.9256
                ],
                [
                  848788.0122,
                  6793315.9256
                ],
                [
                  848788.0122,
                  6793295.9256
                ],
                [
                  848778.0122,
                  6793295.9256
                ],
                [
                  848778.0122,
                  6793275.9256
                ],
                [
                  848768.0122,
                  6793275.9256
                ],
                [
                  848768.0122,
                  6793265.9256
                ],
                [
                  848758.0122,
                  6793265.9256
                ],
                [
                  848758.0122,
                  6793255.9256
                ],
                [
                  848728.0122,
                  6793255.9256
                ],
                [
                  848728.0122,
                  6793245.9256
                ],
                [
                  848698.0122,
                  6793245.9256
                ],
                [
                  848698.0122,
                  6793235.9256
                ],
                [
                  848688.0122,
                  6793235.9256
                ],
                [
                  848688.0122,
                  6793245.9256
                ],
                [
                  848648.0122,
                  6793245.9256
                ],
                [
                  848648.0122,
                  6793255.9256
                ],
                [
                  848638.0122,
                  6793255.9256
                ],
                [
                  848638.0122,
                  6793265.9256
                ],
                [
                  848628.0122,
                  6793265.9256
                ],
                [
                  848628.0122,
                  6793275.9256
                ],
                [
                  848638.0122,
                  6793275.9256
                ],
                [
                  848638.0122,
                  6793305.9256
                ],
                [
                  848648.0122,
                  6793305.9256
                ],
                [
                  848648.0122,
                  6793315.9256
                ],
                [
                  848678.0122,
                  6793315.9256
                ],
                [
                  848678.0122,
                  6793325.9256
                ]
              ]
            ],
            "type": "Polygon"
          },
          "properties": {
            "DN": 1.0
          },
          "type": "Feature"
        },
        {
          "geometry": {
            "coordinates": [
              [
                [
                  831978.0122,
                  6810985.9256
                ],
                [
                  831978.0122,
                  6771275.9256
                ],
                [
                  865438.0122,
                  6771275.9256
                ],
                [
                  865438.0122,
                  6810985.9256
                ],
                [
                  831978.0122,
                  6810985.9256
                ]
              ],
              [
                [
                  848678.0122,
                  6793325.9256
                ],
                [
                  848678.0122,
                  6793315.9256
                ],
                [
                  848648.0122,
                  6793315.9256
                ],
                [
                  848648.0122,
                  6793305.9256
                ],
                [
                  848638.0122,
                  6793305.9256
                ],
                [
                  848638.0122,
                  6793275.9256
                ],
                [
                  848628.0122,
                  6793275.9256
                ],
                [
                  848628.0122,
                  6793265.9256
                ],
                [
                  848638.0122,
                  6793265.9256
                ],
                [
                  848638.0122,
                  6793255.9256
                ],
                [
                  848648.0122,
                  6793255.9256
                ],
                [
                  848648.0122,
                  6793245.9256
                ],
                [
                  848688.0122,
                  6793245.9256
                ],
                [
                  848688.0122,
                  6793235.9256
                ],
                [
                  848698.0122,
                  6793235.9256
                ],
                [
                  848698.0122,
                  6793245.9256
                ],
                [
                  848728.0122,
                  6793245.9256
                ],
                [
                  848728.0122,
                  6793255.9256
                ],
                [
                  848758.0122,
                  6793255.9256
                ],
                [
                  848758.0122,
                  6793265.9256
                ],
                [
                  848768.0122,
                  6793265.9256
                ],
                [
                  848768.0122,
                  6793275.9256
                ],
                [
                  848778.0122,
                  6793275.9256
                ],
                [
                  848778.0122,
                  6793295.9256
                ],
                [
                  848788.0122,
                  6793295.9256
                ],
                [
                  848788.0122,
                  6793315.9256
                ],
                [
                  848778.0122,
                  6793315.9256
                ],
                [
                  848778.0122,
                  6793305.9256
                ],
                [
                  848748.0122,
                  6793305.9256
                ],
                [
                  848748.0122,
                  6793295.9256
                ],
                [
                  848738.0122,
                  6793295.9256
                ],
                [
                  848738.0122,
                  6793275.9256
                ],
                [
                  848728.0122,
                  6793275.9256
                ],
                [
                  848728.0122,
                  6793305.9256
                ],
                [
                  848718.0122,
                  6793305.9256
                ],
                [
                  848718.0122,
                  6793315.9256
                ],
                [
                  848688.0122,
                  6793315.9256
                ],
                [
                  848688.0122,
                  6793325.9256
                ],
                [
                  848678.0122,
                  6793325.9256
                ]
              ]
            ],
            "type": "Polygon"
          },
          "properties": {
            "DN": 0.0
          },
          "type": "Feature"
        }
      ],
      "name": "test",
      "type": "FeatureCollection"
    }
    // sends an event, that the parent component (in this case Mainpage) can listen to
    this.$emit('newRequest', this.response)
    }
  },
  mounted(){
    // do request at mount with the initial configuration
    this.doRequest()
  }
};
</script>
