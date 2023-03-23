<template>
<v-hover v-slot="{ hover }">
    <v-card flat :elevation="hover ? 10 : 2" :class="{ 'on-hover': hover }" style="max-width:300px" outlined class="py-2"> 
        <v-img :src="require('../assets/Honey.png')" class="mx-auto" max-height="200" max-width="200" contain/>
        <v-card-title class="justify-center">Food and Beverage</v-card-title>
    </v-card>
</v-hover>
</template>

<script>


</script>

<style scoped>
.v-card {
  transition: opacity .2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
 }

</style>