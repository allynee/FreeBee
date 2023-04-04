<template>
  <div>
    <v-card width="100%" class="py-1 px-10">
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="8">
              <h1
                class="text-h4 font-weight-medium grey--text text--darken-3 mb-3"
              >
                {{ aTransaction.listing_details.name }}
              </h1>

              <div>
                <span class="grey--text text--darken-3"> Quantity: </span>
                <span class="font-weight-light">
                  {{ aTransaction.quantity }}
                </span>
              </div>

              <div>
                <span class="grey--text text--darken-3">
                  Claimed Item On:
                </span>
                <span class="font-weight-light">
                  {{ aTransaction.created.split("T")[0] }}
                </span>
              </div>

              <div v-if="aTransaction.modified">
                <span class="grey--text text--darken-3">
                  Last Status Update:
                </span>
                <span class="font-weight-light">
                  {{ aTransaction.modified.split("T")[0] }}
                </span>
              </div>

              <div v-else>
                <span class="grey--text text--darken-3">
                  Last Status Update:
                </span>
                <span class="font-weight-light">
                  {{ aTransaction.created.split("T")[0] }}
                </span>
              </div>

              <div>
                <span class="grey--text text--darken-3">
                  Collection Details:
                </span>
                <span class="font-weight-light">
                  {{ aTransaction.listing_details.collection_details }}
                </span>
              </div>
            </v-col>

            <v-col cols="4" align="center" style="max-height: 150px">
              <v-img
                :src="aTransaction.image_url"
                style="height: 150px; width: 100%; object-fit: contain"
                class=""
              ></v-img>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
    props: {
      aTransaction: Object,
    },
    data(){
        return{
        }
    },
    methods: {
       // redirecting function below
        redirect(listingid){
            console.log(listingid)
            this.$store.dispatch('loadedPet', listingid)
            this.$router.push('/FindFreeBee/'+ listingid)
        },
    },
    mounted(){
        console.log(this.aTransaction)
    }

}
</script>

<style scoped>
.v-card {
  transition: opacity 0.2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
}
</style>
