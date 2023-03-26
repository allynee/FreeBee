<template>
  <div class="white pa-15 pt-5 bground">
    <v-container
      class="pl-10 pr-10 pb-10"
      style="width: 45%; height: 45%"
      data-aos="fade-down"
    >
      <span class="text-h6 text-capitalize grey--text"
        >Create your account.</span
      ><br />
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 text-capitalize brown--text"
          >Join thousands of pet lovers.</span
        >
      </v-row>
      <v-container>
        <form @submit.prevent="onRegister">
          <v-layout row>
            <v-flex xs12>
              <v-text-field
                outlined
                name="name"
                label="Name*"
                id="name"
                v-model="name"
                type="text"
                :rules="nameRules"
                required
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                outlined
                name="email"
                label="Email*"
                id="email"
                v-model="email"
                type="email"
                :rules="emailRules"
                required
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                outlined
                name="username"
                label="Username*"
                id="username"
                v-model="username"
                type="text"
                :rules="userRules"
                required
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                outlined
                name="password"
                label="Password*"
                id="password"
                v-model="password"
                :append-icon="value ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append="() => (value = !value)"
                :type="value ? 'password' : 'text'"
                :rules="[passwordLength]"
              >
              </v-text-field>
            </v-flex>
          </v-layout>

          <v-layout row>
            <v-flex xs12>
              <v-text-field
                outlined
                name="confirmpassword"
                label="Confirm Password*"
                id="confirmpassword"
                v-model="confirmpassword"
                :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append="() => (showPassword = !showPassword)"
                :type="showPassword ? 'password' : 'text'"
                :rules="[comparePasswords]"
              >
              </v-text-field>
            </v-flex>
          </v-layout>
          <span class>
            <v-checkbox>
              <template v-slot:label>
                I wish to receive emails regarding activities involving my
                account
              </template>
            </v-checkbox>
          </span>

          <v-layout row>
            <v-flex xs12>
              <v-btn
                type="submit"
                block
                brown
                outlined
                :disabled="!formIsValid"
                :loading="loading"
              >
                Register
                <!-- button loader -->
                <template v-slot:loader>
                  <span class="custom-loader">
                    <v-icon light>mdi-cached</v-icon>
                  </span>
                </template>
              </v-btn>
            </v-flex>
          </v-layout>

          <v-row>
            <v-col class="my-3">
              <v-alert type="error" v-if="errorstatus">
                Email already in use!
              </v-alert>
            </v-col>
          </v-row>

          <!-- Error Message -->
          <!-- <v-layout row>
                                    <v-flex xs12>
                                        <p v-if="errorstatus"></p>
                                    </v-flex>
                                </v-layout> -->
        </form>
      </v-container>
    </v-container>
  </div>

  <!-- </v-card-text>
                </v-card>
            </v-flex>
        </v-layout> -->
</template>

<style src="../style/style.css"></style>

<script>
const axios = require("axios");
export default {
  name: "register",
  data() {
    return {
      name: "",
      email: "",
      username: "",
      password: "",
      confirmpassword: "",
      userid: "",
      errorstatus: false,
      value: String,
      showPassword: String,
      nameRules: [(v) => v.length >= 2 || "Minimum length is 2 characters"],
      emailRules: [
        (v) =>
          !v ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          "E-mail must be valid",
      ],
      userRules: [
        (v) => v.length >= 8 || "Minimum length is 8 characters",
        (v) => /[0-9]/.test(v) || "Must contain at least 1 digit",
      ],
      // pwdRules: [
      //     v => !!v || 'Please type password.',
      //     v => (v && v.length >= 6) || 'Minimum length is 6 characters',
      //     v => /[a-z]/.test(v) || 'Must contain at least 1 lowercase letter',
      //     v => /[A-Z]/.test(v) || 'Must contain at least 1 uppercase letter',
      //     v => /[`!@#$%^&*()_+\-=[\]{};':"\\|,.<>?~]/.test(v) || 'Must contain at least 1 symbol'
      // ],
    };
  },
  computed: {
    loading() {
      return this.$store.getters.loading;
    },
    comparePasswords() {
      return this.password != this.confirmpassword
        ? "Passwords do not match!"
        : "";
    },
    passwordLength() {
      if (this.password.length < 6) {
        return "Minimum length is 6 characters";
      } else if (!this.password.match(/[a-z]/)) {
        return "Must contain at least 1 lowercase letter";
      } else if (!this.password.match(/[A-Z]/)) {
        return "Must contain at least 1 uppercase letter";
      } else if (!this.password.match(/[`!@#$%^&*()_+\-=[\]{};':"\\|,.<>?~]/)) {
        return "Must contain at least 1 symbol";
      } else {
        return true;
      }
    },
    formIsValid() {
      return (
        this.fullname != "" &&
        this.email != "" &&
        this.username != "" &&
        this.password != "" &&
        this.confirmpassword != "" &&
        this.password == this.confirmpassword
      );
    },
  },
  methods: {
    onRegister() {
      axios
        .post("http://localhost:3001/register", {
          email: this.email,
          password: this.password,
          role: "beneficiary",
        })
        .then((response) => {
          const response_data = response.data;
          if (response_data.statusCode == "200") {
            var expires = "";
            var date = new Date();
            date.setTime(date.getTime() + 1 * 60 * 1000);
            expires = "; expires=" + date.toUTCString();
            document.cookie =
              "accessToken=" + response_data.accessToken + ";" + expires;
            console.log("pass");
          } else {
            console.log("fail");
          }
        })
        .catch((error) => {
          console.log("error " + error);
        });
    },
  },
};
</script>
<style scoped>
.bground {
  background: url("../assets/bg.png");
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}
</style>
