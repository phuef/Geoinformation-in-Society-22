<template>
  <v-app>
    <div style="d-flex">
      <v-app-bar elevation="4" color="grey darken-4" class="px-0" dark width>
        <v-toolbar dense>
          <v-toolbar-title>Find Your Spot</v-toolbar-title>
          <v-spacer></v-spacer>
          <div>
            <v-btn to="/map" dark text class="ms-3"> Map </v-btn>
            <v-btn to="/impressum" dark text class="ms-3"> Impressum </v-btn>
          </div>
        </v-toolbar>
        <!--
        <v-container width="50%">
          <MainPage />
        </v-container>-->
      </v-app-bar>
    </div>
    <router-view/>
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
