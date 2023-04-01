<template>
    <div class="white pa-5 bground" style="height:50%">
        <v-container class="pb-15" style="width:50%;" data-aos="fade-down">
            <v-row class="mb-7 ml-1 mt-1">
                <span class="text-h4 text-capitalize brown--text">These freebies are waiting for you!</span>
            </v-row>
            
            <v-tabs v-model="tab" fixed-tabs color="orange" bg-color="white">
                <v-tab>In Progress</v-tab>
                <v-tab>Ready for Collection</v-tab>
                <v-tab>Completed</v-tab>
                <v-tab>Cancelled</v-tab>
            </v-tabs>
            <v-tabs-items v-model="tab">
                <v-tab-item :value="0">
                    <v-card-text>
                        <Transaction></Transaction>
                    </v-card-text>
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
            const transaction_URL = 'http://localhost:9000/transactions'
            axios.get(transaction_URL).then((response) => {
                response.data.forEach((transaction) => {
                    if (transaction.status == 'inProgress') {
                        this.inProgressArray.push(transaction)
                    }
                    else if (transaction.status == 'ready') {
                        this.readyArray.push(transaction)
                    }
                    else if (transaction.status == 'completed') {
                        this.completedArray.push(transaction)
                    }
                    else if (transaction.status == 'cancelled') {
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
        comparePasswords(){
            return this.password!=this.confirmpassword ? 'Passwords do not match!': ''
        },
        passwordLength(){
            if (this.password.length < 6){
                return 'Minimum length is 6 characters'
            }
            else if(!this.password.match(/[a-z]/)){
                return 'Must contain at least 1 lowercase letter'
            }
            else if(!this.password.match(/[A-Z]/)){
                return 'Must contain at least 1 uppercase letter'
            }
            else if(!this.password.match(/[`!@#$%^&*()_+\-=[\]{};':"\\|,.<>?~]/)){
                return 'Must contain at least 1 symbol'
            }
            else {
                return true
            }
        },
        formIsValid(){
            return this.fullname!='' && 
            this.email!='' &&
            this.username!=''&&
            this.password!='' &&
            this.confirmpassword!=''&&
            this.password==this.confirmpassword
        }
    
      
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
  