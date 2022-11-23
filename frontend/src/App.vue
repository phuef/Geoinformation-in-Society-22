<template>
  <v-app>
    <v-card
      color="grey lighten-4"
      flat
      height="100%"
      tile
    >
      <v-toolbar dense>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Find Your Spot</v-toolbar-title>

        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container width="50%">
        <MainPage/>
      </v-container>
    </v-card>
    
  </v-app>
</template>

<script>
import MainPage from './components/MainPage.vue'

export default {
  name: 'App',
  components: {
    MainPage
  }
}
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

