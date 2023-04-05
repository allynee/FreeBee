<template>
    <v-container>
        <v-row>
            <v-col cols="3">
                <v-card
                    height="350"
                    width="256"
                >
                    <v-navigation-drawer
                    class="amber lighten-2"
                    permanent
                    >
                        <v-list>
                            <v-list-item v-for="item in items" :key="item.title" link :to="item.route">
                                <v-list-item-icon>
                                    <v-icon>{{item.icon}}</v-icon>
                                </v-list-item-icon>

                                <v-list-item-content>
                                    {{item.title}}
                                </v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-navigation-drawer>
                </v-card>
            </v-col>

            <v-col>
                <v-card height="500">
                    <br/>
                    <span class="text-h7 font-weight-medium grey--text text--darken-3 mx-5">
                        Username:
                    </span>
                    <br/>
                    <v-text-field outlined style="margin-left: 15px; max-width: 300px;" disabled :value='username'>
                    </v-text-field>
                    
                    <span class="text-h7 font-weight-medium grey--text text--darken-3 mx-5">
                        Email:
                    </span>
                    <br/>
                    <v-text-field outlined style="margin-left: 15px; max-width: 400px;" disabled :value="email">
                    </v-text-field>

                    <span class="text-h7 font-weight-medium grey--text text--darken-3 mx-5">
                        Address:
                    </span>
                    <br/>
                    <v-text-field outlined style="margin-left: 15px; max-width: 400px;" disabled :value="address">
                    </v-text-field>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    data () {
      return {
        username: '',
        email: '',
        address: '',
        items: [
          { title: 'Profile', icon: 'mdi-account', route:'/profile'},
          { title: 'Liked Listings', icon: 'mdi-heart', route:'/liked'},
          { title: 'Subscribed', icon: 'mdi-email', route:'/subscribedlistings'},
          { title: 'Logout', icon: 'mdi-logout' },
        ],
      }
    },
    methods: {
        async fetchUser() {
            const beneficiary_url = 'http://localhost:8421/beneficiary/' + this.$store.state.uid;
            axios.get(beneficiary_url).then((response) => {
                this.username = response.data.username;
                this.email = response.data.email;
                this.address = response.data.address;
            })
        }
    },
    mounted () {
        this.fetchUser();
    }
  }
</script>

<style scoped>

</style>