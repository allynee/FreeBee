<template>
  <v-container>
      <v-row>
          <v-col cols="3">
              <v-card
                  height="350"
                  width="256"
              >
                  <v-navigation-drawer
                  class="amber lighten-2"
                  permanent
                  >
                      <v-list>
                          <v-list-item v-for="item in items" :key="item.title" link>
                              <v-list-item-icon>
                                  <v-icon>{{item.icon}}</v-icon>
                              </v-list-item-icon>

                              <v-list-item-content>
                                  {{item.title}}
                              </v-list-item-content>
                          </v-list-item>
                      </v-list>
                  </v-navigation-drawer>
              </v-card>
          </v-col>

          <v-col>
              <v-tabs v-model="tab" fixed-tabs color="orange" bg-color="white">
                  <v-tab>Subscribed Corporations</v-tab>
                  <v-tab>Liked Listings</v-tab>
              </v-tabs>
              <v-tabs-items v-model="tab">
                  <v-tab-item :value="0">
                      <v-card-text>
                          <v-row>
                              <v-col
                              v-for="aListing in subscriptions"
                              :key="aListing.listing_id"
                              >
                                  <Listing :aListing="aListing" @gotoListing="gotoListing(aListing.listing.listing_id)"></Listing> 
                              </v-col>
                          </v-row>
                      </v-card-text>
                  </v-tab-item>

                  <v-tab-item :value="1">
                      <v-card-text> 
                          <v-row>
                              <v-col
                              v-for="aListing in favourites"
                              :key="aListing.listing_id"
                              >
                                  <Listing :aListing="aListing" @gotoListing="gotoListing(aListing.listing.listing_id)"></Listing> 
                              </v-col>
                          </v-row>
                      </v-card-text>
                  </v-tab-item>
              </v-tabs-items>
          </v-col>
      </v-row>
  </v-container>
</template>

<script>
import Listing from "../components/Listing.vue";
import axios from "axios";

export default {
  data () {
    return {
      items: [
        { title: 'Profile', icon: 'mdi-account' },
        { title: 'Liked Listings', icon: 'mdi-heart'},
        { title: 'Subscribed', icon: 'mdi-email'},
        { title: 'Logout', icon: 'mdi-logout' },
      ],
      subscriptions:null,
      favourites:null,
      fab: false,
      tab: null,
    }
  },
  components: { Listing },
  methods: {
  fetchSubscriptions() {
    const user_url = `http://localhost:5000/subscriptions/${this.$store.state.uid}`;
    axios.get(user_url).then((subscriptions) => {
      this.subscriptions = subscriptions.data;
    });
  },
  gotoListing(listing_id) {
    // console.log(listing_id)
    // console.log("clicked")
    this.$router.push({
      name: "IndividualListing",
      params: { listingid: listing_id },
    });
  },
  fetchLikes() {
    const user_url = `http://localhost:5000/favourites/${this.$store.state.uid}`;
    axios.get(user_url).then((favourites) => {
      this.favourites = favourites.data;
    });
  },
},

computed: {
  loading() {
    return this.$store.getters.loading;
  },
  comparePasswords() {
    return this.password != this.confirmpassword
      ? "Passwords do not match!"
      : "";
  },
  passwordLength() {
    if (this.password.length < 6) {
      return "Minimum length is 6 characters";
    } else if (!this.password.match(/[a-z]/)) {
      return "Must contain at least 1 lowercase letter";
    } else if (!this.password.match(/[A-Z]/)) {
      return "Must contain at least 1 uppercase letter";
    } else if (!this.password.match(/[`!@#$%^&*()_+\-=[\]{};':"\\|,.<>?~]/)) {
      return "Must contain at least 1 symbol";
    } else {
      return true;
    }
  },
  formIsValid() {
    return (
      this.fullname != "" &&
      this.email != "" &&
      this.username != "" &&
      this.password != "" &&
      this.confirmpassword != "" &&
      this.password == this.confirmpassword
    );
  },
},
mounted() {
  this.fetchSubscriptions();
  this.fetchLikes();
},
}
</script>
<style scoped>
.bground {
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}
</style>
