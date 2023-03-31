<template>
  <div>
    <v-container class="pl-10 pr-10 pb-10" style="width:45%;height:45%" data-aos="fade-down">
      <v-card>
        <v-card-title class="text-h4 grey--text text--darken-3">Register as</v-card-title>
        <v-card-text>
          <v-row class="my-15">
            <v-col cols="12" align="center">
              <v-btn variant="tonal" @click='beneficiary()' to="/beneficiary"> Beneficiary </v-btn
              ><v-btn variant="tonal" @click='corporate()' to="/corporate"> Corporate </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
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
