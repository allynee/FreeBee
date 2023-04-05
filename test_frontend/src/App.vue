<template>
  <v-app>
    <Navbar />
    <v-main class="white">
      <router-view/>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from "../src/components/Navbar"
import Footer from "../src/components/Footer.vue"

export default {
  name: 'App',
  components: {Navbar, Footer},
};
</script>
