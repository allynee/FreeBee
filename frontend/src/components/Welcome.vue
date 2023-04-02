<!-- Welcome page -->

<template>
<!-- loading bee -->
  <div v-if="loaded">
    <v-row justify="center" class="my-15">
      <v-col cols="12" align="center" data-aos="fade-left">
        <video-background :src="require(`@/assets/bee.mp4`)" style="height: 250px; width: 180px">
        </video-background>
      </v-col>
    </v-row>
  </div>
  <!-- First Segment -->
<div v-else>
  <div class="white darken-3">
    <div class="py-5">
      <v-row class="my-15 justify-center">
        <span data-aos="fade-right" class="mr-15">
          <video-background
            :src="require(`@/assets/flipbee.mp4`)"
            style="height: 85px; width: 60px"
          >
          </video-background>
        </span>


        <h1
          class="text-md-h3 text-sm-h2 grey--text text--darken-4 font-weight-light justify-center"
          data-aos="fade-down"
        >
          What FreeBee are you looking for?
        </h1>
        <span data-aos="fade-left" class="ml-15">
          <video-background
            :src="require(`@/assets/bee.mp4`)"
            style="height: 85px; width: 60px"
          >
          </video-background>
        </span>
      </v-row>
      <v-row class="my-15">
        <SearchBar></SearchBar>
      </v-row>
      
    </div>

    <div class="mx-15 px-15">

     <!-- Categories -->
      <v-row class="">
        <span class="text-h4 grey--text text--darken-3">Categories</span>
        <!-- <span style="width:80%" class="justify-right">
          <v-btn plain depressed class="grey--text text--darken-4">
          <v-icon small left>mdi-view-grid</v-icon>See all categories</v-btn>
        </span> -->
    </v-row>

      <v-row class ="my-10 justify-center">
        <v-col cols='2' v-for="category in myCategories" :key="category.title">
          <Category :title="category.title" :image="category.image"> </Category>
        </v-col>
      </v-row>

      <v-row class="">
        <h1 class="text-h4 grey--text text--darken-3">Recommended for you</h1>
      </v-row>
      <v-row class="my-15">
        <v-col cols="12" md="4" lg="3" v-for="aListing in recListingsArray.slice(0,4)" :key="aListing.listing_id">
          <Listing :aListing="aListing" @gotoListing="gotoListing(aListing.listing_id)"></Listing>
        </v-col>
      </v-row>
<!-- 
      <v-row justify="center" class="my-15">
        <v-col cols="12" align="center" data-aos="fade-left">
          <video-background :src="require(`@/assets/bee.mp4`)" style="height: 250px; width: 180px">
          </video-background>
        </v-col>
      </v-row> -->

      <v-row class="">
        <h1 class="text-h4 grey--text text--darken-3">All FreeBees</h1>
      </v-row>

      <v-row class="my-15">
        <v-col cols="12" md="4" lg="3" v-for="aListing in allListingsArray" :key="aListing.listing.listing_id">
          <Listing :aListing="aListing" @gotoListing="gotoListing(aListing.listing.listing_id)"></Listing>
        </v-col>
      </v-row>
  </div>

    <!-- scroll to top button -->
    <v-btn v-scroll="onScroll" v-show="fab" fab fixed bottom right color="amber lighten-3" @click="toTop">
      <v-icon>mdi-chevron-up</v-icon>
    </v-btn>

  </div>
</div>
</template>

<script>
import AOS from 'aos'
import Category from './Category.vue';
import SearchBar from './SearchBar.vue';
import Listing from './Listing.vue';
import axios from 'axios';
export default {
  name: "HelloWorld",
  mounted() {
        AOS.init({
            duration: 1600,
        });
        console.log(this.$store.getters.getAccessToken)
        console.log(this.$store.state)
  },  
  data(){
    return{
    fab: false,
    myCategories: [
                { title: 'Food & Drinks', image: 'Honey.png' },
                { title: 'Apparel', image: 'yellowshirt.jpg' },
                { title: 'Electronics', image: 'beeelectronic.jpg' },
                { title: 'Furniture', image: 'beefurniture.jpg' },
                { title: 'Toys & Hobbies', image: 'pigbee.jpg' },
                { title: 'Everything Else', image: 'manybees.jpg' },
            ],
      //listings array retrieved from MS:
      categories: ["Food and Beverage",""],
      allListingsArray:[],
      recListingsArray:[],
      loaded: true,
  };
  },

  components: { SearchBar, Category, Listing},

  methods:{
    async fetchListings() {
        const listing_URL = 'http://localhost:5000/listing_management'
        axios.get(listing_URL).then((response) => {
          // console.log(response.data)
          response.data.forEach(element => {
            // console.log(element)
            if (element.listing.status == "Available"){ //
              this.allListingsArray.push(element)
            }
            // console.log(this.$store.state.area)
            let rec_area = "string" //suppose to be this.$store.state.area
            if (element.area == rec_area || rec_area == null){
              this.recListingsArray.push(element)
            }

          });
        console.log(this.allListingsArray)
        })
        // console.log(this.allListingsArray)

    },
    gotoListing(listing_id){
      // console.log("clicked")
      this.$router.push({ name: 'IndividualListing', params: {listingid: listing_id}})
    },
    onScroll (e) {
      if (typeof window === 'undefined') return
      const top = window.pageYOffset ||   e.target.scrollTop || 0
      this.fab = top > 20
    },
    toTop () {
      this.$vuetify.goTo(0)
    },
  },
  created(){
    this.fetchListings()
    setTimeout(() => {
      this.loaded = false
      console.log(this.loaded)
    }, 2000)
  }
} 
</script>
