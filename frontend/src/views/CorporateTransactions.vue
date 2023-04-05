<template>
  <div class="white pa-5 bground" style="height: 50%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <v-row class="mb-2 ml-1 mt-1">
        <div class="text-h4 brown--text text-darken-1">Transactions for</div>
        <v-icon large right class="brown--text text-darken-3">mdi-bee</v-icon>
      </v-row>

      <v-container>
        <v-row> View Transaction Status of : </v-row>
      </v-container>
      <v-tabs v-model="tab" grow class="rounded-lg">
        <v-tab class="amber lighten-2">In Progress</v-tab>
        <v-tab class="amber lighten-2">Ready for Collection</v-tab>
        <v-tab class="amber lighten-2">Completed</v-tab>
        <v-tab class="amber lighten-2">Cancelled</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab" class="rounded-lg pa-3 amber lighten-5">
        <v-tab-item :value="0">
          <v-card
            flat
            v-for="transaction in this.inProgressArray"
            :key="transaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <CorporateTransactionCard
              :transaction="transaction"
              data-aos="fade-up"
              @update:addUpdate="addUpdate($event)"
            ></CorporateTransactionCard>
          </v-card>
          <!-- <v-row v-for="transaction in shownTransactions" :key="transaction.transaction_id">
                <CorporateTransactionCard
                  :transaction="transaction"
                  v-on:update:addUpdate="addUpdate($event)"
                ></CorporateTransactionCard>
              </v-row> -->
          <v-btn
            color="amber lighten-3"
            style="margin-top: 10px"
            @click="updateDB('Ready for Collection')"
          >
            Update Status
          </v-btn>
        </v-tab-item>

        <v-tab-item :value="1">
            <v-card
              flat
              v-for="transaction in this.readyArray"
              :key="transaction.transaction_id"
              class="my-5 mx-5"
              data-aos="fade-up"
            >
              <CorporateTransactionCard
                :transaction="transaction"
                data-aos="fade-up"
                @update:addUpdate="addUpdate($event)"
              ></CorporateTransactionCard>
            </v-card>
            <v-btn
              color="amber lighten-3"
              style="margin-top: 10px"
              @click="updateDB('Completed')"
            >
              Update Status
            </v-btn>
        </v-tab-item>

        <v-tab-item :value="2">
          <v-card
            flat
            v-for="transaction in this.completedArray"
            :key="transaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <CorporateTransactionCard
              :transaction="transaction"
              data-aos="fade-up"
            ></CorporateTransactionCard>
          </v-card>
        </v-tab-item>

        <v-tab-item :value="3">
          <v-card
            flat
            v-for="transaction in this.cancelledArray"
            :key="transaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <CorporateTransactionCard
              :transaction="transaction"
              data-aos="fade-up"
            ></CorporateTransactionCard>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import CorporateTransactionCard from "../components/CorporateTransactionCard.vue";
import axios from "axios";

export default {
  name: "corporateTransaction",
  data() {
    return {
      tab: false,
      myStatuses: [
        { name: "In Progress", value: "Ready for Collection" },
        { name: "Ready for Collection", value: "Completed" },
        { name: "Completed", value: "Done" },
        { name: "Cancelled", value: "Cancelled" },
      ],
      inProgressArray: [],
      readyArray: [],
      completedArray: [],
      cancelledArray: [],
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
      try {
        const transaction_URL =
          "http://localhost:5100/transaction_management/corporate/" +
          this.$route.params.listingid;
        const response = await axios.get(transaction_URL);
        if (response.data.code == 200) {
          response.data.result.transactions.result.forEach((transaction) => {
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
        }
        this.listing_details = response.data.result.listing_details.result;
      } catch (error) {
        console.log(error);
      }
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
    async updateDB(status) {
      try {
        if (this.update.length > 0) {
          console.log(this.transactionStatus);
          const response = await axios.put(
            `http://localhost:5100/transaction_management`,
            {
              listing: this.listing_details,
              transactions: this.update,
              token: this.$store.state.accessToken,
              status: status,
            }
          );
          if (response.data.code == 500) {
            return alert("Invalid update request");
          } else {
            alert("Update Success");
            location.reload();
          }
        }
      } catch (error) {
        alert(error.message);
      }
    },
  },

  computed: {},
  created() {
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
