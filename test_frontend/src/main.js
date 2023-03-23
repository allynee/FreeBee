// Main Vue Stuff
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

// Animation Library
import AOS from 'aos'
import 'aos/dist/aos.css'
//backend stuff
import { store } from './store/index'
import "./firebase/index"
import {getAuth, onAuthStateChanged} from 'firebase/auth'
// import { 
//     getFirestore, collection, getDocs
// } from 'firebase/firestore'

//connecting to firebase 

// Geolocation
import VueGeolocation from 'vue-browser-geolocation';
Vue.use(VueGeolocation);

// Gmaps
import * as VueGoogleMaps from 'vue2-google-maps';
import VuetifyGoogleAutocomplete from 'vuetify-google-autocomplete';

//Gmap cluster
import GmapCluster from 'vue2-google-maps/dist/components/cluster';
Vue.component('GmapCluster', GmapCluster)

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCsbcA8EHPhaZbxQ_Gubm_ZhQyy-pcn6JM',
    
    libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)
 
    //// If you want to set the version, you can do so:
    // v: '3.26',

  },
 
  //// If you intend to programmatically custom event listener code
  //// (e.g. `this.$refs.gmap.$on('zoom_changed', someFunc)`)
  //// instead of going through Vue templates (e.g. `<GmapMap @zoom_changed="someFunc">`)
  //// you might need to turn this on.
  // autobindAllEvents: false,
 
  //// If you want to manually install components, e.g.
  //// import {GmapMarker} from 'vue2-google-maps/src/components/marker'
  //// Vue.component('GmapMarker', GmapMarker)
  //// then disable the following:
  // installComponents: true,
})

Vue.use(VuetifyGoogleAutocomplete, {
  /*
    not used as loaded with component
    apiKey: key,
  */
  vueGoogleMapsCompatibility: true,
});

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  store:store,
  render: h => h(App),
  created(){
    const auth= getAuth();
    onAuthStateChanged(auth, (user)=>{
      if(user){
        console.log(user.uid)
        this.$store.dispatch('autoSignIn', user.uid)
      }
    })
  },
  mounted() {
    AOS.init()
  },
}).$mount('#app')