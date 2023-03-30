<template>
<div>
<v-hover v-slot="{ hover }">
  <v-card flat :elevation="hover ? 10 : 2" :class="{ 'on-hover': hover }" style="width:350px; height:430px" outlined class="pa-2"> 

  <v-avatar color="grey lighten-2" class="my-1 mx-3">
    <v-img :src="require('../assets/OrangeCat.png')" max-width="30"></v-img>
  </v-avatar>
  <span>{{aListing.corporate_name}}</span>

  <v-img :src="require('../assets/BlackCat.png')" class="mx-auto" max-height="300" max-width="300" contain/>
  
  <v-card-title class="">{{aListing.name}}</v-card-title>
  <!-- <v-card-text>
    {{aListing.description}}
  </v-card-text> -->


  <v-btn density="compact" depressed plain>
      <v-icon left color="green darken-4">mdi-map-marker</v-icon>
      <span class="subheading me-2">{{aListing.address}}</span>
  </v-btn>

  <v-btn density="compact" depressed plain class="ml-20">
      <v-icon left color="red">mdi-heart</v-icon>
      <!-- color can change to red it clicked -->
      <span class="subheading m-3">Like</span>
  </v-btn>

</v-card>
</v-hover>
</div>
</template>

<script>
import AOS from 'aos'
export default {
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
           
        }
    },
    methods: {
       // redirecting function below
        // redirect(petid){
        //     console.log(petid)
        //     this.$store.dispatch('loadedPet', petid)
        //     this.$router.push('/SearchAllPets/'+ petid)
        // }
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