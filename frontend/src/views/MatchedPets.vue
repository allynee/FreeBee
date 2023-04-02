<template>
    <v-container class="py-15">
            <v-row justify="center" class="text-center mb-10" data-aos="fade-down">
                <v-col cols="12">
                    <v-img :src="require('../assets/try.png')" contain height="250"/>
                </v-col>
                <v-col cols="12">
                    <h1 class="text-h4 brown--text text-center">Recommended Pets for You</h1>
                </v-col>
                <v-col cols="8" align="center" >
                    <p class="text-h6 font-weight-light brown--text text--darken-2">
                        These pets are similar to the pet(s) that you have lost or found. 
                    </p>
                </v-col>
            </v-row>
        <v-divider></v-divider>
        
        <v-row class="my-15">
        <!-- Dashboard -->
        
        <v-col cols="12" md="6" lg="4" v-for="aPet in myPets" :key="aPet.petid" align="center">
            <PetCard :aPet="aPet"></PetCard>
        </v-col>
        </v-row>

    </v-container>
</template>

<script>
import PetCard from "../components/PetCard.vue"
import db from '../firebase/index'
import {collection, getDocs} from 'firebase/firestore'

export default {
  components: {PetCard},
  data(){
    return {
        allPetsArray:[],
        allProps: ["petName","petBreed","collarColor","petColor","petGender","petSize"],
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
    listedPets(){
        return this.$store.getters.listedpet
    },
    myPets(){
        let finalArr = []
        this.listedPets.forEach(e1 => {
            let similarCount = 0 ; 
            this.allPetsArray.forEach(e2 => {
                if(e1.petStatus!=e2.petStatus){
                    if(e1.petType==e2.petType){
                        for(let i=0;i<this.allProps.length;i++){
                        let prop = this.allProps[i]
                        console.log(e1[prop])
                        if(e1[prop]==e2[prop]){
                            similarCount += 1;
                        }
                        }
                        if(similarCount>2){
                            finalArr.push(e2)
                        }
                    }
                }
            });
        });
        return finalArr
    },
  },
}
</script>