<template>
  <v-app>
    <NavbarCorp v-if="this.$store.state.corporateName" />
    <Navbar v-else></Navbar>
    <v-main class="white">
      <router-view />
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from "../src/components/Navbar";
import Footer from "../src/components/Footer.vue";
import NavbarCorp from "../src/components/NavbarCorp";

export default {
  name: "App",
  components: { Navbar, Footer, NavbarCorp },
  mounted() {
    console.log(this.$store.state.corporateName);
  },
};
</script>
