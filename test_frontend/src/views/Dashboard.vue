<template>
  <div>
    <v-container class="py-10">
      <!-- title -->
      <v-row justify="center"><v-col cols="12" data-aos="fade-down">
        <div>
        <v-img :src="require('../assets/Dog1Invert.png')" class="d-inline-block mx-3" contain max-height="60" max-width="60"/>
        <span class="text-h4 text-capitalize brown--text">Search for a pet</span>
        </div>
      </v-col></v-row>

        <!-- Filter Bar -->
        <v-row justify="center"><v-col cols="12">  
        <v-expansion-panels flat class="rounded-xl">
        <v-expansion-panel class="rounded-xl">
        <v-expansion-panel-header expand-icon="mdi-filter-variant" class="pa-5 rounded-xl">
          <!-- <v-icon >mdi-filter-variant</v-icon> -->
          <span  class="text-h5 primary--text font-weight-light">Edit Filters</span>
        </v-expansion-panel-header>
  
        <!-- Filter Bar content i.e. the diff filters-->
        <v-expansion-panel-content>
        <v-card flat class="pa-5 rounded-xl"> 

          <!-- All, Lost, or Found -->
          <v-row justify="center" class="">
                <v-radio-group v-model="petStatus">
                <v-col cols="12" align="center">
                  <v-btn rounded depressed color="brown lighten-5 mx-4 my-2">
                       <v-radio label="All Pets" value="All" required ></v-radio>
                    </v-btn> 
                        <v-btn rounded depressed color="brown lighten-5 mx-4 my-2">
                            <v-radio label="Lost Pets" value="Lost Pet" required ></v-radio>
                        </v-btn> 
                        <v-btn rounded depressed color="brown lighten-5 mx-4 my-2" >
                            <v-radio label="Found Pets" value="Found Pet" required ></v-radio>
                        </v-btn>
                </v-col>
                </v-radio-group>
          </v-row>

         
          <v-row>
             <!-- Pet Type -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox outlined v-model="petTypesSelected" :items="petTypes" label="Select Pet Types" multiple></v-combobox>
            </v-col>
            <!-- Pet Breed -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox hide-no-data v-model="petBreedsSelected" outlined :items="petBreeds" label="Select Pet Breeds" class="text-brown" multiple></v-combobox>
            </v-col>
            <!-- Pet Color -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox outlined v-model="petColorsSelected" :items="petColors" label="Select Pet Colors" multiple></v-combobox>
            </v-col>

            <!-- Collar Color -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox outlined v-model="collarColorsSelected" :items="collarColors" label="Select Collar Colors" multiple></v-combobox>
            </v-col>
            <!-- Pet Size -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox outlined v-model="petSizesSelected" :items="petSizes" label="Select Pet Sizes" multiple></v-combobox>
            </v-col>
            <!-- Pet Gender -->
            <v-col cols="12" md="6" lg="4">
              <v-combobox outlined v-model="petGendersSelected" :items="petGenders" label="Select Pet Genders" multiple></v-combobox>
            </v-col>
          </v-row>
        </v-card>
        </v-expansion-panel-content>
        </v-expansion-panel>
        </v-expansion-panels>
  
        <!-- Show all filters applied -->
        
        <v-card flat class="my-1 brown lighten-5">
          <v-card-subtitle>Current Filters Applied:</v-card-subtitle>
          <v-card-text>
            <v-row>
            <!-- petTypes -->
            <v-chip-group column v-model="petTypesSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="petType in petTypesSelected" :key="petType" :value="petType">
                  <span> {{ petType }} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>
            <!-- pet colours -->
            <v-chip-group column v-model="petColorsSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="petColor in petColorsSelected" :key="petColor" :value="petColor">
                  <span> {{ petColor }} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>

            <!--  pet breeds-->
            <v-chip-group column v-model="petBreedsSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="petBreed in petBreedsSelected" :key="petBreed" :value="petBreed">
                  <span> {{ petBreed }} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>

              <!--  collar colous-->
              <v-chip-group column v-model="collarColorsSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="collarColor in collarColorsSelected" :key="collarColor" :value="collarColor">
                  <span> {{ collarColor}} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>

              <!-- pet size-->
              <v-chip-group column v-model="petSizesSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="petSize in petSizesSelected" :key="petSize" :value="petSize">
                  <span> {{ petSize}} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>

              <!-- pet genders-->
              <v-chip-group column v-model="petGendersSelected" multiple>
              <v-chip label filter filter-icon="" class="pa-3 mx-1 brown lighten-5" v-for="petGender in petGendersSelected" :key="petGender" :value="petGender">
                  <span> {{ petGender}} </span>
                  <v-icon small right>mdi-window-close</v-icon>
              </v-chip>
            </v-chip-group>


          </v-row>
          </v-card-text>
        </v-card>
        </v-col>
        </v-row>
        
        <v-divider></v-divider>
      
      <!-- Grid, List, Map View -->
      <v-row class="my-5 pa-5">
      <v-btn depressed class="brown lighten-4 mr-5" @click="view='grid'">
        <v-icon left>mdi-grid</v-icon>
            <span>Grid View</span>
      </v-btn>
      <v-btn depressed class="brown lighten-4 mr-5" @click="view='map'">
        <v-icon left>mdi-map</v-icon>
            <span>Map View</span>
      </v-btn>
      <v-btn depressed class="brown lighten-4 mr-5" @click="view='list'">
        <v-icon left>mdi-format-list-bulleted-square</v-icon>
            <span>List View</span>
      </v-btn>
      </v-row>
      
    <!-- Grid view -->
    <div v-show="view=='grid'" data-aos="fade-up">
    <v-row class="my-5">
    <!-- Dashboard -->
    <v-col cols="12" md="6" lg="4" v-for="aPet in myPets" :key="aPet.petid" align="center">
      <PetCard :aPet="aPet"></PetCard>
    </v-col>
    </v-row>
    </div>
    <!-- Map View -->
    <Map v-show="view=='map'" :allPets="myPets"></Map>
    </v-container>
    <!-- Scroll to top -->
    <v-btn v-scroll="onScroll" v-show="fab" fab fixed bottom right color="brown lighten-4" @click="toTop">
        <v-icon>mdi-chevron-up</v-icon>
    </v-btn>
  
  </div>
