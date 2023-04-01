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
            <h1 class="text-h3 font-weight-medium grey--text text--darken-3 my-2">Name of Item</h1>
            <h1 class="text-subtitle-1 font-weight-light my-1">Post Creation Date</h1>
            <br>
            <!-- v tabs -->
            <div class="" style="height:30%">
            <v-tabs v-model="tab" grow class="rounded-lg">
                <v-tab class="amber lighten-2">Description</v-tab>
                <v-tab class="amber lighten-2">Location</v-tab>
                <v-tab class="amber lighten-2">Company Details</v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab" class="rounded-lg pa-5 amber lighten-5">
                <v-tab-item :value="0">
                    Description blablabla <br>
                    Description blablabla <br>
                    Description blablabla <br>
                </v-tab-item>
                <v-tab-item :value="1">
                    Location blablabla <br>
                    Location blablabla <br>
                    Location blablabla <br>
                </v-tab-item>
                <v-tab-item :value="2">
                    Company blablabla <br>
                    Company blablabla <br>
                    Company blablabla <br>
                </v-tab-item>
            </v-tabs-items>
            </div>
            <br>
            <!-- Claim -->
            <div class="white rounded-xl my-5">
                <v-row>
                <v-col cols="3">
                <h1 class="text-h6 grey--text text--darken-4 font-weight-light" data-aos="fade-down">
                    Claim Now!
                </h1>
                <h1 class="text-subtitle-2 red--text text--darken-4">
                    Only XX left in stock.
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
            </div>
        </v-col>
    </v-row>
    </div>
</div>
</template>
<script>
export default {
    name: 'IndividualListing',
    data(){
        return{
            tab: null,
        }
    },
}

</script>

<style scoped>
</style>
