import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
// import MyMap from "../views/MyMap.vue";
// import Register from '../views/RegisterBeneficiary.vue'
import Login from "../views/Login.vue";
import authguard from "./auth-guard.js";
import notCorp from "./notCorp.js";
import isCorp from './isCorp.js'

// import SignUp from "../views/SignUp.vue";
import Account from "../views/Account.vue";
// import MatchedPets from "../views/MatchedPets.vue";
import Register from "../views/Register.vue";
// import BeneficiarySignUp from "../views/RegisterBeneficiary.vue";
// import CorporateSignUp from "../views/RegisterCorporate.vue";
import CreateListing from "../views/CreateListing.vue";
import UserTransactions from "../views/UserTransactions.vue";
import SubscribedListings from "../views/SubscribedListings.vue";
import CorporateTransactions from "../views/CorporateTransactions.vue";
import CorporateListing from "../views/CorporateListing.vue";
// import CorporateHomePage from "../views/CorporateHomePage.vue";

import Profile from "../views/ProfilePage.vue";
import Liked from "../views/ProfileLiked.vue";
import IndividualListing from "../views/IndividualListing.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  // Indiv Listing
  {
    path: "/FindFreeBee/:listingid",
    props: true,
    name: "IndividualListing",
    component: IndividualListing,
    beforeEnter: notCorp

  },
  {
    path: "/account",
    name: "account",
    component: Account,
    beforeEnter: authguard,
  },
  {
    path: "/login",
    name: "/login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    
  },
  {
    path: "/createlisting",
    name: "Create Listing",
    component: CreateListing,
    beforeEnter: isCorp

  },
  {
    path: "/MyFreeBees",
    name: "My FreeBees",
    component: UserTransactions,
    beforeEnter: notCorp

  },
  {
    path: "/subscribedlistings",
    name: "Subscribed Listings",
    component: SubscribedListings,
  },
  {
    path: "/corporatetransactions/:listingid",
    name: "Corporate Transactions",
    component: CorporateTransactions,
    beforeEnter: isCorp
  },
  {
    path: "/corporatelisting/:listingid",
    name: "Corporate Listing",
    component: CorporateListing,
    beforeEnter: isCorp

  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/liked",
    name: "Liked",
    component: Liked,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
