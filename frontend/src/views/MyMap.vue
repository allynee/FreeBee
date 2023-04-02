<template>
  <div>
        <v-container class="brown lighten-5 pb-10 px-10">
          <v-row justify="center" class="text-center my-10" data-aos="fade-down">
            <v-cols cols="12" align="center" data-aos="fade-left">
              <v-img :src="require('../assets/rabbits.png')" class="my-3" contain height="200"/>
            </v-cols>
            <v-col cols="12">
                <h1 class="text-h4 brown--text text-center">Locate All Reported Pets</h1>
            </v-col>
        <v-col cols="8" align="center" >
            <p class="text-h6 font-weight-light brown--text text--darken-2">
              To view the locations of all the pets that have been reported lost/found, refer to the map below.
              Each location market represents the location where each reported pet was lost/found.
              Click on a marker to zoom in to a pet's specific location and access more information about it!
            </p>
        </v-col>
        </v-row>
      <v-divider></v-divider>
      <Map></Map>
   </v-container>
   </div>
</template>
        
<script>
import Map from "../components/Map";

    export default {
      name: "MyMap",
      components: {Map},
      data(){
        return {
          //no data for now
          
        }
      },
      methods: {
          //no methods for now
      }
    }
</script>