</template>
  
<script>
import PetCard from "../components/PetCard.vue"
import Map from "../components/Map";
import db from '../firebase/index'
import {collection, getDocs} from 'firebase/firestore'
import AOS from 'aos'

  export default {
  components: { PetCard, Map},
  mounted() {
      AOS.init({
        duration: 1400,
      })
  },
  data(){
    return {
      fab: false,
      view: "grid",
      petBreeds: ['Affenpinscher Dog', 'Afghan Hound Dog', 'Alaskan Malamute Dog', 'Australian Kelpie Dog'],
        // data
        petStatus: "",
        petTypes: ["Dog","Rabbit","Cat","Bird","Hamster","Fish","Terrapin","Frog","Guinea Pig","Other Pet Types"],
        petTypesSelected: [],
        petBreedsSelected: [],
        petColors: ["White","Black","Brown","Orange","Other Colours"],
        petColorsSelected: [],
        collarColors: ["No Collar", "Beige", "Black","Brown", "Grey", "White", "Pink", "Blue", "Yellow", "Red", "Others"],
        collarColorsSelected: [],
        petGenders: ['Male','Female',"Unknown"],
        petGendersSelected: [],
        petSizes: ['Small', 'Medium', 'Large'],
        petSizesSelected: [],
          
        //pets array retrieved from firebase:
        allPetsArray:[],
    }
  },
  created(){
    const petRef=collection(db, 'Pets')
    getDocs(petRef)
    .then( (snapshot)=>{
      snapshot.docs.forEach( (doc)=>{
        this.allPetsArray.push( {...doc.data()})
      })
    })
  },
  computed: {
      // toggleView(){

      // },
      myPets(){
        return this.allPetsArray.filter(pet => {
          let finalFilter = "";
          // pet breed
          if(this.petBreedsSelected.length!=0){
            finalFilter += `${this.petBreedsSelected.includes(pet.petBreed)}`;
          }
          // pet type
          if(this.petTypesSelected.length!=0){
            finalFilter += `${this.petTypesSelected.includes(pet.petType)}`;
          }
          // // pet color
          if(this.petColorsSelected.length!=0){
            finalFilter += `${this.petColorsSelected.includes(pet.petColor)}`;
          }

          // pet gender
          if(this.petGendersSelected.length!=0){
            finalFilter += `${this.petGendersSelected.includes(pet.petGender)}`;
          }
          // pet size
          if(this.petSizesSelected.length!=0){
            finalFilter += `${this.petSizesSelected.includes(pet.petSize)}`;
          }
          // pet collar color
          if(this.collarColorsSelected.length!=0){
            finalFilter += `${this.collarColorsSelected.includes(pet.collarColor)}`;
          }

          // status
          if(this.petStatus!="" && this.petStatus!="All"){
            finalFilter += `${this.petStatus == pet.petStatus}`;
          }
          // check if there are any filters
          if (finalFilter.includes("false")){
            return false;
          }else{
            return true;
          }
        })
      },
  },
  methods: {
    onScroll (e) {
      if (typeof window === 'undefined') return
      const top = window.pageYOffset ||   e.target.scrollTop || 0
      this.fab = top > 20
    },
    redirect(petid){
            this.$store.dispatch('loadedPet', petid)
            this.$router.push('/SearchAllPets/'+ petid)
        },
    toTop () {
      this.$vuetify.goTo(0)
    },
  }
  }
  
</script>