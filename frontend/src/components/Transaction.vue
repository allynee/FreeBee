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
                                {{ aTransaction.listing_details.name }}
                            </v-row>
                        </v-col>
                    
                        <v-col>
                            <v-row>
                                Quantity: {{ aTransaction.quantity }}
                            </v-row>
                            <v-row>
                                Claimed Item on {{ aTransaction.created.split("T")[0] }}
                            </v-row>
                            <v-row v-if="aTransaction.modified">
                                Last Status Update: {{ aTransaction.modified.split("T")[0] }}
                            </v-row>
                            <v-row v-else>
                                Last Status Update: {{ aTransaction.created.split("T")[0] }}
                            </v-row>
                            <v-row>
                                Collection Details: {{ aTransaction.listing_details.collection_details }}
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
          aTransaction: Object,
        },
        mounted() {
          AOS.init({
            duration: 1600,
          })
          console.log(this.aTransaction)

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
            },
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