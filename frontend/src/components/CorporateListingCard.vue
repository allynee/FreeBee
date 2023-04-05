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
        <v-card-actions>
          <!-- <v-btn v-if="isRed" depressed plain @click="like" class="">
           <v-icon :class="{'red': isRed}">mdi-heart</v-icon>\ -->

          <!-- </v-btn> -->
          <!-- <v-btn v-else depressed plain @click="like" class="">
          <v-icon :class="{'red': isRed}">mdi-circle</v-icon>
          this not is red
       </v-btn> -->
        </v-card-actions>

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
          <!-- <v-btn small class="amber lighten-4 ml-2" style="margin-bottom: 10px;" depressed outlined @click="subscribe">
            <v-icon left small>mdi-pencil-outline</v-icon>
            View your listing
        </v-btn>
        <v-btn small class="amber lighten-4 ml-2" depressed outlined @click="subscribe">
            <v-icon left small>mdi-delete-empty</v-icon>
            Delete Listing
        </v-btn> -->
        </v-card-text>
      </v-card>
    </v-hover>
  </div>
</template>

<script>
import AOS from "aos";
// import axios from 'axios'

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
