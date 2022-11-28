<template>
  <v-container fluid style="height: 100vh">
    <v-row style="height: 100%">
      <v-col> <MenuView />  </v-col>
      <v-col>
        <div id="mapContainer">
          <MapView />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MapView from "./MapView.vue";
import MenuView from "./MenuView.vue";

export default {
  name: "MainPage",
  components: {
    MapView,
    MenuView
  },
};
</script>

<style scoped>
#mapContainer {
  height: 100%;
}
</style>
