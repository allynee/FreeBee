<template>
  <div>
    <v-hover v-slot="{ hover }">
      <v-card
        flat
        :elevation="hover ? 10 : 2"
        :class="{ 'on-hover': hover }"
        style="width: 350px; height: 470px"
        outlined
        class="pa-2"
      >
        <v-card-actions>
          <!-- <v-btn v-if="isRed" depressed plain @click="like" class="">
       <v-icon :class="{'red': isRed}">mdi-heart</v-icon>\ -->
      <div v-if="favourite">
       <v-btn icon color="pink" @click="unlike">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </div>
      <div v-else>
        <v-btn icon color="grey" @click="like">
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </div>
    <!-- </v-btn> -->
    <!-- <v-btn v-else depressed plain @click="like" class="">
      <v-icon :class="{'red': isRed}">mdi-circle</v-icon>
      this not is red
   </v-btn> -->
        </v-card-actions>

        <v-img
          cover
          style="width: 250px; max-height:200px"
          :src="aListing.firebase_url"
          class="mx-auto"
          contain
          @click="$emit('gotoListing')"
        />

        <v-card-title class="">{{ aListing.listing.name }}</v-card-title>
        <v-divider class="mx-3 mb-1"></v-divider>
        <v-card-text>
          <div class="text-subtitle-2 mb-2">
            Posted By: {{ aListing.listing.corporate_name }}
          </div>
          <div class="mb-2">
            <v-icon small left color="green darken-4">mdi-map-marker</v-icon>
            <span class="subheading me-2">{{ aListing.listing.address }}</span>
          </div>
          <div
            class="text-subtitle-2 font-weight-bold mb-2 red--text text--darken-4"
          >
            {{ aListing.listing.quantity }} left in stock!
          </div>
        </v-card-text>
      </v-card>
    </v-hover>
  </div>
</template>

<script>
import axios from "axios";

export default {
    emits:['gotoListing'],
    props: {
      aListing: Object,
    },
    data(){
        return{ 
          favourite: false,
          loaded: true
        }
    },
    computed: {
    },
    methods: {
      checkLike(){
        let config = {
          headers: { 
            'Content-Type': 'application/json'
          },
          params : {"beneficiary_id": this.$store.state.uid,
                        "listing_id": this.aListing.listing.listing_id
          } 
        }
        axios.get('http://localhost:8421/favourite' , config)
        .then((response) => {
          return response.data
        })
        .catch((error) => {
          console.error(error);
          return false;
        });
      },
      like(){
        if(this.$store.state.uid==null){
          alert("Please register and log in to like this post!")
        }else{
          // console.log("this is the like function")
          const user_URL = 'http://localhost:8421/favourite'
          axios.post(user_URL, {
            beneficiary_id: this.$store.state.uid,
            listing_id: this.aListing.listing.listing_id,
          })
          .then((response) => {
            if (response.status == "201") {
              this.favourite = true;
              console.log("liked!!!")
            } else {
              console.log("fail");
            }
          });
        }
      },
      unlike(){
        // console.log("this is the unlike function")
        const user_URL = 'http://localhost:8421/favourite'
        axios.delete(user_URL, {
            data: {
              beneficiary_id: this.$store.state.uid,
              listing_id: this.aListing.listing.listing_id,
            }
          }).then((response) => {
            const response_data = response.data;
            if (response.status == "200") {
              console.log(response_data.name)
              this.favourite = false;
              console.log("deleted!!!")
            } else {
              console.log("fail");
            }
          });
      }

  },
  created(){
  },
  mounted(){
    // checking if listing is favourited
    axios.get('http://localhost:8421/favourite' , 
          {params : { "beneficiary_id": this.$store.state.uid,
                        "listing_id": this.aListing.listing.listing_id} }
        )
        .then((response) => {
          this.favourite = response.data
        })
        .catch((error) => {
          console.error(error);
          this.favourite = false;
        });
  }
};
</script>

<style scoped>
.v-card {
  transition: opacity 0.2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
}
</style>
