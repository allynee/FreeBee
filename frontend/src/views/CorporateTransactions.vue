<template>
  <div class="white pa-5 bground" style="height: 50%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 text-capitalize brown--text"
          >Existing Transactions</span
        >
      </v-row>
      <v-container>
        <div
          class="d-flex justify-content-center align-items-center amber lighten-2 rounded-circle pa-3"
          style="width: 250px; height: 250px"
        >
          <v-img
            :src="image_url"
            class="rounded-circle"
            style="height: 225px; width: 225px"
          ></v-img>
        </div>
      </v-container>
      <v-container>
        <v-row> View Transaction Status of : </v-row>
        <v-row>
          <v-select
            style="margin-right: 15px; max-width: 300px"
            outlined
            rounded
            name="status"
            placeholder="Choose a Status"
            id="status"
            v-model="transactionStatus"
            :items="myStatuses"
            item-text="name"
            item-value="value"
            @change="clearCheckbox"
          >
          </v-select>
          <v-btn
            color="amber lighten-3"
            style="margin-top: 10px"
            @click="updateDB"
          >
            Update Status
          </v-btn>
        </v-row>
        <v-row
          v-for="transaction in shownTransactions"
          :key="transaction.transaction_id"
        >
          <CorporateTransactionCard
            :transaction="transaction"
            v-on:update:addUpdate="addUpdate($event)"
          ></CorporateTransactionCard>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import CorporateTransactionCard from "../components/CorporateTransactionCard.vue";
import axios from "axios";

export default {
  name: "register",
  data() {
    return {
      fab: false,
      myStatuses: [
        { name: "In Progress", value: "Ready for Collection" },
        { name: "Ready for Collection", value: "Collected" },
        { name: "Collected", value: "Done" },
        { name: "Cancelled", value: "Cancelled" },
      ],
      transactions: [],
      image_url: "",
      listing_details: null,
      update: [],
      transactionStatus: "",
    };
  },
  components: { CorporateTransactionCard },

  methods: {
    async fetchTransactions() {
      const transaction_URL =
        "http://localhost:5100//transaction_management/corporate/" +
        this.$route.params.listingid;
      axios.get(transaction_URL).then((response) => {
        // response.data.transactions.forEach((transaction) => {
        //   if(transaction.status == 'In Progress'))
        this.transactions = response.data.result.transactions;
        this.listing_details = response.data.result.listing_details;
        console.log(response.data);
        this.image_url = `https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F${this.listing_details.listing_id}${this.listing_details.img_ext}?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4`;
      });
    },
    addUpdate(value) {
      console.log(value);
      if (value.value != null) {
        this.update.push(value.data);
      } else {
        for (let i = 0; i < this.update.length; i++) {
          if (this.update[i].data.transaction_id == value.data.transaction_id) {
            this.update.splice(i, 1);
          }
        }
      }
    },
    async updateDB() {
      if (this.update.length > 0) {
        console.log(this.transactionStatus)
        axios
          .put(`http://localhost:5100/transaction_management`, {
            listing: this.listing_details,
            transaction: this.update,
            token: this.$store.state.accessToken,
            status: this.transactionStatus,
          })
          .then((response) => {
            if (response.data.code == 404) {
              alert("Invalid update request");
            } else {
              alert("Success");
              location.reload();
            }
          });
      }
    },
    clearCheckbox() {
      this.update = [];
    },
  },

  computed: {
    shownTransactions() {
      let status;
      console.log(this.transactionStatus);
      if (
        this.transactionStatus == "Ready for Collection" ||
        this.transactionStatus == "In Progress"
      ) {
        status = "In Progress";
      } else if (this.transactionStatus == "Collected") {
        status = "Ready for Collection";
      } else if (this.transactionStatus == "Done") {
        status = "Collected";
      }

      return this.transactions.filter((transaction) => {
        if (transaction.status.includes(status)) {
          return true;
        } else {
          return false;
        }
      });
    },
  },
  mounted() {
    this.fetchTransactions();
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
