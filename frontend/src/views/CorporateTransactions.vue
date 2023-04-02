<template>
    <div class="white pa-5 bground" style="height:50%">
        <v-container class="pb-15" style="width:50%;" data-aos="fade-down">
            <v-row class="mb-7 ml-1 mt-1">
                <span class="text-h4 text-capitalize brown--text">Existing Transactions</span>
            </v-row>
            <v-container>
                <div class="d-flex justify-content-center align-items-center amber lighten-2 rounded-circle pa-3" style="width:250px;height:250px">
                    <v-img src="../assets/apparel.jpg" class="rounded-circle" style="height:225px;width:225px"></v-img>
                </div>
            </v-container>
            <v-container>
                <v-row>
                    Change status to:
                </v-row>
                <v-row>
                    <v-select 
                        style="margin-left: 15px; margin-right: 15px;"
                        outlined
                        rounded
                        name="status"
                        placeholder="In Progress"
                        id="status"
                        v-model="transactionStatus"
                        :items=myStatuses>
                    </v-select>
                </v-row>
            </v-container>
            <CorporateTransactionCard></CorporateTransactionCard>
            <CorporateTransactionCard></CorporateTransactionCard>
            <CorporateTransactionCard></CorporateTransactionCard>
        </v-container>                    
    </div>
</template>
  
  <style src="../style/style.css">
</style>
  
  <script>
    import CorporateTransactionCard from '../components/CorporateTransactionCard.vue'
    // import axios from 'axios'
  
    export default {

      name: 'register',
      data(){
        return{
            fab: false,
            myStatuses: ['In Progress', 'Ready for Collection', 'Collected', 'Cancelled'],    

        }
      },
      components : {CorporateTransactionCard},

      methods:{
        
      },

      computed:{
        
      },
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
  