<template>
<v-hover v-slot="{ hover }">
  <div class="amber lighten-4">
    <v-card flat :elevation="hover ? 10 : 2" :class="{ 'on-hover': hover }" style="max-width:300px" outlined class="py-2"> 
        <v-img :src="require(`@/assets/${image}`)" class="mx-auto" height="200" width="200" contain/>
        <v-card-title class="justify-center">{{ title }}</v-card-title>
    </v-card>
  </div>
</v-hover>
</template>

<script>
export default {
  props: {
    title: String,
    image: String,
    }
  };
</script>

<style scoped>
.v-card {
  transition: opacity .2s ease-in-out;
}
.v-card:not(.on-hover) {
  opacity: 0.95;
 }

</style>