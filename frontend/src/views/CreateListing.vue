<template>
    <div class="white pa-5 bground" style="height:50%">
        <v-container class="pb-15" style="width:50%;" data-aos="fade-down">
            <span class="text-h6 text-capitalize orange--text">Good!</span><br/>
            <v-row class="mb-7 ml-1 mt-1">
                <span class="text-h4 text-capitalize brown--text">Donate is good.</span>
            </v-row>
            
            <v-card>
                        <v-card-text>
                            <form>
                                <v-container>
                                    <v-text-field
                                    outlined
                                    rounded
                                    name="listingName"
                                    label="Name of Item"
                                    id="listingName"
                                    v-model="listingName"
                                    type="text"
                                    required>
                                    </v-text-field>
                                </v-container>

                                <v-container>
                                    <v-file-input
                                    outlined
                                    rounded
                                    name="itemImage"
                                    label="Image of Item"
                                    id="itemImage"
                                    v-model="itemImage"
                                    type="file"
                                    required>
                                    </v-file-input>
                                </v-container>

                                <v-container>
                                    <v-textarea
                                    outlined
                                    rounded
                                    name="itemDescription"
                                    label="Description of Item"
                                    id="itemDescription"
                                    height = "150"
                                    v-model="itemDescription"
                                    type="text"
                                    required>
                                    </v-textarea>
                                </v-container>

                                <v-container>
                                    <v-text-field
                                    outlined
                                    rounded
                                    name="collectionAddress"
                                    label="Collection Address"
                                    id="collectionAddress"
                                    v-model="collectionAddress"
                                    type="text"
                                    required>
                                    </v-text-field>
                                </v-container>

                                <v-container>
                                    <v-text-field
                                    outlined
                                    rounded
                                    name="collectionDetails"
                                    label="Collection Details"
                                    id="collectionDetails"
                                    v-model="collectionDetails"
                                    type="text"
                                    required>
                                    </v-text-field>
                                </v-container>

                                <v-container>
                                    <v-row>
                                        <v-text-field style="margin-left: 15px;"
                                        outlined
                                        rounded
                                        name="quantity"
                                        label="Quantity"
                                        id="quantity"
                                        v-model="quantity"
                                        type="number"
                                        required>
                                        </v-text-field>
                                        <v-select 
                                            style="margin-left: 15px; margin-right: 15px;"
                                            outlined
                                            rounded
                                            name="category"
                                            label="Category"
                                            id="category"
                                            v-model="itemCategory"
                                            :items=myCategories>
                                        </v-select>
                                    </v-row>
                                </v-container>

                                <v-container>
                                    <v-btn type="submit" block brown outlined :disabled="!formIsValid" :loading="loading">
                                        List Item
                                        <!-- button loader -->
                                        <template v-slot:loader>
                                            <span class="custom-loader">
                                            <v-icon light>mdi-cached</v-icon>
                                            </span>
                                        </template>
                                    </v-btn>
                                </v-container>
                            </form>
                        </v-card-text>
            </v-card>
        </v-container>                    
    </div>
</template>
  
  <style src="../style/style.css">
</style>
  
  <script>
    import db from '../firebase/index'
    // import router from '../router/index'
    import { doc, setDoc } from 'firebase/firestore'
    import { getAuth, createUserWithEmailAndPassword} from 'firebase/auth'
  
    export default {

      name: 'register',
      data(){
        return{
            myCategories: ['Food & Drinks', 'Apparel', 'Electronics', 'Furniture', 'Toys & Hobbies', 'Others'],
            listingName:'',
            itemDescription:'',
            collectionAddress:'',
            collectionDetails: '',
            quantity:'',
            itemCategory:'',
        }
      },
      computed:{
        
      },
      methods:{

        onRegister(){
            this.$store.commit('setLoading',true)

            const auth=getAuth()
            //Async Create User function
            createUserWithEmailAndPassword(auth, this.email, this.password)
            .then( user=>{
                console.log(user)
                const uid=user.user.uid
                console.log(uid)
                this.userid=user.user.uid
                const newUser={
                    userid: this.userid,
                    fullname:this.fullname,
                    email: this.email, 
                    username: this.username,
                    password:this.password,
                    listedPets:[],
                }
                //Async function to add this user into collection (inner async loop)
                const docRef=doc(db,"Users", uid)
                setDoc(docRef, newUser)
                .then(()=>{
                    this.$store.commit('setLoading',false)

                    console.log('Registration successful')
                    this.$router.push('/login')
                })

                // addDoc(collection(db, 'Users'), newUser)
                // .then( ()=>{
                //     alert('Registration successful!')
                //     this.$router.push('/login')
                // })
                .catch( (err)=>{
                    this.$store.commit('setLoading',false)

                    console.log(err)
                    this.errorstatus=true
                    return
                })
            })
            .catch( (err)=>{
                this.$store.commit('setLoading',false)
                this.errorstatus=true
                console.log(err)
                //set error to true, display error 
                // this.errorstatus=true
                // alert('Email already in use! Please retry!')
                return
            })
            // console.log('account created')
        }
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