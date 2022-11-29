<template>
  <v-container id="mainContainer" fluid style="height: 100vh">
    <v-row style="height: 100%">
      <v-col v-if="showMenu"> <MenuView /> </v-col>
      <v-col>
        <div id="mapContainer">
          <v-container fill-height>
            <v-icon
              v-if="showMenu"
              @click="showMenu = !showMenu"
              id="collapseIcon"
            >
              mdi-arrow-collapse-left</v-icon
            >
            <v-icon
              v-if="!showMenu"
              @click="showMenu = !showMenu"
              id="openIcon"
            >
              mdi-arrow-collapse-right</v-icon
            >
          </v-container>

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
.container {
  padding: 0px;
}
#mainContainer {
  padding: 0px;
}
#mapContainer {
  height: 100%;
}
#collapseIcon,
#openIcon {
  padding: 0px;
  margin: left;
  border-radius: 2px;
  height: 100px;
  background-color: white;
  border: 1px solid grey;
  z-index: 9999;
}
</style>
