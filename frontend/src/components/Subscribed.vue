<template>
    <div>
      <v-card width="650px" style="margin-bottom: 15px">
        <v-card-text>
          <v-container>
            <v-row>
                Corporate Name
            </v-row>
            <v-row>
                Description
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
  