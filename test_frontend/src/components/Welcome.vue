<!-- Welcome page -->

<template>
  <div class="white darken-3">
    <v-container class="py-10">
      <v-row class="my-5 justify-center">
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

      <v-row>
        <v-col cols="10">
          <h1 class="text-h4 grey--text text--darken-3">Categories</h1>
        </v-col>
        <v-col cols="2" class="justify-right">
          <v-btn plain depressed class="grey--text text--darken-4">
            <v-icon small left>mdi-view-grid</v-icon>See all categories</v-btn
          >
        </v-col>
      </v-row>

      <v-row class ="my-15">
        <v-col cols='3' v-for="category in myCategories" :key="category.title">
          <Category :title="category.title" :image="category.image"> </Category>
        </v-col>
      </v-row>

      <!-- <v-row class="my-15">
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
        <v-col cols="3">
          <Category></Category>
        </v-col>
      </v-row> -->
      <v-row>
        <h1 class="text-h4 grey--text text--darken-3">Recommended for you</h1>
      </v-row>

      <v-row justify="center" class="my-5">
        <v-col cols="12" align="center" data-aos="fade-left">
          <!-- <div data-aos="fade-left"> -->
          <video-background
            :src="require(`@/assets/bee.mp4`)"
            style="height: 250px; width: 180px"
          >
          </video-background>
          <!-- </div> -->
        </v-col>
      </v-row>
      <v-row>
        <h1 class="text-h4 grey--text text--darken-3">All FreeBees</h1>
      </v-row>
      
      <!-- <v-row class ="my-15">
        <v-col cols='3' v-for="listing in allListingsArray" :key="listing.title">
          <Listing :title="listing.title" :image="listing.image" :desc="listing.desc"> </Listing>
        </v-col>
      </v-row> -->

      <v-row class="my-15">
        <v-col cols="12" md="6" lg="4" v-for="aListing in allListingsArray" :key="aListing.listingID">
          <Listing :aListing="aListing"></Listing>
        </v-col>
        <!-- <v-col cols="4">
          <Listing></Listing>
        </v-col>
        <v-col cols="4">
          <Listing></Listing>
        </v-col> -->
      </v-row>

      <!-- <v-col cols="12" md="6" lg="4" v-for="aPet in myPets" :key="aPet.petid" align="center">
      <PetCard :aPet="aPet"></PetCard>
    </v-col> -->

    </v-container>

    <!-- scroll to top button -->
    <v-btn
      v-scroll="onScroll"
      v-show="fab"
      fab
      fixed
      bottom
      right
      color="amber"
      @click="toTop"
    >
      <v-icon>mdi-chevron-up</v-icon>
    </v-btn>
  </div>
</template>

<script>
import AOS from 'aos'
import Category from './Category.vue';
import SearchBar from './SearchBar.vue';
import Listing from './Listing.vue';
export default {
  name: "HelloWorld",
  mounted() {
        AOS.init({
            duration: 1600,
        });
  },
  data(){
    return{
    fab: false,
    myCategories: [
                { title: 'Food and Beverage', image: 'Honey.png' },
                { title: 'Apparel', image: 'yellowshirt.jpg' },
                { title: 'Electronics', image: 'beeelectronic.jpg' },
                { title: 'Furniture', image: 'beefurniture.jpg' },
            ],
      //listings array retrieved from MS:
      categories: ["Food and Beverage",""],
      allListingsArray:[],
  };
  },

  components: { SearchBar, Category, Listing},

  methods:{
      // async fetchListings() {
      //     const listing_URL = 'http://0.0.0.0:8000/listing'
      //     const response =
      //       fetch(listing_URL)
      //           .then(response => response.json())
      //           .then(data => {
      //               console.log(response);
      //           })
      //           .catch(error => {
      //               // Errors when calling the service; such as network error, 
      //               // service offline, etc
      //               console.log(this.message + error);
      //           });
      // }
    async fetchListings() {
        const listing_URL = 'http://0.0.0.0:8000/listing'
        this.axios.get(listing_URL).then((response) => {
          // console.log("hello")
          // console.log(response.data)
          response.data.forEach(element => {
            // console.log("An ELeemnt")
            // console.log(element)
            this.allListingsArray.push(element)
          });
        })
        console.log(this.allListingsArray)

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
  }
} 
</script>
