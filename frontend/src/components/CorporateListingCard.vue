<template>
  <div>
    <v-hover v-slot="{ hover }">
      <v-card
        flat
        :elevation="hover ? 10 : 2"
        :class="{ 'on-hover': hover }"
        style="width: 350px; height: 375px"
        outlined
        class="pa-2"
      >
        <v-img
          cover
          style="max-height: 200px"
          :src=aListing.firebase_url
          class="mx-auto"
          @click="$emit('gotoListing')"
        />

        <v-card-title class="">{{ aListing.listing.name }}</v-card-title>
        <v-divider class="mx-3 mb-1"></v-divider>
        <v-card-text>
          <div
            class="text-subtitle-2 font-weight-bold mb-2 black--text text--darken-4"
          >
            Quantity Left: {{ aListing.listing.quantity }}
          </div>
          <div
            class="text-subtitle-2 font-weight-bold mb-2 red--text text--darken-4"
            v-if=" aListing.listing.status == 'Unavailable'"
            >
            Status: {{ aListing.listing.status }}
          </div>
          <div
            class="text-subtitle-2 font-weight-bold mb-2 green--text text--darken-4"
            v-if=" aListing.listing.status == 'Available'"
            >
            Status: {{ aListing.listing.status }}
          </div>
        </v-card-text>
      </v-card>
    </v-hover>
  </div>
</template>

<script>
import AOS from "aos";

export default {
  emits:['gotoListing'],

  props: {
    aListing: Object,
  },
  mounted() {
    AOS.init({
      duration: 1600,
    });
  },
  data() {
    return {
      isRed: false,
    };
  },
  methods: {},
};
</script>

<style scoped>
.v-card {
  transition: opacity 0.2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
}
</style>
