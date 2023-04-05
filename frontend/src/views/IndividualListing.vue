<template>
  <!-- loading bee -->
  <div v-if="loaded">
    <v-row justify="center" class="my-15">
      <v-col cols="12" align="center" data-aos="fade-left">
        <video-background
          :src="require(`@/assets/bee.mp4`)"
          style="height: 250px; width: 180px"
        >
        </video-background>
      </v-col>
    </v-row>
  </div>
  <div v-else>
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
            <v-row>
              <v-col cols="10" align="left">
                <h1
                  class="text-h3 font-weight-medium grey--text text--darken-3 my-2"
                  data-aos="fade-right"
                >
                  {{ listing.name }}
                </h1>
                <h1 class="text-subtitle-1 font-weight-light my-1">
                  Posted on: {{ listing.created.split("T")[0] }}
                </h1>
              </v-col>
              <v-col cols="2" align="center" justify-content-center>
                <div v-if="favourite">
                  <v-btn x-large icon color="pink" @click="unlike">
                    <v-icon>mdi-heart</v-icon>
                  </v-btn>
                </div>
                <div v-else>
                  <v-btn x-large icon color="grey" @click="like">
                    <v-icon>mdi-heart</v-icon>
                  </v-btn>
                </div>
              </v-col>
            </v-row>
            <br />
            <!-- v tabs -->
            <div class="">
              <v-tabs v-model="tab" grow class="rounded-lg">
                <v-tab class="amber lighten-2">About this Post</v-tab>
                <v-tab class="amber lighten-2">Collection Location</v-tab>
              </v-tabs>

              <v-tabs-items
                v-model="tab"
                class="rounded-lg pa-3 amber lighten-5"
              >
                <v-tab-item :value="0">
                  <v-row>
                    <v-col cols="7">
                      <span
                        class="text-h6 font-weight-medium grey--text text--darken-3"
                      >
                        Corporate Name:
                      </span>
                      <span
                        class="text-h6 font-weight-light grey--text text--darken-3"
                      >
                        {{ listing.corporate_name }}
                      </span>
                    </v-col>
                    <v-col cols="5">
                      <div v-if="checkSubscribed">
                        <v-btn
                          small
                          class="amber lighten-4"
                          depressed
                          outlined
                          @click="unsubscribe"
                        >
                          <v-icon left small>mdi-bell-off</v-icon>
                          Unsubscribe to company
                        </v-btn>
                      </div>
                      <div v-else>
                        <v-btn
                          small
                          class="amber lighten-3"
                          depressed
                          outlined
                          @click="subscribe"
                        >
                          <v-icon left small>mdi-bell</v-icon>
                          Subscribe to company
                        </v-btn>
                      </div>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12">
                      <span
                        class="text-h6 font-weight-medium grey--text text--darken-3 mt-3 mb-1"
                      >
                        Description:
                      </span>
                      <span
                        class="text-h6 font-weight-light grey--text text--darken-3"
                      >
                        {{ listing.description }}
                      </span>
                    </v-col>
                  </v-row>
                </v-tab-item>
                <v-tab-item :value="1">
                  <span
                    class="text-h6 font-weight-medium grey--text text--darken-3"
                  >
                    Address:
                  </span>
                  <span class="text-h6 font-weight-light">
                    {{ listing.address }}
                  </span>
                  <br />
                  <span
                    class="text-h6 font-weight-medium grey--text text--darken-3"
                  >
                    Postal Code:
                  </span>
                  <span class="text-h6 font-weight-light">
                    {{ listing.postal }}
                  </span>
                </v-tab-item>
              </v-tabs-items>
            </div>
            <br />
            <!-- Claim -->
            <div v-if="notAvailable">
              <v-row>
                <v-col cols="9" align="left">
                  <v-btn
                    rounded-xl
                    x-large
                    class="red lighten-3 ml-2 my-1"
                    disabled
                  >
                    This listing is no longer available
                  </v-btn>
                </v-col>
                <v-col cols="2" align="right">
                  <span data-aos="fade-left" class="ml-15" justify-center>
                    <video-background
                      :src="require(`@/assets/bee.mp4`)"
                      style="height: 50px; width: 36px"
                    ></video-background>
                  </span>
                </v-col>
              </v-row>
            </div>
            <div v-else class="white rounded-xl my-5 pa-4">
              <form @submit.prevent="onClaim()">
                <v-row>
                  <v-col cols="5">
                    <h1
                      class="text-h6 grey--text text--darken-4 font-weight-light"
                    >
                      Claim Now!
                    </h1>
                    <h1 class="text-subtitle-2 red--text text--darken-4">
                      We have {{ listing.quantity }} left in stock.
                    </h1>
                  </v-col>
                  <v-col cols="2">
                    <span data-aos="fade-left" class="ml-15">
                      <video-background
                        :src="require(`@/assets/bee.mp4`)"
                        style="height: 50px; width: 36px"
                      ></video-background>
                    </span>
                  </v-col>
                </v-row>
                <v-row>
                  <div style="width: 30%; height: 40px" class="ml-3">
                    <v-text-field
                      outlined
                      class=""
                      type="number"
                      required
                      name="quantity"
                      label="Quantity"
                      id="quantity"
                      min="1"
                      v-model="quantity"
                    >
                    </v-text-field>
                  </div>
                  <v-btn
                    rounded-xl
                    x-large
                    type="submit"
                    class="amber lighten-3 ml-2 my-1"
                    depressed
                    outlined
                  >
                    Claim
                  </v-btn>
                </v-row>
              </form>
            </div>
          </v-col>
        </v-row>
      </div>
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
      image: null,
      favourite: false,
      subscribed: false,
      loaded: true,
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
          console.log(this.listing);
          this.image = `https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F${this.listing.listing_id}${this.listing.img_ext}?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4`;
          if (this.listing.status == "Unavailable") {
            this.notAvailable = true;
          }
          this.checksubscribe();
        })
        .catch((exception) => {
          console.log(exception);
        });
    },
    async onClaim() {
      try {
        if (this.quantity == 0) {
          return "No";
        } else {
          if (this.$store.state.accessToken) {
            const transactionManagement_URL =
              "http://localhost:5100/transaction_management";
            const response = await axios.post(transactionManagement_URL, {
              listing: this.listing,
              beneficiary_id: this.$store.state.uid,
              token: this.$store.state.accessToken,
              quantity: this.quantity,
            });
            console.log(response.data[1])
            if (response.data[1] == 200) {
              alert(response.data[0].message);
              this.$router.push("/");
            }else{
              alert(response.data[0].message)
            }
          } else {
            this.$router.push("/login");
          }
        }
      } catch (error) {
        alert(error.message);
      }
    },
    checksubscribe() {
      // console.log("this is the checking function")
      const user_URL = `http://localhost:8421/subscription/corporate/${this.listing.corporate_id}`;
      axios.get(user_URL).then((response) => {
        console.log(response.data);
        response.data.forEach((subscriber) => {
          if (subscriber.beneficiary_id == this.$store.state.uid) {
            this.subscribed = true;
          }
        });
      });
    },
    async subscribe() {
      try {
        if (this.$store.state.uid == null) {
          alert("Please register and log in to like this post!");
        } else {
          // console.log("this is the like function")
          const user_URL = "http://localhost:8421/subscription";
          const response = await axios.post(user_URL, {
            beneficiary_id: this.$store.state.uid,
            corporate_id: this.listing.corporate_id,
          });
          if (response.status == "201") {
            this.subscribed = true;
          } else {
            return alert("Subscription failed ");
          }
        }
      } catch (error) {
        alert(error.message);
      }
    },
    unsubscribe() {
      // console.log("this is the unsubscribe function")
      const user_URL = "http://localhost:8421/subscription";
      axios
        .delete(user_URL, {
          data: {
            beneficiary_id: this.$store.state.uid,
            corporate_id: this.listing.corporate_id,
          },
        })
        .then((response) => {
          if (response.status == "200") {
            this.subscribed = false;
          } else {
            return alert("Unscription failed");
          }
        });
    },
    like() {
      if (this.$store.state.uid == null) {
        alert("Please register and log in to like this post!");
      } else {
        // console.log("this is the like function")
        const user_URL = "http://localhost:8421/favourite";
        axios
          .post(user_URL, {
            beneficiary_id: this.$store.state.uid,
            listing_id: this.$route.params.listingid,
          })
          .then((response) => {
            if (response.status == "201") {
              this.favourite = true;
            } else {
              return alert("Favourite failed");
            }
          });
      }
    },
    unlike() {
      // console.log("this is the unlike function")
      const user_URL = "http://localhost:8421/favourite";
      axios
        .delete(user_URL, {
          data: {
            beneficiary_id: this.$store.state.uid,
            listing_id: this.$route.params.listingid,
          },
        })
        .then((response) => {
          if (response.status == "200") {
            this.favourite = false;
          } else {
            return alert("Unfavourite failed");
          }
        });
    },
  },
  computed: {
    checkSubscribed() {
      return this.subscribed;
    },
  },
  created() {
    console.log("Created");
    this.fetchListing();
    // this.checksubscribe();
    setTimeout(() => {
      this.loaded = false;
      // console.log(this.loaded)
    }, 1250);
  },
  mounted() {
    let listing_id = this.$route.params.listingid;
    axios
      .get("http://localhost:8421/favourite", {
        params: {
          beneficiary_id: this.$store.state.uid,
          listing_id: listing_id,
        },
      })
      .then((response) => {
        this.favourite = response.data;
      })
      .catch((error) => {
        console.error(error);
        this.favourite = false;
      });
  },
};
</script>

<style scoped></style>
