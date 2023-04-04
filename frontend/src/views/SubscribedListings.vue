<template>
  <div class="white pa-5 bground" style="height: 50%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 text-capitalize brown--text"
          >These freebies are waiting for you!</span
        >
      </v-row>

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
                <Listing :aListing="aListing" @gotoListing="gotoListing(aListing.listing.listing_id)"></Listing> </v-col
            ></v-row>
          </v-card-text>
        </v-tab-item>

        <v-tab-item :value="1">
          <v-card-text> </v-card-text>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import Listing from "../components/Listing.vue";
import axios from "axios";

export default {
  name: "register",
  data() {
    return {
      fab: false,
      tab: null,
      inProgressArray: [],
      readyArray: [],
      completedArray: [],
      cancelledArray: [],
      subscriptions:null,
    };
  },
  components: { Listing },

  methods: {
    async fetchTransactions() {
      const transaction_URL = "http://localhost:9000/transactions";
      axios.get(transaction_URL).then((response) => {
        response.data.forEach((transaction) => {
          if (transaction.status == "In Progress") {
            this.inProgressArray.push(transaction);
          } else if (transaction.status == "Ready for Collection") {
            this.readyArray.push(transaction);
          } else if (transaction.status == "Completed") {
            this.completedArray.push(transaction);
          } else if (transaction.status == "Cancelled") {
            this.cancelledArray.push(transaction);
          }
        });
      });
    },
    fetchSubscriptions() {
      const user_url = `http://localhost:5000/subscriptions/${this.$store.state.uid}`;
      axios.get(user_url).then((subscriptions) => {
        this.subscriptions = subscriptions.data;
        console.log(subscriptions.data);
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
