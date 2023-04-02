<template>
<div>
<v-hover v-slot="{ hover }">
  <v-card flat :elevation="hover ? 10 : 2" :class="{ 'on-hover': hover }" style="width:350px; height:470px" outlined class="pa-2"> 
  <v-card-actions>
    <!-- <v-btn v-if="isRed" depressed plain @click="like" class="">
       <v-icon :class="{'red': isRed}">mdi-heart</v-icon>\ -->
      <div v-if="isRed">
       <v-btn icon color="pink">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </div>
      <div v-else>
        <v-btn icon color="grey">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </div>
    <!-- </v-btn> -->
    <!-- <v-btn v-else depressed plain @click="like" class="">
      <v-icon :class="{'red': isRed}">mdi-circle</v-icon>
      this not is red
   </v-btn> -->
  </v-card-actions>

  <v-img cover :src="require('../assets/BlackCat.png')" class="mx-auto" contain
  @click="$emit('gotoListing')"/>
  
  <v-card-title class="">{{aListing.name}}</v-card-title>
  <v-divider class="mx-3 mb-1"></v-divider>
  <v-card-text> 
    <div class="text-subtitle-2 mb-2">
      Posted By: {{aListing.corporate_name}}
    </div>
    <div class="mb-2">
      <v-icon small left color="green darken-4">mdi-map-marker</v-icon>
      <span class="subheading me-2">{{aListing.address}}</span>
    </div>
    <div class="text-subtitle-2 font-weight-bold mb-2 red--text text--darken-4">
      {{aListing.quantity}} left in stock!
    </div>
  </v-card-text>

</v-card>
</v-hover>
</div>
</template>

<script>
import AOS from 'aos'
import axios from 'axios'

export default {
    emits:['gotoListing'],
    props: {
      aListing: Object,
    },
    mounted() {
      AOS.init({
        duration: 1600,
      })
    },
    data(){
        return{ 
           isRed: false
        }
    },
    methods: {
      like(){
        const user_URL = 'http://localhost:8421/favourite'
        axios.post(user_URL, {
          // beneficiary_id: this.$store.state.uid,
          // listing_id: this.aListing.listing_id
          beneficiary_id: "blabla",
          listing_id: this.aListing.listing_id
        }).then((response) => {
          const response_data = response.data;
          if (response_data.statusCode == "200") {
            console.log(response_data.name)
            this.isRed = true;
            console.log(this.isRed);
          } else {
            console.log("fail");
          }
        })
      }
    },
}
</script>

<style scoped>
.v-card {
  transition: opacity .2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
 }

</style>