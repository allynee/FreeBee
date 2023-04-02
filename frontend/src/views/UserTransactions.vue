<template>
    <div class="white pa-5 bground" style="height:50%">
        <v-container class="pb-15" style="width:50%;" data-aos="fade-down">
            <v-row class="mb-7 ml-1 mt-1">
                <span class="text-h4 text-capitalize brown--text">These freebies are waiting for you!</span>
            </v-row>
            
            <v-tabs v-model="tab" grow class="rounded-lg">
                <v-tab class="amber lighten-2">In Progress</v-tab>
                <v-tab class="amber lighten-2">Ready for Collection</v-tab>
                <v-tab class="amber lighten-2">Completed</v-tab>
                <v-tab class="amber lighten-2">Cancelled</v-tab>
            </v-tabs>
            <v-tabs-items v-model="tab" class="rounded-lg pa-3 amber lighten-5">
                <v-tab-item :value="0">
                    <v-card flat v-for="aTransaction in inProgressArray" :key="aTransaction.transaction_id" class="my-5 mx-5">
                        <Transaction :aTransaction="aTransaction"></Transaction>
                    </v-card>
                </v-tab-item>
                    
                <v-tab-item :value="1">
                    <v-card-text>
                            
                    </v-card-text>
                </v-tab-item>

                <v-tab-item :value="2">
                    <v-card-text>
                            
                    </v-card-text>
                </v-tab-item>

                <v-tab-item :value="3">
                    <v-card-text>
                            
                    </v-card-text>
                </v-tab-item>
            </v-tabs-items>
        </v-container>                    
    </div>
</template>
  
  <style src="../style/style.css">
</style>
  
  <script>
    import Transaction from '../components/Transaction.vue'
    import axios from 'axios'
  
    export default {

      name: 'register',
      data(){
        return{
            fab: false,
            tab: null,
            inProgressArray:[],
            readyArray:[],
            completedArray:[],
            cancelledArray:[],
        }
      },
      components : {Transaction},

      methods:{
        async fetchTransactions() {
            const transaction_URL = 'http://localhost:5100/transaction_management/beneficiary/' + this.$store.state.uid
            axios.get(transaction_URL).then((response) => {
                console.log(response.data.result)
                response.data.result.forEach((transaction) => {
                    if (transaction.status == 'In Progress') {
                        this.inProgressArray.push(transaction)
                    }
                    else if (transaction.status == 'Ready for Collection') {
                        this.readyArray.push(transaction)
                    }
                    else if (transaction.status == 'Completed') {
                        this.completedArray.push(transaction)
                    }
                    else if (transaction.status == 'Cancelled') {
                        this.cancelledArray.push(transaction)
                    }
                })
            })
        }
      },

      computed:{
        loading(){
            return this.$store.getters.loading
        },
        
      },
      mounted(){
        this.fetchTransactions()
      }
    }
  </script>
  <style scoped>
  .bground {
    background-size: cover;
    height: 120vh;
    background-position: 20px;
    width: 100%
  }
  </style>
  