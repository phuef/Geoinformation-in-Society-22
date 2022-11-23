<template>
  <div id="mapContainer"></div>
</template>

<script>
import L from 'leaflet';
//import 'leaflet';
export default {
  name: 'MainView',
  data(){
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [51.505, -0.159],
      markerLatLng: [51.504, -0.159],
      map: null
      };
    },
    methods:{ 
      initMap: function(){
        this.map=L.map("mapContainer").setView([37.7749, -122.4194], 13); 
        
        }
        },
        mounted(){
          this.initMap()
        }}
</script>

<style>
#mapContainer { height: 200px; }
</style>