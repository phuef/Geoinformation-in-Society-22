<template>
  <v-app>
    <div style="d-flex">
      <v-app-bar elevation="4" color="grey darken-4" class="px-0" dark width>
        <v-toolbar-title style="cursor: pointer" @click="$router.push('/')"
          >Find your spot</v-toolbar-title
        >

        <v-spacer></v-spacer>
        <div class="d-none d-sm-flex align-items-center">
          <v-toolbar-items>
            <v-btn to="/" dark text class="ms-3"> Main </v-btn>
            <v-btn to="/impressum" dark text class="ms-3"> Legal Notice </v-btn>
          </v-toolbar-items>
        </div>
        <div class="d-flex d-sm-none align-items-center">
          <v-menu offset-y z-index="1000">
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
        </div>
      </v-app-bar>
    </div>
    <router-view />
  </v-app>
</template>

<script>
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
