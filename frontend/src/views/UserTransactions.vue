<template>
  <div class="white pa-5 bground" style="height: 50%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 brown--text text-darken-1"
          >Status of my FreeBees</span
        >
        <v-icon large right class="brown--text text-darken-3">mdi-bee</v-icon>
      </v-row>

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
            v-for="aTransaction in inProgressArray"
            :key="aTransaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <Transaction
              :aTransaction="aTransaction"
              data-aos="fade-up"
            ></Transaction>
          </v-card>
        </v-tab-item>

        <v-tab-item :value="1">
          <v-card
            flat
            v-for="aTransaction in readyArray"
            :key="aTransaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <Transaction
              :aTransaction="aTransaction"
              data-aos="fade-up"
            ></Transaction>
          </v-card>
        </v-tab-item>

        <v-tab-item :value="2">
          <v-card
            flat
            v-for="aTransaction in completedArray"
            :key="aTransaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <Transaction
              :aTransaction="aTransaction"
              data-aos="fade-up"
            ></Transaction>
          </v-card>
        </v-tab-item>

        <v-tab-item :value="3">
          <v-card
            flat
            v-for="aTransaction in cancelledArray"
            :key="aTransaction.transaction_id"
            class="my-5 mx-5"
            data-aos="fade-up"
          >
            <Transaction
              :aTransaction="aTransaction"
              data-aos="fade-up"
            ></Transaction>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import Transaction from "../components/Transaction.vue";
import axios from "axios";
import AOS from "aos";

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
    };
  },
  components: { Transaction },

  methods: {
    async fetchTransactions() {
      try {
        const transaction_URL =
          "http://localhost:5100/transaction_management/beneficiary/" +
          this.$store.state.uid;
        const response = await axios.get(transaction_URL);
        if (response.data.result.length > 0) {
          response.data.result.forEach((transaction) => {
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
      } catch (error) {
        console.log(error);
      }
    },
  },

  computed: {
    loading() {
      return this.$store.getters.loading;
    },
  },
  mounted() {
    this.fetchTransactions();
    AOS.init({
      duration: 800,
    });
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
