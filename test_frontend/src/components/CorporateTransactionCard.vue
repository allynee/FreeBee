<template>
    <div>
        <v-card width="100%">
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col>
                            <v-row>
                                Status
                            </v-row>
                            <v-row>
                                <v-select
                                style="margin-right: 15px"
                                rounded
                                outlined
                                name="status"
                                placeholder="In Progress"
                                id="status"
                                v-model="CurrentStatus"
                                :items=myStatuses>
                                </v-select>
                            </v-row>
                        </v-col>
                    
                        <v-col>
                            <v-row>
                                Beneficiary: Melvin
                            </v-row>
                            <v-row>
                                Quantity claimed: 100
                            </v-row>
                            <v-row>
                                Claimed Item on 10/10/2021 13:01
                            </v-row>
                            <v-row>
                                Last Status Update: 12/10/2021 08:40
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
                myStatuses: ['In Progress', 'Ready for Collection', 'Collected', 'Cancelled'],               
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