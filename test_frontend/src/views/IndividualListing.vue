<template>
<div fluid class="white pa-12" align="center">
    <div class="pa-5 rounded-xl" style="height:50%;">
    <v-row>
        <v-col cols="5">
            <div class="amber lighten-2 rounded-circle justify-center pa-3" style="width:450px;height:450px">
                <v-img src="../assets/apparel.jpg" class="rounded-circle" style="height:425px;width:425px"></v-img>
            </div>
        </v-col>
        <v-col cols="6" align="left">
            <h1 class="text-h3 font-weight-medium grey--text text--darken-3 my-2" data-aos="fade-right">{{listing.name}}</h1>
            <h1 class="text-subtitle-1 font-weight-light my-1">Posted on: {{listing.created.split('T')[0]}}</h1>
            <br>
            <!-- v tabs -->
            <div class="">
            <v-tabs v-model="tab" grow class="rounded-lg">
                <v-tab class="amber lighten-2">About this Post</v-tab>
                <v-tab class="amber lighten-2">Collection Location</v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab" class="rounded-lg pa-5 amber lighten-5">
                <v-tab-item :value="0">
                    <span class="text-h6 font-weight-medium grey--text text--darken-3">
                        Corporate Name: 
                    </span>
                    <span class="text-h6 font-weight-light grey--text text--darken-3">
                        {{ listing.corporate_name }}
                    </span>
                    <h1 class="text-h6 font-weight-medium grey--text text--darken-3 mt-3 mb-1">
                        Description:
                    </h1>
                    <h1 class="text-body-1 font-weight-light grey--text text--darken-3">
                        {{listing.description}}
                    </h1>
                </v-tab-item>
                <v-tab-item :value="1">
                    <span class="text-h6 font-weight-medium grey--text text--darken-3">
                        Address:
                    </span>
                    <span class="text-h6 font-weight-light">
                        {{listing.address}}
                    </span>
                    <br>
                    <span class="text-h6 font-weight-medium grey--text text--darken-3">
                        Postal Code: 
                    </span>
                    <span class="text-h6 font-weight-light">
                        {{listing.postal}}
                    </span>
                </v-tab-item>
            </v-tabs-items>
            </div>
            <br>
            <!-- Claim -->
            <div class="white rounded-xl my-5">
                <form @submit.prevent="onClaim()">
                <v-row>
                <v-col cols="5">
                <h1 class="text-h6 grey--text text--darken-4 font-weight-light">
                    Claim Now!
                </h1>
                <h1 class="text-subtitle-2 red--text text--darken-4">
                    We have {{ listing.quantity }} left in stock.
                </h1>
                </v-col>
                <v-col cols="2">
                    <span data-aos="fade-left" class="ml-15">
                    <video-background
                        :src="require(`@/assets/bee.mp4`)"
                        style="height:50px; width:36px"
                    ></video-background>
                    </span>
                </v-col>
                </v-row>
                <v-row>
                <div style="width:30%; height:40px" class="ml-3">
                <v-text-field outlined class="" type="number" required 
                    name="quantity" label="Quantity" id="quantity"
                    v-model="quantity">
                </v-text-field>
                </div>
                    <v-btn rounded-xl x-large type="submit" class="amber lighten-3 ml-2 my-1" depressed outlined>
                        Claim
                    </v-btn>
                </v-row>
                </form>
            </div>
        </v-col>
    </v-row>
    </div>
</div>
</template>
<script>
import axios from 'axios';

export default {
    name: 'IndividualListing',
    data(){
        return{
            tab: null,
            listing: null,
            quantity: 0,
        }
    },
    methods: {
        async fetchListing(){
            const listing_URL = 'http://0.0.0.0:8000/listing/' + this.$route.params.listingid
            axios.get(listing_URL).then((response) => {
                this.listing = response.data
            }).catch((exception) => {
                console.log(exception);
            });
        },
        onClaim(){
            const listingManagement_URL = 'blabla'
            axios.post(listingManagement_URL, {
                listing: this.listing,
                beneficiary_id: this.$store.state.uid,
                quantity: this.quantity,
            })
        },
    },
    created(){
        this.fetchListing()
    }
}

</script>

<style scoped>
</style>
