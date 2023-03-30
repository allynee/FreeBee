<template>
<v-hover v-slot="{ hover }">
    <v-card flat :elevation="hover ? 10 : 2" :class="{ 'on-hover': hover }" style="width:500px" outlined class="pa-1"> 
        <v-img :src="require(`@/assets/${image}`)" class="mx-auto" height="150" width="150" contain/>
        <v-card-title class="justify-center">{{ title }}</v-card-title>
    </v-card>
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