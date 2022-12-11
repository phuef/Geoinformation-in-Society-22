<template>
  <v-container
    id="mainContainer"
    class="fill-height"
    fluid
    style="height: 100vh"
  >
    <v-row no-gutters class="fill-height" style="height: 100%">
      <v-col cols="12" xs="12" :sm="menuWidth"
        ><!--v-if="showMenu"> replaced sm="6" by the binded attribute on top-->

        <MenuView
          @newRequest="processNewRequest"
          :style="{
            'padding-left': !showMenu ? '200px!important' : '0px',
          }"
        />
        <!--<v-navigation-drawer v-model="drawer" absolute temporary hide-overlay>
          <v-list-item>
            <v-list-item-avatar>
              <v-img
                src="https://randomuser.me/api/portraits/men/78.jpg"
              ></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>John Leider</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-divider></v-divider>

          <v-list dense>
            <v-list-item v-for="item in items" :key="item.title" link>
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>-->
      </v-col>
      <v-col cols="12" xs="12" :sm="mapViewSize">
        <div id="mapContainer">
          <!--:style="{ width: width }">-->
          <!--:key="mapViewSize">-->
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
      drawer: null, // this and the following 4 lines could be removed by deciding against nav drawer
      items: [
        { title: "Home", icon: "mdi-view-dashboard" },
        { title: "About", icon: "mdi-forum" },
      ],
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
