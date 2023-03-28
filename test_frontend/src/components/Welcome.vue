<!-- Welcome page -->

<template>
  <div class="white darken-3">
    <v-container class="py-10">
      <v-row class="my-5 justify-center">
        <h1
          class="text-md-h3 text-sm-h2 grey--text text--darken-4 font-weight-light justify-center"
          data-aos="fade-down"
        >
          What FreeBee are you looking for?
        </h1>
      </v-row>
      <v-row class="my-15">
        <SearchBar></SearchBar>
      </v-row>

      <v-row>
        <v-col cols="10">
          <h1 class="text-h4 grey--text text--darken-3">Categories</h1>
        </v-col>
        <v-col cols="2" class="justify-right">
          <v-btn plain depressed class="grey--text text--darken-4">
            <v-icon small left>mdi-view-grid</v-icon>See all categories</v-btn
          >
        </v-col>
      </v-row>

      <v-row class="my-15">
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
      </v-row>
      <v-row>
        <h1 class="text-h4 grey--text text--darken-3">Recommended for you</h1>
      </v-row>

      <v-row justify="center" class="my-5">
        <v-col cols="12" align="center" data-aos="fade-left">
          <!-- <div data-aos="fade-left"> -->
          <video-background
            :src="require(`@/assets/test.mp4`)"
            style="height: 300px; width: 300px"
          >
          </video-background>
          <!-- </div> -->
        </v-col>
      </v-row>
      <v-row>
        <h1 class="text-h4 grey--text text--darken-3">All FreeBees</h1>
      </v-row>
      <v-row class="my-15">
        <v-col cols="4">
          <Listing></Listing>
        </v-col>
        <v-col cols="4">
          <Listing></Listing>
        </v-col>
        <v-col cols="4">
          <Listing></Listing>
        </v-col>
      </v-row>

      <!-- <v-row justify="center" class="">
        <v-col cols="8" align="center" >
        <h1 class="text-h4 brown--text text--darken-2 font-weight-bold">What categories are you looking for?</h1>
        <br>
        <p class="text-h6 font-weight-light brown--text text--darken-1 mb-11">
          FindPetNOW is an online platform that supports you in your journey <br>of finding your lost pet. 
          Report your lost dog, cat, terrapin and other pets<br> today to boost the chances
          of finding your lost pet. 
        </p>
        </v-col>
      </v-row> -->
    </v-container>

    <!-- scroll to top button -->
    <v-btn
      v-scroll="onScroll"
      v-show="fab"
      fab
      fixed
      bottom
      right
      color="green lighten-2"
      @click="toTop"
    >
      <v-icon>mdi-chevron-up</v-icon>
    </v-btn>
  </div>
</template>

<script>
import AOS from 'aos'
import Category from './Category.vue';
import SearchBar from './SearchBar.vue';
import Listing from './Listing.vue';
  export default {
    name: "HelloWorld",
    mounted() {
        AOS.init({
            duration: 1600,
        });
    },
    data() {
        return {
            fab: false,
            //listings array retrieved from MS:
            categories: ["Food and Beverage",""],
            allListingsArray:[],
        };
    },
    scroll() {
      document.querySelector(this.href).scrollIntoView({ behavior: "smooth" });
    },
    components: { SearchBar, Category, Listing},
    methods:{
      async fetchListings() {
          const listing_URL = 'http://0.0.0.0:8000/listing'
          const response =
            fetch(listing_URL)
                .then(response => response.json())
                .then(data => {
                    console.log(response);
                })
                .catch(error => {
                    // Errors when calling the service; such as network error, 
                    // service offline, etc
                    console.log(this.message + error);
                });
      }
    },
    created(){
      this.fetchListings()
    }
} 
</script>
