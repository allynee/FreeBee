<template>
  <div class="white bground">
    <v-container
      class="mx-auto"
      style="width: 45%; height: 45%"
      data-aos="fade-down"
    >
      <v-row class="mt-16">
        <span class="mt-16"> </span>
      </v-row>
      <v-row class="mt-16">
        <span> </span>
      </v-row>
      <v-row class="mb-7 mt-16 pt-0 d-flex align-center">
        <span class="text-h4 mt-16 text-capitalize brown--text mx-auto"
          >Login</span
        >
      </v-row>
      <!-- <v-row> -->
      <!-- <v-card style="width:45%;height:75%;" elevation="2" class="mx-auto brown pt-9 pb-10 lighten-4">
                    <v-card-text>  -->
      <v-container>
        <form @submit.prevent="sampleLogin">
          <!-- <v-row >
                                    <v-col>
                                    <v-alert v-if="this.loggedout" type="info">
                                    You have logged out successfully
                                    </v-alert>
                                   
                                    </v-col>

                                </v-row> -->

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                name="email"
                label="Email"
                id="email"
                v-model="email"
                type="email"
                outlined
                required
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                name="password"
                label="Password"
                id="password"
                v-model="password"
                type="password"
                outlined
                required
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-btn
                block
                outlined
                brown
                type="submit"
                :disabled="!formIsValid"
                :loading="loading"
              >
                Login
                <!-- button loader -->
                <template v-slot:loader>
                  <span class="custom-loader">
                    <v-icon light>mdi-cached</v-icon>
                  </span>
                </template>
              </v-btn>

              <v-row>
                <v-col class="my-3">
                  <v-alert type="error" v-if="error">
                    Login failed. Please enter again!
                  </v-alert>
                </v-col>
              </v-row>
            </v-flex>
          </v-layout>
        </form>
      </v-container>
      <!-- </v-card-text>
                </v-card>  -->
      <!-- </v-row> -->
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
const axios = require("axios");

export default {
  name: "login",
  data() {
    return {
      email: "",
      password: "",
      userid: "",
      error: false,
    };
  },
  computed: {
    loading() {
      return this.$store.getters.loading;
    },
    formIsValid() {
      return this.email != "" && this.password != "";
    },

    user() {
      return this.$store.getters.getuser;
    },
  },
  watch: {
    user(value) {
      if (value != null && value != undefined) {
        this.$router.push("/");
      }
    },
  },
  methods: {
    sampleLogin() {
      let data = "";

      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `http://localhost:3001/login/${this.email}/${this.password}`,
        headers: {},
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          
          var expires = "";
          var date = new Date();
          date.setTime(date.getTime() + 10 * 60 * 1000);
          expires = "; expires=" + date.toUTCString();
          document.cookie =
            "accessToken=" + response.data.accessToken + ";" + expires;
          console.log("Logged in");
          this.$router.push('/')
        })

        .catch((error) => {
          console.log(error);
        });
    },
  //  checkAccess() {
  //     let accessToken = null;
  //     var nameEQ = "accessToken=";
  //     var ca = document.cookie.split(";");
  //     for (var i = 0; i < ca.length; i++) {
  //       var c = ca[i];
  //       while (c.charAt(0) == " ") c = c.substring(1, c.length);
  //       if (c.indexOf(nameEQ) == 0) {
  //         accessToken = c.substring(nameEQ.length, c.length);
  //       }
  //     }
  //     if (accessToken) {
  //       let data = "";

  //       let config = {
  //         method: "get",
  //         maxBodyLength: Infinity,
  //         url: ` http://localhost:3001/auth/checkaccess/${accessToken}`,
  //         headers: {},
  //         data: data,
  //       };

  //       axios
  //         .request(config)
  //         .then((response) => {
  //           console.log('response')
  //           console.log(response.data);
  //         })
  //         .catch((error) => {
  //           console.log(error);
  //         });
  //     }
  //   },
  },
};
</script>
<style scoped>
.bground {
  background: url("../assets/dogss.png");
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}
</style>
