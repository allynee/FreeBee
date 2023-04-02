<template>
  <Corporate v-if="this.$store.state.corporateName" />

  <Welcome v-else />
</template>

<script>
import Welcome from "../components/Welcome";
import Corporate from "../views/CorporateHomePage";
export default {
  name: "Home",

  components: {
    Welcome,
    Corporate,
  },
  mounted() {},
};
</script>
