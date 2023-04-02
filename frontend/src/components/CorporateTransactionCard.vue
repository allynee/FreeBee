<template>
    <div>
        <v-card width="100%" style="margin-bottom: 15px;" >
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col>  
                            <v-row>
                            <v-list-item>
                                <v-checkbox/>
                            </v-list-item>
                            </v-row>    
                            <v-row>
                                <v-btn tile color="green" style="margin-left: 15px;">
                                        {{ transaction.status }}
                                </v-btn>
                            </v-row>
                        </v-col>
                        <v-col>
                            <v-row>
                                Beneficiary ID: {{ transaction.beneficiary_id }}
                            </v-row>
                            <v-row>
                                Quantity claimed: {{ transaction.quantity }}
                            </v-row>
                            <v-row>
                                Claimed Item on {{ transaction.created.split('T')[0] }} {{ transaction.created.split('T')[1] }}
                            </v-row>
                            <v-row v-if="transaction.modified">
                                Last Status Update: {{ transaction.modified.split('T')[0] }} {{ transaction.modified.split('T')[1] }}
                            </v-row>
                            <v-row v-else>
                                Last Status Update: {{ transaction.created.split('T')[0] }} {{ transaction.created.split('T')[1] }}
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
          transaction: Object,
        },
        mounted() {
          AOS.init({
            duration: 1600,
          })
          console.log(this.transaction)
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