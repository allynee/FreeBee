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
                <v-card height="450">
                    <br/>
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3 mx-5" 
                    >
                        Username:
                    </span>
                    <span class="text-body-1 font-weight-light"> username </span>
                    <br />
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3 mx-5"
                    >
                        Email:
                    </span>
                    <span class="text-body-1 font-weight-light"> email </span>
                    <br />
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3 mx-5"
                    >
                        Address
                    </span>
                    <span class="text-body-1 font-weight-light"> address </span>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data () {
      return {
        items: [
          { title: 'Profile', icon: 'mdi-account', route:'/profile'},
          { title: 'Liked Listings', icon: 'mdi-heart', route:'/liked'},
          { title: 'Subscribed', icon: 'mdi-email', route:'/subscribedlistings'},
          { title: 'Logout', icon: 'mdi-logout' },
        ],
      }
    },
  }
</script>

<style scoped>

</style>