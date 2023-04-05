<template>
    <div class="white pa-15">
        <v-container class="brown lighten-5 pa-10">
            <!-- top -->
            <v-row justify="center" class="text-center mb-10" data-aos="fade-down">
                <v-col cols="12">
                    <v-img :src="require('../assets/DogCat.png')" class="my-3" contain height="150"/>
                </v-col>
                <v-col cols="12">
                    <h1 class="text-h4 brown--text text-center">Report a Lost/Found Pet</h1>
                </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-form class="px-3 my-5" v-model="valid" ref="formInput" @submit.prevent="getGeoloc" data-aos="fade-down" >
                <v-row justify="center" class="my-5">
                <!-- Choose btwn lost and found -->
                <v-col cols="12"> 
                    <h1 class="text-h6 brown--text text-center font-weight-light ">I am reporting a...</h1>
                </v-col>
                <v-radio-group v-model="petStatus">
                <v-col cols="12" align="center">
                    
                        <v-btn rounded depressed large color="brown lighten-4 mx-4">
                            <v-radio label="Lost Pet" value="Lost Pet" required ></v-radio>
                        </v-btn> 
                        <v-btn rounded depressed large color="brown lighten-4 mx-4" >
                            <v-radio label="Found Pet" value="Found Pet" required ></v-radio>
                        </v-btn>
                 
                </v-col>
                </v-radio-group>
                </v-row>
                <v-row justify="center mb-3">
                <!-- Pet's Name -->
                    <v-col cols="12" md="6">
                        <v-text-field label="Pet's Name*" placeholder="Enter unknown if pet's name is not known"
                        :rules="inputRules" name:pname outlined v-model="petName">
                        </v-text-field>
                    </v-col>
                <!-- Last seen Location-->
                    <v-col cols="12" md="6">
    
                        <!-- placeholder="Enter the pet's last seen location..." -->
                        <!-- removed bc there's some weird overlap-->
                        <!-- <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }"> -->
                        <vuetify-google-autocomplete id="search" label="Pet's Last Seen Location" 
                            outlined
                            country="sg"
                            v-model="petLocation"
                            hint="Press the icon to retrieve current location."
                        >
                            <template v-slot:append>
                                <v-tooltip top>
                                    <template v-slot:activator="{ on }">
                                        <v-icon v-on="on" @click="getUserLoc">mdi-map-marker</v-icon>
                                    </template>
                                Retrieve current location
                                </v-tooltip>
                            </template>
                        </vuetify-google-autocomplete>
                    </v-col>
                <!-- Date -->
                <v-col cols="12" md="6">
                    <v-menu ref="menu" v-model="menu" :close-on-content-click="false" :return-value.sync="date"
                                transition="scale-transition" offset-y min-width="auto">
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field v-model="date" label="Pet's Last Seen Date*" outlined :rules="calRule"
                                    v-bind="attrs" v-on="on"></v-text-field>
                        </template>
                        <v-date-picker v-model="date" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="menu = false">
                            Cancel
                        </v-btn>
                        <v-btn text color="primary" @click="$refs.menu.save(date)">
                            OK
                        </v-btn>
                        </v-date-picker>
                        </v-menu>
                    </v-col>
                <!-- Pet type-->
                    <v-col cols="12" md="6">
                        <v-combobox v-model="petType" outlined :items="petTypes" :rules="typeRule" label="Pet's Type*" placeholder="Select the Pet's Type..." class="text-brown"></v-combobox>
                    </v-col>
                <!-- Breed -->
                    <v-col cols="12" md="6">
                        <v-combobox hide-no-data v-model="petBreed" outlined :items="filteredPetBreeds" label="Pet's Breed" placeholder="Select the Pet's Breed..." class="text-brown"></v-combobox>
                    </v-col>
                <!-- Colour -->
                <v-col cols="12" md="6">
                    <v-combobox v-model="petColor" outlined :items="petColours" :rules="colorRule" label="Pet's Color*" placeholder="Select the Pet's Colour(s)..." class="text-brown"></v-combobox>
                </v-col>
                <!-- Collar colour -->
                <v-col cols="12" md="6">
                    <v-combobox v-model="collarColor" outlined :items="collarColours" :rules="collarColorRule" label="Pet's Collar Color*" placeholder="Select the Pet's Collar Colour..." class="text-brown"></v-combobox>
                </v-col>
                <!-- Size -->
                <v-col cols="12" md="6">
                    <v-combobox v-model="petSize" outlined :items="petSizes" :rules="sizeRule" label="Pet's Size*" placeholder="Select the Pet's Size.." class="text-brown"></v-combobox>
                </v-col>
                <!-- Gender -->
                <v-col cols="12" md="6">
                    <v-combobox v-model="petGender" outlined :items="petGenders" :rules="genderRule" label="Pet's Gender*" placeholder="Select the Pet's Gender..." class="text-brown"></v-combobox>
                </v-col>
                <!-- Submit Photo -->
                <v-col cols="12" md="6">
                    <v-file-input outlined label="Pet's Image*" accept="image/*"
                     placeholder="Upload an Image of the Pet"
                     :model="imageText"
                     @change="filePicked()"
                prepend-icon="" append-icon="mdi-camera">
                <!-- <template v-slot:append>
                    <v-tooltip top>
                        <template v-slot:activator="{ on }">
                                <v-icon v-on="on">mdi-camera</v-icon>
                        </template>
                            Retrieve current location
                    </v-tooltip>
                </template> -->
            </v-file-input>
                    <!-- @change="checkFileType" -->
                </v-col>
                </v-row>
                <!-- Submit -->
                <v-row align="center" justify="center" class="mt-5">
                    <v-col cols="12" align="center">
                        <v-btn x-large depressed color="brown lighten-4" type="submit" :disabled="!formIsValid" :loading="loading">

                            Submit
                             <!-- button loader -->
                             <template v-slot:loader>
                                                <span class="custom-loader">
                                                <v-icon light>mdi-cached</v-icon>
                                                </span>
                                            </template>
                        </v-btn>
                    </v-col>
                </v-row>

          

                <v-row >
                    <v-col>
                    <v-alert v-if="success" type="success">
                    Pet listed successfully!
                    </v-alert>
                    <v-alert type="error" v-if="error">
                    Failed to list pet. Try again!
                    </v-alert>
                    </v-col>

                </v-row>
            </v-form>
        </v-container>
        <!-- scroll to top button -->
        <v-btn v-scroll="onScroll" v-show="fab" fab fixed bottom right color="brown lighten-4" @click="toTop">
        <v-icon>mdi-chevron-up</v-icon>
        </v-btn>
    </div>
    </template>
    
  <style src="../style/style.css">
