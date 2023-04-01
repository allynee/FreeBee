import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MyMap from '../views/MyMap.vue'
// import Register from '../views/RegisterBeneficiary.vue'
import Login from '../views/Login.vue'
import authguard from './auth-guard.js'
import MyFreeBees from '../views/MyFreeBees.vue'

import SignUp from '../views/SignUp.vue'
import Account from '../views/Account.vue'
import MatchedPets from '../views/MatchedPets.vue'
import Register from '../views/Register.vue'
import BeneficiarySignUp  from '../views/RegisterBeneficiary.vue'
import CorporateSignUp  from '../views/RegisterCorporate.vue'
import CreateListing from '../views/CreateListing.vue'
import UserTransactions from '../views/UserTransactions.vue'
import SubscribedListings from '../views/SubscribedListings.vue'

import IndividualListing from '../views/IndividualListing.vue'

import Image from '../views/Image.vue'
// import RegisterFilter from '../views/RegisterFilter.vue'
// import RegisterFilter from '../views/RegisterFilter.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // Indiv Listing
  {
    path:'/FindFreeBee/:listingid',
    props: true,
    name:'IndividualListing',
    component: IndividualListing,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/MyMap',
    name: 'MyMap',
    component: MyMap,
    beforeEnter:authguard,
  },
  {
    path: '/MyFreeBees',
    name: 'MyFreeBees',
    component: MyFreeBees,
    // beforeEnter:authguard,

  },
  {
    path: '/account',
    name: 'account',
    component: Account,
    beforeEnter:authguard,

  },
  { 
    path:'/login',
    name:'/login',
    component:Login
  },
  {
    path: '/MatchedPets',
    name: 'MatchedPets',
    component: MatchedPets,
    beforeEnter:authguard,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/beneficiary',
    name: 'Register Beneficiary',
    component: BeneficiarySignUp,
  },
  {
    path: '/corporate',
    name: 'Register Corporate',
    component: CorporateSignUp,
  },
  {
    path: '/createlisting',
    name: 'Create Listing',
    component: CreateListing,
  },
  {
    path:'/image',
    name : 'Image',
    component: Image
  },
  {
    path: '/usertransactions',
    name: 'User Transactions',
    component: UserTransactions,
  },
  {
    path: '/subscribedlistings',
    name: 'Subscribed Listings',
    component: SubscribedListings,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
