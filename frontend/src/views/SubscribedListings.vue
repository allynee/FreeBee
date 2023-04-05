<template>
  <v-container style="margin-left: 0">
    <v-row>
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

      <v-col style="margin: 0">
        <v-row class="mb-2 ml-1 mt-1" style="margin: 0; width: 50vw">
          <span class="text-h4 text-capitalize brown--text"
            >FreeBees from Corporations you follow</span
          >
        </v-row>
        <v-row>
          <v-col
            v-for="aListing in subscriptions"
            :key="aListing.listing_id"
            style="margin-right: 0;width:15vw"
            
          >
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
      subscriptions: null,
      favourites: null,
      fab: false,
      tab: null,
    };
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
  },
};
</script>
<style scoped>
.bground {
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}
</style>
