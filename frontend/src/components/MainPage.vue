<template>
  <v-container
    id="mainContainer"
    class="fill-height"
    fluid
    style="height: 100vh"
  >
    <v-row no-gutters class="fill-height" style="height: 100%">
      <v-col cols="12" xs="12" sm="6" v-if="showMenu">
        <MenuView
          @newRequest="processNewRequest"
          :style="{
            'padding-left': !showMenu ? '200px!important' : '0px',
          }"
        />
      </v-col>
      <v-col cols="12" xs="12" :sm="mapViewSize">
        <div id="mapContainer" :key="mapViewSize">
          <div class="d-none d-sm-flex align-items-center" id="iconContainer">
            <v-icon v-if="showMenu" @click="handleClick" id="collapseIcon">
              mdi-menu-left</v-icon
            >
            <v-icon v-if="!showMenu" @click="handleClick" id="openIcon">
              mdi-menu-right</v-icon
            >
          </div>
          <MapView :geojson="requestResponse" ref="mapComponent" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MapView from "./MapView.vue";
// eslint-disable-next-line
import MenuView from "./MenuView.vue";

export default {
  name: "MainPage",
  components: {
    MapView,
    // eslint-disable-next-line
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
      return this.showMenu ? "6" : "11";
    },
    menuWidth: function () {
      return this.showMenu ? "6" : "1";
    },
    /*computedWidth: function () {
      return this.width;
    },*/
  },
  methods: {
    processNewRequest: function (response) {
      this.requestResponse = response;
    },
    reloadMap: function () {
      //this.$refs.mapComponent.reloadMap();
    },
    // eslint-disable-next-line
    handleClick: function (event) {
      this.showMenu = !this.showMenu;
      /*if (this.showMenu) {
        this.$refs.mapComponent.setCenter([
          7.686768985374442, 51.84331355040922,
        ]);
      } else {
        this.$refs.mapComponent.setCenter([7.62451171875, 51.96288477548509]);
      }*/
      /*if (this.width == "50vw") {
        this.width = "100vw";
      } else {
        this.width = "50vw";
      }*/
    },
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
  width: 100vw;
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
