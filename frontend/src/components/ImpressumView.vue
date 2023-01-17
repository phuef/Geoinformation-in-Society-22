<template>
  <div class="container pt-10">
    <h1>Legal notice</h1>
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
    <div>
      <h3 class="pt-8">Data Source</h3>
      <br />
      <p>
        The
        <a href="https://opendata.stadt-muenster.de/" target="_blank"
          >Muenster Open Data</a
        >
        which is mantained by the Münster city administration was used as the
        main data source for this application. <br />
      </p>

      <ul>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/b%C3%A4der"
            target="_blank"
            >Baths</a
          >
        </li>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/standorte-der-kinos"
            target="_blank"
            >Cinemas</a
          >
        </li>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/standorte-der-museen"
            target="_blank"
            >Museums</a
          >
        </li>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/kinderspielpl%C3%A4tze"
            target="_blank"
            >Playgrounds</a
          >
        </li>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/sporthallen-und-sportst%C3%A4tten-standorte"
            target="_blank"
            >Sport Facilities</a
          >
        </li>
        <li>
          <a
            href="https://opendata.stadt-muenster.de/dataset/theater-m%C3%BCnster"
            target="_blank"
            >Theaters</a
          >
        </li>
      </ul>
    </div>
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

a {
  color: #000000;
  text-decoration: none;
}
</style>
