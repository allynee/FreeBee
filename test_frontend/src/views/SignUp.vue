<template>
    <div class="white pa-15 pt-5 bground">
        <v-container class="pl-10 pr-10 pb-10" style="width:45%;height:45%">
            <span class="text-h6 text-capitalize grey--text">Create your account.</span><br/>
            <v-row class="mb-7 ml-1 mt-1">
                <span class="text-h4 text-capitalize brown--text">Join thousands of pet lovers.</span>
            </v-row>

            <v-form ref="form" v-model="valid">
                <v-row class="no-gutters">
                    <v-col
                    cols="12"
                        xs="12"
                        >
                        <v-text-field
                            label="Username*"
                            placeholder="Enter Username"
                            :rules = "userRules"
                            outlined
                        ></v-text-field>
                    </v-col>

                    <v-col
                    cols="12"
                        xs="12"
                        >
                        <v-text-field
                            label="Email*"
                            placeholder="Enter Email"
                            :rules = "emailRules"
                            outlined
                        ></v-text-field>
                    </v-col>

                    <v-col
                    cols="12"
                        xs="12"
                        >
                        <v-text-field
                            label="Password*"
                            placeholder="Enter Password"
                            v-model = "password"
                            :rules = "pwdRules"
                            :value="myPass"
                            :append-icon="value ? 'mdi-eye-off' : 'mdi-eye'"
                            @click:append="() => (value = !value)"
                            :type="value ? 'password' : 'text'"
                            outlined
                        ></v-text-field>
                    </v-col>

                    <v-col
                    cols="12"
                        xs="12"
                        >
                        <v-text-field
                            label="Confirm Password*"
                            v-model="confirmPassword"
                            placeholder="Type Confirm Password"
                            :rules="cfmpwdRules"
                            :value="mycfmPass"
                            :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                            @click:append="() => (showPassword = !showPassword)"
                            :type="showPassword ? 'password' : 'text'"
                            outlined
                        ></v-text-field>
                    </v-col>
                    <span class="ml-4 ">
                        <v-checkbox>
                            <template v-slot:label>
                                I wish to receive emails regarding activities involving my account
                            </template>
                        </v-checkbox>
                    </span>
                </v-row>
                <v-btn block :disabled="!valid" @click="validate"
                        color="brown" outlined>
                        Submit
                </v-btn>
            </v-form>
                
        </v-container>
    </div>
</template>

<script>

export default {
data(){
    return {
        valid: true,
        password: '',
        confirmPassword: '',
        value: String,
        showPassword: String,
        isFormValid: false,
        userRules: [
            v => v.length >= 8 || 'Minimum length is 8 characters',
            v => /[0-9]/.test(v) || 'Must contain at least 1 digit',
        ],
        fnameRules: [
        v => v.length >= 3 || 'Minimum length is 3 characters'
        ],
        emailRules: [
        v => !v || /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
        ],
        pwdRules: [
            v => !!v || 'Please type password.',
            v => (v && v.length >= 6) || 'Minimum length is 6 characters',
            v => /[a-z]/.test(v) || 'Must contain at least 1 lowercase letter',
            v => /[A-Z]/.test(v) || 'Must contain at least 1 uppercase letter',
            v => /[`!@#$%^&*()_+\-=[\]{};':"\\|,.<>?~]/.test(v) || 'Must contain at least 1 symbol'
        ],
        cfmpwdRules: [
            v => !!v || 'Please type confirm password.',
            v => v === this.password || 'The passwords do not match.'
        ],
    }
},
methods: {
    validate () {
        this.$refs.form.validate()
      },
},
computed: {
    FormValid(){
        if (this.pwdRules == true){
            return this.isFormValid == true
        }
        return console.log('na')
    }
}
}
</script>

<style scoped>
.bground {
  background: url('../assets/bg.png');
  background-size: cover;
  height: 120vh;
  background-position: 20px;
  width: 100%
}
</style>