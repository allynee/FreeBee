<template>
  <div>
    <v-card style="margin-bottom: 15px">
      <v-card-text>
        <v-container>
          <v-row>
          <v-col cols="3">
            <v-list-item>
              <v-checkbox
                v-if="
                  (transaction.status != 'Completed') &
                  (transaction.status != 'Cancelled')
                "
                value="checked"
                v-model="checkbox"
                @click="addTransaction()"
              />
            </v-list-item>
          </v-col>
          <v-col cols="9">
            <v-row> Beneficiary ID: {{ transaction.beneficiary_id }} </v-row>
            <v-row> Quantity claimed: {{ transaction.quantity }} </v-row>
            <v-row>
              Claimed Item on {{ transaction.created.split("T")[0] }}
              {{ transaction.created.split("T")[1] }}
            </v-row>
            <v-row v-if="transaction.modified">
              Last Status Update: {{ transaction.modified.split("T")[0] }}
              {{ transaction.modified.split("T")[1] }}
            </v-row>
            <v-row v-else>
              Last Status Update: {{ transaction.created.split("T")[0] }}
              {{ transaction.created.split("T")[1] }}
            </v-row>
          </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import AOS from "aos";
export default {
  props: {
    transaction: Object,
  },
  mounted() {
    AOS.init({
      duration: 1600,
    });
  },
  data() {
    return {
      myStatuses: [
        "In Progress",
        "Ready for Collection",
        "Collected",
        "Cancelled",
      ],
      checkbox: "",
    };
  },
  methods: {
    // redirecting function below
    redirect(listingid) {
      this.$store.dispatch("loadedPet", listingid);
      this.$router.push("/FindFreeBee/" + listingid);
    },
    addTransaction() {
      this.$emit("update:addUpdate", {
        data: this.transaction,
        value: this.checkbox,
      });
    },
  },
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
