<template>
    <div>
    <v-hover v-slot="{ hover }">
    <v-card flat :elevation="hover ? 12 : 2" :class="{ 'on-hover': hover }" style="max-width:400px" outlined>
    
        <!-- Lost or Found -->
        <div :class="{'green': isGreen, 'red': !isGreen, 'lighten-3' : true ,'py-2':true}">
            <div class="d-flex">
                <div class="text-h6 ml-5 my-1">{{aPet.petStatus}}</div>
                <v-spacer></v-spacer>
                <v-tooltip top color="brown lighten-4">
                    <template v-slot:activator="{ on, attrs }">
                        <v-tab color="primary" v-bind="attrs" v-on="on">
                            <!-- delete button -->
                            <v-btn small icon outlined class="text-capitalize my-1" @click="deletePet(aPet)">
                            <v-icon class="primary--text mx-0">mdi-trash-can-outline</v-icon>
                            </v-btn>
                        </v-tab>
                    </template>
                    <span class="black--text">Delete this Post</span>
                </v-tooltip>
            </div>
        </div>
    
        <!-- Image -->
        <v-card-text class="d-flex justify-center align-center" style="height:250px;">
            <v-img :src="aPet.image" class="" contain max-height="250" max-width="300"/>
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
             <v-btn outlined small class="text-capitalize my-3" @click="redirect(aPet.petid)">
            <span class="primary--text">view pet page</span>
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
            // getImgUrl(pic){
            //     console.log(this.aPet.petStatus)
            // return require('../assets/' + pic)
            // },
            redirect(petid){
                console.log(petid)
                this.$store.dispatch('loadedPet', petid)
                this.$router.push('/SearchAllPets/'+ petid)
            },
            deletePet(pet_obj){
                
                this.$store.dispatch('deletePetArray', pet_obj)
                var newarray=this.$store.getters.getuser
                console.log(newarray)
                this.$store.dispatch('deleteUserArray',newarray)
            },
        },
        computed: {
            isGreen(){
                if(this.aPet.petStatus=="Found Pet"){
                    return true
                }else{
                    return false
                }
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