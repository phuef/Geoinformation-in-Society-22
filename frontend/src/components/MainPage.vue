<template>
<div>
  <v-card>
    <MapView/>
  </v-card>
      
</div>
</template>

<script>
import MapView from './MapView.vue'

export default {
  name: 'MainPage',
  components: {
    MapView
  }
}
</script>