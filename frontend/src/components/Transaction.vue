<template>
    <div>
        <v-card width="100%">
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col>
                            <v-row>
                                <v-img :src="require('../assets/pigbee.jpg')" max-width="70"></v-img>
                            </v-row>
                            <v-row>
                                Item Name
                            </v-row>
                        </v-col>
                    
                        <v-col>
                            <v-row>
                                Quantity: 10
                            </v-row>
                            <v-row>
                                Claimed Item on 10/10/2021 13:01
                            </v-row>
                            <v-row>
                                Last Status Update: 12/10/2021 08:40
                            </v-row>
                            <v-row>
                                Collection Details: Please ring doorbell 8 times
                            </v-row>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
        </v-card>
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
            redirect(listingid){
                console.log(listingid)
                this.$store.dispatch('loadedPet', listingid)
                this.$router.push('/FindFreeBee/'+ listingid)
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