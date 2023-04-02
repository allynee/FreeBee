<template>
  <Welcome/>
</template>

<script>
  import Welcome from '../components/Welcome'

  export default {
    name: 'Home',

    components: {
      Welcome,
    },
    mounted(){
      // console.log(document.cookie)
      // console.log('first')
    }
  }
</script>
