<template>
<div v-if="loaded">
    <v-row justify="center" class="my-15">
      <v-col cols="12" align="center" data-aos="fade-left">
        <video-background :src="require(`@/assets/bee.mp4`)" style="height: 250px; width: 180px">
        </video-background>
      </v-col>
    </v-row>
</div>
<div v-else>
  <div class="white darken-3">
    <div class="py-5">
      <v-row class="my-15 justify-center">
        <span data-aos="fade-right" class="mr-15">
          <video-background
            :src="require(`@/assets/flipbee.mp4`)"
            style="height: 85px; width: 60px"
          >
          </video-background>
        </span>


        <h1
          class="text-md-h3 text-sm-h2 grey--text text--darken-4 font-weight-light justify-center"
          data-aos="fade-down"
        >
          Welcome Back!
        </h1>
        <span data-aos="fade-left" class="ml-15">
          <video-background
            :src="require(`@/assets/bee.mp4`)"
            style="height: 85px; width: 60px"
          >
          </video-background>
        </span>
      </v-row>
      <v-row class="my-15">
        <SearchBar></SearchBar>
      </v-row>
      
    </div>

    <div class="mx-15 px-15">

     <!-- Categories -->
      <v-row class="">
        <span class="text-h4 grey--text text--darken-3">Your Listings</span>
        <!-- <span style="width:80%" class="justify-right">
          <v-btn plain depressed class="grey--text text--darken-4">
          <v-icon small left>mdi-view-grid</v-icon>See all categories</v-btn>
        </span> -->
      </v-row>

      <v-row class="my-15">
        <v-col>
          <CorporateListingCard></CorporateListingCard>
        </v-col>
      </v-row>
  </div>

    <!-- scroll to top button -->
    <v-btn v-scroll="onScroll" v-show="fab" fab fixed bottom right color="amber lighten-3" @click="toTop">
      <v-icon>mdi-chevron-up</v-icon>
    </v-btn>

  </div>
</div>

</template>

<script>

// import AOS from 'aos'
// import axios from 'axios'
import CorporateListingCard from '@/components/CorporateListingCard.vue';
import SearchBar from '@/components/SearchBar.vue';

export default {

name: 'corporatehomepage',
data(){
  return{
      fab: false,
      myStatuses: ['In Progress', 'Ready for Collection', 'Collected', 'Cancelled'],    

  }
},
components : {CorporateListingCard, SearchBar},

methods:{
  
},

computed:{
  
},
}

</script>

<style scoped>

</style>