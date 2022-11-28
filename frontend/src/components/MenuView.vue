<template>
  <div>
      <v-card>
        <v-card-text>
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
                thumb-label='always'
                ticks
                max="1000"
                dense
                :label="slider.label + ':'" 
                append-icon="mdi-close"
                prepend-icon="mdi-information-outline"
                @click:append="slider.active=false, removeLayer(slider.name)"
            ></v-slider>
        </div>
        </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "MapView",
  data(){
      return{
        sliders: [
          {name:"Parks",label:"Distance to parks", value:0, active:true, infoLabel:"Move the slider to remove all areas that have a certain distance to parks"},
          {name:"Water",label:"Distance to areas of water", value:0, active:true, infoLabel:"Move the slider to remove all areas that have a certain distance to areas of water"},
          {name:"Trashcans",label:"Distance to trashcan", value:0, active:true, infoLabel:"Move the slider to remove all areas that have a certain distance to trashcans"}
          ],
          activeSliders:["Parks", "Water", "Trashcans"]
      }
  },
  methods:{
    changeActiveState(){
      for (var h in this.sliders){this.sliders[h].active=false}
      for (var i in this.sliders){
        for (var j in this.activeSliders){
          if (this.sliders[i].name==this.activeSliders[j]){
            this.sliders[i].active=true
          }
        }
      }
    },
    removeLayer(name){
      for (var j in this.activeSliders){
        if (this.activeSliders[j]==name){
          this.activeSliders.splice(j, 1)
        }
      }
    }
  }
  
}
</script>