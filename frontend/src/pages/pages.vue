<template>
  <v-app>
    <v-btn id="Login" @click="googleSignIn">Login</v-btn>
    <v-main>
      <label for="autocomplete-input">Enter a location:</label>
      <input id="autocomplete-input" type="text" />
      <v-btn @click="geoCoding()">Get Area</v-btn>
      <div v-if="geocodeResult">
        <p>{{ geocodeResult }}</p>
      </div>
      <div v-if="area">
        <p>{{ area }}</p>
      </div>
    </v-main>
  </v-app>
</template>

<!-- <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script> -->

<!-- <script
  type="text/javascript"
  src="../../../backend/simple_microservices/geocoding/geocoding.js"
></script> -->

<script>
import { signInWithGoogle } from "../components/authentication.js";
import {
  geocode,
  initAutocomplete,
} from "../../../backend/simple_microservices/geocoding/geocoding.js";

export default {
  mounted() {
    initAutocomplete(this.apiKey, this);
    // (address) => {
    //   this.geocodeResult = address;
    // }) // not sure of this, maybe parse it in a different way to another window
  },
  data() {
    return {
      area: null,
      geocodeResult: null,
      apiKey: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
    };
  },
  methods: {
    googleSignIn() {
      signInWithGoogle();
    },
    geoCoding() {
      if (this.geocodeResult) {
        geocode(this.geocodeResult).then((response) => {
          console.log(response);
          this.area = response;
        });
      }
    },
  },
};
</script>
