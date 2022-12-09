<template>
  <v-container
    id="mainContainer"
    class="fill-height"
    fluid
    style="height: 100vh"
  >
    <v-row no-gutters class="fill-height" style="height: 100%">
      <v-col cols="12" xs="12" sm="6" v-if="showMenu">
        <MenuView @newRequest="processNewRequest" />
      </v-col>
      <v-col cols="12" xs="12" :sm="mapViewSize">
        <div id="mapContainer" :key="mapViewSize">
          <div class="d-none d-sm-flex align-items-center" id="iconContainer">
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
          <MapView :geojson="requestResponse" />
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
      requestResponse: null,
    };
  },
  computed: {
    mapViewSize: function () {
      // makes sure that the map is displayed on the full screen when the menu is not shown
      return this.showMenu ? "6" : "12";
    },
  },
  methods: {
    processNewRequest(response) {
      this.requestResponse = response;
    },
  },
};
</script>

<style scoped>
/*@media (max-width: 600px) {
  .v-row {
    flex-direction: column;
  }
}
@media (min-width: 601px) {
  .v-row {
    flex-direction: row;
  }
}*/
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
