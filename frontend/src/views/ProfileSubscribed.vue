<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <v-card height="350" width="256">
          <v-navigation-drawer class="amber lighten-2" permanent>
            <v-list>
              <v-list-item v-for="item in items" :key="item.title" link>
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                  {{ item.title }}
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-navigation-drawer>
        </v-card>
      </v-col>

      <v-col>
        <v-row class="mb-2 ml-1 mt-1">
          <span class="text-h4 text-capitalize brown--text"
            >Liked Listings</span
          >
        </v-row>
        <Listing></Listing>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Listing from "../components/Listing.vue";
import axios from "axios";

export default {
  data() {
    return {
      items: [
        { title: "Profile", icon: "mdi-account" },
        { title: "Liked Listings", icon: "mdi-heart" },
        { title: "Subscribed", icon: "mdi-email" },
        { title: "Logout", icon: "mdi-logout" },
      ],
      subscriptions: null,
      favourites: null,
      fab: false,
      tab: null,
    };
  },
  components: { Listing },
  methods: {
    async fetchSubscriptions() {
      try {
        const user_url = `http://localhost:5000/subscriptions/${this.$store.state.uid}`;
        const subscriptions = await axios.get(user_url);
        if (subscriptions.status == 201) {
          this.subscriptions = subscriptions.data;
        }
      } catch (error) {
        alert(error.message);
      }
    },
    gotoListing(listing_id) {
      // console.log(listing_id)
      // console.log("clicked")
      this.$router.push({
        name: "IndividualListing",
        params: { listingid: listing_id },
      });
    },
    async fetchLikes() {
      try {
        const user_url = `http://localhost:5000/favourites/${this.$store.state.uid}`;
        const favourites = await axios.get(user_url);
        if (favourites.status == 201) {
          this.favourites = favourites.data;
        } else {
          return alert(favourites.data.detail);
        }
      } catch (error) {
        alert(error.message);
      }
    },
  },

  computed: {
    loading() {
      return this.$store.getters.loading;
    },

  },
  mounted() {
    this.fetchSubscriptions();
    this.fetchLikes();
  },
};
</script>

<style scoped></style>
