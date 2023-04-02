<template>
    <div class="white pa-15">
        <v-container class="brown lighten-5 pa-0">
            <!-- Pet Status -->
            <div :class="bgColor()">{{loadedPet.petStatus}}</div>
            
            <v-row class="px-10 py-10">
                <v-col cols="12" class="brown lighten-5 px-12" align="center">
                    <!-- Name and Picture -->
                    <h1 class="text-h4 primary--text mb-10">Pet Name: {{loadedPet.petName}}</h1>
                    <v-img :src="loadedPet.image" max-height="500" max-width="500" class="my-10"></v-img>
                </v-col>
            </v-row>

            <v-row class="px-10">
                <v-col cols="12" md="6" class="brown lighten-5 px-12" >
                    <!-- Pet Info -->
                    <h1 class="text-h5 primary--text mb-10">Pet Information</h1>
                    <v-card outlined>
                        <v-list dense>
                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Type</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item>{{loadedPet.petType}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>

                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Breed</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.petBreed}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>

                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Colour</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.petColor}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>

                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Collar Colour</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.collarColor}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>

                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Size</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.petSize}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>

                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Gender</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.petGender}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider v-show="i!=items.length-1"></v-divider>
                            <v-list-item class="ma-0">
                                <v-list-item-content>
                                    <v-list-item-title>Last Seen Date</v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-content>
                                    <v-list-item >{{loadedPet.petDate}}</v-list-item>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-card>
                </v-col>
                <span>
                    <v-divider vertical></v-divider>
                </span>
                <v-col cols="12" md="6" class="brown lighten-5 px-12">
                    <!-- Map -->
                    <h1 class="text-h6 primary--text mb-8">Last Seen Location: {{loadedPet.petLocation}}</h1>
                    <!-- <v-row class="px-3 my-5">
                        <span>{{loadedPet.petLocation}}</span>
                    </v-row> -->
                    <MyMap style="width:100%;height:400px;" :petGeoLoc="loadedPet.petGeoLoc" :petLoc="loadedPet.petLocation"></MyMap>
                    <a :href="gmapsLink" style="text-decoration: none;">
                        <v-btn small outlined class="my-2 py-2" style="width:100%">
                            <v-icon left>mdi-map-outline</v-icon>
                            <span>Open in GMaps</span>
                    </v-btn></a>
                </v-col>
            </v-row>
            
            <!-- Owner Information -->
            <v-row class="my-10 px-10">
                <v-col cols="12" class="brown lighten-5 px-12">
                    <h1 class="text-h6 primary--text mb-5 d-inline">Poster</h1>
                    <div>
                    <v-btn small outlined class="my-5 d-inline " @click="contactOthers(loadedPet)">
                        <v-icon left>mdi-inbox-outline</v-icon>
                        <span>Contact poster</span>
                    </v-btn>
                </div>
                    <v-card outlined class="px-5">
                        <h1 class="text-body-1 primary--text my-5">Owner Username: <strong>{{loadedPet.username}}</strong></h1>
                        <v-divider></v-divider>
                        <h1 class="text-body-1 primary--text my-5">Owner Email: <strong>{{loadedPet.useremail}}</strong></h1>
                    </v-card>
                </v-col>
            </v-row> 
            <v-row class="my-15">
            </v-row>
        </v-container>
    </div>
    </template>
    
    <script>
    import MyMap from "../components/GMap.vue";
        export default{
            components: {MyMap},
            props: {
                aPet: Object,
                
            }, 
            data(){
                return{
                    petStatus: 'Found',
                    items: [
                        { text: 'aPet.petBreed', cont: 'Type'},
                        { text: 'aPet.petBreed', cont: 'Breed'},
                        { text: 'aPet.petColour', cont: 'Colour'},
                        { text: 'aPet.collarColour', cont: 'Collar Colour'},

                        { text: 'aPet.petSize', cont: 'Size' },
                        { text: 'aPet.petGender', cont: 'Gender'},
                    ],
                    details: [
                        {text: 'aPet.lastSeenLocation',cont:'Last Seen Location'},
                        {text: 'aPet.missingSince',cont:'Last Seen Date'}
                    ],
                    ownerDetails: [
                        {text: 'aPet.lastSeenLocation',cont:'Username'},
                        {text: 'aPet.missingSince',cont:'Email'},
                        {text: 'aPet.missingSince',cont:'Phone Number'},
                    ]
                }
            },
            methods: {
                // getImgUrl(pic){
                // return require('../assets/' + pic)
                // },
                bgColor(){
                    if (this.loadedPet.petStatus == 'Found Pet'){
                        return "text-h5 green lighten-3 font-weight-medium text-center mb-4 py-3"
                    }
                    else {
                        console.log(this.loadedPet.petStatus)
                        return "text-h5 red lighten-3 font-weight-medium text-center mb-4 py-3"
                    }
                    
                },
                contactOthers(others_obj){
                    this.$store.dispatch('setOthers',others_obj)
                    this.$router.push('/inbox')

                }
            },
            computed: {
                loadedPet(){
                    // console.log('here' + this.$store.getters.loadedpet)
                    return this.$store.getters.loadedpet
                    
                },
                gmapsLink(){
                    let str = "https://www.google.com/maps/place/"
                    str += this.loadedPet.petLocation;
                    return str
                }
            }
        }
    </script>