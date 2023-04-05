<template>
<div>
<v-hover v-slot="{ hover }">
<v-card flat :elevation="hover ? 12 : 2" :class="{ 'on-hover': hover }" style="max-width:400px" outlined>

    <!-- Lost or Found -->
    <div :class="{'green': isGreen, 'red': !isGreen, 'lighten-3' : true ,'py-2':true}">
        <div class="text-h6 text-center">{{aPet.petStatus}}</div>
    </div>

    <!-- Image -->
    <v-card-text class="d-flex justify-center align-center" style="height:300px;">
        <v-img :src="aPet.image" class="" contain max-height="250" max-width="350"/>
    </v-card-text>
        
    <!-- Pet Name --> 
    <div class="mx-1">
    <v-list-item>
        <span class="text-h5 primary--text"> {{aPet.petName}}</span>
        <!-- <v-chip right class="ml-5 font-weight-medium" color="green" text-color="white"> {{aPet.petStatus}} </v-chip> -->
        <!-- <v-chip class="green lighten-3 font-weight-medium
        primary--text ml-5 py-3 px-2">{{aPet.petStatus}}</span> -->
    </v-list-item>

    <!-- Location -->
    <v-list-item class="text-left">
    <v-icon left class="primary--text">mdi-map-marker</v-icon>
    <v-list-item-subtitle class="primary--text mx-2">{{aPet.petLocation}}</v-list-item-subtitle>
    </v-list-item>
        
    <!-- Date -->
    <v-list-item class="mb-2 text-left">
    <!-- <v-list-item-icon>
        <v-icon class="primary--text">mdi-calendar</v-icon>
    </v-list-item-icon> -->
    <v-icon left class="primary--text">mdi-calendar</v-icon>
    <v-list-item-subtitle class="primary--text mx-2"> {{ aPet.petDate}}</v-list-item-subtitle>
    </v-list-item>
        
    <v-divider></v-divider>
    
    <!-- More Details: to add unique pet id as query -->
    <v-card-actions>
         <v-btn depressed small class="brown lighten-4 text-capitalize my-3" @click="redirect(aPet.petid)">
        <span class="primary--text">view more details</span>
        <v-icon right class="primary--text">mdi-arrow-top-right</v-icon>
        </v-btn>
    </v-card-actions>
    </div>
</v-card>
</v-hover>
</div>
</template>

<script>
import AOS from 'aos'
export default {
    props: {
      aPet: Object,
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
        redirect(petid){
            console.log(petid)
            this.$store.dispatch('loadedPet', petid)
            this.$router.push('/SearchAllPets/'+ petid)
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