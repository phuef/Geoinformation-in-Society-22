<template>
  <v-container id="mainContainer" fluid style="height: 100vh">
    <v-row
      class="d-none d-sm-flex align-items-center"
      style="height: 100%; flex-direction: row"
    >
      <v-col v-if="showMenu"> <MenuView /> </v-col>
      <v-col>
        <div id="mapContainer">
          <div id="iconContainer">
            <v-icon
              v-if="showMenu"
              @click="showMenu = !showMenu"
              id="collapseIcon"
            >
              mdi-menu-left</v-icon
            >
            <v-icon
              v-if="!showMenu"
              @click="showMenu = !showMenu"
              id="openIcon"
            >
              mdi-menu-right</v-icon
            >
          </div>
          <MapView />
        </div>
      </v-col>
    </v-row>
    <v-row
      class="d-flex d-sm-none align-items-center"
      style="height: 100%; flex-direction: column"
    >
      <v-col> <MenuView /> </v-col>
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
#iconContainer {
  margin: 0;
  position: absolute;
  top: 45%;
}
#mainContainer {
  padding: 0px;
  width: 100%;
}
#mapContainer {
  height: 100%;
}
#collapseIcon,
#openIcon {
  padding: 0px;
  margin: left;
  border-radius: 4px;
  width: 15px;
  height: 80px;
  background-color: white;
  opacity: 0.8;
  border: 1px solid grey;
  z-index: 9999;
}
</style>
