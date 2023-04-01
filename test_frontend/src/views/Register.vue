<template>
  <div class="white pa-5 bground" style="height: 25%">
    <v-container class="pb-15" style="width: 50%" data-aos="fade-down">
      <span class="text-h6 text-capitalize orange--text"
        >Create your account.</span
      ><br />
      <v-row class="mb-7 ml-1 mt-1">
        <span class="text-h4 text-capitalize brown--text"
          >Join our community.</span
        >
      </v-row>

      <v-card>
        <v-tabs v-model="tab" fixed-tabs color="orange" bg-color="white">
          <v-tab>User</v-tab>
          <v-tab>Corporate</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item :value="0">
            <v-card-text>
              <form @submit.prevent="onRegister('beneficiary')">
                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="username"
                    label="Username"
                    id="username"
                    v-model="username"
                    type="text"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="email"
                    label="Email"
                    id="email"
                    v-model="email"
                    type="email"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="phone"
                    label="Mobile Number"
                    id="phone"
                    v-model="phone"
                    type="number"
                    hide-spin-buttons
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="address"
                    label="Street Address"
                    id="address"
                    v-model="address"
                    type="text"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="password"
                    label="Password"
                    id="password"
                    v-model="password"
                    :append-icon="value ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="() => (value = !value)"
                    :type="value ? 'password' : 'text'"
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="confirmpassword"
                    label="Confirm Password"
                    id="confirmpassword"
                    v-model="confirmpassword"
                    :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="() => (showPassword = !showPassword)"
                    :type="showPassword ? 'password' : 'text'"
                  >
                  </v-text-field>
                </v-container>
                <span class>
                  <v-checkbox>
                    <template v-slot:label>
                      I wish to receive emails regarding activities involving my
                      account
                    </template>
                  </v-checkbox>
                </span>

                <v-container>
                  <v-btn
                    type="submit"
                    block
                    brown
                    outlined
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
                </v-container>

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
            </v-card-text>
          </v-tab-item>

          <v-tab-item :value="1">
            <v-card-text>
              <form @submit.prevent="onRegister('corporate')">
                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="corporatename"
                    label="Corporate Name"
                    id="corporatename"
                    v-model="corporatename"
                    type="text"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="corporateEmail"
                    label="Corporate Email"
                    id="corporateEmail"
                    v-model="corporateEmail"
                    type="email"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="description"
                    label="Description"
                    id="description"
                    v-model="description"
                    type="text"
                    required
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="password"
                    label="Password"
                    id="password"
                    v-model="password"
                    :append-icon="value ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="() => (value = !value)"
                    :type="value ? 'password' : 'text'"
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-text-field
                    outlined
                    rounded
                    name="confirmpassword"
                    label="Confirm Password"
                    id="confirmpassword"
                    v-model="confirmpassword"
                    :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="() => (showPassword = !showPassword)"
                    :type="showPassword ? 'password' : 'text'"
                  >
                  </v-text-field>
                </v-container>

                <v-container>
                  <v-btn
                    type="submit"
                    block
                    brown
                    outlined
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
                </v-container>

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
            </v-card-text>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-container>
  </div>
</template>

<style src="../style/style.css"></style>

<script>
import axios from 'axios';

export default {
  name: "register",
  data() {
    return {
      tab: null,
      username: "",
      email: "",
      phone: "",
      address: "",
      corporatename: "",
      corporateEmail: "",
      description: "",
      password: "",
      confirmpassword: "",
      userid: "",
      corporateid: "",
      errorstatus: false,
      value: String,
      showPassword: String,
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
    onRegister(role) {
        console.log(role)
        let name
        let email
        if(role == 'corporate'){
            name = this.corporatename 
            email = this.corporateEmail
        }
        else{
            name = null
            email = this.email
        }
      axios
        .post("http://localhost:3001/register", {
          email: email,
          password: this.password,
          role: role,
          name: name
        })
        .then((response) => {
          const response_data = response.data;
          if (response_data.statusCode == "200") {
            console.log(response_data.name)
            this.$store.commit('access',{
                accessToken: response_data.accessToken ,
                uid: response_data.uid,
                corporateName: response_data.name
            })
            this.$router.push('/')
            // if function to push to sql db
          } else {
            console.log("fail");
            alert(`${response_data.authStatus},${response_data.errorMessage}`)
          }
          console.log(this.$store.state.accessToken, this.$store.state.uid)
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
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}
</style>