</style>
    
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyCsbcA8EHPhaZbxQ_Gubm_ZhQyy-pcn6JM&libraries=places"></script>
    
    <script>
    import AOS from 'aos'
    // const { validationMixin, default: Vuelidate } = require('vuelidate')
    // const { required} = require('vuelidate/lib/validators')
    import db from '../firebase/index'
    import { collection, addDoc, doc, updateDoc } from 'firebase/firestore'
    import {uploadBytes, getDownloadURL, ref, getStorage} from 'firebase/storage'
    //collection ref
    
    // //import gmaps
    // import * as VueGoogleMaps from 'vue2-google-maps';
    
    
    export default {
    
    name:'reportpet',
    
    
    mounted() {
        AOS.init({
        duration: 1000,
        });
    },
    data(){
      return {
        valid: true,
        menu: '',
        radioGroup:"Lost Pet",
        date:"",
        userCoordinates:{
                        lat: 0,
                        lng: 0
                    },
        myGeocoder: null,
        fab: false,
        petTypes: ["Dog","Rabbit","Cat","Bird","Hamster","Terrapin","Guinea Pig","Other Pet Types"], 
        defaultBreed: {header: "Please select Pet Type first"},
        weirdTypes: {header: "No need to select breed for Other Pet Types"},
        petBreeds: ['Affenpinscher Dog', 'Afghan Hound Dog', 'Alaskan Malamute Dog', 'Australian Kelpie Dog', 
        'Australian Terrier Dog', 
        'Basenji Dog',
        'Basset Bretagne Dog',
                'Basset Hound Dog',
                'Beagle Dog',
                'Bearded Collie Dog',
                'Belgian Shepherd Dog',
                'Bernese Mountain Dog',
                'Bichon Frise Dog',
                'Bloodhound Dog',
                'Border Collie Dog',
                'Border Terrier Dog',
                'Borzoi Dog',
                'Boston Terrier Dog',
                'Bouvier Flandres Dog',
                'Boxer Dog',
                'Briard Dog',
                'British Bulldog',
                'Brittany Dog',
                'Chihuahua Dog',
                'Cocker Spaniel Dog',
                'Dalmatian Dog',
                'Doberman Dog',
                'French Bulldog',
                'German Shepherd Dog',
                'Golden Retriever Dog',
                'Great Dane Dog',
                'Greyhound Dog',
                'Labrador Dog',
                'Maltese Dog',
                'Pomeranian Dog',
                'Poodle Dog',
                'Pug Dog',
                'Shiba Inu Dog',
                'Shih Tzu Dog',
                'Siberian Husky Dog',
                'Welsh Corgi Dog',
                'Yorkshire Terrier Dog',
                'Abyssinian Cat', 
                'American Bobtail Cat', 
                'American Curl Cat',
                'Birman Cat',
                'Bombay Cat',
                'Burmese Cat',
                'Chartreux Cat',
                'Cornish Rex Cat', 
                'Devon Rex Cat',
                'Egyptian Mau Cat',
                'Exotic Shorthair Cat',
                'Havana Brown Cat',
                'Himalayan Cat',
                'Japanese Bobtail Cat',
                'LaPerm Cat',
                'Maine Coon Cat',
                'Manx Cat',
                'Munchkin Cat',
                'Norwegian Forest Cat','Ocicat Cat',
                'Oriental Shorthair Cat',
                'Persian Cat',
                'Pixiebob Cat',
                'Ragamuffin Cat',
                'Ragdoll Cat',
                'Russian Blue Cat',
                'Savannah Cat',
                'Scottish Fold Cat',
                'Selkirk Rex Cat',
                'Siamese Cat',
                'Siberian Cat',
                'Singapura Cat',
                'Somali Cat',
                'Tonkinese Cat',
                'Turkish Angora Cat',
                'Turkish Van Cat',
                'Holland Lop Rabbit',
                "Lionhead Rabbit",
                "Rex Rabbit",
                "Mini Lop Rabbit",
                "Dutch Rabbit",
                "Netherland Dwarf Rabbit",
                "Polish Rabbit",
                "Dwarf Hotot Rabbit",
                "Dove Bird",
                "Zebra Finch Bird",
                "Canary Bird",
                "Ring-Necked Parakeet Bird",
                "Cockatiel Bird",
                "Peach-Faced Lovebird Bird",
                "Budgerigar Bird",
                "Red Eared Sliders Terrapin",
                "Abyssinian Guinea Pig",
                "American Guinea Pig",
                "Baldwin Guinea Pig",
                "Coronet Guinea Pig",
                "Peruvian Guinea Pig",
                "Rex Guinea Pig",
                "Sheltie Guinea Pig",
                "Skinny Guinea Pig",
                "Teddy Guinea Pig",
                "Texel Guinea Pig",
                "White-crested Guinea Pig",
                "Syrian Hamster", "Winter White Hamster", "Hybrid Dwarf Hamster", 
                "Campbell Hamster", "Roborovski Hamster" 
            
            ],
    
        petColours: ["Beige", "Black", "Brown", "Orange", "Grey", "White", "Others"],
        collarColours: ["No Collar", "Beige", "Black","Brown", "Grey", "White", "Pink", "Blue", "Yellow", "Red", "Others"],
        petGenders: ['Male','Female',"Unknown"],
        petSizes: ['Small', 'Medium', 'Large'],
        colour: [1,4],
        petStatus:'',
        petLocation:'',
        petGeoLoc: '',
        petName:'',
        petType:'',
        petColor:'',
        petGender:'',
        collarColor:'',
        petBreed:'',
        petSize:'',
        date:null,
        imageText:'',
        imageURL:"",
        image:null,
        fromDateMenu: false,
        fromDateVal: null,
        success:false,
        fail:false,
        minDate: "2019-07-04",
        colorRule: [
            v => v.length >= 1 || "Pet's colour cannot be empty"
        ],
        collarColorRule: [
            v => !!v || "Pet's collar colour cannot be empty"
        ],
        genderRule: [
            v => !!v || "Pet's gender cannot be empty"
        ],
        sizeRule:[
            v => !!v || "Pet's size cannot be empty"
        ],
        fileRule: [
            v => this.checkFileType(v) == true || 'Image must be .jpeg or .png'
        ],
        calRule: [
            v => v.length == 10 || 'Date cannot be empty'
        ],
        typeRule: [
            v => !!v || "Pet's type cannot be empty"
        ],
        mapRule: [
            v => v.length >= 1 || "Last seen location cannot be empty"
        ]
    
      }
    },
    // validations (){
        // return {
        //     pname: {required},
        //     loc: {required},
        //     missingSince: {required},
        //     zip: {required},
        //     petType: {required},
        //     petCol: {required},
        //     petColCol: {required},
        //     breed: {required},
        //     gen: {required},
        //     petSize: {required}
        // }
    // },
    methods: {
        validate () {
            this.$refs.form.validate()
          },
        checkFileType(e){
            console.log(e)
            if(e['type']==='image/jpeg' || e['type']==='image/png'){
                return true
            }
            else {
                return false
            }
        },
        submitForm() {
            // this.getGeoloc()
            this.$store.commit('setLoading',true)
            console.log(this.petGeoLoc)
            const user_obj=this.$store.getters.getuser
            console.log(user_obj)
            const form_doc={
                petStatus: this.petStatus,
                petName:this.petName,
                petLocation: this.petLocation,
                petDate: this.date,
                petType: this.petType,
                petBreed: this.petBreed,
                petColor:this.petColor,
                collarColor:this.collarColor,
                petSize:this.petSize,
                petGender:this.petGender,
                image:'',
                petGeoLoc: this.petGeoLoc,
                petid:'',
                userid:user_obj.userid,
                useremail:user_obj.email, 
                username:user_obj.username,
            }
            console.log(form_doc)
            let key

            const docRef= addDoc(collection(db, 'Pets'), form_doc)
            .then( (data)=>{
                key=data.id
                form_doc.petid=key
                const documentRef=doc(db, "Pets", key)
                //updating petid into database
                updateDoc(documentRef, {petid:key}, {merge:true})
                .then((snapshot)=>{
                    console.log('PetID updated')
                    // alert('Pet listed!')
                    console.log(this.image)
                    const filename=this.image.name
                    const extension=filename.slice(filename.lastIndexOf('.'))

                    const imageRef=ref( getStorage(), `Pets/${key}${extension}`)
                    uploadBytes(imageRef, this.image)
                    .then( (snapshot)=>{
                        console.log("Uploaded to storage")
                        console.log("snapshot:"+ snapshot)
                        getDownloadURL(snapshot.ref)
                        .then( (url)=>{
                            console.log("Got Download URL")
                            updateDoc(documentRef, {image:url}, {merge:true})
                            .then( ()=>{
                                form_doc.image=url
                                this.$store.commit('setLoading',false)
                                console.log("pic added to database")

                                //gotta assign the listed petID to user database
                                // const payload={
                                //     userid:user_obj.userid,
                                //     petid:key
                                // }
                                this.$store.dispatch('updatePetArray', form_doc)
                                this.$refs.formInput.reset()
                                this.success=true
                            })
                            .catch( ()=>{
                                this.$store.commit('setLoading',false)
                                this.success=false
                                this.fail=true

                                console.log("Pic not added to database")
                            })

                        })
                        .catch( (err)=>{
                            this.$store.commit('setLoading',false)
                            this.success=false
                                this.fail=true
                            console.log(err)
                            console.log("Error getting download URL")
                        })

                    })
                    .catch( (err)=>{
                        this.$store.commit('setLoading',false)
                        this.success=false
                                this.fail=true
                        console.log(err)
                        console.log("Error uploading to storage")
                    })
                })
                        
                    })
                .catch((err)=>{
                    console.log('failed to add petid')
                    console.log(err)
                    this.success=false
                    this.fail=true
                    return
                })
            //     alert('Pet listed!')
            //     console.log(this.image)
            //     const filename=this.image.name
            //     const extension=filename.slice(filename.lastIndexOf('.'))

            //     const imageRef=ref( getStorage(), `Pets/${key}${extension}`)
            //     uploadBytes(imageRef, this.image)
            //     .then( (snapshot)=>{
            //         console.log("Uploaded to storage")
            //         console.log("snapshot:"+ snapshot)
            //         getDownloadURL(snapshot.ref)
            //         .then( (url)=>{
            //             console.log("Got Download URL")
            //             updateDoc(documentRef, {image:url}, {merge:true})
            //             .then( ()=>{
            //                 this.$store.commit('setLoading',false)
            //                 console.log("pic added to database")
            //             })
            //             .catch( ()=>{
            //                 this.$store.commit('setLoading',false)

            //                 console.log("Pic not added to database")
            //             })

            //         })
            //         .catch( (err)=>{
            //             this.$store.commit('setLoading',false)

            //             console.log(err)
            //             console.log("Error getting download URL")
            //         })

            //     })
            //     .catch( (err)=>{
            //         this.$store.commit('setLoading',false)

            //         console.log(err)
            //         console.log("Error uploading to storage")
            //     })
            // })
            .catch( (err)=>{
                this.$store.commit('setLoading',false)

                console.log(err)
                console.log("error adding pet into database")
            })

           
    
        },
        // get user current location
        getUserLoc(){
            // if(localStorage.center){
            //         this.myCoordinates = JSON.parse(localStorage.center);
            // }else{
                    // this.$getLocation({})
                    // .then(coordinates => {
                    //     this.petLocation = "Retrieving your current location...";
                    //     this.userCoordinates = coordinates;
                    //     this.geocodeLatLng();
                    // })
                    // .catch(this.petLocation = "There was an error. Please key in your address manually instead!");
            // }
            this.petLocation = "Retrieving your current location...";
            if(navigator.geolocation){
    
                    navigator.geolocation.getCurrentPosition(position=>{
                    this.userCoordinates.lat = position.coords.latitude
                    this.userCoordinates.lng = position.coords.longitude
                    this.geocodeLatLng();
                },
                error=>{
                    this.petLocation = "There was an error. Please key in your address manually instead!"
                })
                
            }else{
                this.petLocation = "Your browser does not support geolocation API. Please key in your address manually instead!";
            }
        },
        //lat lng to address
        geocodeLatLng(){
            this.myGeocoder = new google.maps.Geocoder();
            const latlng = {
            lat: this.userCoordinates.lat,
            lng: this.userCoordinates.lng
            };
            this.myGeocoder
            .geocode({ location: latlng })
            .then((response) => {
            if (response.results[0]) {
                this.petLocation = response.results[0].formatted_address;
            } else {
                this.petLocation = "No results found.";
            }
            })
            .catch((e) => this.petLocation = "There was an error. Please key in your address manually instead!");
        },
    
        // get user current location
        // getUserLoc(){
        //     if(navigator.geolocation){
        //         navigator.geolocation.getCurrentPosition(position=>{
        //             console.log(position.coords.latitude);
        //             console.log(position.coords.longitude);
        //         },
        //         error=>{
        //             console.log(error.message);
        //         })
        //     }else{
        //         console.log("Your browser does not support geolocation API ");
        //     }
        // },
        // // functions for scrolling to top
        // onScroll (e) {
        //   if (typeof window === 'undefined') return
        //   const top = window.pageYOffset ||   e.target.scrollTop || 0
        //   this.fab = top > 20
        // },
        // toTop () {
        //   this.$vuetify.goTo(0)
        // }
        //address to geoloc
        getGeoloc(){
            this.myGeocoder = new google.maps.Geocoder();
            this.myGeocoder
            .geocode({ address: this.petLocation })
            .then((response) => {
            if (response.results[0]) {
                this.petGeoLoc = {
                    lat: response.results[0].geometry.location.lat(),
                    lng: response.results[0].geometry.location.lng()
                };
                console.log(this.petGeoLoc)
            } else {
                this.petGeoLoc = {};
            }
            this.submitForm()
            })
            .catch((e) => {this.petGeoLoc = {}
            this.submitForm()});
        },
        filePicked(){
            const files=event.target.files[0]
            this.filename=files.name
            this.image=files
        }

    },
    computed: {
        //   fromDateDisp() {
        //     return this.fromDateVal ? this.formatDate(this.fromDateVal) : "";
        //     // format date, apply validations, etc. Example below.
        //     // return this.fromDateVal ? this.formatDate(this.fromDateVal) : "";
        //   },
        loading(){
            return this.$store.getters.loading
        },
        filteredPetBreeds () {
            if(this.petType==""){
                return this.defaultBreed;
            }
            if(this.petType=="Other Pet Types"){
                return this.weirdTypes
            }
            // if (!this.petType.includes("Dog") || !this.petType.includes("Cat") ) {
            //     return this.weirdTypes;
            // }
            if(this.petType){
                return this.petBreeds.filter(e => e.includes(this.petType))
            }
                return this.petBreeds
        },
        formIsValid() {
            return this.petStatus!='' && 
            this.petName!='' && 
            this.petType!='' && 
            this.petColor!='' && 
            this.petGender!=''&& 
            this.collarColor!=''&& 
            // this.petBreed!=''&& 
            this.petSize!=''&&
            this.petLocation!=''&&
            this.date!=null
            //left with validation for image and date
        },
    },
    }
    </script>
    
    <!-- <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyCsbcA8EHPhaZbxQ_Gubm_ZhQyy-pcn6JM&libraries=places"></script> -->
    
    <!-- <script>
        
        google.maps.event.addDomListener(window,'load',initialize)
        function initialize(){
            var autocomplete = new google.maps.places.Autocomplete(document.getElementById('search'));
                google.maps.event.addListener(autocomplete, 'place_changed', function(){
                    var place = autocomplete.getPlace();
                    var location = place.formatted_address;
                    var lat = place.geometry.location.lat();
                    var long = place.geometry.location.lng();
                    console.log(lat,long)
                })
        }
    </script> -->
