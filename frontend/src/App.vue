<template>
  <v-app>
    <div style="d-flex">
      <v-app-bar elevation="4" color="grey darken-4" class="px-0" dark width>
        <v-toolbar dense>
          <v-toolbar-title>Find Your Spot</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items class="d-none d-md-flex align-items-center">
            <v-btn to="/" dark text class="ms-3"> Main </v-btn>
            <v-btn to="/impressum" dark text class="ms-3"> Legal Notice </v-btn>
          </v-toolbar-items>
          <v-menu
            class="d-flex d-md-none align-items-center"
            offset-y
            z-index="1000"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                dark
                class="ms-8 p-1 menu-button"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon large>mdi-menu</v-icon>
              </v-btn>
            </template>
            <v-list nav>
              <v-list-item link to="/">
                <v-list-tile-title> Main </v-list-tile-title>
              </v-list-item>
              <v-list-item link to="/impressum">
                <v-list-tile-title> Legal Notice </v-list-tile-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-app-bar>
    </div>
    <router-view />
  </v-app>
</template>

<script>
//import MainPage from "./components/MainPage.vue";

export default {
  name: "App",
  components: {},
};
</script>

<style>
html,
body {
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  flex-direction: column;
  height: 100%;
  color: #2c3e50;
}
</style>
