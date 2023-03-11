<template>
  <v-app>
    <v-btn id="Login" @click="googleSignIn">Login</v-btn>
  </v-app>
</template>

<script>
import { signInWithGoogle } from "../components/authentication.js";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    googleSignIn() {
      signInWithGoogle();
    },
  },
};
</script>
