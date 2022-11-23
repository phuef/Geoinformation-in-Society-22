<template>
  <div class="container pt-10">
    <h1>Impressum</h1>
    <v-row justify="center">
      <h2 class="pt-4">Angaben gemäß §5 TMG</h2>
      <p>
        Digital Peaks<br />
        Institut für Geoinformatik<br />
        Heisenbergstraße 2<br />
        48149 Münster<br />
      </p>
    </v-row>
    <v-btn
      class="pt-10"
      elevation="0"
      color="white"
      href="https://github.com/digital-peaks"
      target="_blank"
    >
      <v-icon>mdi-github</v-icon> Github
    </v-btn>
  </div>
</template>
<script>
export default {
  name: "ImpressumView",
};
</script>

<style scoped>
.v-btn:not(.v-btn--round).v-size--default {
  height: 36px;
  min-width: 64px;
  padding: 0 3px;
}
</style>
