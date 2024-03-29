<template>
  <div fluid class="white pa-12" align="center">
    <div class="pa-5 rounded-xl" style="height: 50%">
      <v-row>
        <v-col cols="5">
          <div
            class="amber lighten-2 rounded-circle justify-center pa-3"
            style="width: 450px; height: 450px"
          >
            <v-img
              :src="this.image"
              class="rounded-circle"
              style="height: 425px; width: 425px"
            ></v-img>
          </div>
        </v-col>
        <v-col cols="6" align="left">
          <h1
            class="text-h3 font-weight-medium grey--text text--darken-3 my-2"
            data-aos="fade-right"
          >
            {{ this.listing.name }}
          </h1>
          <h1 class="text-subtitle-1 font-weight-light my-1">
            Posted on: {{ this.listing.created.split("T")[0] }}
          </h1>
          <br />
          <v-container style="margin-bottom: 15px">
            <v-row>
              <v-btn
                class="amber lighten-4 ml-2"
                depressed
                outlined
                @click="gotoTransactions"
              >
                <v-icon left small>mdi-account-multiple</v-icon>
                View Transactions
              </v-btn>
              <div v-if="notAvailable">
                <v-btn
                  class="amber lighten-4 ml-2"
                  depressed
                  outlined
                  disabled
                  @click="deleteListing"
                >
                  <v-icon left small>mdi-delete-empty</v-icon>
                  Listing unavailable to public
                </v-btn>
              </div>
              <div v-else>
                <v-btn
                  class="amber lighten-4 ml-2"
                  depressed
                  outlined
                  @click="deleteListing"
                >
                  <v-icon left small>mdi-delete-empty</v-icon>
                  Delete Listing
                </v-btn>
              </div>
            </v-row>
          </v-container>
          <!-- v tabs -->
          <div class="">
            <v-tabs v-model="tab" grow class="rounded-lg">
              <v-tab class="amber lighten-2">About this Post</v-tab>
              <v-tab class="amber lighten-2">Collection Location</v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab" class="rounded-lg pa-5 amber lighten-5">
              <v-tab-item :value="0">
                <h1
                  class="text-h6 font-weight-medium grey--text text--darken-3 mt-3 mb-1"
                >
                  Description:
                </h1>
                <h1 class="text-h6 font-weight-light grey--text text--darken-3">
                  {{ this.listing.description }}
                </h1>
                <span>
                  <h1
                    class="text-h6 font-weight-medium grey--text text--darken-3 mt-3 mb-1"
                  >
                    Quantity Left:
                  </h1>
                  <h1
                    class="text-h6 font-weight-light grey--text text--darken-3"
                  >
                    {{ this.listing.quantity }}
                  </h1>
                </span>
              </v-tab-item>
              <v-tab-item :value="1">
                <span
                  class="text-h6 font-weight-medium grey--text text--darken-3"
                >
                  Address:
                </span>
                <span
                  class="text-h6 font-weight-light grey--text text--darken-3"
                >
                  {{ this.listing.address }}
                </span>
                <br />
                <span
                  class="text-h6 font-weight-medium grey--text text--darken-3"
                >
                  Postal Code:
                </span>
                <span
                  class="text-h6 font-weight-light grey--text text--darken-3"
                >
                  {{ this.listing.postal }}
                </span>
              </v-tab-item>
            </v-tabs-items>
          </div>
          <br />
          <div class="white rounded-xl"></div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "IndividualListing",
  data() {
    return {
      tab: null,
      listing: null,
      quantity: 0,
      notAvailable: false,
    };
  },
  methods: {
    async fetchListing() {
      const listing_URL =
        "http://localhost:8000/listing/" + this.$route.params.listingid;
      axios
        .get(listing_URL)
        .then((response) => {
          this.listing = response.data;
          this.image = `https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F${this.listing.listing_id}${this.listing.img_ext}?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4`;
          if (this.listing.status == "Unavailable") {
            this.notAvailable = true;
          }
        })
        .catch((exception) => {
          console.log(exception);
        });
    },

    gotoTransactions() {
      this.$router.push(
        `/corporatetransactions/${this.$route.params.listingid}`
      );
    },
    async deleteListing() {
      try {
        this.listing.status = "Unavailable";
        const transaction_management_get = `http://localhost:5100/transaction_management/corporate/${this.$route.params.listingid}`;
        const transactions = await axios.get(transaction_management_get);
        if (transactions.data.code != 200) {
          return alert(transactions.data.message);
        }
      if (transactions.data.result.transactions.result.length > 0) {
          const transaction_management_put = `http://localhost:5100/transaction_management`;
          const update_result = await axios.put(transaction_management_put, {
            listing: this.listing,
            token: this.$store.state.accessToken,
            transactions: transactions.data.result.transactions.result,
            status: "Cancelled",
          });
          if (update_result.data.code != 200) {
            return alert(update_result.data.message);
          }
        }
        const listing_management_url = `http://localhost:5000/listing_management/${this.$route.params.listingid}`;
        const listing_update = await axios.put(listing_management_url, {
          listing: this.listing,
          token: this.$store.state.accessToken,
        });
        if (listing_update.data.code != 200) {
          return alert(listing_update.data.message);
        }
        this.notAvailable = true;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.fetchListing();
  },
};
</script>

<style scoped></style>
