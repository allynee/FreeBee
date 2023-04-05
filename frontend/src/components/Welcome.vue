<!-- Welcome page -->

<template>
  <!-- loading bee -->
  <div v-if="loaded">
    <v-row justify="center" class="my-15">
      <v-col cols="12" align="center" data-aos="fade-left">
        <video-background
          :src="require(`@/assets/bee.mp4`)"
          style="height: 250px; width: 180px"
        >
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
          <v-container class="px-15">
            <v-text-field
              outlined
              prepend-icon="mdi-magnify"
              class="rounded-xl px-5"
              label="Search for a FreeBee"
              clearable
              v-model="search"
            >
            </v-text-field>
          </v-container>
        </v-row>
      </div>

      <div class="mx-15 px-15">
        <v-row class="">
          <span class="text-h4 grey--text text--darken-3">Categories</span>
        </v-row>

        <v-row class="my-10 justify-center">
          <v-col
            cols="2"
            v-for="category in myCategories"
            :key="category.title"
          >
            <Category
              :title="category.title"
              :image="category.image"
              @chooseCat="chooseCat(category.title)"
            >
            </Category>
          </v-col>
        </v-row>

        <v-row class="">
          <h1 class="text-h4 grey--text text--darken-3">Recommended for you</h1>
        </v-row>
        <v-row class="my-15">
          <v-col
            cols="12"
            md="4"
            lg="3"
            v-for="aListing in recListingsArray"
            :key="aListing.listing_id"
          >
            <Listing
              :aListing="aListing"
              @gotoListing="gotoListing(aListing.listing.listing_id)"
            ></Listing>
          </v-col>
        </v-row>
        <v-row class="">
          <h1 class="text-h4 grey--text text--darken-3">All FreeBees</h1>
        </v-row>

        <v-row class="my-15">
          <v-col
            cols="12"
            md="4"
            lg="3"
            v-for="aListing in filteredListings"
            :key="aListing.listing.listing_id"
          >
            <Listing
              :aListing="aListing"
              @gotoListing="gotoListing(aListing.listing.listing_id)"
            ></Listing>
          </v-col>
        </v-row>
      </div>

      <!-- scroll to top button -->
      <v-btn
        v-scroll="onScroll"
        v-show="fab"
        fab
        fixed
        bottom
        right
        color="amber lighten-3"
        @click="toTop"
      >
        <v-icon>mdi-chevron-up</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import AOS from "aos";
import Category from "./Category.vue";
import Listing from "./Listing.vue";
import axios from "axios";
export default {
  name: "HelloWorld",
  mounted() {
    AOS.init({
      duration: 1600,
    });
  },
  data() {
    return {
      fab: false,
      myCategories: [
        { title: "Food & Drinks", image: "Honey.png" },
        { title: "Apparel", image: "yellowshirt.jpg" },
        { title: "Electronics", image: "beeelectronic.jpg" },
        { title: "Furniture", image: "beefurniture.jpg" },
        { title: "Toys & Hobbies", image: "pigbee.jpg" },
        { title: "Everything Else", image: "manybees.jpg" },
      ],
      //listings array retrieved from MS:
      allListingsArray: [],
      recListingsArray: [],
      filteredCategories: [
        "Food & Drinks",
        "Apparel",
        "Electronics",
        "Furniture",
        "Toys & Hobbies",
        "Everything Else",
      ],
      loaded: true,
      search: "",
    };
  },
  computed: {
    filteredListings() {
      return this.allListingsArray.filter((listing) => {
        if (
          this.filteredCategories.includes(listing.listing.category) &&
          listing.listing.name.toLowerCase().includes(this.search)
        ) {
          return true;
        } else {
          return false;
        }
      });
    },
  },

  components: { Category, Listing },

  methods: {
    async fetchListings() {
      try {
        const listing_URL = `http://localhost:5000/listing_management`;
        const response = await axios.get(listing_URL);
        response.data.forEach((element) => {
          if (element.listing.status == "Available") {
            //
            this.allListingsArray.push(element);
          }
        });
        console.log("this.filter_recc called")
        this.filter_recc();
      } catch (error) {
        console.log(error);
      }
    },
    gotoListing(listing_id) {
      this.$router.push({
        name: "IndividualListing",
        params: { listingid: listing_id },
      });
    },
    chooseCat(cat) {
      if (
        this.filteredCategories.length == 1 &&
        this.filteredCategories.includes(cat)
      ) {
        this.filteredCategories = [
          "Food & Drinks",
          "Apparel",
          "Electronics",
          "Furniture",
          "Toys & Hobbies",
          "Everything Else",
        ];
      } else {
        this.filteredCategories = [];
        this.filteredCategories.push(cat);
      }
    },
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    filter_recc(){
      console.log("filter_recc called")
      console.log (this.allListingsArray)
      let rec_area = this.$store.state.area;
      let rec_district = this.$store.state.district;
      console.log(rec_area)
      console.log(rec_district)
      if(this.allListingsArray.length <= 4){
        this.recListingsArray = this.allListingsArray
        console.log("this.allListingsArray.length <= 4")
      }
      else if(rec_area == null){
        this.recListingsArray = this.allListingsArray.slice(-4)
        console.log("rec_area == null")
      }
      else{
        console.log("filtering")
        for (let i = 0; i < this.allListingsArray.length; i++){
          let each_listing = this.allListingsArray[i]
          if(each_listing['listing']['district'] == rec_district && !(this.recListingsArray.includes(each_listing))){

            this.recListingsArray.push(each_listing);
          }
        }
        if (this.recListingsArray.length < 4){
          for (let i = 0; i < this.allListingsArray.length; i++){
            let each_listing = this.allListingsArray[i]
            if(each_listing['listing']['area'] == rec_area && !(this.recListingsArray.includes(each_listing))){
              this.recListingsArray.push(each_listing);
            }
          }
        }
        if (this.recListingsArray.length < 4){
          while (this.recListingsArray.length < 4 ){
            let elem = this.allListingsArray.pop()
            if (!(this.recListingsArray.includes(elem))){
              this.recListingsArray.push(elem);
            }
          }
        }
        console.log(this.recListingsArray)
      }
    },
  },
  created() {
    this.fetchListings();
    setTimeout(() => {
      this.loaded = false;
    }, 1250);
  },
};
</script>
