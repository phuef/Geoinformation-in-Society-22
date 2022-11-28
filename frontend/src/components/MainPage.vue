<template>
  <v-container fluid style="height: 100vh">
    <v-row style="height: 100%">
      <v-col
        ><v-card>
          <v-level-drawer v-model="drawer" absolute temporary>
            <v-divider></v-divider>
            <v-btn icon @click.stop="mini = !mini">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
          </v-level-drawer>
        </v-card>
      </v-col>
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

export default {
  name: "MainPage",
  components: {
    MapView,
  },
};
</script>

<style scoped>
#mapContainer {
  height: 100%;
}
</style>
