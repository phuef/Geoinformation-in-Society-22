<template>
  <v-container fluid style="height: 100vh">
    <v-row style="height: 100%">
      <v-col v-if="showMenu"> <MenuView /> </v-col>
      <v-col>
        <div id="mapContainer">
          <v-icon
            v-if="showMenu"
            @click="showMenu = !showMenu"
            id="collapseIcon"
          >
            mdi-arrow-collapse-left</v-icon
          >
          <v-icon v-if="!showMenu" @click="showMenu = !showMenu" id="openIcon">
            mdi-arrow-collapse-right</v-icon
          >
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
    MenuView,
  },
  data() {
    return {
      showMenu: true,
    };
  },
};
</script>

<style scoped>
#mapContainer {
  height: 100%;
}
#collapseIcon,
#openIcon {
  background-color: white;
  z-index: 9999;
}
</style>
