<template>
  <div>
    <v-container>
      <v-btn variant="tonal" @click='beneficiary()' to="/beneficiary"> Beneficiary </v-btn
      ><v-btn variant="tonal" @click='corporate()' to="/corporate"> Corporate </v-btn>
    </v-container>
  </div>
</template>

<script>
export default{
    methods:{
        beneficiary(){
            // go beneficiary register page
            console.log("beneficiary")
        },
        corporate(){
            // go corporate register page
        }
    }
}
</script>

<style scoped>
.bground {
  background: url("../assets/bg.png");
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%;
}

.box {
  background-color: blue;
  height: 20vh;
  width: 20vh;
  border: black solid 1em;
}
</style>
