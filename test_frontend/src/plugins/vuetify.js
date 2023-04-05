import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import VideoBackground from 'vue-responsive-video-background-player'
import { Plugin } from 'vue-responsive-video-background-player'

Vue.use(Vuetify);
Vue.component('video-background', VideoBackground);
Vue.use(Plugin);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#3E2723',
                secondary: '#D3530D',
            }
        }
    }
});
