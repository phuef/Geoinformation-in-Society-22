<template>
  <v-app>
    <v-app-bar app color="#313641" elevation="0" dark>
      <v-toolbar-title style="cursor: pointer" @click="$router.push('/')">
        Find your spot
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="d-none d-sm-flex">
        <v-btn to="/" dark text class="ms-3">Home</v-btn>
        <v-btn to="/impressum" dark text class="ms-3">About</v-btn>
      </v-toolbar-items>
      <div class="d-flex d-sm-none">
        <v-menu z-index="1000">
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list nav>
            <v-list-item link to="/">
              <v-list-tile-title>Home</v-list-tile-title>
            </v-list-item>
            <v-list-item link to="/impressum">
              <v-list-tile-title>About</v-list-tile-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-app-bar>
    <v-main style="height: 100vh">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  components: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
html,
body {
  height: 100%;
  overflow-y: auto !important;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
