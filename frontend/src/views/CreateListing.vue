<template>
  <div class="white pa-5 bground" style="height: 50%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <span class="text-h6 text-capitalize orange--text"
        >Give back to the Community</span
      ><br />
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 text-capitalize brown--text"
          >Create a listing</span
        >
      </v-row>

      <v-card>
        <v-card-text>
          <form @submit.prevent="onSubmit">
            <v-container>
              <v-text-field
                outlined
                rounded
                name="listingName"
                label="Name of Item"
                id="listingName"
                v-model="listingName"
                type="text"
                required
              >
              </v-text-field>
            </v-container>

            <v-container>
              <v-file-input
                outlined
                rounded
                name="itemImage"
                label="Image of Item"
                id="itemImage"
                v-model="itemImage"
                type="file"
                required
              >
              </v-file-input>
            </v-container>
            <v-container>
              <v-text-field
                outlined
                rounded
                name="itemDescription"
                label="Description of Item"
                id="itemDescription"
                height="150"
                v-model="itemDescription"
                type="text"
                required
              >
              </v-text-field>
            </v-container>

            <v-container>
              <v-row>
                <v-text-field
                  style="margin-left: 15px"
                  outlined
                  rounded
                  name="address"
                  id="address"
                  v-model="address"
                  type="text"
                  required
                >
                </v-text-field>
              </v-row>
            </v-container>

            <v-container>
              <v-text-field
                outlined
                rounded
                name="collectionDetails"
                label="Collection Details"
                id="collectionDetails"
                v-model="collectionDetails"
                type="text"
                required
              >
              </v-text-field>
            </v-container>

            <v-container>
              <v-row>
                <v-text-field
                  style="margin-left: 15px"
                  outlined
                  rounded
                  name="quantity"
                  label="Quantity"
                  id="quantity"
                  v-model="quantity"
                  type="number"
                  required
                >
                </v-text-field>
                <v-select
                  style="margin-left: 15px; margin-right: 15px"
                  outlined
                  rounded
                  name="category"
                  label="Category"
                  id="category"
                  v-model="itemCategory"
                  :items="myCategories"
                >
                </v-select>
              </v-row>
            </v-container>

            <v-container>
              <v-btn type="submit" block brown outlined>
                List Item
                <!-- button loader -->
                <template v-slot:loader>
                  <span class="custom-loader">
                    <v-icon light>mdi-cached</v-icon>
                  </span>
                </template>
              </v-btn>
            </v-container>
          </form>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import axios from "axios";
/* global google */

export default {
  name: "CreateListing",
  data() {
    return {
      myCategories: [
        "Food & Drinks",
        "Apparel",
        "Electronics",
        "Furniture",
        "Toys & Hobbies",
        "Others",
      ],
      listingName: "",
      itemDescription: "",
      collectionAddress: "",
      collectionDetails: "",
      quantity: "",
      itemCategory: "",
      itemImage: null,
      image: null,
      imageUrl: null,
      address: null,
      apiKey: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
      geocodeResult: null,
    };
  },
  computed: {},
  methods: {
    async onSubmit() {
      try {
        const formData = new FormData();

        formData.append("image", this.itemImage, this.itemImage.name);
        let listing = {
          corporate_id: this.$store.state.uid,
          corporate_name: this.$store.state.corporateName,
          name: this.listingName,
          description: this.itemDescription,
          collection_details: this.collectionDetails,
          address: this.geocodeResult,
          postal: 0,
          district: 0,
          area: "",
          category: this.itemCategory,
          quantity: this.quantity,
          status: "Available",
        };
        // formData.append("listing", listing);
        let token = this.$store.state.accessToken;
        var data = {
          listing: JSON.stringify(listing),
          token: token,
        };
        formData.append("data", JSON.stringify(data));

        const listingManagementUrl = "http://localhost:5000/listing_management";
        const response = await axios.post(listingManagementUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        if (response.data[1] == 200) {
          alert("Listing Successful !");
          this.$router.push("/");
        }else{
          alert(response.data[0].message)
        }
      } catch (error) {
        console.log(error);
      }
    },
    loadGoogleMaps(apiKey) {
      return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
        script.onload = () => {
          resolve();
        };
        script.onerror = () => {
          reject(new Error("Failed to load Google Maps API script"));
        };
        document.head.appendChild(script);
      });
    },
    async initAutocomplete(apiKey) {
      await this.loadGoogleMaps(apiKey);
      const input = document.getElementById("address");
      const autocomplete = new google.maps.places.Autocomplete(input);
      // Set options for the autocomplete search box
      autocomplete.setFields(["place_id", "formatted_address"]);
      autocomplete.setTypes(["geocode"]);
      // Listen for changes to the input field
      autocomplete.addListener("place_changed", async () => {
        autocomplete.getPlace();
        // Use the getPlacePredictions() function to get more autocomplete results
        const service = new google.maps.places.AutocompleteService();
        const request = {
          input: input.value,
          types: ["geocode"],
        };
        try {
          const results = await new Promise((resolve, reject) => {
            service.getPlacePredictions(request, (results, status) => {
              if (status === google.maps.places.PlacesServiceStatus.OK) {
                resolve(results);
              } else {
                reject(status);
              }
            });
          });
          const address = results[0].description;
          this.geocodeResult = address; // parase address information to Vue
        } catch (error) {
          console.error(error);
        }
      });
    },
  },
  mounted() {
    this.initAutocomplete(this.apiKey, this);
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
