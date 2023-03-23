<template>
    <div class="white bground" >
        <v-container class="mx-auto" style="width:45%;height:45%" data-aos="fade-down">
            <v-row class="mt-16">
                <span class="mt-16"> </span>
            </v-row>
            <v-row class="mt-16">
                <span> </span>
            </v-row>
            <v-row class="mb-7 mt-16 pt-0 d-flex align-center">
            <span class="text-h4 mt-16 text-capitalize brown--text mx-auto">Login</span>
            </v-row>
            <!-- <v-row> -->
                <!-- <v-card style="width:45%;height:75%;" elevation="2" class="mx-auto brown pt-9 pb-10 lighten-4">
                    <v-card-text>  -->
                        <v-container>
                            <form @submit.prevent="sampleLogin">
                                <!-- <v-row >
                                    <v-col>
                                    <v-alert v-if="this.loggedout" type="info">
                                    You have logged out successfully
                                    </v-alert>
                                   
                                    </v-col>

                                </v-row> -->


                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                        name="email"
                                        label="Email"
                                        id="email"
                                        v-model="email"
                                        type="email"
                                        outlined
                                        required>
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                            

                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                        name="password"
                                        label="Password"
                                        id="password"
                                        v-model="password"
                                        type="password"
                                        outlined
                                        required
                                        >
                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                

                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn block outlined brown type="submit" :disabled="!formIsValid" :loading="loading">
                                            Login
                                            <!-- button loader -->
                                            <template v-slot:loader>
                                                <span class="custom-loader">
                                                <v-icon light>mdi-cached</v-icon>
                                                </span>
                                            </template>
                                            </v-btn>

                                            <v-row >
                                                <v-col class="my-3">
                                            
                                                <v-alert type="error" v-if="error">
                                                Login failed. Please enter again!
                                                </v-alert>
                                                </v-col>

                                            </v-row>
                                        
                                    </v-flex>
                                </v-layout>
                            </form>
                        </v-container>
                    <!-- </v-card-text>
                </v-card>  -->
            <!-- </v-row> -->
        </v-container>
    </div>


   


  </template>
  

  <style src="../style/style.css">
</style>

  <script>
    import db from '../firebase/index'
    // import router from '../router/index'
    import {  doc, getDoc } from 'firebase/firestore'
    import { getAuth, signInWithEmailAndPassword} from 'firebase/auth'
  
    export default {

      name: 'login',
      data(){
        return{
            email:'',
            password:'',
            userid:'',
            error:false,
        }
      },
      computed:{
        loading(){
            return this.$store.getters.loading
        },
        formIsValid(){
            return this.email!='' && 
            this.password!='' 
        },

        user(){
            return this.$store.getters.getuser
        }
    
      
      },
      watch:{
        user (value){
            if (value!=null &&  value!=undefined){
                this.$router.push('/')
            }
        }
      },
      methods:{

        sampleLogin(){
            this.$store.commit('setLoading',true)
            const auth=getAuth()
            signInWithEmailAndPassword(auth, this.email, this.password)
            .then( (credentials)=>{
                console.log(credentials.user.uid)
                const uid=credentials.user.uid
                const docRef=doc(db, 'Users',uid)
                getDoc(docRef)
                .then( (snapshot)=>{
                    const user_obj= snapshot.data()
                    this.$store.dispatch('signUserIn',user_obj)

                    console.log(user_obj)

                })
                .catch( (err)=>{
                    this.$store.commit('setLoading', false)
                    this.error=true
                    console.log(err)
                    console.log(2)
                })
       
                
                // const q= query(collection(db, 'Users'), where('userID', '==', uid))
                // getDocs(q)
                // .then( (documents)=>{
                //     documents.docs.forEach((oneDoc)=>{
                //         var user_obj=oneDoc.data()
                //         console.log(user_obj)
                //     })
                //     // console.log(user_obj)
                // })
                // // console.log(data)
            })
            .catch((err)=>{
                this.$store.commit('setLoading',false)
                console.log(1)
                this.error=true
                console.log(err)
            })
        },

        
      }
    }
  </script>
  <style scoped>
  .bground {
    background: url('../assets/dogss.png');
    background-size: cover;
    height: 120vh;
    background-position: 20px;
    width: 100%
  }
  </style>