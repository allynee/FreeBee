import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportPet from '../views/ReportPet.vue'
import Search from '../views/Dashboard.vue'
import MyMap from '../views/MyMap.vue'
// import Register from '../views/RegisterBeneficiary.vue'
import Login from '../views/Login.vue'
import authguard from './auth-guard.js'
import MyFreeBees from '../views/MyFreeBees.vue'

import SignUp from '../views/SignUp.vue'
import Account from '../views/Account.vue'
import Onepet from '../views/Onepet.vue'
import MatchedPets from '../views/MatchedPets.vue'
import Register from '../views/Register.vue'
import BeneficiarySignUp  from '../views/RegisterBeneficiary.vue'
import CorporateSignUp  from '../views/RegisterCorporate.vue'
import CreateListing from '../views/CreateListing.vue'
import UserTransactions from '../views/UserTransactions.vue'

import IndividualListing from '../views/IndividualListing.vue'

import Image from '../views/Image.vue'
import Maps from '../views/maps.vue'
// import RegisterFilter from '../views/RegisterFilter.vue'
// import RegisterFilter from '../views/RegisterFilter.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/reportpet',
    name: 'reportpet',
    component: ReportPet,
    beforeEnter:authguard,
  },
  {
    path: '/SearchAllPets',
    name: 'search',
    component: Search,
    beforeEnter:authguard,
  },
  {
    path:'/SearchAllPets/:petid',
    props:true,
    name:'Onepet',
    component:Onepet,
    // beforeEnter:authguard
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
    path: '/maps',
    name: 'maps',
    component: Maps,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
