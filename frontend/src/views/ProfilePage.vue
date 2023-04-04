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
                            <v-list-item v-for="item in items" :key="item.title" link>
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
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3"
                    >
                        Username:
                    </span>
                    <span class="text-body-1 font-weight-light"> username </span>
                    <br />
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3"
                    >
                        Email:
                    </span>
                    <span class="text-body-1 font-weight-light"> email </span>
                    <br />
                    <span
                    class="text-h7 font-weight-medium grey--text text--darken-3"
                    >
                        Address
                    </span>
                    <span class="text-body-1 font-weight-light"> address </span>
                    <br />
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
          { title: 'Profile', icon: 'mdi-account' },
          { title: 'Liked Listings', icon: 'mdi-heart' },
          { title: 'Subscribed', icon: 'mdi-email'},
          { title: 'Logout', icon: 'mdi-logout' },
        ],
      }
    },
  }
</script>

<style scoped>

</style>