import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportPet from '../views/ReportPet.vue'
import Search from '../views/Dashboard.vue'
import MyMap from '../views/MyMap.vue'
// import Register from '../views/RegisterBeneficiary.vue'
import Login from '../views/Login.vue'
import authguard from './auth-guard.js'
import Inbox from '../views/Inbox.vue'

import SignUp from '../views/SignUp.vue'
import Account from '../views/Account.vue'
import Onepet from '../views/Onepet.vue'
import MatchedPets from '../views/MatchedPets.vue'
import BeneficiarySignUp  from '../views/RegisterBeneficiary.vue'
import CorporateSignUp  from '../views/RegisterCorporate.vue'

import RegisterFilter from '../views/RegisterFilter.vue'
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
    path: '/inbox',
    name: 'inbox',
    component: Inbox,
    // beforeEnter:authguard,

  },
  {
    path: '/account',
    name: 'account',
    component: Account,
    beforeEnter:authguard,

  },
  // {
  //   path:'/register',
  //   name:'register',
  //   component:Register
  // },
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
    name: 'Register Filter',
    component: RegisterFilter,
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
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
