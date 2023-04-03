<template>
  <nav>
    <!-- left side of app bar -->
    <v-app-bar flat app class="px-2" color="white">
      <!-- hamburger bar/navigation drawer for small screens -->
      <v-app-bar-nav-icon
        class="grey--text hidden-md-and-up"
        @click="hamburger = !hamburger"
      ></v-app-bar-nav-icon>

      <!-- logo -->
      <v-btn plain color="yellow darken-3" to="/">
        <v-img
          :src="require('../assets/BeeLogoSmall.png')"
          class="mr-2"
          max-height="50"
          max-width="50"
          contain
        />
        <v-app-bar-title class="text-no-wrap">
          <div>
            <span class="font-weight-regular">Free</span>
            <span class="font-weight-bold">Bee!</span>
            <span class="font-weight-light"> CORPORATE</span>
          </div>
        </v-app-bar-title>
      </v-btn>

      <v-spacer></v-spacer>

      <!-- right side of app bar -->

      <div class="hidden-sm-and-down">
          <v-btn
            plain
            depressed
            color="grey darken-4"
            to="/createlisting"
            class="font-weight-bold hidden-sm-only"
          >
            <v-icon small left>mdi-pencil-outline</v-icon>
            <span
              plain
              color="grey darken-4"
              class="text-body-2 font-weight-bold"
              >Create Listing</span
            >
          </v-btn>
        <v-btn
          v-if="this.$store.state.accessToken"
          @click="onLogout"
          plain
          depressed
          color="grey darken-4"
        >
          <v-icon small left>mdi-logout</v-icon>
          <span plain color="grey darken-4" class="text-body-2 font-weight-bold"
            >Logout</span
          >
        </v-btn>
      </div>
    </v-app-bar>

    <!-- navigation drawer -->
    <v-navigation-drawer
      v-if="!$vuetify.breakpoint.mdAndUp"
      v-model="hamburger"
      app
      temporary
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6"> Menu </v-list-item-title>
          <br /><br />
          <v-list-item-subtitle> Select a page to visit </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-list class="hidden-md-and-up">
        <v-list-item to="/createlisting">
          <v-list-item-action>
            <v-icon>mdi-pencil-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Create Listing</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- logout -->
        <v-list-item v-if="userLoggedIn" @click="onLogout">
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
const axios = require("axios");
export default {
  data() {
    return {
      showDropdown: false,
      hamburger: false,
      authorisation: false,
    };
  },
  computed: {
    links() {
      console.log("links");
      let linkitems;
      if (this.$store.state.accessToken) {
        linkitems = [
          { text: "Find a FreeBee!", route: "/", icon: "mdi-magnify" },
          // {text: 'Report Pet', route:'/ReportPet', icon: 'mdi-dog-side'},
          // {text: 'Search Pet', route:'/SearchAllPets', icon: 'mdi-magnify'},
          { text: "My FreeBees", route: "/usertransactions", icon: "mdi-beehive-outline" },
          { text: "My Account", route: "/Account", icon: "mdi-account" },
          // {text: 'Matched Pets', route:'/MatchedPets', icon: 'mdi-paw'},
        ];
        console.log("login");
      } else {
        linkitems = [
        { text: "Find a FreeBee!", route: "/", icon: "mdi-magnify" },
          { text: "Register", route: "/register", icon: "mdi-account-plus" },
          { text: "Login", route: "/login", icon: "mdi-login" },
        ];
        console.log("not login");
      }
      return linkitems;
    },
  },
  methods: {
    async onLogout() {
      try {
        this.$store.commit("resetState");
        await axios.get(`http://localhost:3001/signout`);
        location.reload();
      } catch (error) {
        console.log(error);
      }
    },
    async userLoggedIn() {
      try {
        // let accessToken = null;
        // var nameEQ = "accessToken=";
        // var ca = document.cookie.split(";");
        // for (var i = 0; i < ca.length; i++) {
        //   var c = ca[i];
        //   while (c.charAt(0) == " ") c = c.substring(1, c.length);
        //   if (c.indexOf(nameEQ) == 0) {
        //     accessToken = c.substring(nameEQ.length, c.length);
        //   }
        // }
        // if (accessToken) {
        //   const response = await axios.get(
        //     ` http://localhost:3001/auth/checkaccess/${accessToken}`
        //   );
        //   if (response.data.statusCode == 200) {
        //     this.authorisation = true;
        //   } else {
        //     this.authorisation = false;
        //   }
        // }
        if (this.$store.getters.getuser != null) {
          this.authorisation = true;
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>
