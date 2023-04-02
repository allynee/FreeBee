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

/* global google */
export default {
  mounted() {
    this.initAutocomplete(this.apiKey, this);
  },
  data() {
    return {
      email: "",
      password: "",
      area: null,
      geocodeResult: null,
      apiKey: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
    };
  },
  methods: {
    loadGoogleMaps(apiKey) {
      return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
        script.onload = () => {
          resolve();
        };
        script.onerror = () => {
          reject(new Error("Failed to load Google Maps API script"));
        };
        document.head.appendChild(script);
      });
    },
    async initAutocomplete(apiKey) {
      await this.loadGoogleMaps(apiKey);
      const input = document.getElementById("autocomplete-input");
      const autocomplete = new google.maps.places.Autocomplete(input);
      // Set options for the autocomplete search box
      autocomplete.setFields(["place_id", "formatted_address"]);
      autocomplete.setTypes(["geocode"]);
      // Listen for changes to the input field
      autocomplete.addListener("place_changed", async () => {
        autocomplete.getPlace();
        // Use the getPlacePredictions() function to get more autocomplete results
        const service = new google.maps.places.AutocompleteService();
        const request = {
          input: input.value,
          types: ["geocode"],
        };
        try {
          const results = await new Promise((resolve, reject) => {
            service.getPlacePredictions(request, (results, status) => {
              if (status === google.maps.places.PlacesServiceStatus.OK) {
                resolve(results);
              } else {
                reject(status);
              }
            });
          });
          const address = results[0].description;
          this.geocodeResult = address; // parase address information to Vue
        } catch (error) {
          console.error(error);
        }
      });
    },
  },
};
</script>
