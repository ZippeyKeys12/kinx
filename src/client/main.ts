import Vue from 'vue';

// @ts-ignore
import Vuetify from 'vuetify/lib'
import "vuetify/dist/vuetify.min.css";

Vue.use(Vuetify, {
    theme: {
        primary: "#3f51b5",
        secondary: "#fff",
        accent: "#1A237E"
    },
    components: {
    },
    directives: {
    }
});

// @ts-ignore
import App from "./App";
import router from "./router";

Vue.config.productionTip = false;

new Vue({
    el: "#app",
    router,
    template: "<App/>"
}).$mount('#app');