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
                <Listing></Listing>
            <v-col>
                
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import Listing from "../components/Listing.vue"

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
    components: { Listing },
  }
</script>

<style scoped>

</style>