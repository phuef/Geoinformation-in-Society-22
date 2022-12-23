<template>
  <div class="container pt-10">
    <h1>Legal Notice</h1>
    <h2 class="pt-4">Disclosures according to §5 TMG</h2>
    <br />
    <p>
      Find your spot<br />
      Institute for Geoinformatics<br />
      Heisenbergstraße 2<br />
      48149 Münster<br />
    </p>
    <v-btn
      elevation="0"
      color="white"
      href="https://github.com/phuef/Geoinformation-in-Society-22"
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
