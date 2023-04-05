<template>
  <v-container style="margin:0">
    <v-row >
      <v-col cols="3">
        <v-card height="350" width="256">
          <v-navigation-drawer class="amber lighten-2" permanent>
            <v-list>
              <v-list-item
                v-for="item in items"
                :key="item.title"
                link
                :to="item.route"
              >
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
            >Liked FreeBees</span
          >
        </v-row>
        <v-row>
          <v-col v-for="aListing in favourites" :key="aListing.listing_id">
            <Listing
              :aListing="aListing"
              @gotoListing="gotoListing(aListing.listing.listing_id)"
            ></Listing>
          </v-col>
        </v-row>
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
        { title: "Profile", icon: "mdi-account", route: "/profile" },
        { title: "Liked Listings", icon: "mdi-heart", route: "/liked" },
        {
          title: "Subscribed",
          icon: "mdi-email",
          route: "/subscribedlistings",
        },
        { title: "Logout", icon: "mdi-logout" },
      ],
      favourites: null,
    };
  },
  methods: {
    fetchLikes() {
      const user_url = `http://localhost:5000/favourites/${this.$store.state.uid}`;
      axios.get(user_url).then((favourites) => {
        this.favourites = favourites.data;
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
  },
  components: { Listing },
  mounted() {
    this.fetchLikes();
  },
};
</script>

<style scoped></style>
