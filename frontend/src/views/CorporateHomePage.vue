<template>
<CorporateListingCard></CorporateListingCard>
</template>

<script>

// import AOS from 'aos'
// import axios from 'axios'
import CorporateListingCard from '@/components/CorporateListingCard.vue';

export default {

name: 'corporatehomepage',
data(){
  return{
      fab: false,
      myStatuses: ['In Progress', 'Ready for Collection', 'Collected', 'Cancelled'],    
        
  }
},
components : {CorporateListingCard},

methods:{
  
},

computed:{
  
},
}

</script>

<style scoped>

</style>